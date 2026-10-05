import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import path from 'node:path';

test('experience stories, app icons and Cakradata top posts',async({page})=>{
 await page.goto('./');
 const hima=page.locator('#experience-hima');await expect(hima).toContainText('81 of 92');await expect(hima).toContainText('approximately 88%');await expect(hima).toContainText('All established program KPIs were achieved');
 await expect(page.locator('#experience-bem')).toContainText('14-member');await expect(page.locator('#experience-bem')).toContainText('Welcoming Party');
 await expect(page.locator('#experience-theatre')).toContainText('15-person');await expect(page.locator('#experience-theatre')).toContainText('nine divisions');
 await expect(page.locator('#experience-ideation')).toContainText('four event segments');await expect(page.locator('#experience-ideation')).toContainText('seven-person');
 for(const id of ['fikomnex','hima','bem','theatre','ideation']){const e=page.locator('#experience-'+id);await e.scrollIntoViewIfNeeded();await expect(e.locator('.organization-mark img')).toHaveAttribute('alt',/.+/);await expect.poll(()=>e.locator('.organization-mark img').evaluate((i:HTMLImageElement)=>i.complete&&i.naturalWidth>0)).toBeTruthy();}
 await page.locator('#cakradata').scrollIntoViewIfNeeded();await expect(page.locator('#cakradata .metric-strip')).toContainText('13,000');await expect(page.locator('#cakradata .metric-strip')).toContainText('2,000');await expect(page.locator('#cakradata .metric-strip')).toContainText('Top-performing post');
 await page.locator('.tools-inventory').scrollIntoViewIfNeeded();await expect(page.locator('.tools-inventory img')).toHaveCount(8);for(const name of ['Docs','Sheets','Slides','Drive','Word','PowerPoint','Excel','Canva'])await expect(page.locator('.tools-inventory').getByRole('img',{name:name+' logo',exact:true})).toBeVisible();
 await expect(page.locator('.tools-inventory')).toContainText('Simple data processing');await expect(page.locator('.tools-inventory')).toContainText('Light visual editing');
 expect(await page.locator('main').innerText()).not.toMatch(/mentioned on CV|based on (the )?CV|supplied CV|summarized from.*CV|role in the CV|tracker independently records/i);
});

test('full TIRIZ report opens the unchanged original PDF',async({page,request})=>{
 await page.goto('./');const link=page.getByRole('link',{name:'Full TIRIZ campaign report',exact:true});await expect(link).toHaveAttribute('href','./documents/TIRIZ_Laporan_Kampanye.pdf');
 const response=await request.get('documents/TIRIZ_Laporan_Kampanye.pdf');expect(response.status()).toBe(200);expect(response.headers()['content-type']).toContain('application/pdf');const body=await response.body();expect(body.equals(fs.readFileSync(path.resolve('../01_TIRIZ/TIRIZ_Laporan_Kampanye.pdf')))).toBeTruthy();
 const popup=page.waitForEvent('popup');await link.click();const tab=await popup;await expect(tab).toHaveURL(/documents\/TIRIZ_Laporan_Kampanye.pdf$/);await tab.close();
 await page.locator('#tiriz').getByRole('button',{name:'View proof',exact:true}).click();await expect(page.getByRole('dialog').getByRole('link',{name:'Open full TIRIZ campaign report'})).toHaveAttribute('href','./documents/TIRIZ_Laporan_Kampanye.pdf');await page.keyboard.press('Escape');
});

test('continuous town-to-core world without discovery panels',async({page})=>{
 await page.goto('./');const scene=page.locator('.earth-scene');await page.locator('#profile').scrollIntoViewIfNeeded();await expect(scene).toBeVisible();await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-camera','continuous');
 const expected=['Surface','Topsoil','Sedimentary rock','Crust','Upper mantle','Lower mantle','Outer core','Inner core'];const stages:string[]=[];for(const [index,fraction] of [0,0.12,0.25,0.40,0.55,0.70,0.88,1].entries()){await page.evaluate(f=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*f,behavior:'instant'}),fraction);await expect.poll(()=>page.locator('.earth-backdrop').getAttribute('data-layer')).toBe(expected[index]);stages.push((await page.locator('.earth-backdrop').getAttribute('data-layer'))!);}
 expect(stages).toEqual(expected);await expect(page.locator('.discovery-window,.depth-guide,.treasure-link')).toHaveCount(0);await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-world','town-to-core');await expect(page.locator('.earth-texture')).toHaveCount(1);await expect(page.locator('.hero .scene')).toHaveCount(0);await expect(page.locator('#contact footer')).not.toContainText('Original pixel world');
 const scan=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();expect(scan.violations).toEqual([]);
 await page.goto('./#contact');await expect(page.locator('.earth-texture')).toBeVisible();await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-layer','Inner core');
});

test('motion off keeps a still scene within each layer and persists',async({page})=>{
 await page.goto('./');await page.getByRole('button',{name:'Motion on',exact:true}).click();await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-camera','still');
 await page.evaluate(()=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*0.51,behavior:'instant'}));await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-layer','Upper mantle');const transform=await page.locator('.earth-scene').evaluate(e=>getComputedStyle(e).transform);
 await page.evaluate(()=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*0.54,behavior:'instant'}));await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-layer','Upper mantle');await expect(page.locator('.earth-scene')).toHaveCSS('transform',transform);
 await page.reload();await expect(page.getByRole('button',{name:'Motion off',exact:true})).toBeVisible();await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-camera','still');
 await page.evaluate(()=>localStorage.clear());await page.emulateMedia({reducedMotion:'reduce'});await page.reload();await expect(page.locator('.earth-backdrop')).toHaveAttribute('data-camera','still');
});
