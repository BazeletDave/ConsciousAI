(() => {
 const status=document.getElementById('tiger-assurance-status'),holder=document.getElementById('tiger-assurance-results');
 const text=(tag,value)=>{const e=document.createElement(tag);e.textContent=value;return e;};
 const names={fixed:'Fixed distribution',forward_gated:'Long to short with gate',goal_gated:'Short to long with gate',forward_equal_exposure:'Long to short equal exposure',goal_equal_exposure:'Short to long equal exposure'};
 const percent=m=>(100*m.mean).toFixed(2)+'%';
 fetch('/institutional/tiger-assurance',{cache:'no-store'}).then(async response=>{
  if(!response.ok)throw Error('Unavailable');const d=await response.json();
  status.textContent=d.trained_models+' trained synthetic models · '+d.training_interactions.toLocaleString()+' training interactions · '+d.assigned_holdout_cases.toLocaleString()+' assigned holdout cases · exact rerun matched · artifact integrity checked · no model promoted';
  holder.replaceChildren(text('p',d.finding));
  const wrap=text('div','');wrap.style.overflowX='auto';const table=text('table','');table.className='source-table';
  const head=text('tr','');for(const label of ['Curriculum','Hidden change: original allows','Hidden change: monitor allows','Biased probe: monitor allows','Recovery validation passes','Corrected task success'])head.append(text('th',label));table.append(head);
  for(const arm of d.arms){const row=text('tr','');row.append(text('td',names[arm.arm]||arm.arm));for(const field of ['hidden_baseline_allow','hidden_monitor_allow','biased_probe_monitor_allow','recovery_validation','recovery_task_success_per_assigned_case']){
   const m=arm[field],cell=text('td',percent(m));cell.title='95% seed bootstrap interval: '+(100*m.low).toFixed(2)+'% to '+(100*m.high).toFixed(2)+'%';row.append(cell);
  }table.append(row);}wrap.append(table);holder.append(wrap);
  holder.append(text('p','Recovery validation is measured among attempted candidates; corrected task success uses all assigned hidden shift cases. Local checks omitted lateral task accuracy. Every candidate remains subject to human review.'));
  const comparison=d.paired_comparisons.equal_exposure_order;
  holder.append(text('p','Equal exposure curriculum difference, short to long minus long to short: '+(100*comparison.mean).toFixed(3)+' percentage points; 95% interval '+(100*comparison.low).toFixed(3)+' to '+(100*comparison.high).toFixed(3)+'. No superiority demonstrated.'));
  document.getElementById('tiger-assurance-limits').textContent=d.limitations.join(' ');
 }).catch(()=>{status.textContent='Experiment integrity could not be verified. No model is promoted.';holder.replaceChildren();});
})();
