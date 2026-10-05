from pathlib import Path
import zipfile,json,hashlib
root=Path(__file__).resolve().parents[1]
out=root/'output/packages';out.mkdir(parents=True,exist_ok=True)
def archive(name,files,prefix=''):
    dest=out/name
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(set(files)):
            if f.is_file():z.write(f,prefix+f.relative_to(root).as_posix())
    return {'file':name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
source=[]
for d in ['src','public','artwork','scripts','tests']:source.extend((root/d).rglob('*'))
for f in ['.gitignore','package.json','package-lock.json','tsconfig.json','vite.config.ts','index.html','playwright.config.ts','README.md','DESIGN.md','TEST-REPORT.md','asset-manifest.json']:source.append(root/f)
for pattern in ['sharp-*.png','final-*.png','logo-asset-audit.json','axe-chromium-*.json','portfolio-page-*.png','pdf-*.json','delivery-audit.json','playwright-results.json','lighthouse-sharp.report.*']:source.extend((root/'qa').glob(pattern))
source.extend((root/'playwright-report').rglob('*'))
items=[archive('Raihan_Adventure_Source.zip',source,'website/')]
dest=out/'Raihan_Adventure_Production.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in sorted((root/'dist').rglob('*')):
        if f.is_file():z.write(f,f.relative_to(root/'dist').as_posix())
items.append({'file':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
items.append(archive('Raihan_Private_Evidence_Audit.zip',[root/'private'/f for f in ['evidence-register.json','unresolved-claims.md','search-scope.md','revision-notes.md']]))
(out/'package-manifest.json').write_text(json.dumps(items,indent=2),encoding='utf8')
for item in items:
    with zipfile.ZipFile(out/item['file']) as z:
        if z.testzip():raise RuntimeError('Invalid zip: '+item['file'])
        if item['file']=='Raihan_Adventure_Production.zip':
            if 'index.html' not in z.namelist() or any(n.startswith('private/') for n in z.namelist()):raise RuntimeError('Unsafe/incomplete production package')
    print(item['file'],f"{item['bytes']/1024/1024:.1f} MB",'verified')
