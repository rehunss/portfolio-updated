from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'src/App.tsx';s=p.read_text(encoding='utf-8')
s=s.replace('MotionConfig, useReducedMotion','MotionConfig')
s=s.replace('const reduce=useReducedMotion();',"""const [reduce,setReduce]=useState(()=>matchMedia('(prefers-reduced-motion: reduce)').matches);
  useEffect(()=>{const query=matchMedia('(prefers-reduced-motion: reduce)');const sync=()=>setReduce(query.matches);query.addEventListener('change',sync);sync();return()=>query.removeEventListener('change',sync);},[]);""")
s=s.replace('aria-labelledby="proof-title" onCancel={close}', '''aria-labelledby="proof-title" onKeyDown={e=>{if(e.key!=='Tab')return;const nodes=[...e.currentTarget.querySelectorAll<HTMLElement>('button,a[href],[tabindex="0"]')].filter(el=>el.offsetWidth>0||el.offsetHeight>0);const first=nodes[0],last=nodes[nodes.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus();}}} onCancel={close}''')
s=s.replace('<img src={asset(evidence.file)} alt={evidence.alt}/>', '<img src={asset(evidence.file)} alt={evidence.alt} width={evidence.width} height={evidence.height}/>')
p.write_text(s,encoding='utf-8')
p=root/'src/Charts.tsx';s=p.read_text(encoding='utf-8')
s=s.replace('onClick={()=>setTip(tip===mid?null:mid)}','onClick={()=>setTip(mid)}')
s=s.replace('onClick={()=>setTip(tip===r.label?null:r.label)}','onClick={()=>setTip(r.label)}')
s=s.replace('onClick={()=>setActive(active===r.label?null:r.label)}','onClick={()=>setActive(r.label)}')
s=s.replace('className="chart-panel platform-chart"','className="chart-panel platform-chart" onKeyDown={e=>{if(e.key===\'Escape\')setTip(null);}}')
s=s.replace('className="chart-panel tiriz-chart"','className="chart-panel tiriz-chart" onKeyDown={e=>{if(e.key===\'Escape\')setTip(null);}}')
s=s.replace('className="chart-panel age-chart"','className="chart-panel age-chart" onKeyDown={e=>{if(e.key===\'Escape\')setActive(null);}}')
p.write_text(s,encoding='utf-8')
print('Modal trapping, reactive reduced motion, proof dimensions and tap/Escape chart details refined.')
