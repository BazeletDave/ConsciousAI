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
      const records = document.getElementById('enrollment-records'); records.replaceChildren();
      for (const r of d.records) {
        const card = text('article', ''); card.className = 'model-field';
        card.append(text('h3', r.title), text('p', r.verification.replaceAll('_', ' ')), text('p', r.summary), text('p', 'AI role: ' + r.ai_role), link('Source and provenance', r.source_url)); records.append(card);
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
    }
  }
  form.addEventListener('submit', e => { e.preventDefault(); render(); });
  document.getElementById('enrollment-country').addEventListener('change', render);
  render();
})();
