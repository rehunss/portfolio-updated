import {firefox,webkit} from 'playwright';
import {writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
process.chdir(fileURLToPath(new URL('../',import.meta.url)));
const results={};
for(const [name,type] of Object.entries({firefox,webkit})){
 try{const b=await type.launch({headless:true});const page=await b.newPage();await page.goto('http://127.0.0.1:4174/portfolio-updated/');results[name]={available:true,title:await page.title()};await b.close();}
 catch(e){results[name]={available:false,reason:e.message.split('\n').slice(0,3).join(' ')};}
}
await writeFile('qa/browser-availability.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
