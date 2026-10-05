import {useEffect,useState} from 'react';
import {useMotionValueEvent,useScroll,useTransform} from 'motion/react';
import * as motion from 'motion/react-m';
import {asset} from './content';

const layers=[
 {name:'Surface',at:0},
 {name:'Topsoil',at:0.10},
 {name:'Sedimentary rock',at:0.18},
 {name:'Crust',at:0.34},
 {name:'Upper mantle',at:0.48},
 {name:'Lower mantle',at:0.64},
 {name:'Outer core',at:0.82},
 {name:'Inner core',at:0.94}
];
const finds=[
 {index:0,top:20,left:5,size:88}, {index:1,top:38,left:86,size:85},
 {index:2,top:100,left:3,size:150}, {index:2,top:116,left:89,size:92},
 {index:3,top:151,left:87,size:115}, {index:4,top:190,left:2,size:150},
 {index:5,top:180,left:84,size:128}, {index:6,top:267,left:2,size:124},
 {index:7,top:284,left:89,size:125}
];
export function EarthWorld({motionOn}:{motionOn:boolean}){
 const {scrollYProgress}=useScroll();
 const [viewport,setViewport]=useState({height:0,dpr:1});
 useEffect(()=>{const measure=()=>setViewport({height:window.innerHeight,dpr:window.devicePixelRatio||1});measure();window.addEventListener('resize',measure);return()=>window.removeEventListener('resize',measure);},[]);
 // Keep camera movement on whole physical pixels to avoid resampling the artwork.
 const y=useTransform(scrollYProgress,p=>-Math.round(p*viewport.height*6*viewport.dpr)/viewport.dpr);
 const [layer,setLayer]=useState(0);
 useMotionValueEvent(scrollYProgress,'change',v=>{let i=0;for(let n=1;n<layers.length;n++)if(v>=layers[n].at)i=n;setLayer(i);});
 // Without motion, switch to a still view only when a geological layer changes.
 const still=-Math.round((layer===layers.length-1?1:layers[layer].at)*viewport.height*6*viewport.dpr)/viewport.dpr;
 const current=layers[layer];
 return <div className="earth-backdrop" aria-hidden="true" data-world="town-to-core" data-layer={current.name} data-camera={motionOn?'continuous':'still'}>
   <motion.div className="earth-scene" style={{y:motionOn?y:still,height:viewport.height?viewport.height*7:undefined}}>
    <picture className="earth-picture">
     <source media="(max-width:900px)" type="image/avif" srcSet={asset('assets/continuous-world-sharp-2x.avif')}/>
     <source type="image/avif" srcSet={asset('assets/continuous-world-sharp-4x.avif')}/>
     <img className="earth-texture pixel-art" src={asset('assets/continuous-world-sharp-4x.webp')} width="2896" height="8688" alt="" fetchPriority="high"/>
    </picture>
    {finds.map((f,i)=><span key={i} className={`earth-find find-${f.index}`} style={{top:`${f.top+100}vh`,left:`${f.left}%`,width:f.size,height:f.size,backgroundImage:`url(${asset('assets/underground-finds.webp')})`}}/>)}
   </motion.div>
   <div className="earth-shade"/>
  </div>;
}
