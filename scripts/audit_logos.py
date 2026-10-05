from pathlib import Path
import json
from PIL import Image

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'src/content.json').read_text(encoding='utf8'))
paths={p['logo'] for p in data['projects']+data['experience']}
paths.update(a['icon'] for g in data['toolGroups'] for a in g['apps'])
records=[]
for path in sorted(paths):
    source=root/'public'/path
    vector=source.suffix=='.svg'
    bitmap=source.with_name(source.stem+'-pdf.png') if vector else source
    image=Image.open(bitmap).convert('RGBA')
    alpha=image.getchannel('A')
    histogram=alpha.histogram()
    transparent=histogram[0]/(image.width*image.height)
    assert alpha.getextrema()==(0,255),f'Missing actual alpha transparency: {path}'
    assert transparent>0.1,f'Unexpected opaque background: {path}'
    assert vector or max(image.size)>=1024,f'Insufficient bitmap resolution: {path}'
    assert (root/'dist'/path).read_bytes()==source.read_bytes(),f'Stale build asset: {path}'
    records.append({'file':path,'nativeVector':vector,'bitmapDimensions':list(image.size),'alphaRange':list(alpha.getextrema()),'transparentFraction':round(transparent,4),'bytes':source.stat().st_size})
assert len(records)==15
text=(root/'src/content.json').read_text(encoding='utf8')
assert not any(s in text for s in ['\u00c2','\u00c3','\u00e2\u20ac']), 'Corrupt text encoding'
result={'uniqueLogoAssets':len(records),'allHaveTransparentBackgrounds':True,'allUseHighResolutionOrVectorAssets':True,'contentEncoding':'UTF-8 verified','logos':records}
(root/'qa/logo-asset-audit.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
