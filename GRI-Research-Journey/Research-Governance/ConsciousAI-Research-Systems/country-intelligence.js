/* Country evidence explorer. All remote strings render as text, never HTML. */
(() => {
  'use strict';
  const byId = id => document.getElementById(id);
  const names = {
    political_institutions: 'Political institutions', trade_investment: 'Trade and investment',
    organizational_management: 'Global management', algorithmic_management: 'Algorithmic management',
    artificial_intelligence: 'Artificial intelligence', needs_review: 'Topic requires review'
  };
  const node = (tag, text, className) => {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  };
  const date = value => {
    const d = new Date(value);
    return value && !Number.isNaN(d.getTime()) ? d.toLocaleString() : 'Not supplied by publisher';
  };
  const link = (label, url) => {
    const a = node('a', label);
    try { if (new URL(url).protocol !== 'https:') return node('span', label); }
    catch { return node('span', label); }
    a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a;
  };
  let lastSelection = '';
  let page = 0;
  const pageSize = 8;
  let initialized = false;
  let inFlight = null;
  async function refresh() {
    if (inFlight) inFlight.abort();
    const controller = new AbortController(); inFlight = controller;
    const timer = setTimeout(() => controller.abort(), 15000);
    const selected = byId('country-select').value || 'BRA';
    const topic = byId('country-topic').value;
    byId('country-refresh').disabled = true;
    byId('country-state').textContent = 'Loading country evidence…';
    if (lastSelection !== selected + '|' + topic) {
      for (const id of ['country-records', 'country-channels', 'country-comparative', 'country-sources']) byId(id).replaceChildren();
      byId('country-comparative').hidden = true;
      byId('country-baseline').textContent = 'Loading the selected country assessment…';
      byId('country-evolution').textContent = '';
      byId('country-page').textContent = '';
      byId('country-prev').disabled = true; byId('country-next').disabled = true;
      byId('country-brazil-link').hidden = true;
    }
    try {
      const query = new URLSearchParams({country: selected});
      if (topic) query.set('topic', topic);
      const response = await fetch('/intelligence/countries?' + query, {cache: 'no-store', signal: controller.signal});
      if (!response.ok) throw Error('HTTP ' + response.status);
      const data = await response.json();
      if (controller !== inFlight) return;
      if (!initialized) {
        const groups = [['South America pilot', c => c.pilot], ['Comparative cases: Israel and United States', c => c.comparison_country], ['Other countries and economies · limited coverage', c => !c.pilot && !c.comparison_country]];
        byId('country-select').replaceChildren();
        for (const [label, matches] of groups) {
          const group = document.createElement('optgroup'); group.label = label;
          data.countries.filter(matches).forEach(c => {
            const option = node('option', c.name); option.value = c.code; group.append(option);
          });
          byId('country-select').append(group);
        }
        byId('country-select').value = selected;
        initialized = true;
      }
      const country = data.countries.find(c => c.code === selected);
      lastSelection = selected + '|' + topic;
      const rows = data.records;
      const evolution = data.research_evolution;
      byId('country-evolution').textContent = evolution && evolution.generated_at ? 'Research connections updated ' + date(evolution.generated_at) + ' · ' + evolution.document_count + ' public research documents · ' + evolution.connected_records + ' evidence records connected. ' + (evolution.learning_candidate.status === 'blocked' ? 'Model development awaits reviewed training and evaluation data.' : 'A learning candidate has been evaluated; the active model remains unchanged pending review.') : 'Research connection index awaiting its first build.';
      byId('country-state').textContent = country.name + ' · ' + rows.length + ' evidence candidates · Snapshot ' + date(data.generated_at);
      byId('country-baseline').textContent = 'Political direction: awaiting reviewed baseline. Country mentions and newly discovered records do not establish a political shift. Business effects require institutional and sector review.';
      const channels = byId('country-channels'); channels.replaceChildren();
      Object.entries(data.channels).forEach(([key, question]) => {
        const card = node('article', undefined, 'model-field');
        card.append(node('b', names[key]), node('span', rows.filter(r => r.topic.label === key).length + ' candidates in this selection'), node('p', question, 'model-note'));
        channels.append(card);
      });
      const research = byId('country-comparative'); research.replaceChildren();
      const comparison = data.comparative_research;
      research.hidden = !comparison || !comparison.countries.includes(selected);
      if (!research.hidden) {
        research.append(node('h3', comparison.title), node('p', comparison.notice, 'model-note'));
        const cases = node('div', undefined, 'intel-nav');
        for (const item of comparison.cases) {
          const button = node('button', 'View ' + (data.countries.find(c => c.code === item.code)?.name || item.code) + ' evidence');
          button.type = 'button'; button.disabled = item.code === selected;
          button.addEventListener('click', () => { byId('country-select').value = item.code; byId('country-select').dispatchEvent(new Event('change')); });
          cases.append(button, link(item.label, item.url));
        }
        research.append(cases, link('Read the comparative institutional framework', comparison.comparison_url));
        const themes = node('div', undefined, 'country-channels');
        for (const theme of comparison.themes) {
          const card = node('article', undefined, 'model-field');
          card.append(node('b', theme.name), node('p', theme.question, 'model-note'), node('span', theme.evidence_status)); themes.append(card);
        }
        research.append(themes);
      }
      const health = byId('country-sources'); health.replaceChildren();
      for (const source of data.sources) {
        const age = source.last_success_at ? (Date.now() - Date.parse(source.last_success_at)) / 3600000 : NaN;
        const current = Number.isFinite(age) && age >= -5/60 && age <= 6;
        const label = source.status === 'failed' ? 'Collection failed' : !current ? 'Collection stale or unavailable' : source.status === 'empty' ? 'Fetched with no usable items' : 'Collection current';
        const p = node('p', undefined, 'meta');
        p.append(link(source.publisher, source.url), node('span', ' · ' + label + ' · Last success ' + date(source.last_success_at)));
        health.append(p);
      }
      if (!data.sources.length) health.append(node('p', 'Awaiting first source collection.'));
      const list = byId('country-records'); list.replaceChildren();
      const changes = new Map((data.changes || []).map(c => [c.record_id, c.kind]));
      const visible = byId('country-changes-only').checked ? rows.filter(r => changes.has(r.id)) : rows;
      page = Math.min(page, Math.max(0, Math.ceil(visible.length / pageSize) - 1));
      for (const record of visible.slice(page * pageSize, (page + 1) * pageSize)) {
        const card = node('article', undefined, 'country-record');
        const label = names[record.topic.label] || 'Topic requires review';
        card.append(node('span', label, 'pill'), node('span', 'Human review required', 'pill'));
        if (changes.has(record.id)) card.append(node('span', changes.get(record.id) === 'metadata_changed' ? 'Metadata revised since prior run' : 'Newly discovered in latest run', 'pill'));
        card.append(node('h4', record.title), node('p', record.publisher + ' · Published ' + (record.published_at ? date(record.published_at) : record.publication_date || 'Not supplied by publisher'), 'meta'));
        const provenance = node('details'); provenance.append(node('summary', 'Evidence and model details'));
        provenance.append(node('p', 'First observed ' + date(record.first_seen_at) + ' · Last seen ' + date(record.last_seen_at), 'meta'));
        if (record.source_observed_at) provenance.append(node('p', 'Upstream observation ' + date(record.source_observed_at) + '. Local snapshot compilation does not establish a new source fetch.', 'meta'));
        provenance.append(node('p', 'Country assignment: publisher jurisdiction or title mention, subject to review. Legal status: ' + record.legal_status.replaceAll('_', ' ') + '.', 'meta'));
        provenance.append(node('p', record.topic.abstained ? 'ML abstained. A reviewer must assign the topic.' : 'Experimental ML topic suggestion · uncalibrated weight ' + record.topic.score + '. This is not impact confidence.', 'meta'));
        card.append(provenance, link('Inspect publisher record', record.source_url));
        if (record.related_research && record.related_research.length) {
          const related = node('details'); related.append(node('summary', 'Connections to GRI research'));
          related.append(node('p', 'Suggested title similarities; not verified evidence or causal conclusions.', 'meta'));
          for (const research of record.related_research) { const p = node('p'); p.append(link(research.title, research.url)); related.append(p); }
          card.append(related);
        }
        list.append(card);
      }
      if (!visible.length) list.append(node('p', 'No candidates in this selection. Limited source coverage does not imply no political or policy activity.', 'status-note'));
      byId('country-page').textContent = visible.length ? 'Showing ' + (page * pageSize + 1) + '–' + Math.min((page + 1) * pageSize, visible.length) + ' of ' + visible.length : 'No candidates';
      byId('country-prev').disabled = page === 0;
      byId('country-next').disabled = (page + 1) * pageSize >= visible.length;
      const model = data.model;
      byId('country-model').textContent = model ? 'Experimental topic model: ' + model.model_version + '. ' + model.training_examples + ' author created training examples; ' + model.evaluation_examples + ' instructional holdout examples. Holdout macro F1 ' + model.macro_f1.toFixed(3) + '. No independent labels or real news validation. No political or economic forecasts.' : 'Model evaluation awaiting collection.';
      byId('country-brazil-link').hidden = selected !== 'BRA';
      byId('country-brazil-link').href = data.brazil_research_url;
    } catch (error) {
      if (controller !== inFlight) return;
      byId('country-state').textContent = 'Country evidence unavailable. Other dashboard services remain available.';
      byId('country-records').replaceChildren(node('p', 'The request failed or timed out. Refresh to retry.'));
      byId('country-channels').replaceChildren();
      byId('country-comparative').replaceChildren();
      byId('country-comparative').hidden = true;
      byId('country-sources').replaceChildren();
      byId('country-model').textContent = 'Model information unavailable for this request.';
      byId('country-baseline').textContent = 'Country assessment unavailable for this request.';
      byId('country-evolution').textContent = 'Research connections unavailable for this request.';
      byId('country-page').textContent = '';
      byId('country-prev').disabled = true; byId('country-next').disabled = true;
      byId('country-brazil-link').hidden = true;
    } finally {
      clearTimeout(timer);
      if (controller === inFlight) byId('country-refresh').disabled = false;
    }
  }
  const requested = new URLSearchParams(window.location.search).get('country');
  if (requested && /^[A-Z]{3}$/.test(requested)) {
    const option = node('option', requested); option.value = requested;
    byId('country-select').append(option); byId('country-select').value = requested;
  }
  byId('country-select').addEventListener('change', () => {
    const url = new URL(window.location.href); url.searchParams.set('country', byId('country-select').value);
    window.history.replaceState(null, '', url);
  });
  ['country-select', 'country-topic', 'country-changes-only'].forEach(id => byId(id).addEventListener('change', () => { page = 0; refresh(); }));
  byId('country-prev').addEventListener('click', () => { page = Math.max(0, page - 1); refresh(); });
  byId('country-next').addEventListener('click', () => { page += 1; refresh(); });
  byId('country-refresh').addEventListener('click', refresh);
  refresh();
  setInterval(() => { if (!document.hidden) refresh(); }, 60000);
})();
