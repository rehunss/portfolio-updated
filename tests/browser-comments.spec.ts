import {test,expect} from '@playwright/test';

test('comment viewport has compact identity, large clear photos and readable copy',async({page})=>{
 await page.setViewportSize({width:766,height:652});await page.goto('./#experience');
 for(const id of ['fikomnex','hima','bem','theatre','ideation']){
  const card=page.locator('#experience-'+id);await card.scrollIntoViewIfNeeded();
  const logo=card.locator('.organization-mark img');const photo=card.locator('.experience-photo img');
  await photo.scrollIntoViewIfNeeded();await photo.evaluate((i:HTMLImageElement)=>i.decode());
  const size=await photo.evaluate((i:HTMLImageElement)=>({visibleWidth:Math.min(i.clientWidth,i.clientHeight*i.naturalWidth/i.naturalHeight),visibleHeight:Math.min(i.clientHeight,i.clientWidth*i.naturalHeight/i.naturalWidth),fit:getComputedStyle(i).objectFit}));
  expect(size.visibleWidth).toBeGreaterThan(250);expect(size.visibleHeight).toBeGreaterThan(250);expect(size.fit).toBe('contain');
  expect(await logo.evaluate(i=>i.clientHeight)).toBeLessThanOrEqual(88);
  expect(await card.locator('.organization-label').evaluate(i=>parseFloat(getComputedStyle(i).fontSize))).toBeGreaterThanOrEqual(21);
  expect(await card.locator('.experience-main p').first().evaluate(i=>parseFloat(getComputedStyle(i).fontSize))).toBeGreaterThanOrEqual(18);
  await card.locator('.experience-photo').click();await expect(page.getByRole('dialog')).toBeVisible();await page.keyboard.press('Escape');
 }
 await expect(page.locator('#divia .project-brand img')).toHaveCSS('filter','none');
 await expect(page.locator('.discovery-window,.depth-guide')).toHaveCount(0);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);
});

test('background camera continues smoothly across the landing boundary',async({page})=>{
 await page.goto('./');await page.evaluate(()=>document.fonts.ready);await page.locator('.earth-texture').evaluate((i:HTMLImageElement)=>i.decode());await expect(page.getByRole('button',{name:'Motion on',exact:true})).toBeVisible();
 const boundary=await page.locator('#start').evaluate(i=>i.getBoundingClientRect().height);
 const positions:number[]=[];const source=await page.locator('.earth-texture').getAttribute('src');
 for(const offset of [-120,0,120]){
  await page.evaluate(y=>scrollTo({top:y,behavior:'instant'}),boundary+offset);
  await expect.poll(()=>page.locator('.earth-scene').evaluate(i=>new DOMMatrixReadOnly(getComputedStyle(i).transform).m42)).toBeLessThan(positions.at(-1)??0);
  positions.push(await page.locator('.earth-scene').evaluate(i=>new DOMMatrixReadOnly(getComputedStyle(i).transform).m42));
  await expect(page.locator('.earth-texture')).toHaveAttribute('src',source!);
 }
 expect(Math.abs((positions[1]-positions[0])-(positions[2]-positions[1]))).toBeLessThan(2);
 await expect(page.locator('.earth-texture')).toHaveCount(1);await expect(page.locator('.hero .scene')).toHaveCount(0);
});
