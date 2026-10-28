/* Isolated panel: failures never disable the other dashboard modules. */
(() => {
  const state = document.getElementById('enrollment-state');
  const form = document.getElementById('enrollment-search');
  let sequence = 0;
  const text = (tag, value) => { const e = document.createElement(tag); e.textContent = value; return e; };
  const link = (title, url) => {
    const e = text('a', title);
    try { const u = new URL(url); if (u.protocol === 'https:' && !u.username && !u.password) { e.href = u.href; e.target = '_blank'; e.rel = 'noopener noreferrer'; } } catch (_) {}
    return e;
  };
  async function render() {
    const request = ++sequence;
    state.textContent = 'Loading research…';
    const query = document.getElementById('enrollment-query').value.trim();
    const country = document.getElementById('enrollment-country').value;
    const params = new URLSearchParams({q: query});
    if (country) params.set('country', country);
    try {
      const response = await fetch('/intelligence/enrollment-research?' + params, {cache: 'no-store'});
      if (!response.ok) throw Error('Research unavailable');
      const d = await response.json();
      if (request !== sequence) return;
      state.textContent = d.counts.attributed_incidents + ' attributed incident · ' + d.counts.institutional_references + ' institutional references · TF IDF index: ' + d.retrieval.fitted_documents + ' documents · independent evaluation pending · reviewed ' + d.updated_at;
      const discovery = d.discovery;
      const selector = document.getElementById('enrollment-country');
      const countryNames = {USA:'United States', GBR:'United Kingdom', AUS:'Australia'};
      const all = text('option', 'All available countries'); all.value = '';
      selector.replaceChildren(all);
      for (const code of [...new Set([...d.coverage.countries, ...(discovery.countries || [])])].sort()) {
        const option = text('option', countryNames[code] || code); option.value = code; selector.append(option);
      }
      selector.value = country;
      const learning = document.getElementById('enrollment-learning');
      learning.textContent = discovery.model ? 'Collection: ' + discovery.status.replaceAll('_', ' ') + ' · last run ' + discovery.generated_at + ' · last successful source fetch ' + (discovery.last_success_at || 'none') + ' · model version ' + discovery.model.version + ' · ' + discovery.model.documents + ' metadata titles · ' + discovery.model.vocabulary_size + ' learned terms. Independent relevance evaluation pending.' : 'Awaiting first source collection.';
      const health = document.getElementById('enrollment-source-health'); health.replaceChildren();
      for (const source of discovery.sources) {
        const card = text('div', ''); card.className = 'model-field';
        card.append(text('b', source.publisher), text('p', source.status.replaceAll('_', ' ') + ' · ' + source.items + ' relevant titles' + (source.error_type ? ' · ' + source.error_type : ''))); health.append(card);
      }
      const leads = document.getElementById('enrollment-discovery-records'); leads.replaceChildren();
      const candidates = query ? discovery.matches : discovery.records.slice(0, 30);
      for (const row of candidates) {
        const item = text('p', ''); item.append(link(row.title, row.source_url), text('span', ' · ' + row.country + ' · unreviewed publisher metadata · last seen ' + row.last_seen_at + ' · AI involvement not established')); leads.append(item);
      }
      if (!candidates.length) leads.append(text('p', 'No matching publisher leads in the current collection.'));
      const opportunities = document.getElementById('enrollment-opportunities'); opportunities.replaceChildren();
      for (const o of d.opportunities) {
        const card = text('article', ''); card.className = 'model-field';
        card.append(text('h4', o.title), text('p', o.question), text('p', 'Proposed method: ' + o.design), text('p', 'Measures: ' + o.metrics.join('; ')), text('p', 'Potential submission: ' + o.submission_path + ' · study design requires review'));
        for (const id of o.source_ids) {
          const source = d.records.find(r => r.id === id);
          if (source) card.append(link(source.title, source.source_url), text('br', ''));
        }
        for (const lead of (o.discovery_leads || [])) card.append(text('p', 'Automated research lead: '), link(lead.title, lead.source_url));
        opportunities.append(card);
      }
      const records = document.getElementById('enrollment-records'); records.replaceChildren();
      for (const r of d.records) {
        const card = text('article', ''); card.className = 'model-field';
        card.append(text('h3', r.title), text('p', r.verification.replaceAll('_', ' ')), text('p', r.summary), text('p', 'Evidence: ' + (r.evidence_detail || r.verification).replaceAll('_', ' ') + ' · source date ' + (r.source_date || 'not specified')), text('p', 'AI role: ' + r.ai_role), link('Source and provenance', r.source_url)); records.append(card);
      }
      const matches = document.getElementById('enrollment-matches'); matches.replaceChildren();
      if (query) {
        matches.append(text('h3', 'Related institutional documents'));
        for (const m of d.retrieval.matches) {
          const row = text('p', ''); row.append(link(m.title, m.source_url), document.createTextNode(' · relevance ' + m.similarity.toFixed(3) + ' · shared terms: ' + m.matched_terms.join(', '))); matches.append(row);
        }
        if (!d.retrieval.matches.length) matches.append(text('p', 'No related documents in the current corpus.'));
      }
    } catch (_) {
      if (request !== sequence) return;
      state.textContent = 'Enrollment research is unavailable. Try searching again.';
      document.getElementById('enrollment-records').replaceChildren();
      document.getElementById('enrollment-matches').replaceChildren();
      for (const id of ['enrollment-source-health', 'enrollment-discovery-records', 'enrollment-opportunities']) document.getElementById(id).replaceChildren();
      document.getElementById('enrollment-learning').textContent = 'Collection status unavailable.';
    }
  }
  form.addEventListener('submit', e => { e.preventDefault(); render(); });
  document.getElementById('enrollment-country').addEventListener('change', render);
  // Keep an open dashboard current without creating a new collection job.
  setInterval(() => { if (document.visibilityState === 'visible') render(); }, 60000);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') render(); });
  render();
})();
