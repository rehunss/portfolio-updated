"""Curate existing evidence without modifying any source file."""
from pathlib import Path
import json, shutil, hashlib
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / 'website'
data = json.loads((OLD/'src/content.json').read_text(encoding='utf-8'))
data['settings'] = {'publicSiteUrl': 'https://rehunss.github.io/portfolio-updated/', 'publicDocumentBase': 'https://rehunss.github.io/portfolio-updated/', 'modernPublished': False}
data['profile']['portfolio'] = 'documents/Raihan_Modern_Portfolio.pdf'
data['profile']['portrait'] = 'assets/portrait-960.webp'
data['projects'][0]['narrative'] = "Divia Unpad TV is a campus media organization. In its three-person marketing team, I used audience insights to plan platform-specific content, activate LinkedIn and support partnership communication. The account results below reflect our shared work. My takeaway: a clear audience and a repeatable process help useful stories travel across platforms."
data['projects'][1]['narrative'] = "Our five-person Pancarona team ran a two-month campaign for TIRIZ, an ice-cream brand. I contributed to content strategy and execution, creator collaboration and the Choose Your Mood offline activation. Content delivery exceeded targets, while average Instagram feed reach fell short. My takeaway: evaluate delivery volume and audience response separately."
data['projects'][2]['narrative'] = "At Cakradata, a technology company, I researched audiences, monitored media and turned student needs into content plans, soft-selling copy and technology explainers. I also contributed on camera. Selected top posts recorded 13,000 TikTok views and 2,000 Instagram views. My takeaway: start with a familiar audience need, then explain the product benefit."
for p in data['projects']:
    p.pop('landmark', None)
for m in data['metrics']:
    if m['id'].startswith('cakradata-'):
        m['period'] = 'Selected top-performing post; analytics date not established'
        m['rolePeriod'] = 'Jan-Feb 2025 internship'
        m['label'] = 'Top TikTok post views' if 'tiktok' in m['id'] else 'Top Instagram post views'
data['metrics'] += [
    dict(id='li-clicks',label='Carousel clicks',value=104,display='104',unit='clicks',period='Jun 2-Jul 29, 2026 UTC export; post Jun 19',attribution='Divia LinkedIn team content',sourceId='divia-linkedin',note='104 / 160 x 100 = 65.0% CTR.'),
    dict(id='tt-comparison',label='Net followers vs. comparison period',value=31.5,display='+31.5%',unit='change in net followers',period='Jun 1-Jul 29, 2026',attribution='Divia TikTok account',sourceId='divia-tiktok',note='Comparison of net followers, not total-follower growth.')]
data['capabilities'] = [
    {'name':'Content strategy & copywriting','example':"Platform-specific LinkedIn planning at Divia and student-focused technology explainers at Cakradata.",'project':'divia'},
    {'name':'Social analytics & campaign evaluation','example':'TIRIZ target-versus-actual evaluation and Divia audience interpretation.','project':'tiriz'},
    {'name':'Partnership communication & outreach','example':'Divia partnership materials and Fikomnex media-partner outreach.','project':'fikomnex'},
    {'name':'Event planning & cross-division coordination','example':'Four Ideation event segments and the HIMA Internship Program across eight divisions.','project':'ideation'},
    {'name':'Recruitment & team coordination','example':'A 15-person HR team at Home Theatre, including recruitment and internal conflict resolution.','project':'theatre'}]
data['certification']['completionId'] = '424502059'
data['certification']['file'] = 'documents/Fundamentals_of_digital_marketing.pdf'
data['certification']['publicUrl'] = data['settings']['publicDocumentBase']+data['certification']['file']

manifest=[]
old_manifest=json.loads((OLD/'asset-manifest.json').read_text(encoding='utf-8'))
def public_manifest_entry(entry):
    # Keep public output details, but never publish local source-evidence paths.
    for key in ('original','sha256Original','worksheet','rows'):
        entry.pop(key, None)
    source=entry.get('source')
    if isinstance(source,str) and not source.startswith(('http://','https://','@fontsource/')):
        entry.pop('source', None)
    return entry

def copy(rel, source=None):
    src=source or OLD/'public'/rel
    dst=ROOT/'public'/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)
    entry=next((public_manifest_entry(x.copy()) for x in old_manifest if x['file']==rel),{'file':rel})
    entry=public_manifest_entry(entry)
    entry['sha256']=hashlib.sha256(dst.read_bytes()).hexdigest()
    manifest.append(entry)

for s in data['sources']:
    copy(s['file'])
    if s.get('excerpt'): copy(s['excerpt'])
copy(data['profile']['cv'],ROOT.parent/'09_Profil_dan_Portofolio/CV_Raihan.pdf')
copy(data['profile']['campaignReport'],ROOT.parent/'01_TIRIZ/TIRIZ_Laporan_Kampanye.pdf')
copy(data['certification']['file'])

