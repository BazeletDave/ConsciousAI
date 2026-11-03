"""Offline unit tests for the existing Kiongozi World Bank WDI collector."""
import importlib.util, json, pathlib, unittest
from unittest.mock import patch
SCRIPT=pathlib.Path(__file__).with_name("world_bank_africa_baseline.py")
spec=importlib.util.spec_from_file_location("wb_collector",SCRIPT)
wb=importlib.util.module_from_spec(spec)
spec.loader.exec_module(wb)
class FakeResponse:
    def __init__(self,content): self.content=content
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def read(self,n): return self.content
class WorldBankBaselineTests(unittest.TestCase):
    def test_dimensions_and_missing_are_explicit(self):
        def fake_open(request,timeout):
            return FakeResponse(json.dumps([{"pages":1},[{"countryiso3code":"GHA","date":"2024","value":62.5}]]).encode())
        with patch.object(wb.urllib.request,"urlopen",side_effect=fake_open):
            rows=wb.collect(2024,2024)
        self.assertEqual(len(rows),20)
        self.assertEqual(len([r for r in rows if r["iso3"]=="GHA" and r["value_status"]=="reported"]),4)
        self.assertTrue(all(r["value"]=="" and r["value_status"]=="missing" for r in rows if r["iso3"]=="KEN"))
        self.assertTrue(all(len(r["response_sha256"])==64 for r in rows))
    def test_refuses_partial_pagination(self):
        with patch.object(wb.urllib.request,"urlopen",return_value=FakeResponse(json.dumps([{"pages":2},[]]).encode())):
            with self.assertRaises(ValueError): wb.collect(2024,2024)
    def test_refuses_oversize(self):
        with patch.object(wb.urllib.request,"urlopen",return_value=FakeResponse(b"x"*5_000_001)):
            with self.assertRaises(ValueError): wb.collect(2024,2024)
if __name__=="__main__": unittest.main()
