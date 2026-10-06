import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
process.chdir(fileURLToPath(new URL('../',import.meta.url)));
const report=JSON.parse(await readFile('qa/delivery-audit.json','utf8'));
const urls=report.uniquePublicUrls;
const results=await Promise.all(urls.map(async url=>{
  try{
    let method='HEAD';
    let r=await fetch(url,{method,redirect:'follow',signal:AbortSignal.timeout(30000)});
    const headStatus=r.status;
    if(r.status===405){
      method='GET';
      r=await fetch(url,{method,redirect:'follow',signal:AbortSignal.timeout(30000)});
      await r.body?.cancel();
    }
    const result={url,status:r.status,method,headStatus,finalUrl:r.url,type:r.headers.get('content-type'),checkedAt:new Date().toISOString()};
    if(r.status>=400)result.note='Automated request could not confirm this destination; browser/login restrictions may apply.';
    return result;
  }catch(e){return {url,error:e.message};}
}));
await writeFile('qa/public-links.json',JSON.stringify(results,null,2));
console.log(JSON.stringify(results,null,2));
if(results.some(r=>r.error||r.status>=400))process.exitCode=1;
