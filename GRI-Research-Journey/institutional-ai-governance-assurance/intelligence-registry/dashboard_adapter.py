"""Read-only adapter for existing GRI dashboard service. No private data or network calls."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def summary(path=None):
    path=Path(path) if path else ROOT/'evidence_ledger.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    records=data['records']
    return {'schema_version':'1.0','mode':'research_review_only',
            'total':len(records),'requires_human_review':sum(bool(x.get('human_review_required',True)) for x in records),
            'records':[{'id':x['id'],'source_url':x['source_url'],
                        'review_status':x['review_status'],'verification':x['verification'],
                        'last_seen_at':x['last_seen_at']} for x in records],
            'notice':'Public-source metadata, not evidence of safety, compliance or wrongdoing.'}
