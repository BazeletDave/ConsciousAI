"""Reproducible synthetic experiment and SVG charts; no third-party dependencies."""
import csv, json, random
from pathlib import Path
from governance import Event, evaluate, POLICY_VERSION

def run(n=1000, seed=20261021, out=None):
    rng=random.Random(seed)
    rows=[]
    for i in range(n):
        moving=rng.random()<0.85
        handling=rng.random()<0.25
        attributed=rng.random()<0.9
        confidence=round(rng.random(),3)
        # Synthetic reference label is NOT a real-world ground truth.
        truth=moving and handling and attributed and rng.random()<0.85
        ev=Event(f"sim-{i:05}",moving,handling,attributed,confidence)
        decision=evaluate(ev)
        rows.append(dict(event_id=ev.event_id, moving=int(moving),
            handling_detected=int(handling), driver_attribution_verified=int(attributed),
            confidence=confidence, synthetic_reference_label=int(truth),
            action=decision["action"], policy_version=POLICY_VERSION,
            decision_hash=decision["decision_hash"]))
    tp=sum(r["action"]=="WARNING_PERMITTED" and r["synthetic_reference_label"] for r in rows)
    fp=sum(r["action"]=="WARNING_PERMITTED" and not r["synthetic_reference_label"] for r in rows)
    fn=sum(r["action"]!="WARNING_PERMITTED" and r["synthetic_reference_label"] for r in rows)
    tn=n-tp-fp-fn
    summary=dict(dataset="synthetic", seed=seed, n=n, policy_version=POLICY_VERSION,
        true_positive=tp,false_positive=fp,false_negative=fn,true_negative=tn,
        precision=tp/(tp+fp) if tp+fp else None,
        recall=tp/(tp+fn) if tp+fn else None,
        false_positive_rate=fp/(fp+tn) if fp+tn else None,
        warning_count=tp+fp, review_count=sum(r["action"]=="REVIEW_EVIDENCE" for r in rows))
    if out:
        p=Path(out);p.mkdir(parents=True,exist_ok=True)
        with (p/"synthetic_events.csv").open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        (p/"synthetic_metrics.json").write_text(json.dumps(summary,indent=2)+"\n")
        labels=["TP","FP","FN","TN"]
        values=[tp,fp,fn,tn]
        mx=max(values) or 1
        bars="".join(f'<rect x="190" y="{55+i*64}" width="{420*v/mx:.1f}" height="35" fill="#3b6c93"/><text x="40" y="{78+i*64}" font-size="17">{labels[i]}: {v}</text>' for i,v in enumerate(values))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="700" height="365"><rect width="700" height="365" fill="white"/><text x="28" y="30" font-size="19">Synthetic governance experiment (n={n}; seed={seed})</text>{bars}<text x="30" y="341" font-size="13">Illustrative simulation only; not measured driving performance</text></svg>'
        (p/"synthetic_confusion_matrix.svg").write_text(svg)
    return summary

if __name__=="__main__":
    print(json.dumps(run(out="results"),indent=2))
