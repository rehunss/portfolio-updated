"""Create a clearly labeled, selected-cell transcription from the original XLS."""
from pathlib import Path
import json,hashlib,html
root=Path(__file__).resolve().parents[1]
original=Path('C:/Users/Hp/Downloads/divia-unpad-tv-fikom_content_1785500685838.xls')
raw=json.loads((root/'private/linkedin-export.json').read_text(encoding='utf8'))
rows=raw['All posts']; headers=rows[1]
records=[]
for date,label in [('06/04/2026','Launch post'),('06/08/2026','Partnership post'),('06/19/2026','Career carousel')]:
    row=next(r for r in rows[2:] if r[5]==date)
    records.append({'label':label,'title':row[0].split('\n')[0],'link':row[1],'date':row[5],'impressions':int(row[9]),'clicks':int(row[12]),'ctr':row[13],'row':rows.index(row)+1,'poster':'Raihan' if row[4]=='Muhammad Raihan Ramadhan' else 'Teammate'})
checksum=hashlib.sha256(original.read_bytes()).hexdigest()
body=''.join(f'<tr><th scope="row">{r["label"]}</th><td>{r["date"]} UTC</td><td>{r["impressions"]}</td><td>{r["clicks"]}</td><td>{r["clicks"]/r["impressions"]*100:.1f}%</td><td>{r["poster"]}</td><td>{r["row"]}</td></tr>' for r in records)
titles=''.join(f'<li><a href="{html.escape(r["link"])}">{r["label"]}</a>: {html.escape(r["title"])}</li>' for r in records)
document=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Divia LinkedIn — original export excerpt</title><style>body{{max-width:960px;margin:40px auto;padding:0 24px;background:#f7f4eb;color:#142733;font:18px/1.6 system-ui,sans-serif}}h1{{font-size:32px;line-height:1.2}}a{{color:#246f78}}a:focus-visible{{outline:3px solid #aa6b09;outline-offset:4px}}.table{{overflow:auto}}table{{border-collapse:collapse;width:100%;background:white}}th,td{{padding:12px;text-align:left;border:1px solid #c6d2d1}}code{{overflow-wrap:anywhere;font-size:13px}}small{{color:#4b626d}}caption{{text-align:left;margin-bottom:12px}}</style></head><body><a href="../index.html?divia=LinkedIn#divia">Return to Divia case study</a><h1>Divia LinkedIn: original export excerpt</h1><p>Selected cells transcribed from the <strong>All posts</strong> worksheet of the July 31, 2026 export. This is a readable source excerpt, not an analytics screenshot. Original numerical values are preserved; CTR is displayed as a percentage rounded to one decimal.</p><div class="table"><table><caption>Account / team content. Export reporting window: June 2–July 29, 2026. Created dates and times in UTC.</caption><thead><tr><th>Post</th><th>Created date</th><th>Impressions</th><th>Clicks</th><th>CTR</th><th>Poster</th><th>Excel row</th></tr></thead><tbody>{body}</tbody></table></div><p>CTR = clicks ÷ impressions × 100. Career carousel: 104 ÷ 160 × 100 = <strong>65.0%</strong>. The export names a teammate as poster; this result is credited to the team. Poster labels summarize the source's Posted by column.</p><h2>Matched published posts</h2><ul>{titles}</ul><p><a href="https://drive.google.com/file/d/1Glx99H3Ka_S3G5sRo2wbbg59Jsyy3jgJ/view">Open the original workbook on Drive</a> (existing access permissions apply).</p><small>Source file: divia-unpad-tv-fikom_content_1785500685838.xls<br>SHA-256: <code>{checksum}</code><br>Reviewed October 5, 2026. Only three selected rows are reproduced.</small></body></html>'''
dest=root/'public/proof/divia-linkedin-export.html';dest.write_text(document,encoding='utf8')
c=json.loads((root/'src/content.json').read_text(encoding='utf8'))
next(s for s in c['sources'] if s['id']=='divia-linkedin')['excerpt']='proof/divia-linkedin-export.html'
(root/'src/content.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
manifest=json.loads((root/'asset-manifest.json').read_text(encoding='utf8'))
manifest=[m for m in manifest if m['file']!='proof/divia-linkedin-export.html']
manifest.append({'file':'proof/divia-linkedin-export.html','type':'source-evidence-transcription','source':str(original),'worksheet':'All posts','rows':[r['row'] for r in records],'sha256Original':checksum,'transform':'Selected cells transcribed to semantic HTML; CTR formatted to one decimal; poster names summarized as Raihan/Teammate. No generated analytics.'})
(root/'asset-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Curated export excerpt created:',[(r['label'],r['row'],r['impressions'],r['clicks']) for r in records])
