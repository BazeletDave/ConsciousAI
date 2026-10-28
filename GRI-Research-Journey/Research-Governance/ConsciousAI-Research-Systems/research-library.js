(() => {
  const byId = id => document.getElementById(id);
  const text = (tag, value) => {const el = document.createElement(tag); el.textContent = value; return el;};
  const link = (title, url) => {const a=text('a',title); try {const u=new URL(url); if(u.protocol==='https:' && u.hostname==='github.com' && !u.username && !u.password){a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';}}catch(_){}return a;};
  let catalog=null, page=0, request=0;
  async function get(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Research unavailable');return r.json();}
  function browse(){
    if(!catalog)return;
    const q=byId('research-library-filter').value.trim().toLowerCase();
    const topic=byId('research-topic').value;
    const rows=catalog.documents.filter(d=>(!topic||d.topics.includes(topic))&&(!q||(d.title+' '+d.path).toLowerCase().includes(q)));
    page=Math.max(0,Math.min(page,Math.max(0,Math.ceil(rows.length/12)-1)));
    byId('research-library-count').textContent=rows.length+' matching documents · page '+(page+1);
    const holder=byId('research-library-documents');holder.replaceChildren();
    for(const d of rows.slice(page*12,page*12+12)){const card=text('article','');card.className='model-field';card.append(link(d.title,d.url),text('p',d.path),text('p',d.evidence_status.replaceAll('_',' ')));holder.append(card);}
    byId('research-library-prev').disabled=page===0;byId('research-library-next').disabled=(page+1)*12>=rows.length;
  }
  byId('research-library-filter').addEventListener('input',()=>{page=0;browse();});
  byId('research-topic').addEventListener('change',()=>{page=0;browse();});
  byId('research-library-prev').addEventListener('click',()=>{page--;browse();});
  byId('research-library-next').addEventListener('click',()=>{page++;browse();});
  byId('research-question-form').addEventListener('submit',async event=>{
    event.preventDefault();const q=byId('research-question').value.trim();const answer=byId('research-answer');
    if(!q){answer.textContent='Enter a research question.';return;}
    const sequence=++request;answer.textContent='Searching indexed passages…';
    const params=new URLSearchParams({q});if(byId('research-topic').value)params.set('topic',byId('research-topic').value);
    try{
      const d=await get('/research/ask?'+params);if(sequence!==request)return;answer.replaceChildren(text('h3','Research answer'),text('p',d.answer));
      for(const source of d.sources){const card=text('article','');card.className='model-field';card.append(link('['+source.citation+'] '+source.title,source.url),text('blockquote',source.excerpt),text('p','Evidence status: '+source.evidence_status.replaceAll('_',' ')));answer.append(card);}
      if(d.unmatched_terms.length)answer.append(text('p','Question terms without matching support in these passages: '+d.unmatched_terms.join(', ')));
      answer.append(text('p',d.limitations.join(' ')));
    }catch(_){if(sequence===request)answer.textContent='The research answer service is unavailable. Other dashboard modules remain available.';}
  });
  get('/research/catalog').then(d=>{
    catalog=d;byId('research-library-status').textContent=d.document_count+' indexed documents · '+d.passage_count+' passages · '+d.linked_artifacts.length+' linked artifacts · '+(1+(d.external_sources||[]).length)+' connected repositories · updated '+d.generated_at;
    for(const source of (d.external_sources||[])){byId('research-library-status').append(text('p',source.repository+' · '+(source.status||'initial snapshot')+' · '+source.documents+' documents'));}
    for(const topic of d.topics){const option=text('option',topic.title+' ('+topic.documents+')');option.value=topic.id;byId('research-topic').append(option);}
    const artifacts=byId('research-library-artifacts');artifacts.replaceChildren();for(const a of d.linked_artifacts){const p=text('p','');p.append(link(a.title,a.url));artifacts.append(p);}browse();
  }).catch(()=>{byId('research-library-status').textContent='Research coverage is unavailable. Other dashboard modules remain available.';});
})();
