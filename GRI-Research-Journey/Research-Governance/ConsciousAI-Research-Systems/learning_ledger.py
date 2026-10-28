"""GRI versioned research observations and proposed learning connections.

Consumes existing public metadata files. No network or model promotion.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'learning_ledger/snapshot.json'
MAX_EVENTS = 500
TRACKS = {
    'robotics': ('robot', 'robotic', 'robotics', 'humanoid', 'optimu'),
    'road_autonomy': ('waymo', 'zoox', 'cybercab', 'robotaxi', 'robo-taxi', 'autonomous vehicle', 'automated driving'),
    'air_mobility': ('evtol', 'powered lift', 'powered-lift', 'air taxi', 'air taxis', 'advanced air mobility'),
    'institutional_correction': ('antiquit', 'restitution', 'provenance', 'latchford', 'cambodia'),
    'algorithmic_management': ('algorithmic management', 'platform labor', 'gestão algor', 'gestao algor'),
}


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def stamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.utcoffset() is None:
        raise ValueError('timezone required')
    return result


def verify(snapshot):
    if not isinstance(snapshot, dict) or snapshot.get('content_sha256') != digest({k:v for k,v in snapshot.items() if k != 'content_sha256'}):
        raise ValueError('snapshot integrity failure')
    previous = snapshot['history_anchor']
    for event in snapshot['events']:
        if event['previous_event_sha256'] != previous or event['event_sha256'] != digest({k:v for k,v in event.items() if k != 'event_sha256'}):
            raise ValueError('event chain integrity failure')
        previous = event['event_sha256']
    return snapshot


def build(feeds, program, previous=None, now=None, candidate=None):
    now = now or datetime.now(timezone.utc).isoformat()
    clock = stamp(now)
    if previous is not None:
        verify(previous)
        if clock < stamp(previous['generated_at']):
            raise ValueError('clock moved backwards')
    previous = previous or {}
    records, health = {}, []
    for name, feed in sorted(feeds.items()):
        try:
            age = (clock - stamp(feed['generated_at'])).total_seconds()
            if age < 0:
                raise ValueError('future collection timestamp')
            sources = feed.get('sources', [])
            failed = sum(s.get('status') in ('failed', 'error', 'unavailable') for s in sources)
            health.append({'feed': name, 'generated_at': feed['generated_at'],
                           'age_seconds': age, 'status': 'stale' if age > 21600 else 'source_failures' if failed else 'snapshot_available',
                           'reported_source_failures': failed,
                           'scope': 'upstream_snapshot_age_not_article_or_source_freshness'})
            rows = feed.get('records', feed.get('queue', []))
            if not isinstance(rows, list):
                raise ValueError('records list required')
            for row in rows:
                if not all(isinstance(row.get(k), str) and row[k].strip() for k in ('id','source_id','title','source_url')):
                    raise ValueError('record provenance required')
                key = name + ':' + row['id']
                if key in records:
                    raise ValueError('duplicate record identity')
                text = row['title'].casefold()
                tracks = [track for track, terms in TRACKS.items() if any(t in text for t in terms)]
                content = {k:row.get(k) for k in ('title','source_url','source_id','publisher','country_codes','jurisdiction','published_at','legal_status','content_sha256','source_kind','configured_track')}
                if row.get('configured_track') in TRACKS and row['configured_track'] not in tracks:
                    tracks.append(row['configured_track'])
                records[key] = dict(content, id=key, metadata_sha256=digest(content), tracks=tracks,
                                    relation='keyword_candidate_not_verified_comparison',
                                    human_review_required=True, publication_authorized=False)
        except (KeyError, TypeError, AttributeError, ValueError):
            # A malformed feed cannot partially contribute observations.
            records = {k:v for k,v in records.items() if not k.startswith(name + ':')}
            health = [h for h in health if h['feed'] != name]
            health.append({'feed':name, 'status':'invalid_or_missing', 'age_seconds':None})
    events = list(previous.get('events', []))
    anchor = previous.get('history_anchor')
    old = {r['id']:r for r in previous.get('records', [])}
    for key, row in sorted(records.items()):
        prior = old.get(key)
        if prior is None or prior['metadata_sha256'] != row['metadata_sha256']:
            event = {'record_id':key, 'observed_at':now,
                     'kind':'metadata_revised' if prior else 'first_observed',
                     'metadata_sha256':row['metadata_sha256'],
                     'prior_metadata_sha256':prior['metadata_sha256'] if prior else None,
                     'previous_event_sha256':events[-1]['event_sha256'] if events else anchor}
            event['event_sha256'] = digest(event)
            events.append(event)
    evicted = max(0, len(events)-MAX_EVENTS)
    if evicted:
        anchor = events[evicted-1]['event_sha256']
        events = events[evicted:]
    # Keep prior observations across outages and upstream retention windows.
    cumulative = dict(old)
    cumulative.update(records)
    result = {'schema_version':'1.0', 'generated_at':now,
              'cycle_count':previous.get('cycle_count',0)+1,
              'mode':'metadata_observation_and_learning_sequence_review',
              'feed_health':health, 'records':list(cumulative.values()),
              'records_observed_this_cycle':len(records), 'events':events,
              'history_anchor':anchor, 'archived_event_count':previous.get('archived_event_count',0)+evicted,
              'program':program, 'program_sha256':digest(program),
              'candidate_evaluation':candidate or {'status':'not_observed'},
              'model_updated':False, 'verification_promoted':False,
              'notice':'Observed metadata changes are not deployment milestones, regulatory findings, or learned model improvements. Event history beyond the retained window remains in Git history.'}
    result['content_sha256'] = digest(result)
    return result


def load_snapshot(root=ROOT):
    path = root / 'learning_ledger/snapshot.json'
    if not path.exists():
        return {'status':'awaiting_first_cycle', 'model_updated':False}
    return verify(json.loads(path.read_text(encoding='utf8')))


def main():
    def read(path, fallback=None):
        if not path.exists() and fallback is not None:
            return fallback
        return json.loads(path.read_text(encoding='utf8'))
    feeds = {'countries':read(ROOT/'country_intelligence/feed.json', {}),
             'robotics_pages':read(ROOT/'learning_ledger/robotics_pages.json', {}),
             'mobility':read(ROOT/'international_mobility_feed.json', {})}
    program = read(ROOT/'learning_ledger/program.json')
    previous = read(OUTPUT) if OUTPUT.exists() else None
    evolution = read(ROOT/'country_intelligence/research_evolution.json', {})
    candidate = {'snapshot_generated_at':evolution.get('generated_at'),
                 'evaluation':evolution.get('learning_candidate'),
                 'scope':'existing_topic_classifier_not_robot_motor_learning'}
    result = build(feeds, program, previous, candidate=candidate)
    from curriculum_experiment_bridge import snapshot as experiment_snapshot
    try:
        result['curriculum_experiment'] = experiment_snapshot()
    except (OSError, ValueError, KeyError, TypeError):
        result['curriculum_experiment'] = {'status':'integrity_unavailable', 'model_promoted':False}
    result['content_sha256'] = digest({k:v for k,v in result.items() if k != 'content_sha256'})
    OUTPUT.parent.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile('w', dir=OUTPUT.parent, delete=False, encoding='utf8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
        name = handle.name
    os.replace(name, OUTPUT)
    print(json.dumps({'observed':result['records_observed_this_cycle'], 'cycle':result['cycle_count'], 'model_updated':False}))


if __name__ == '__main__':
    main()
