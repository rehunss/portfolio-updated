# Raihan modern portfolio

Reading: a recruiter-facing portfolio with a bright, photography-led Apple-inspired presentation. This is a visual adaptation, not an official Apple component library. Variance 3/10, motion 6/10, density 2/10 follow the brief.

References inspected on October 6, 2026: [Apple homepage](https://www.apple.com/) and [MacBook Pro](https://www.apple.com/macbook-pro/), both at 1440 x 900 and 390 x 844. Captures are in `qa/references/`. The local community Apple DESIGN.md informed spacing, photography and blue action controls. The user brief governs typography and the contiguous dark projects chapter.

The previous site uses pixel illustrations, Silkscreen / Source Sans 3, a continuous underground scene and game metaphors. Its approved content records, proof controls, original document links and URL-backed chart states were retained in a separate implementation. Its source, build, source evidence, PDFs and publication were preserved. No SEO migration or live-site replacement is involved.

## Tokens

Three layers live in `src/styles.css`: primitives, semantic purpose aliases and component tokens. White #ffffff, cool gray #f5f5f7 and dark #0b0b0d form the canvases. Ink is #1d1d1f; secondary light text #626267. Dark secondary text #aaaab3. Blue #0066cc is interactive on light surfaces; #70b7ff provides readable dark-surface actions. Charts use the same blue with gray comparison marks. Status is always spelled out.

Geist 400 and 600 are self-hosted with `font-display: swap`. SIL OFL 1.1 is included with the fonts. Body is 18-21px; mobile body 17-18px. Main display headings reach 78-80px on desktop and 38-43px on mobile. Number comparisons use tabular numerals. Reading width is 1200px. Structural spacing follows an 8px base, with 96-144px desktop chapters and 64-80px mobile chapters.

Panels use 24px radius (22px mobile), nested media 12-16px, actions pill radius. Full-width chapters are square. Shadows are confined to the open mobile navigation. A single sticky navigation layer sits at z-index 10; the skip link at 20; native dialog uses the browser top layer.

## Composition and interaction

Bright profile with immediate project/CV/PDF access; one continuous dark chapter for Divia, TIRIZ and Cakradata; bright experience, skills and contact. Neutral transition strips connect the canvases. Divia pairs a large real carousel with its CTR; TIRIZ pairs an activation photo with a target comparison; Cakradata gives a vertical work sample its own format. Five full, uncropped organization photographs are prominent in experience.

Motion gives chapters a 20px entry and a 550ms opacity transition. Hover media scale is 1.012. Nothing is pinned; browser scrolling and anchors remain native. Reduced motion and the persisted on/off control show complete final states. Mobile drops continuous effects. Entry animations run once on intersection; no offscreen loops run. Evidence never blurs.

Native buttons, links, details, tables and modal dialogs support keyboard and touch. Chart tabs support arrows, Home and End; selected views persist in the URL and restore on Back/Forward. Every chart has stable labels, its own units/period/attribution, tooltip or focus detail, a proof link and an HTML table. Target comparisons use independent scales. Proof combines native modal behavior with explicit Tab/Shift+Tab wrapping, Escape and focus return. Mobile targets are at least 44px tall. Focus is outlined and anchors clear the 64px navigation.

## Content and assets

`src/content.json` drives the site and the ten-page PDF. Original source metrics, rounded displays, team attribution and personal confirmations remain distinct in the private register. No fabricated time series. CV and full TIRIZ report are byte-identical copies. HIMA uses the genuine 281px original at a 68-76px display size; the previous AI-assisted enlarged version is excluded. Other approved transparent marks and official app assets retain proportions and colors. New photographs are WebP variants; full-size proof retains source bytes. Source dimensions reserve layout space.

PDF is bright, landscape A4, with selectable Geist text and public links. It uses React print templates from the shared model and Chromium PDF rendering for consistent typography, SVG charts and native hyperlinks. Poppler-rendered pages are checked after export. `settings.publicSiteUrl` stays at the verified existing public portfolio until a modern publication is authorized and verified.

Following the user's logo review, project wordmarks use transparent backgrounds; PDF project marks render proportionally within a 132 x 60px area without inset padding. Home Theatre's dark lettering sits directly on the light experience canvas. The BEM white mark retains its dark neutral surface. Website navigation uses "Raihan"; PDF headers use the full profile name.
