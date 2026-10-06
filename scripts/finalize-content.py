from pathlib import Path
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[1]
p=root/'src/content.json';data=json.loads(p.read_text(encoding='utf-8'))
data['projects'][1]['takeaway']='Content output and audience response need separate evaluation.'
for s in data['sources']:
    im=Image.open(root/'public'/s['file']);s['width'],s['height']=im.size
def normalize(v):
    if isinstance(v,str): return v.replace('\u2013','-').replace('\u2014','. ')
    if isinstance(v,list): return [normalize(x) for x in v]
    if isinstance(v,dict): return {k:normalize(x) for k,x in v.items()}
    return v
data=normalize(data);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
mf=root/'asset-manifest.json';manifest=json.loads(mf.read_text(encoding='utf-8'))
for name in ['geist-latin-400-normal.woff2','geist-latin-600-normal.woff2','Geist-OFL.txt']:
    f=root/'public/fonts'/name
    manifest.append({'file':'fonts/'+name,'source':'@fontsource/geist npm package, locally installed','license':'SIL Open Font License 1.1, included as Geist-OFL.txt','transform':'none','sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Source dimensions, concise takeaway, ASCII ranges and Geist license recorded.')
