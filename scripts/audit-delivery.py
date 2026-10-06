from pathlib import Path
import json,re,hashlib
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'src/content.json').read_text(encoding='utf-8'))
pdf=PdfReader(root/'output/pdf/Raihan_Modern_Portfolio.pdf')
assert len(pdf.pages)==10
texts=[p.extract_text() for p in pdf.pages];joined=' '.join(texts)
norm=lambda s:re.sub(r'-\s+', '-', ' '.join(s.split()))
for p in data['projects']: assert norm(p['narrative']) in norm(joined),p['id']
for e in data['experience']:
    for k in ['context','contribution','result']: assert norm(e[k]) in norm(joined),(e['id'],k)
for v in ['22K','11K','133','78','4,427','417','31.5%','160','104','65.0%','814.1','81.41%','69,024','6,072','17,256','13,000','2,000','424502059','9,898','180','9,745','3,765','2,471','401.1K','3.1K']:
    assert v in joined,v
for term in ['800%','GPA','game','underground']: assert term.lower() not in joined.lower(),term
links=[]
for i,page in enumerate(pdf.pages):
    assert abs(float(page.mediabox.width)-841.89)<1 and abs(float(page.mediabox.height)-595.28)<1
    assert f'{i+1:02d} / 10' in texts[i]
    for ann in page.get('/Annots',[]):
        obj=ann.get_object();url=obj.get('/A',{}).get('/URI')
        if url: links.append(str(url))
assert data['settings']['publicSiteUrl'] in links
assert all('localhost' not in u and '127.0.0.1' not in u for u in links)
assert any(u.startswith('mailto:') for u in links)
docchecks=[]
for rel,original in [(data['profile']['cv'],'09_Profil_dan_Portofolio/CV_Raihan.pdf'),(data['profile']['campaignReport'],'01_TIRIZ/TIRIZ_Laporan_Kampanye.pdf')]:
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    hashes=[digest(root/'public'/rel),digest(root/'dist'/rel),digest(root.parent/original)]
    assert len(set(hashes))==1,rel
    docchecks.append({'file':rel,'sha256':hashes[0],'sourceByteIdentical':True,'productionByteIdentical':True})
assert (root/'public/documents/Raihan_Modern_Portfolio.pdf').read_bytes()==(root/'output/pdf/Raihan_Modern_Portfolio.pdf').read_bytes()
assert (root/'dist/documents/Raihan_Modern_Portfolio.pdf').read_bytes()==(root/'output/pdf/Raihan_Modern_Portfolio.pdf').read_bytes()
assert not (root/'dist/private').exists()
assets=json.loads((root/'asset-manifest.json').read_text(encoding='utf-8'))
for item in assets:
    f=root/'public'/item['file'];assert f.exists(),str(f)
    if item.get('sha256'): assert hashlib.sha256(f.read_bytes()).hexdigest()==item['sha256'],item['file']
logo_alpha=[]
for name in set([p['logo'] for p in data['projects']]+[e['logo'] for e in data['experience']]):
    im=Image.open(root/'public'/name).convert('RGBA');alpha=im.getchannel('A');assert alpha.getextrema()[0]==0,name
    logo_alpha.append({'file':name,'dimensions':im.size,'transparent':True})
report={'pages':10,'pageFormat':'A4 landscape','links':len(links),'uniquePublicUrls':sorted(set(u for u in links if u.startswith('http'))),'selectableText':True,'contentModelNarrativesAndExperienceMatch':True,'approvedNumbersPresent':True,'excludedClaimsAbsent':True,'documents':docchecks,'curatedAssetEntries':len(assets),'logos':logo_alpha,'privateExcludedFromBuild':True,'websitePublicSetting':data['settings']['publicSiteUrl'],'projectNarrativeWords':{p['id']:len(p['narrative'].split()) for p in data['projects']}}
(root/'qa/delivery-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['pages','links','curatedAssetEntries','contentModelNarrativesAndExperienceMatch','privateExcludedFromBuild','projectNarrativeWords']},indent=2))
# Actual Poppler page renders, two review sheets with all ten pages.
pages=sorted((root/'qa/pdf').glob('page-*.png'))
if len(pages)==10:
    for group in range(0,10,5):
        sheet=Image.new('RGB',(2246,3*830),'#d9d9dd');draw=ImageDraw.Draw(sheet)
        for i,path in enumerate(pages[group:group+5]):
            im=Image.open(path).convert('RGB');im.thumbnail((1100,778))
            x=(i%2)*1123;y=(i//2)*830+32
            sheet.paste(im,(x,y));draw.text((x+20,y-23),path.stem,fill='#111111')
        sheet.save(root/'qa/pdf'/f'review-sheet-{group//5+1}.jpg',quality=95)
