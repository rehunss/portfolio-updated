from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'private/pdf_reader'))
import json,html,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTFont as FontConverter
from PIL import Image

root=Path(__file__).resolve().parents[1];data=json.loads((root/'src/content.json').read_text(encoding='utf8'))
out=root/'output/pdf/Raihan_Adventure_Portfolio.pdf';out.parent.mkdir(parents=True,exist_ok=True)
fonts=root/'tmp/fonts';fonts.mkdir(parents=True,exist_ok=True)
for family,pkg,weight in [('Body','source-sans-3',400),('Bold','source-sans-3',700),('Pixel','silkscreen',400)]:
    path=root/f'node_modules/@fontsource/{pkg}/files/{pkg}-latin-{weight}-normal.woff'
    f=FontConverter(path);f.flavor=None;f.save(fonts/f'{family}.ttf');pdfmetrics.registerFont(TTFont(family,str(fonts/f'{family}.ttf')))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
W,H=841.89,595.28
navy='#142733';muted='#4b626d';amber='#aa6b09';teal='#246f78';line='#c6d2d1';light='#f7f4eb';white='#ffffff'
c=canvas.Canvas(str(out),pagesize=(W,H));c.setTitle('Muhammad Raihan Ramadhan - Adventure Portfolio');c.setAuthor('Muhammad Raihan Ramadhan');c.setSubject('Selected marketing communication, content strategy and collaboration work. Verified October 2026.')
metrics={m['id']:m for m in data['metrics']};sources={s['id']:s for s in data['sources']};projects={p['id']:p for p in data['projects']}
links=[];boxes=[]
def clean(s):return str(s).replace('–','-').replace('—','-').replace('\u2011','-').replace('÷','/').replace('×','x')
def rect(x,y,w,h,fill,stroke=None):
    c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill));c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
def text(s,x,y,size=12,font='Body',color=navy):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,clean(s))
def para(s,x,y,w,size=13,color=navy,font='Body',leading=None,maxh=500):
    style=ParagraphStyle('body',fontName=font,fontSize=size,leading=leading or size*1.4,textColor=HexColor(color),spaceAfter=0)
    p=Paragraph(clean(s),style);pw,ph=p.wrap(w,maxh)
    if ph>maxh:raise ValueError(f'Paragraph exceeds frame on page {c.getPageNumber()}: {ph}>{maxh}: {s[:80]}')
    p.drawOn(c,x,H-y-ph);boxes.append({'page':c.getPageNumber(),'x':x,'y':y,'w':w,'h':ph,'text':s[:100]});return ph
def link(label,url,x,y,w=350,size=11):
    h=para(html.escape(label)+' (link)',x,y,w,size,teal,maxh=60)
    c.linkURL(url,(x,H-y-h,x+w,H-y),relative=0,thickness=0);links.append({'page':c.getPageNumber(),'label':label,'url':url});return h
def image(path,x,y,w,h):
    p=root/'public'/path
    # Website uses native app vectors; their 512px transparent render is for print.
    if p.suffix=='.svg':p=p.with_name(p.stem+'-pdf.png')
    im=Image.open(p);iw,ih=im.size;ratio=min(w/iw,h/ih);dw,dh=iw*ratio,ih*ratio
    c.drawImage(ImageReader(im),x+(w-dw)/2,H-y-h+(h-dh)/2,dw,dh,mask='auto',preserveAspectRatio=True)
def image_cover(path,x,y,w,h):
    im=Image.open(root/'public'/path);iw,ih=im.size;ratio=max(w/iw,h/ih);dw,dh=iw*ratio,ih*ratio
    c.saveState();p=c.beginPath();p.rect(x,H-y-h,w,h);c.clipPath(p,stroke=0,fill=0)
    c.drawImage(ImageReader(im),x+(w-dw)/2,H-y-h,dw,dh,mask='auto');c.restoreState()
def header(chapter,title,num):
    rect(0,0,W,H,light);rect(0,0,W,8,navy);rect(40,36,6,6,amber);text(chapter.upper(),57,30,9,'Pixel',teal)
    para(html.escape(title),40,59,750,25,navy,'Pixel',leading=34,maxh=75)
    c.setStrokeColor(HexColor(line));c.line(40,H-108,W-40,H-108)
    text('MUHAMMAD RAIHAN RAMADHAN / SELECTED WORK',40,H-30,8,'Pixel',muted);text(f'{num:02d} / 10',W-103,H-30,8,'Pixel',muted)
