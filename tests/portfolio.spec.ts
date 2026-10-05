import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import path from 'node:path';
const dimensions=[[390,844],[768,1024],[1440,900],[1920,1080]];

for(const [width,height] of dimensions){
test(`layout, assets and accessibility ${width}x${height}`,async({page},testInfo)=>{
 const errors:string[]=[];const missing:string[]=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('response',r=>{if(r.status()>=400&&r.url().includes('127.0.0.1'))missing.push(r.url())});
 await page.setViewportSize({width,height});await page.goto('./');await page.evaluate(()=>document.fonts.ready);await expect(page.getByRole('heading',{level:1})).toContainText('Ideas with purpose');
 for(const id of ['start','projects','divia','tiriz','cakradata','experience','experience-hima','experience-bem','experience-theatre','experience-ideation','skills','contact']){await page.locator('#'+id).scrollIntoViewIfNeeded();await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);}
 await expect.poll(()=>page.locator('img').evaluateAll(imgs=>imgs.filter((x:any)=>x.getBoundingClientRect().bottom>0&&x.getBoundingClientRect().top<innerHeight&&(!x.complete||x.naturalWidth===0)).map((x:any)=>x.src))).toEqual([]);expect(errors).toEqual([]);expect(missing).toEqual([]);
 if(width===390)expect(await page.locator('a,button,summary,select').evaluateAll(els=>els.filter(e=>e.getClientRects().length).map(e=>({label:e.textContent?.trim(),width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height})).filter(e=>e.width<44||e.height<44))).toEqual([]);
 await page.goto('./');await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:`qa/${testInfo.project.name}-${width}x${height}-start.png`});
 const scan=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();fs.writeFileSync(`qa/axe-${testInfo.project.name}-${width}.json`,JSON.stringify(scan.violations,null,2));expect(scan.violations).toEqual([]);
 if(width===390||width===1440){await page.locator('#divia').scrollIntoViewIfNeeded();await page.getByRole('button',{name:'Motion on',exact:true}).click();await page.screenshot({path:`qa/${testInfo.project.name}-${width}-divia.png`});await page.locator('#tiriz').scrollIntoViewIfNeeded();await page.screenshot({path:`qa/${testInfo.project.name}-${width}-tiriz.png`});await page.locator('#contact').scrollIntoViewIfNeeded();await page.screenshot({path:`qa/${testInfo.project.name}-${width}-contact.png`});}
});}

