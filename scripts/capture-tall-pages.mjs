import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
process.chdir(fileURLToPath(new URL('../', import.meta.url)));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const reports = [];
  for (const [width, height] of [[390,844],[768,1024]]) {
    const page = await browser.newPage({ viewport: { width, height }, reducedMotion:'reduce' });
    await page.goto('http://127.0.0.1:4174/portfolio-updated/', { waitUntil:'networkidle' });
    await page.evaluate(async () => {
      await document.fonts.ready;
      for(let y=0;y<document.body.scrollHeight;y+=600) {
        scrollTo(0,y);
        await new Promise(resolve=>requestAnimationFrame(resolve));
      }
      await Promise.all([...document.images].map(image=>image.decode().catch(()=>{})));
      scrollTo(0,0);
    });
    const facts = await page.evaluate(()=>({
      height:document.documentElement.scrollHeight,
      headingCount:document.querySelectorAll('h1').length,
      contactCount:document.querySelectorAll('#contact').length,
      headerHeight:document.querySelector('header').getBoundingClientRect().height
    }));
    const directory = `qa/visual-review/viewport-${width}`;
    await mkdir(directory,{recursive:true});
    const captures = [];
    for(let y=0,index=0;;y+=height-facts.headerHeight,index++) {
      await page.evaluate(target=>scrollTo({top:target,behavior:'instant'}), y);
      await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
      const scrollY = await page.evaluate(()=>window.scrollY);
      const path = `${directory}/part-${String(index).padStart(2,'0')}.png`;
      await page.screenshot({path});
      captures.push({path,scrollY});
      if(scrollY+height>=facts.height-1)break;
    }
    reports.push({width,viewportHeight:height,...facts,captures});
    await page.close();
  }
  await writeFile('qa/visual-review/tall-capture.json',JSON.stringify(reports,null,2));
  console.log(JSON.stringify(reports.map(({captures,...facts})=>({...facts,viewportCaptures:captures.length})),null,2));
} finally { await browser.close(); }