def footer_source(s,y=522):para(html.escape(s),40,y,760,8,muted,leading=11,maxh=34)
def section(label,x,y):text(label.upper(),x,y,9,'Pixel',teal)
def stat(m,x,y,w=172):
    rect(x,y,w,82,white,line);text(m['label'],x+13,y+11,10,'Body',muted);text(m['display'],x+13,y+29,23,'Pixel',navy)
    para(html.escape(m['unit']),x+13,y+62,w-25,8,muted,maxh=18)
def comparison(m,x,y,w=345):
    label=m['label'];para(html.escape(label),x,y,w,12,navy,'Bold',maxh=40)
    maximum=max(m['value'],m['target']);bh=12;available=w-82
    for i,(name,val,color) in enumerate([('Target',m['target'],'#93a9b2'),('Actual',m['value'],teal if m['value']>=m['target'] else '#b77b1e')]):
        yy=y+27+i*27;text(name,x,yy-1,10,'Body',muted);rect(x+45,yy,available,bh,'#e0e7e5');rect(x+45,yy,available*val/maximum,bh,color)
        text(f'{val:,.1f}' if val%1 else f'{int(val):,}',x+w-31,yy-1,9,'Bold',navy)
    text(f"{m['value']/m['target']*100:,.2f}% of target | {m['unit']}",x,y+84,9,'Body',muted)
def end():c.showPage()

# 1: cover
header('Start / profile','A creative adventure',1)
text(data['profile']['name'],40,132,25,'Bold')
para('Marketing communication.<br/>Content strategy. Public relations.',40,170,490,23,navy,'Bold',leading=29,maxh=100)
para(html.escape(data['profile']['intro']),40,273,475,15,muted,maxh=72)
para(html.escape(data['profile']['education'])+'.',40,348,440,12,muted,maxh=50)
image('assets/raihan-profile.jpg',573,122,210,286)
rect(40,420,762,88,navy);image_cover('assets/creative-town.webp',40,420,762,88)
for i,(name,desc) in enumerate([('DIVIA','Campus media'),('TIRIZ','F&B campaign'),('CAKRADATA','Technology content')]):
    x=53+i*252;rect(x,439,223,48,light);text(name,x+10,447,10,'Pixel');text(desc,x+10,467,10,'Body',muted)
footer_source('Marketing communication, content strategy and public relations. Selected work and team outcomes, October 2026.');end()

# 2: Divia process
p=projects['divia'];header('01 / The campus studio','Divia Unpad TV',2)
image(p['logo'],40,118,190,48)
image(p['sample'],430,129,370,259)
section('Marketing communication internship',40,177);text(p['period'],40,197,12,'Body',muted)
para(html.escape(p['headline']),40,226,350,23,navy,'Bold',maxh=85)
para(html.escape(p['narrative']),40,284,350,13,muted,maxh=160)
para('Published career-tips carousel. Team content; the export names a teammate as the poster.',430,397,360,11,muted,maxh=55)
section('My contribution',40,440);para(html.escape(p['contribution']),40,460,350,12,maxh=47)
link('Open the published carousel',sources['divia-linkedin']['url'],430,465,340)
footer_source('Sources: Divia content planner and job-training report; published work sample; LinkedIn original July 31 export.');end()

# 3: Divia data
header('01 / Platform field notes','Three platforms. Separate signals.',3)
for i,id in enumerate(['ig-views','ig-viewers','ig-shares','ig-saves']):stat(metrics[id],40+i*192,126,176)
para('Instagram - May 31-Jul 30, 2026. Account-level results; K values are rounded as displayed.',40,218,760,10,muted,maxh=30)
section('TikTok / Jun 1-Jul 29, 2026',40,260)
text(metrics['tt-total']['display'],40,289,25,'Pixel');text(metrics['tt-total']['label'].lower(),40,328,12)
text(metrics['tt-net']['display'],225,289,25,'Pixel');text(metrics['tt-net']['label'].lower(),225,328,12)
para('+31.5% compares net followers with the comparison period. It is not total-follower growth.',40,358,340,12,muted,maxh=80)
section('LinkedIn / export Jun 2-Jul 29, UTC',432,260)
text(metrics['li-ctr']['display']+' CTR',432,289,24,'Pixel')
para('104 clicks / 160 impressions x 100. Team carousel result.',432,323,355,10,muted,maxh=31)
for i,id in enumerate(['li-launch','li-sop','li-carousel']):
    m=metrics[id];yy=354+i*21;text(m['label'],432,yy-2,9,'Body',muted);rect(543,yy,200,7,'#e0e7e5');rect(543,yy,200*m['value']/max(metrics[x]['value'] for x in ['li-launch','li-sop','li-carousel']),7,teal);text(m['display'],755,yy-3,9,'Bold')
