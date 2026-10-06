from pathlib import Path
p=Path(__file__).resolve().parents[1]/'src/Charts.tsx'
s=p.read_text(encoding='utf-8')
s=s.replace("</div>{platform==='linkedin'&&<svg", "</div><PlatformBars platform={platform}/>{platform==='linkedin'&&<svg")
s=s.replace("caption={`${m.label}, Oct 1-Nov 30, 2025; ${m.unit}; team/account outcomes`} headers={['Measure','Target','Actual','% of target']}", "caption=\"TIRIZ campaign, Oct 1-Nov 30, 2025; team/account outcomes; separate units and scales\" headers={['Measure','Unit','Target','Actual','% of target']}")
s=s.replace("return [t.label,format(t.target!),format(t.value)","return [t.label,t.unit,format(t.target!),format(t.value)")
p.write_text(s,encoding='utf-8')