# Prefer the genuine 281px HIMA source to the previous AI-assisted enlargement.
data['experience'][1]['logo']='logos/hima.png'
for rel in set([p['logo'] for p in data['projects']]+[e['logo'] for e in data['experience']]):
    copy(rel)
    im=Image.open(ROOT/'public'/rel).convert('RGBA')
    original=im.size
    im.thumbnail((600,600),Image.Resampling.LANCZOS)
    # Same proportions, colours and alpha, optimized display variant.
    name=Path(rel).stem+'-display.webp'
    im.save(ROOT/'public/logos'/name,lossless=True)
    dest='logos/'+name
    manifest.append({'file':dest,'transform':'proportional downsample and lossless WebP; no filters','sourceDimensions':original,'dimensions':im.size})
    for item in data['projects']+data['experience']:
        if item['logo']==rel:
            item['logo']=dest
            item['logoWidth'],item['logoHeight']=im.size
for group in data['toolGroups']:
    for app in group['apps']:
        copy(app['icon'])
        if group['name']=='Google Workspace': app['name']='Google '+app['name']
        if app['name']=='Excel': app['use']='Simple data processing & reporting'

media={}
inputs={'portrait':'assets/raihan-profile.jpg'}
inputs.update({p['id']:p['sample'] for p in data['projects']})
inputs.update({e['id']:data['sources'][next(i for i,s in enumerate(data['sources']) if s['id']==e['sourceId'])]['file'] for e in data['experience']})
for key,rel in inputs.items():
    im=ImageOps.exif_transpose(Image.open(OLD/'public'/rel)).convert('RGB')
    variants=[]
    for width in (480,960,1440):
        out=im.copy()
        out.thumbnail((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)
        dest=f'assets/{key}-{width}.webp'
        out.save(ROOT/'public'/dest,quality=87,method=6)
        variants.append({'src':dest,'width':out.width,'height':out.height})
        manifest.append({'file':dest,'transform':'proportional resize and WebP encoding; no content editing','dimensions':out.size,'sha256':hashlib.sha256((ROOT/'public'/dest).read_bytes()).hexdigest()})
    media[key]={'src':variants[1]['src'],'width':im.width,'height':im.height,'variants':variants}
data['media']=media
(ROOT/'src/content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'asset-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

for name in ['evidence-register.json','unresolved-claims.md','revision-notes.md','search-scope.md']:
    shutil.copy2(OLD/'private'/name,ROOT/'private'/('imported-'+name))
reg=json.loads((OLD/'private/evidence-register.json').read_text(encoding='utf-8'))
reg['reviewDate']='2026-10-06'
reg['modernReview']={'originalSources':'Current local originals and curated proof inspected. User brief confirms experience and top-post claims.','calculations':{'LinkedIn CTR':'104 / 160 * 100 = 65.0%','HIMA participation':'81 / 92 * 100 = 88.043478%, displayed approximately 88%','TIRIZ creator average':'69024 / 4 = 17256','TIRIZ feed reach':'814.1 / 1000 * 100 = 81.41% of target'},'logoDecision':'Genuine original 281px HIMA logo used; previous AI-assisted enlarged version excluded. Other approved owner-repository transparent marks preserved.','searchScope':'Only current nine numbered folders and existing website content, private registers, manifest, source implementation, and curated assets. No new Drive search, sharing changes or wider disk search.'}
(ROOT/'private/evidence-register.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(OLD/'private/unresolved-claims.md',ROOT/'private/unresolved-claims.md')

# Read all primary document text into a private, reviewable current extraction.
extracted=[]
for folder,name in [('09_Profil_dan_Portofolio','CV_Raihan.pdf'),('09_Profil_dan_Portofolio','Portofolio_Raihan_Creative_Revised.pdf'),('01_TIRIZ','TIRIZ_Laporan_Kampanye.pdf')]:
    pdf=PdfReader(ROOT.parent/folder/name)
    extracted.append({'file':folder+'/'+name,'pages':[p.extract_text() for p in pdf.pages]})
(ROOT/'private/primary-documents-text.json').write_text(json.dumps(extracted,ensure_ascii=False,indent=2),encoding='utf-8')

# Contact sheets are for visual inspection only, never published.
refs=[(k,OLD/'public'/v) for k,v in inputs.items()]
refs += [(s['id'],ROOT/'public'/s['file']) for s in data['sources'] if s['id'] in ['divia-ig','divia-audience','divia-tiktok','tiriz-kpi','tiriz-kol','certificate']]
for batch in range(0,len(refs),8):
    subset=refs[batch:batch+8]
    sheet=Image.new('RGB',(1600,1000),'#e6e6e9'); draw=ImageDraw.Draw(sheet)
    for i,(label,path) in enumerate(subset):
        im=ImageOps.exif_transpose(Image.open(path)).convert('RGB'); im.thumbnail((380,430))
        x=(i%4)*400+(400-im.width)//2; y=(i//4)*500+35
        sheet.paste(im,(x,y)); draw.text(((i%4)*400+20,(i//4)*500+10),label,fill='#111111')
    sheet.save(ROOT/'qa'/f'asset-contact-{batch//8+1}.jpg')
print('Prepared',len(manifest),'curated assets; primary PDF pages:',[len(e['pages']) for e in extracted])