text('Impressions - original All posts worksheet',432,417,8,'Body',muted)
section('Instagram follower age / May 31-Jul 30',40,421)
for i,r in enumerate(data['audience']['rows']):
    yy=441+i*11;text(r['label'],40,yy-1,9,'Body',muted);rect(82,yy+2,210,6,'#e0e7e5');rect(82,yy+2,210*r['value']/100,6,amber if i==1 else teal);text(f"{r['value']:.1f}%",304,yy-1,9,'Bold')
para(html.escape(data['audience']['takeaway']),432,454,355,12,muted,maxh=62)
link('Open original LinkedIn export','https://drive.google.com/file/d/1Glx99H3Ka_S3G5sRo2wbbg59Jsyy3jgJ/view',432,499,355,10)
footer_source('Sources: original Instagram Insights (May 31-Jul 30, 2026); TikTok follower report; LinkedIn XLS All posts worksheet. Source definitions retained.');end()

# 4: TIRIZ campaign
p=projects['tiriz'];header('02 / The campaign marketplace','TIRIZ: from content to experience',4)
section('Academic client campaign / five-person team',40,130);text(p['period'],40,150,12,'Body',muted)
image(p['logo'],40,171,230,90)
para(html.escape(p['narrative']),40,277,345,13,muted,leading=17,maxh=119)
section('My contribution',40,411);para(html.escape(p['contribution']),40,431,345,12,maxh=80)
image('proof/tiriz-offline-event.png',423,125,378,302)
para('Choose Your Mood activation. The report dates the booth to November 25, 2025. A digital campaign brought to life through an interactive booth.',423,441,370,11,muted,maxh=65)
footer_source('Sources: TIRIZ campaign report pp.9-11,16-17,19; working content planner. Team campaign / Oct-Nov 2025.');end()

