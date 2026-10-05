import raw from './content.json';
export type Source={id:string;label:string;file:string;alt:string;context:string;url?:string;download?:string;downloadLabel?:string;excerpt?:string};
export type Metric={id:string;label:string;value:number;display:string;unit:string;period:string;attribution:string;sourceId:string;note:string;target?:number};
export type Project={id:string;chapter:string;landmark:string;name:string;category:string;period:string;headline:string;narrative:string;contribution:string;takeaway:string;sample:string;sampleAlt:string;sampleCaption:string;sourceIds:string[];metricIds:string[];logo:string;logoAlt:string};
export type Experience={id:string;name:string;role:string;period:string;type:string;text:string;sourceId:string;image:string;headline:string;context:string;contribution:string;result:string;logo:string;logoAlt:string;brandLabel:string;highlights:{value:string;label:string}[]};
export const content=raw;
export const sources:Source[]=raw.sources;
export const metrics:Metric[]=raw.metrics;
export const projects:Project[]=raw.projects;
export const experiences:Experience[]=raw.experience;
export const metric=(id:string)=>metrics.find(m=>m.id===id)!;
export const source=(id:string)=>sources.find(s=>s.id===id)!;
// Public assets stay relative to index.html in both static HTML and React hydration.
// This also works when the same build is hosted in a GitHub Pages subdirectory.
export const asset=(path:string)=>`./${path.replace(/^\/+/, '')}`;
