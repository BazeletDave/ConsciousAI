"""Bounded public publisher page observations, not extracted deployment facts."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
from country_intelligence import fetch, DocumentTitle, plain

ROOT = Path(__file__).resolve().parent
SOURCES = [
    {'id':'WAYMO-SAFETY', 'publisher':'Waymo', 'url':'https://www.waymo.com/safety/impact/', 'host':'www.waymo.com', 'kind':'company_self_report', 'track':'road_autonomy'},
    {'id':'ZOOX-SAFETY', 'publisher':'Zoox', 'url':'https://zoox.com/safety/', 'host':'zoox.com', 'kind':'company_self_report', 'track':'road_autonomy'},
    {'id':'FAA-AAM', 'publisher':'Federal Aviation Administration', 'url':'https://www.faa.gov/aam', 'host':'www.faa.gov', 'kind':'regulator_information', 'track':'air_mobility'},
    {'id':'NHTSA-SGO', 'publisher':'NHTSA', 'url':'https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting', 'host':'www.nhtsa.gov', 'kind':'regulator_information', 'track':'road_autonomy'},
    {'id':'BRA-ANAC-AAM', 'publisher':'ANAC', 'url':'https://www.gov.br/anac/pt-br/noticias/2026/anac-abre-consultas-setoriais-sobre-criterios-de-aeronavegabilidade-e-ruido-para-o-evtol-eve-100', 'host':'www.gov.br', 'kind':'dated_regulator_consultation_announcement', 'track':'air_mobility', 'country':'BRA'},
    {'id':'ISR-TRAFFIC-AUTHORITY', 'publisher':'Israel Ministry of Transport and Road Safety', 'url':'https://www.gov.il/en/departments/units/ministry_of_transport_traffic_authority', 'host':'www.gov.il', 'kind':'agency_remit_page_not_operating_permission', 'track':'road_autonomy', 'country':'ISR'},
]


def collect(fetcher=fetch, now=None):
    now = now or datetime.now(timezone.utc).isoformat()
    rows, health = [], []
    for source in SOURCES:
        try:
            raw = fetcher(source)
            title_parser = DocumentTitle()
            title_parser.feed(raw.decode('utf8', 'replace'))
            title = plain(' '.join(title_parser.parts))
            if len(title) < 5 or any(term in title.casefold() for term in ('access denied','just a moment','captcha','forbidden')):
                raise ValueError('publisher title absent or access wall')
            rows.append({'id':source['id'], 'source_id':source['id'], 'publisher':source['publisher'],
                         'title':title, 'source_url':source['url'], 'country_codes':[source.get('country','USA')],
                         'content_sha256':sha256(raw).hexdigest(), 'published_at':None,
                         'source_kind':source['kind'], 'configured_track':source['track'],
                         'verification_status':'publisher_page_observation_unreviewed',
                         'human_review_required':True, 'publication_authorized':False})
            health.append({'source_id':source['id'], 'status':'fetched', 'bytes':len(raw)})
        except (OSError, ValueError) as error:
            health.append({'source_id':source['id'], 'status':'failed', 'error_type':type(error).__name__})
    return {'generated_at':now, 'records':rows, 'sources':health,
            'notice':'Page byte changes may reflect layout or tracking changes. They are not evidence of a robotics deployment, safety improvement, or regulatory approval.'}


if __name__ == '__main__':
    target = ROOT/'learning_ledger/robotics_pages.json'
    target.parent.mkdir(exist_ok=True)
    result = collect()
    with tempfile.NamedTemporaryFile('w', dir=target.parent, delete=False, encoding='utf8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
        name=handle.name
    os.replace(name,target)
    print(json.dumps(result['sources']))
