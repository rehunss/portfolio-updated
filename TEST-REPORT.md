# Final verification — October 6, 2026

The separate modern website and ten-page portfolio PDF are complete. The production preview runs at `http://127.0.0.1:4174/portfolio-modern/`. No publishing, live-site replacement, Drive permission change, or original document edit was performed.

## Logo and name review — subsequent revision

Applied all PDF and browser comments: transparent project-logo treatments, slightly larger Divia/TIRIZ/Cakradata PDF marks (132px wide, 60px container height, proportional rendering), transparent Home Theatre treatment, full name in every PDF header, and "Raihan" in website navigation. Original logo files, colors, proportions and evidence content were preserved.

The revised production build passed. Two focused Playwright checks passed in 9.4 seconds: real document responses/unchanged originals and the ten-page shared print layout/public links/footer clearance. Results are `qa/logo-review-tests.txt`. The delivery integrity audit passed again, and all ten revised Poppler-rendered PDF pages were inspected individually. The revised output, public download and production download are byte-identical.

The open in-app browser was refreshed and the Divia, Cakradata and Home Theatre logos visually reviewed in context. Computed backgrounds are fully transparent with zero padding. Current screenshots are `qa/logo-review-divia-browser.png`, `qa/logo-review-cakradata-browser.png`, and `qa/logo-review-home-browser.png`. The earlier four-viewport captures and 15-test report below describe the initial completed build; the focused results above describe this subsequent visual revision. Performance was not remeasured for this revision.

## Production and browser checks

`npm run build` passed TypeScript and Vite production compilation. The final build uses `/portfolio-modern/`; all tested image, font and document paths resolve within that base. Editable source is in `src/`, and the deployable static output is in `dist/`. The private evidence register and raw source records are absent from the build.

The initial full Playwright run used the production preview and locally installed Chrome (Chromium), one worker, with no retries. **15 tests passed; 0 failures, 0 skips, 0 flaky results**, in 59.83 seconds. That run started at 12:30:12 WIB, before the logo/name revision. Raw results: `qa/playwright-results.json`; readable HTML report: `playwright-report/index.html`.

| Check | Actual result |
|---|---|
| 390 × 844, 768 × 1024, 1440 × 900, 1920 × 1080 | All four layouts passed; no horizontal overflow, broken loaded images, failed local requests, page errors or console errors. |
| Navigation | Project anchors, direct refresh, section navigation, browser Back and Forward passed. Chart choices restore from URL state. |
| Mobile menu and keyboard | Open/close, Escape, focus return, section selection and visible controls at least 44px high passed. |
| Skip link | Keyboard entry and the next focused control remained visible below the sticky navigation. |
| Proof dialogs | Desktop/mobile opening, forward focus wrapping, Escape, focus return and actual proof-file responses passed. All five experience-photo views passed. Explicit reverse wrapping is implemented as well. |
| Divia results | Instagram 22K / 11K / 133 / 78; TikTok 4,427 / +417 / +31.5%; LinkedIn 160 / 104 / 65.0% passed. Definitions, periods, team attribution, keyboard tab selection, focus details and tables are present. |
| TIRIZ evaluation | All four selectable metrics passed, including 81.41% of feed-reach target and the explicit 185.9-account shortfall. Creator target/above-target percentages remain distinct. |
| Follower age | All seven exact percentages passed; hover, keyboard focus, tap and the table alternative passed. The text identifies followers. |
| Motion | On/off persistence and a dynamically changed system reduced-motion setting passed. Reduced motion immediately shows opacity 1 final states. |
| Documents | Real PDF responses and file signatures passed. CV/report bytes matched the originals; desktop and mobile links point to real base-relative files and open in a new tab. |
| Experience layout | Fikomnex 2 and 5 share a numerical baseline within 1px. Every experience image exceeds 350px on larger layouts and fills the available mobile width. |
| Shared print content | Ten pages, matching project/experience text, public hyperlinks and at least 8px clearance above every footer passed. |

## Accessibility and visual review

axe-core scans using WCAG 2 A/AA, 2.1 AA and 2.2 AA tags found **zero automated violations at each of the four viewports**, and zero in both tested proof-dialog layouts. Raw page scans are `qa/axe-390.json`, `qa/axe-768.json`, `qa/axe-1440.json`, and `qa/axe-1920.json`. This is automated evidence plus focused keyboard/visual review, not an independent accessibility certification.

The actual desktop and mobile pages were visually reviewed, including chapter transitions, project compositions, chart labels, genuine logos, full-subject experience photographs, aligned numbers, app tools, certificate and contact controls. Source screenshots remain readable through full-size proof views. BEM uses a neutral dark surface for its genuine white mark. HIMA uses the original 281px logo at a much smaller display size rather than an AI enlargement.

Captures are `qa/final-{width}-{section}.png`, `qa/dialog-{width}.png`, and the segmented overviews in `qa/visual-review/`. Native captures of pages taller than 16,384px showed a browser graphics artifact near the bottom. The final 390px and 768px full-page files were therefore assembled from overlapping, unaltered viewport screenshots; the capture positions and original images are retained in `qa/visual-review/tall-capture.json` and its viewport folders. DOM checks confirmed one profile heading and one contact section. The actual footer/contact views were inspected after assembly.

