import {test,expect} from '@playwright/test';

for(const [width,height] of [[390,844],[768,1024],[1440,900],[1920,1080]]){
 test(`transparent high-resolution logos fit at ${width} × ${height}`,async({page})=>{
  await page.setViewportSize({width,height});await page.goto('./');
  const logos=page.locator('.project-brand img,.organization-mark img,.tools-inventory img');
  await expect(logos).toHaveCount(16);
  for(const logo of await logos.all()){
   await logo.scrollIntoViewIfNeeded();
   await expect.poll(()=>logo.evaluate((i:HTMLImageElement)=>i.complete&&i.naturalWidth>0)).toBeTruthy();
   const size=await logo.evaluate((i:HTMLImageElement)=>({width:i.clientWidth,height:i.clientHeight,natural:i.naturalWidth,vector:i.src.endsWith('.svg'),background:getComputedStyle(i).backgroundColor}));
   expect(size.background).toBe('rgba(0, 0, 0, 0)');
   if(!size.vector)expect(size.natural).toBeGreaterThanOrEqual(size.width*2);
   expect(size.width).toBeGreaterThanOrEqual(64);
   if(await logo.evaluate(i=>!!i.closest('.organization-mark'))){expect(size.height).toBeGreaterThanOrEqual(64);expect(size.height).toBeLessThanOrEqual(88);}
  }
  for(const mark of await page.locator('.organization-mark').all())await expect(mark).toHaveCSS('background-color','rgba(0, 0, 0, 0)');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);
 });
}
