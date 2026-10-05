import {asset,experiences,source,type Source} from './content';
const dimensions:Record<string,[number,number]>={fikomnex:[1600,900],hima:[1108,1477],bem:[960,1706],theatre:[1536,2048],ideation:[1108,1477]};
export function ExperienceLog({onProof}:{onProof:(s:Source)=>void}){
 return <div className="experience-list">{experiences.map((e,i)=>{
  const proof=source(e.sourceId);const [width,height]=dimensions[e.id];
  return <article className="experience-card" key={e.id} id={`experience-${e.id}`}>
   <div className="experience-identity">
    <span className="log-number">0{i+1}</span>
    <div className="organization-mark"><img src={asset(e.logo)} alt={e.logoAlt} width="80" height="80" loading="lazy"/></div>
    <span className="organization-label"><span>{e.id==='fikomnex'?'Fikomnex':e.brandLabel}</span>{e.id==='fikomnex'&&<small>Organized by BEM Fikom Unpad</small>}</span>
   </div>
   <div className="experience-main">
    <div className="experience-meta"><span>{e.type}</span><span>{e.period}</span></div>
    <h3>{e.headline}</h3><strong className="experience-role">{e.role}</strong>
    <p>{e.context}</p><p>{e.contribution}</p><p className="experience-result">{e.result}</p>
    <dl className="experience-highlights">{e.highlights.map(h=><div key={h.label}><dt>{h.label}</dt><dd>{h.value}</dd></div>)}</dl>
    <button className="text-button" onClick={()=>onProof(proof)}>View documentation <span aria-hidden="true">↗</span></button>
   </div>
   <button className="experience-photo" aria-label={`View ${e.name} documentation`} onClick={()=>onProof(proof)}><img src={asset(proof.file)} alt={proof.alt} width={width} height={height} loading="lazy"/></button>
  </article>;
 })}</div>;
}