## Measured performance

The completed production preview was measured after the browser tests and temporary reference browsers had finished. Lighthouse 13.5.0 used Headless Chrome 154 on Windows, a fresh storage state, a 412 × 823 mobile screen at device scale 1.75, and simulated throttling: 150ms RTT, 1,638.4 Kbps nominal throughput, 1,474.56 Kbps download / 675 Kbps upload, and 4× CPU slowdown. The preview was served locally by Vite; this measures the static build under simulation, not a deployed site's geographic latency or real-user field data.

| Metric | Measured | Requested target |
|---|---:|---:|
| Largest Contentful Paint | **2.012 seconds** | Below 2.5 seconds — passed |
| Cumulative Layout Shift | **0.000** | Below 0.1 — passed |
| First Contentful Paint | 1.562 seconds | — |
| Total Blocking Time | 129.5ms | — |
| Performance score | 98 / 100 | — |

No Lighthouse run warnings. Raw measurement: `qa/lighthouse-mobile.json`, taken at 12:35:40 WIB, before the subsequent logo/name revision. The current build's JS is 376,261 bytes (115.58KB gzip at build); CSS is 44,983 bytes (9.94KB gzip). The portrait is prioritized; other media use responsive WebP variants and reserved dimensions. PDF downloads are opened on demand.

## PDF and evidence integrity

`output/pdf/Raihan_Modern_Portfolio.pdf` is **10 landscape A4 pages**, 8,245,172 bytes after the logo/name revision, with selectable text and **37 clickable link annotations**. The same bytes are served from `public/documents/` and `dist/documents/`. No localhost address occurs in its clickable destinations. The preceding PDF is retained in `output/pdf/history/`.

All ten actual exported PDF pages were rendered with Poppler at 120dpi and inspected individually. Text, source notes, chart labels, logos, images and footer clearance were checked. The final pages have no identified clipping or overlap. Browser captures provide a secondary comparison; review renders are `qa/pdf/page-01.png` through `page-10.png`.

| Pages | Reviewed content |
|---|---|
| 1 | Real portrait, profile, positioning and selected-work overview. |
| 2–3 | Divia case study, team carousel, platform results and follower age composition. |
| 4–5 | TIRIZ activation, delivery, independent target scales, creator results and missed feed-reach target. |
| 6 | Cakradata contribution and selected 13,000 / 2,000 top-post figures. |
| 7 | Fikomnex and HIMA, with genuine marks, photographs and aligned numeric highlights. |
| 8 | BEM, Home Theatre and Ideation context, contribution and outcome. |
| 9 | Capabilities, eight application logos and verified course completion. |
| 10 | Contact, existing public website and selected evidence links. |

The integrity audit passed: shared project narratives (50 / 49 / 51 words), experience context/contribution/results, approved figures, excluded unsupported claims, transparent logo dimensions, 71 curated asset-manifest entries and private-file exclusion. See `qa/delivery-audit.json` and `asset-manifest.json`.

Unchanged original document SHA-256 values:

- CV: `40c98d26bb310d6ef57ed5669e2fa7c7fffffa900602957d017a684f7157818f`
- Full TIRIZ report: `63cbcaa9cf99cd0acc600f56471456061f01c32727ddf610021ac3cbbba923a5`

Original documentation, user confirmations, derived calculations and unresolved claims remain distinct in `private/evidence-register.json`. Cakradata's selected top-post counts and approved personal experience outcomes retain their user-confirmed class. Internship dates remain role context. Old conflicting claims in the supplied CV remain privately recorded because the original CV is served unchanged at the user's request.

## Public links and unavailable checks

The fourteen unique existing-portfolio website/document/proof destinations used in the PDF responded HTTP 200 with suitable MIME types. The supplied LinkedIn profile rejected HEAD with 405 and GET with LinkedIn's 999 restriction response. Its browser/login availability could not be established through automated requests; its user-supplied address was retained. See `qa/public-links.json`.

Firefox and WebKit checks were **unavailable**: their Playwright browser executables are not installed. `qa/browser-availability.json` records both launch failures. No Firefox, Safari, physical iPhone/Android, email delivery, or new public hosting verification is claimed. The modern site has not been published. `settings.publicSiteUrl` remains the verified existing portfolio address until a modern publication exists; update and verify the public settings before regenerating a future published PDF.

## Repeat checks

Build, start `npm run preview`, then run `npm test`. Run `npm run pdf` after shared-content or print-layout changes, inspect every exported page, then rebuild to include the new PDF. `scripts/audit-delivery.py` needs the bundled Python libraries and the surrounding original source folders. `scripts/audit-public-links.mjs` intentionally reports a nonzero exit if any destination cannot be verified, including a third-party restriction.

For unusually tall mobile screenshots, run `node scripts/capture-tall-pages.mjs`, followed by `scripts/stitch-tall-captures.py` and `scripts/review-site-captures.py` with the bundled Python runtime. These helpers only create review artifacts; they do not alter site assets.