# 5: TIRIZ evaluation final-state charts
header('02 / Campaign evaluation','Delivery and response are different.',5)
for i,id in enumerate(['tiriz-stories','tiriz-videos','tiriz-feed-reach','tiriz-tt-views']):comparison(metrics[id],40+(i%2)*398,130+(i//2)*123,354)
rect(40,390,762,104,white,line)
section('Creator collaboration / campaign totals',55,401)
for i,id in enumerate(['tiriz-kol-views','tiriz-kol-engagements','tiriz-kol-average']):
    m=metrics[id];x=55+i*251;text(m['display'],x,425,22,'Pixel');text(m['label'],x,460,10)
para('Four KOL pieces. 69,024 / 4 = 17,256 average views. That is 1,725.6% of the 1,000-view target, or 1,625.6% above it.',40,501,760,10,muted,maxh=31)
link('Read the full TIRIZ campaign report',data['profile']['campaignReportUrl'],40,541,760,9)
footer_source('Oct 1-Nov 30, 2025. Team/account and creator outcomes. Source: TIRIZ original report p.16 (targets) and p.9 (KOL totals). Average feed reach missed target.',527);end()

# 6: Cakradata
p=projects['cakradata'];header('03 / The strategy workshop','Cakradata: start with the audience',6)
image(p['logo'],40,122,270,85)
section('Marketing internship / Jan-Feb 2025',40,214)
para(html.escape(p['headline']),40,230,430,23,navy,'Bold',leading=29,maxh=62)
para(html.escape(p['narrative']),40,296,410,13,muted,leading=17,maxh=102)
for i,id in enumerate(p['metricIds']):stat(metrics[id],40+i*208,404,193)
image('proof/cakradata.jpg',505,130,278,366)
footer_source('Top-performing content: views per selected post, not total account views. Marketing work: audience research, content planning and soft-selling copy.');end()

# 7: Fikomnex and HIMA
header('04 / Collaboration hub','Outreach and organizational growth',7)
for i,id in enumerate(['fikomnex','hima']):
    e=next(e for e in data['experience'] if e['id']==id);x=40+i*397
    image(e['image'],x,128,243,109)
    if id=='fikomnex':rect(x+252,128,113,109,navy)
    image(e['logo'],x+252,128,113,109)
    para(html.escape(e['headline']),x,249,365,19,navy,'Bold',leading=24,maxh=55)
    para(html.escape(e['role']),x,306,365,12,teal,'Bold',leading=16,maxh=39)
    text(e['period'],x,351,10,'Body',muted)
    para(html.escape(e['context']),x,374,365,11,muted,leading=15,maxh=62)
    para(html.escape(e['contribution']),x,438,365,12,navy,leading=16,maxh=49)
    para(html.escape(e['result']),x,489,365,11,teal,leading=14,maxh=40)
footer_source('Student event / organization roles. Fikomnex: organized by BEM Fikom Unpad. HIMA participation: 81 / 92 x 100 = 88.04%, rounded to approximately 88%.',542);end()

# 8: BEM, Home Theatre and Ideation
header('04 / Party log','Teams that shaped my approach',8)
for i,id in enumerate(['bem','theatre','ideation']):
    e=next(e for e in data['experience'] if e['id']==id);y=125+i*137
    rect(40,y,762,129,white,line)
    if id=='bem':rect(49,y+8,105,113,navy)
    image(e['logo'],49,y+8,105,113)
    para(html.escape(e['headline']),166,y+6,620,17,navy,'Bold',leading=22,maxh=25)
    para(html.escape(e['role'])+' | '+html.escape(e['period']),166,y+34,620,10.5,teal,'Bold',leading=13,maxh=27)
    para(html.escape(e['text']),166,y+65,620,11,muted,leading=14,maxh=58)
footer_source('Student organizations and events: organizational supervision, HR coordination and international competition delivery.',543);end()

# 9: Skills and hard-skill tools from the same content model
header('05 / Inventory','Skills and tools for the work',9)
for i,a in enumerate(data['capabilities']):
    x=40+(i%2)*396;y=126+(i//2)*99;rect(x,y,368,89,white,line)
    para(html.escape(a['name']),x+14,y+9,340,15,navy,'Bold',leading=18,maxh=23)
    para(html.escape(a['tools']),x+14,y+35,340,10,muted,leading=13,maxh=28)
    para(html.escape(a['example']),x+14,y+65,340,9,teal,leading=12,maxh=18)
for i,g in enumerate(data['toolGroups']):
    x=40+i*258;rect(x,335,246,141,white,line)
    text(g['name'],x+13,346,14,'Bold')
    para(html.escape(g['description']),x+13,371,220,10,muted,leading=13,maxh=38)
    apps=g['apps'];step=min(55,220/len(apps))
    for j,a in enumerate(apps):
        xx=x+12+j*step;image(a['icon'],xx,412,128 if a['name']=='Canva' else 48,48)
        para(html.escape(a['name']),xx-3,462,step+3,8,navy,leading=9,maxh=12)
rect(40,488,762,47,white,line)
text(data['certification']['name'],53,496,14,'Bold');text(data['certification']['date'],53,516,10,'Body',muted)
link('Open completion certificate','https://drive.google.com/file/d/1ueCDiIOzBVkAIv1bCabXRrzgBjl9yfR9/view',548,505,237,10)
footer_source('Course completion: original certificate p.1, completion ID 424502059. Excel: simple data processing. Canva: light editing.',545);end()

# 10 Contact/evidence
header('06 / Next chapter','Let\'s make something worth sharing.',10)
text(data['profile']['name'],40,138,24,'Bold')
para('For opportunities in marketing communication,<br/>social media, digital marketing and public relations.',40,181,580,18,muted,maxh=74)
link(data['profile']['email'],'mailto:'+data['profile']['email'],40,274,620,16)
link('LinkedIn / Muhammad Raihan Ramadhan',data['profile']['linkedin'],40,321,660,14)
link('Visit portfolio website / rehunss.github.io/portfolio-updated', 'https://rehunss.github.io/portfolio-updated/',40,359,760,13)
section('Selected evidence links',40,405)
for i,(label,url) in enumerate([
('Divia published career carousel',sources['divia-linkedin']['url']),
('Divia original analytics folder','https://drive.google.com/drive/folders/1ctP-28KCyufR_ADB9BJdL5SSxZoUrSSD'),
('Full TIRIZ campaign report',data['profile']['campaignReportUrl']),
('Fundamentals of digital marketing certificate','https://drive.google.com/file/d/1ueCDiIOzBVkAIv1bCabXRrzgBjl9yfR9/view')]):
    link(label,url,40+(i%2)*397,431+(i//2)*36,365,11)
para('The website includes full-size curated proof and both document downloads. External source links retain their existing permissions; some may require access.',40,515,760,10,muted,maxh=24)
footer_source('Muhammad Raihan Ramadhan | Selected work and experience | October 2026',545);end()
c.save();shutil.copy2(out,root/'public/documents'/out.name)
(root/'qa/pdf-links.json').write_text(json.dumps(links,indent=2),encoding='utf8');(root/'qa/pdf-text-frames.json').write_text(json.dumps(boxes,indent=2),encoding='utf8')
print(f'Created {out}, 10 landscape pages, {len(links)} clickable links. Website download synchronized.')
