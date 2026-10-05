# Creative town and underground design system

The website is a dusk adventure menu with a clear recruiter journey. Pixel art and headings establish the setting; readable body text and real screenshots explain the work. Native links and scrolling provide immediate access. The user's explicit 16-bit game aesthetic determines the typography, stepped edges, chapter numbering and menu controls.

## Tokens

| Role | Website | Print |
|---|---|---|
| Background | `#101e2a` | `#f7f4eb` |
| Content panel | `#182b37` | `#ffffff` |
| Text | `#f5efdf` | `#142733` |
| Supporting text | `#c0cbd0` | `#4b626d` |
| Interactive accent | `#ffd17a` | `#aa6b09` |
| Supporting accent | `#91cfca` | `#246f78` |
| Border | `#48616c` | `#c6d2d1` |

Tokens are defined in `src/styles.css` with Tailwind v4 `@theme` and CSS variables. Silkscreen 400 is for short titles, menus and large figures. Source Sans 3 400/600/700 is for readable narrative, controls, definitions and chart labels. The content width is 1200px; spacing follows a restrained 4px base with larger chapter breaks.

## Art and interaction

One generated town-to-core panorama connects the landing sky, mountain town, grass, roots, soil, sedimentary rock, crust, mantle and core. The same image remains behind every section: no separate hero scene or background swap interrupts the journey. The image tool restored crisp edges at its native 724 × 2172 size. A 4× nearest-neighbor, lossless 2896 × 8688 master supplies the website; modern browsers receive optimized full-color AVIF at 1448 × 4344 on narrow screens and 2896 × 8688 on desktop, with a lossless WebP fallback; this pixel-preserving export does not imply additional native detail. Both masters and the exact prompt are preserved. The browser uses crisp-edge sampling and a camera snapped to whole physical pixels, avoiding interpolation as it scrolls.

The transparent eight-object sprite atlas adds earthworms/pebbles, sedimentary fossils, crustal quartz/gold, a fictional miner's chest, and upper-mantle diamonds/peridotite in their relative layers. The mantle becomes dense rock; the outer core liquid metal; the inner core solid metal. Illustrated distances are compressed. The scenery has no labels baked into the artwork. Earlier town, workshop, marketplace, avatar and cross-section originals remain reusable assets. Only decorative art uses pixel rendering.

Content uses navy panels separated by glimpses of the continuous terrain. Documentary photos and screenshots retain ordinary image rendering and meaning. Organization marks float on transparent backgrounds without recoloring or added outline filters. App icons accompany plain descriptions of Docs, Sheets, Slides, Drive, Word, PowerPoint, Excel and Canva. Fikomnex explicitly identifies its BEM Fikom organizer mark. The PDF uses Raihan's real portrait and the same verified experience/results/tool content.

The shared panorama follows native document scrolling. Its seven-viewport scene travels six viewport heights, starting with the town and ending at the core. One continuous transform crosses the landing boundary without a jump. There are no endless loops, sounds or gameplay barriers. The section indicator shows location. Motion preference persists; OS reduced-motion is respected. Reduced mode replaces continuous camera movement with still views at layer boundaries, retaining all chart values and controls. Direct anchors and refresh load the correct scene.

Decorative objects remain part of the scenery, without standalone discovery panels or geological fact controls. The full TIRIZ report remains available in its case study and proof dialog. The decorative footer sentence was removed.

Audience shares use a fixed 0–100% scale in both website and PDF. Charts compare like units on shared scales; different platforms/definitions remain separate. Target comparisons use actual/target, with the missed feed-reach target labeled in text. Bars animate only transforms. Every chart has a source, reporting period, attribution, stable figures and a data table. Focus, tap and hover reveal the metric note.

Native `dialog` provides modal focus trapping and Escape handling. Menus, disclosures and charts use semantic controls. Touch targets are at least 44px. Project links and query-based chart state preserve browser history. See the test report for measured behavior.

## Logo and experience presentation

Experience identity rows use 80px logo frames, reduced to 72px on mobile, beside organization names at 21–24px. Body descriptions are 18–19px and role labels 18–19px. Full original photos remain uncropped, displayed up to 340px wide in the desktop side column and up to 560px wide / 490px high in the stacked tablet layout. Mobile photos fill the available card width. Clicking a photo opens its full-size proof.

Project wordmarks remain prominent; app marks use 64px icons, with the Canva wordmark 104px wide. No pixel rendering or extra outline filters are applied to logos. Brand colors and intrinsic logo shapes remain present. The existing matching print portfolio retains its larger marks and high-resolution transparent renders of native app vectors.