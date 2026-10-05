# Verification report — October 5, 2026

Production preview: `http://127.0.0.1:4173/portfolio-preview/`. The finished build was served with gzip compression under a GitHub Pages-style subdirectory. No live site was modified.

## Browser and interaction results

Playwright 1.63 with installed Google Chrome / Chromium 154: the earlier full suite passed **20 tests in 1.4 minutes**. After the sharp-background and camera update, the targeted current suite passed **6 tests in 52.5 seconds**, with zero failures, skips or flaky results. These cover the continuous landing transition, all underground stages, reduced-motion persistence, experience controls and full-report link. The installed Playwright CLI was also used for direct desktop/mobile interaction, touch-target measurement and screenshot review. The final logo revision also checks native vector or at least 2× bitmap resolution at each rendered size, transparent presentation, image loading and responsive fit at all four viewports. An additional 766 × 652 check matches the browser-comment viewport.

| Check | Result |
|---|---|
| 390 × 844, 768 × 1024, 1440 × 900, 1920 × 1080 | Passed: no horizontal overflow, broken visible images, local 404s, page errors or console errors |
| Section links, project links, refresh, Back/Forward | Passed, including native hash links and chart query state |
| Mobile menu | Passed: open, select section, close and Escape |
| Keyboard and focus | Passed: skip link, visible focus, proof dialog entry/trap/return and Escape |
| Charts | Passed: platform selection, focus/tap details, accessible tables, query restoration and target calculations |
| Motion | Passed: persistent on/off setting, OS reduced-motion, values retained and parallax removed |
| Continuous journey | Passed: one town-to-core image covers the landing and all later sections; equal camera travel across the landing boundary; correct final scene; still scenes in reduced motion; fresh contact deep link |
| Browser-comment removals | Passed: no discovery panels, depth-facts control or decorative footer sentence; full report remains linked in the TIRIZ case study and proof dialog |
| Experience proportions | Passed: all five logos at 72–80px, organization labels 21–24px, narrative 18–19px; full original photos uncropped and clickable; photo dialogs close with Escape |
| Divia outline | Passed: native transparent mark, no added white outline filter; visually inspected |
| Revised content and logos | Passed: HIMA, BEM, Home Theatre and Ideation responsibilities/results; Cakradata 13,000 / 2,000 top-post views; genuine organization marks and eight app icons |
| Mobile touch controls | Passed: visible actionable targets at least 44 × 44 pixels |
| Documents | Passed: real PDF responses, expected filename/download, unchanged CV bytes and complete original 19-page TIRIZ report bytes |
| Public source excerpt | Passed: original LinkedIn cells 160 impressions / 104 clicks / 65.0% CTR; team attribution; return link |
| Public build privacy | Passed: source register and source files are not served |

The earlier full-suite axe scans using WCAG 2 A/AA, 2.1 AA and 2.2 AA tags reported **zero violations at each of the four viewports**. Screenshot review covered the start, landing transition, projects, charts, proof dialog, all five experience photos and contact. Dark panels and readable body type retain contrast over the decorative art; focus indicators and labels remain visible. This is a tested implementation, not a certification of complete WCAG conformance or a screen-reader usability study.

Firefox and WebKit checks were **unavailable**: Playwright browser downloads timed out at the available mirrors. These engines were not tested. Their configurations are included for a later run when the binaries can be installed.

## PDF and source consistency

The updated 10-page portfolio PDF now includes the user-confirmed Fikomnex media-partnership description. The Fikomnex and HIMA page was regenerated and rendered; all ten pages are included in the refreshed source package.

All **10 A4 landscape pages** were rendered with Poppler and visually inspected. Text is selectable on every page. The revised cover embeds the real supplied portrait, confirmed by comparing decoded pixels with the source. Experience copy, including Fikomnex media partnerships with five Fikom Unpad student organizations, results, organization marks and app icons match the updated content model. All **10 link annotations** match their intended destinations, including the complete TIRIZ report. External Drive links preserve existing access permissions; link correctness does not imply public permission or uninterrupted service availability.

The delivery audit confirms all 19 metric records match the private evidence register; all metric display values appear in the new PDF; the audience shares total 100%; 29 supplied original files retain their registered fingerprints; the supplied CV and full TIRIZ report are unchanged; all 14 public proof sources exist; and the output, public and production portfolio PDF copies are identical. All eight app names and the revised experience counts occur in the PDF. There are no CV-source caveats in its narrative.

Figures preserve their definitions: TikTok 4,427 total versus +417 net followers; Divia's rounded 22K/11K; LinkedIn 104/160 = 65.0% team content; TIRIZ's missed 814.1/1,000 reach target; and percentage of target versus percentage above target. The user's explicit revision statement supplies Cakradata top-post results and organizational team/KPI counts; the private register labels these as user-confirmed, without claiming independent analytics or attendance verification. HIMA participation is 81 / 92 x 100 = 88.04%, approximately 88%. Additional unresolved figures remain excluded.

