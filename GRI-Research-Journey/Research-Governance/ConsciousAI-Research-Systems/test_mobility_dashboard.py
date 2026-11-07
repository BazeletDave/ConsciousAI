"""Regression and interaction contract tests for the existing GRI mobility dashboard.

No network, corporate systems, personal trip records or trained models required.
Node.js is optional for JavaScript execution; static checks always run.
"""
import html.parser
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "dashboard.html"

class Elements(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.sections = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a":
            self.links.append(a)
        if tag == "section":
            self.sections.append(a)

class MobilityDashboardAcceptance(unittest.TestCase):
    def test_accessibility_and_research_boundaries(self):
        markup = HTML.read_text(encoding="utf-8")
        parser = Elements()
        parser.feed(markup)
        self.assertIn("mobility-governance-evidence", parser.ids)
        self.assertTrue({"gri-av-fixed", "gri-av-revenue", "gri-av-variable",
                         "gri-av-result", "gri-av-bar"}.issubset(parser.ids))
        self.assertIn('aria-live="polite"', markup)
        self.assertIn("not actual company unit economics", markup)
        self.assertIn("no validated mobility ML model", markup)
        self.assertIn("independent review", markup)
        links = [a["href"] for a in parser.links if "href" in a]
        self.assertTrue(any("2026-11-07-strategic-mobility-transition-assessment.md" in x for x in links))
        self.assertTrue(any("DATASET12-INTEGRATION.md" in x for x in links))
        self.assertEqual(markup.count('id="mobility-governance-evidence"'), 1)

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable; JS interaction not executed")
    def test_actual_dashboard_javascript_interactions(self):
        markup = HTML.read_text(encoding="utf-8")
        section = markup.split('id="mobility-governance-evidence"', 1)[1]
        js = section.split("<script>", 1)[1].split("</script>", 1)[0]
        # Executes the actual inline script in a minimal DOM fixture and fires input events.
        # This is a JavaScript unit test, not an independent graphical browser test.
        cases = [
            (100,15,3,"9 paid rides",30),
            (0,15,3,"0 paid rides",0),
            (120,15,3,"10 paid rides",100/3),
            (300,15,3,"25 paid rides",250/3),
            (360,15,3,"30 paid rides",100),
            (372,15,3,"31 paid rides",100),
            (100,3,3,"No finite break even",0),
            (100,2,3,"No finite break even",0),
            (-1,15,3,"Enter nonnegative",0),
            (100,-1,3,"Enter nonnegative",0),
            (100,15,-1,"Enter nonnegative",0),
            (100,0,0,"No finite break even",0),
            (1,2,1,"1 paid rides",100/30),
            (1,1.5,1,"2 paid rides",200/30),
            (200,25,5,"10 paid rides",100/3),
            (200,25,0,"8 paid rides",80/3),
            (50,10,5,"10 paid rides",100/3),
            (75,10,5,"15 paid rides",50),
            (150,10,5,"30 paid rides",100),
            (1000,50,0,"20 paid rides",200/3),
            (1000,25,5,"50 paid rides",100),
            (1,100,0,"1 paid rides",100/30),
            (0,1,0,"0 paid rides",0),
            (5,2,1,"5 paid rides",50/3),
            (90,9,0,"10 paid rides",100/3),
            (90,9,8,"90 paid rides",100),
            (100,100,99,"100 paid rides",100),
            (100,100,98,"50 paid rides",100),
            (250,20,10,"25 paid rides",250/3),
            (250,20,15,"50 paid rides",100),
        ]
        payload = json.dumps({"script":js,"cases":cases})
        runner = r"""
const {script,cases}=JSON.parse(process.argv[1]);
const els={};
for(const id of ['gri-av-fixed','gri-av-revenue','gri-av-variable','gri-av-result','gri-av-bar']){
 els[id]={value:'0',textContent:'',style:{width:''},listeners:{},addEventListener(ev,fn){this.listeners[ev]=fn}};
}
global.document={getElementById:id=>els[id]};
eval(script);
for(let i=0;i<cases.length;i++){
 const [f,r,v,expected,width]=cases[i];
 for(const [id,value] of [['gri-av-fixed',f],['gri-av-revenue',r],['gri-av-variable',v]])
   els[id].value=String(value);
 els['gri-av-fixed'].listeners.input();
 const actual=els['gri-av-result'].textContent;
 const pct=parseFloat(els['gri-av-bar'].style.width);
 if(!actual.includes(expected)||Math.abs(pct-width)>0.0001)
   throw Error('Case '+i+' expected '+expected+' and '+width+'%, got '+actual+' and '+pct+'%');
}
console.log('PASS '+cases.length+' calculator interaction scenarios');
"""
        result = subprocess.run(["node","-e",runner,payload],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("PASS 30",result.stdout)

if __name__ == "__main__":
    unittest.main()
