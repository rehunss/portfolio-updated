from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parents[1]
output = root / 'qa' / 'visual-review'
output.mkdir(exist_ok=True)
for width in (390, 768, 1440, 1920):
    shot = Image.open(root / 'qa' / f'final-{width}-full.png').convert('RGB')
    segment_height = 1800 if width < 1000 else 2400
    panels = []
    for index, top in enumerate(range(0, shot.height, segment_height)):
        panel = shot.crop((0, top, shot.width, min(top + segment_height, shot.height)))
        if width >= 1000:
            panel = panel.resize((720, round(panel.height * 720 / panel.width)), Image.Resampling.LANCZOS)
        canvas = Image.new('RGB', (panel.width, panel.height + 28), '#e7e7eb')
        canvas.paste(panel, (0, 28))
        ImageDraw.Draw(canvas).text((12, 8), f'{width}px / part {index+1} / y={top}', fill='#1d1d1f')
        canvas.save(output / f'website-{width}-part-{index+1:02}.jpg', quality=94)
        panels.append(canvas)
    # A compact overview supports chapter-transition review; use individual parts for text.
    overview = Image.new('RGB', (len(panels) * 230, max(round(p.height * 230 / p.width) for p in panels)), '#e7e7eb')
    for index, panel in enumerate(panels):
        overview.paste(panel.resize((230, round(panel.height * 230 / panel.width)), Image.Resampling.LANCZOS), (index*230, 0))
    overview.save(output / f'website-{width}-overview.jpg', quality=94)