Fikomnex uses the genuine BEM Fikom organizer mark with an explicit organizer label; no separate Fikomnex logo was located. Other real organization marks come from the user's existing portfolio assets, and app icons from official endpoints. Provenance is recorded in the asset manifest.

## Transparent logo revision

All **15 unique logo assets** have actual alpha transparency, including eight app marks. Organization bitmaps are 1254–3222px wide; wide wordmarks are optimized to 1600px. Four app marks use official native SVG and four use official 1024px PNG. The small HIMA source was restored with the image tool and checked against its original lettering and central symbols; it is not an organization-supplied high-resolution master. Original marks remain preserved. Website logos remain transparent. Experience identity frames are now 80px, reduced to 72px on mobile, beside larger organization labels. App icons are 64px (Canva wordmark 104px wide). The original high-resolution asset files remain unchanged. PDF marks were enlarged and all ten pages rendered and inspected. Copy encoding was corrected and the final website and PDF verified.

`qa/logo-asset-audit.json` records source dimensions, alpha channels and current production asset matches. `qa/comment-*.png` shows the current proportional logos, uncropped photos and continuous world at mobile, comment, laptop and wide-desktop sizes. Earlier logo captures are historical.

## Sharper background revision

The built-in image tool restored the existing scene at native 724 × 2172. A nearest-neighbor 4× pixel-preserving export produces a 2896 × 8688 PNG master and lossless WebP fallback. This export does not claim new native detail. Modern browsers receive full-color AVIF: 1448 × 4344 / 1.46MB below 901px viewport width, and 2896 × 8688 / 2.62MB on wider screens. The 3.52MB lossless WebP remains a fallback. The original scene is preserved.

Chrome supports crisp-edge sampling, which replaces smoothed interpolation for this decorative image. Camera movement is snapped to whole physical pixels, including after resizing; continuous scenery and native scrolling remain. Final direct Playwright CLI review confirmed the correct responsive image dimensions, crisp-edge rendering, zero horizontal overflow and final core position at all four inspected sizes. All underground layers and the landing boundary were visually reviewed. The optimized picture sources have correct image MIME types and media-specific preloads. No documentary evidence or factual content was modified.

## Loading measurement

The following measurement was repeated on the final build after the sharper background, responsive AVIF exports and camera pixel-alignment revisions.

Lighthouse 13.5.0, Headless Chrome 154, Windows, a cold-cache local production server with gzip, simulated mobile **412 × 823**, device scale 1.75, **4× CPU slowdown**, 150ms RTT and 1,638.4Kbps throughput. No concurrent browser test suite ran during the measurement. Fetch time: 2026-10-05 16:51 UTC.

| Measure | Current measured result | Goal |
|---|---:|---:|
| Largest Contentful Paint | **3.63 seconds** | Below 2.5 seconds — not met on this profile |
| Cumulative Layout Shift | **0.0000** | Below 0.1 — met |
| First Contentful Paint | 2.10 seconds | Informational |
| Total Blocking Time | 202ms | Informational |
| Performance score | 81 / 100 | Informational |
| Accessibility score | 100 / 100 | Informational |

Generated illustrations and real display previews were optimized, text responses compressed, headings preloaded with self-hosted fonts, content rendered to static HTML, and Motion features split into a separate chunk. Final labels and reserved media dimensions keep layout stable. The LCP target remains unmet on this simulated slow profile. No field INP or real-user performance measurement is claimed. These are laboratory measurements on this machine, not real-user performance or a guarantee for a future host.

## Artifacts

- `qa/playwright-results.json` and `playwright-report/index.html`: current six-check background regression run. Earlier full-suite results are summarized above.
- `qa/axe-chromium-*.json`: accessibility findings (empty violation arrays).
- `qa/final-*.png` and `qa/chromium-*-start.png`: representative desktop/mobile and all-viewport screenshots.
- `qa/sharp-*.png`: current town-to-core backgrounds and landing transitions at 390px, 766px, 1440px and 1920px widths. Earlier comment/revision/logo captures are historical and excluded from the current source package.
- `qa/portfolio-page-01.png` through `10.png`: inspected PDF page renders.
- `qa/pdf-links.json`, `qa/pdf-text-frames.json`, `qa/delivery-audit.json`: document/source checks.
- `qa/lighthouse-sharp.report.html` / `.json`: current throttled production measurement after the sharper background and camera update.
- `private/evidence-register.json`, `private/unresolved-claims.md`, `private/search-scope.md`: claim traceability, limitations and actual search scope. Keep private.
