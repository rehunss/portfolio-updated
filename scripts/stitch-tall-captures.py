from pathlib import Path
from PIL import Image
import json

root = Path(__file__).resolve().parents[1]
reports = json.loads((root/'qa/visual-review/tall-capture.json').read_text())
for report in reports:
    canvas = Image.new('RGB',(report['width'],report['height']),'white')
    for index,capture in enumerate(report['captures']):
        viewport = Image.open(root/capture['path']).convert('RGB')
        top = 0 if index==0 else round(report['headerHeight'])
        canvas.paste(viewport.crop((0,top,viewport.width,viewport.height)),(0,round(capture['scrollY'])+top))
    canvas.save(root/'qa'/f"final-{report['width']}-full.png")
print('Replaced tall mobile/tablet captures with overlapping real viewport captures.')
