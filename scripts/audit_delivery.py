from pathlib import Path
import json,hashlib,re
from PIL import Image
from io import BytesIO
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
content=json.loads((root/'src/content.json').read_text(encoding='utf8'))
register=json.loads((root/'private/evidence-register.json').read_text(encoding='utf8'))
claims={c['id']:c for c in register['claims']}
pdf=PdfReader(root/'output/pdf/Raihan_Adventure_Portfolio.pdf')
text='\n'.join(page.extract_text() for page in pdf.pages)
checks={}
checks['tenLandscapePages']=len(pdf.pages)==10 and all(float(p.mediabox.width)>float(p.mediabox.height) for p in pdf.pages)
checks['selectableTextEveryPage']=all(len(p.extract_text().strip())>300 for p in pdf.pages)
checks['allMetricDisplaysInPDF']=all(m['display'] in text for m in content['metrics'])
checks['websiteRegisterMetricConsistency']=all(all(m[k]==claims[m['id']][k] for k in ['label','value','display','unit','period','attribution','sourceId']) for m in content['metrics'])
checks['audienceTotals100']=abs(sum(r['value'] for r in content['audience']['rows'])-100)<0.000001
checks['sourceOriginalsPreserved']=all(hashlib.sha256((root.parent/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in register['inputInventory'])
checks['originalCVBytesPreserved']=(root/'public/documents/CV_Raihan.pdf').read_bytes()==(root.parent/'09_Profil_dan_Portofolio/CV_Raihan.pdf').read_bytes()
checks['fullTirizReportBytesPreserved']=(root/'public/documents/TIRIZ_Laporan_Kampanye.pdf').read_bytes()==(root.parent/'01_TIRIZ/TIRIZ_Laporan_Kampanye.pdf').read_bytes()==(root/'dist/documents/TIRIZ_Laporan_Kampanye.pdf').read_bytes()
portrait=Image.open(root/'public/assets/raihan-profile.jpg').convert('RGB')
checks['realPortraitEmbeddedOnCover']=any(Image.open(BytesIO(i.data)).convert('RGB').tobytes()==portrait.tobytes() for i in pdf.pages[0].images)
checks['hardSkillAppsInPDF']=all(a['name'] in text for g in content['toolGroups'] for a in g['apps'])
compact=re.sub(r'\s+',' ',text)
checks['revisedExperienceCountsInPDF']=all(s in compact for s in ['81 of 92','approximately 88%','14-member','15-person','four event segments','seven-person team'])
checks['noCVSourceCaveatsInPDF']=not re.search(r'mentioned on CV|based on (the )?CV|supplied CV|CV p\.',text,re.I)
checks['pdfCopiesMatch']=len({hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['output/pdf/Raihan_Adventure_Portfolio.pdf','public/documents/Raihan_Adventure_Portfolio.pdf','dist/documents/Raihan_Adventure_Portfolio.pdf']})==1
links=[str(a.get_object()['/A']['/URI']) for p in pdf.pages for a in p.get('/Annots',[]) if '/A' in a.get_object() and '/URI' in a.get_object()['/A']]
expected=json.loads((root/'qa/pdf-links.json').read_text(encoding='utf8'))
checks['pdfLinkAnnotationsMatch']=links==[e['url'] for e in expected]
checks['publicProofFilesExist']=all((root/'public'/s['file']).is_file() and (root/'dist'/s['file']).is_file() and (not s.get('excerpt') or (root/'dist'/s['excerpt']).is_file()) for s in content['sources'])
checks['privateAuditNotInBuild']=not (root/'dist/private').exists()
checks['staticHTMLHasProfileAndProjects']=all(s in (root/'dist/index.html').read_text(encoding='utf8') for s in ['Muhammad Raihan Ramadhan','id="divia"','id="tiriz"','814.1','65.0%'])
result={'checkedAt':'2026-10-05','checks':checks,'pages':len(pdf.pages),'links':len(links),'metricRecords':len(content['metrics']),'originalFiles':len(register['inputInventory']),'publicProofSources':len(content['sources']),'pdfSHA256':hashlib.sha256((root/'output/pdf/Raihan_Adventure_Portfolio.pdf').read_bytes()).hexdigest()}
(root/'qa/delivery-audit.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
if not all(checks.values()):raise SystemExit('Delivery audit failed')