test('navigation, deep links, refresh and browser history',async({page})=>{
 await page.goto('./');await page.getByRole('link',{name:'Explore projects',exact:true}).click();await expect(page).toHaveURL(/#projects$/);await page.getByRole('link',{name:'02 TIRIZ',exact:false}).first().click();await expect(page).toHaveURL(/#tiriz$/);await page.reload();await expect(page.locator('#tiriz')).toBeInViewport();await page.goBack();await expect(page).toHaveURL(/#projects$/);await page.goForward();await expect(page).toHaveURL(/#tiriz$/);
 await page.setViewportSize({width:390,height:844});await page.getByRole('button',{name:'Menu',exact:false}).click();await expect(page.locator('#main-nav')).toBeVisible();await page.locator('#main-nav').getByRole('link',{name:'Contact',exact:true}).click();await expect(page).toHaveURL(/#contact$/);await expect(page.locator('#main-nav')).toBeHidden();await page.getByRole('button',{name:'Menu',exact:false}).click();await page.keyboard.press('Escape');await expect(page.locator('#main-nav')).toBeHidden();
});

test('keyboard, skip link, proof dialog focus and escape',async({page})=>{
 await page.goto('./');await page.keyboard.press('Tab');await expect(page.getByRole('link',{name:'Skip to content'})).toBeFocused();await page.keyboard.press('Enter');await expect(page).toHaveURL(/#main$/);
 const trigger=page.locator('#divia').getByRole('button',{name:'View proof',exact:true});await trigger.focus();await page.keyboard.press('Enter');await expect(page.getByRole('dialog')).toBeVisible();await expect(page.getByRole('button',{name:'Close proof'})).toBeFocused();
 await page.keyboard.press('Shift+Tab');await expect.poll(()=>page.evaluate(()=>document.querySelector('dialog')?.contains(document.activeElement))).toBeTruthy();await page.keyboard.press('Tab');await page.keyboard.press('Escape');await expect(page.getByRole('dialog')).not.toBeVisible();await expect(trigger).toBeFocused();
 await expect.poll(()=>trigger.evaluate(e=>getComputedStyle(e).outlineStyle)).not.toBe('none');
});

test('charts retain definitions, expose tables and support focus and tap',async({page})=>{
 await page.goto('./');const divia=page.locator('#divia');await divia.getByRole('button',{name:'TikTok',exact:true}).click();await expect(divia.locator('.chart-panel').first()).toContainText('4,427');await expect(divia.locator('.chart-panel').first()).toContainText('+417');await expect(divia.locator('.chart-takeaway').first()).toContainText('not total follower growth');
 await divia.getByRole('button',{name:'LinkedIn',exact:true}).click();await expect(page).toHaveURL(/divia=LinkedIn/);await expect(divia.locator('.chart-takeaway').first()).toContainText('104 clicks from 160');await divia.locator('.data-table').first().getByText('View data table',{exact:true}).click();await expect(divia.locator('table').first()).toContainText('65.0%');
 const label=page.locator('#li-launch-control');await label.focus();await expect(page.locator('#li-launch-detail')).toBeVisible();await page.keyboard.press('Escape');await expect(page.locator('#li-launch-detail')).toBeHidden();await label.click();await expect(page.locator('#li-launch-detail')).toBeVisible();
 const target=page.locator('#target-metric');await target.selectOption('tiriz-feed-reach');await expect(page.locator('#tiriz .chart-takeaway')).toContainText('81.41% of target');await expect(page.locator('#tiriz .chart-takeaway')).toContainText('target missed');await target.selectOption('tiriz-kol-average');await expect(page.locator('#tiriz .chart-takeaway')).toContainText('1,725.6% of target');await page.reload();await expect(target).toHaveValue('tiriz-kol-average');await page.goBack();await expect(target).toHaveValue('tiriz-feed-reach');
 await page.setViewportSize({width:390,height:844});const age=page.locator('#age-1-control');await age.click();await expect(page.locator('#age-1-detail')).toBeVisible();await expect(page.locator('#age-1-detail')).toContainText('54.0%');
});

test('persistent motion preference and system reduced motion',async({page})=>{
 await page.goto('./');await expect(page.getByRole('button',{name:'Motion on',exact:true})).toBeVisible();await page.getByRole('button',{name:'Motion on',exact:true}).click();await page.reload();await expect(page.getByRole('button',{name:'Motion off',exact:true})).toHaveAttribute('aria-pressed','false');await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-camera','still');await expect(page.locator('#tiriz')).toContainText('120');
 await page.evaluate(()=>localStorage.clear());await page.emulateMedia({reducedMotion:'reduce'});await page.reload();await expect(page.getByRole('button',{name:'Motion off',exact:true})).toBeVisible();await page.locator('#tiriz').scrollIntoViewIfNeeded();await expect(page.locator('#tiriz')).toContainText('69,024');await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-camera','still');
});

test('real PDF responses, downloads and source privacy',async({page,request},testInfo)=>{
 await page.goto('./');for(const file of ['CV_Raihan.pdf','Raihan_Adventure_Portfolio.pdf']){const response=await request.get(`documents/${file}`);expect(response.status()).toBe(200);expect(response.headers()['content-type']).toContain('application/pdf');const body=await response.body();expect(body.subarray(0,5).toString()).toBe('%PDF-');if(file==='CV_Raihan.pdf')expect(body.equals(fs.readFileSync(path.resolve('../09_Profil_dan_Portofolio/CV_Raihan.pdf')))).toBeTruthy();}
 const promise=page.waitForEvent('download');await page.getByRole('link',{name:'Download portfolio',exact:true}).click();const download=await promise;expect(download.suggestedFilename()).toBe('Raihan_Adventure_Portfolio.pdf');await download.saveAs(`qa/download-${testInfo.project.name}.pdf`);
 expect((await request.get('private/evidence-register.json')).status()).toBe(404);expect((await request.get('src/content.json')).status()).toBe(404);
});

test('LinkedIn source excerpt is readable and matches original export cells',async({page})=>{
 await page.goto('./');await page.locator('#divia').getByRole('button',{name:'View proof',exact:true}).click();
 const link=page.getByRole('link',{name:'Read original export excerpt'});await expect(link).toHaveAttribute('href','./proof/divia-linkedin-export.html');
 const tabPromise=page.waitForEvent('popup');await link.click();const tab=await tabPromise;await tab.waitForLoadState();
 await expect(tab.getByRole('heading',{level:1})).toContainText('original export excerpt');const carousel=tab.getByRole('row').filter({has:tab.getByRole('rowheader',{name:'Career carousel',exact:true})});
 await expect(carousel).toContainText('160');await expect(carousel).toContainText('104');await expect(carousel).toContainText('65.0%');await expect(carousel).toContainText('Teammate');
 await tab.getByRole('link',{name:'Return to Divia case study'}).click();await expect(tab).toHaveURL(/divia=LinkedIn#divia$/);await expect(tab.locator('#divia')).toBeInViewport();await tab.close();
});
