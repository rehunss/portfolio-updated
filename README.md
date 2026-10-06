# Raihan modern portfolio

Modern Apple-inspired portfolio for Muhammad Raihan Ramadhan and its matching ten-page landscape A4 PDF. The repository's `main` branch deploys automatically to GitHub Pages.

## Run locally

From this folder, run `npm ci`, then `npm run dev`. Open `http://127.0.0.1:4174/portfolio-updated/`. For the production version, run `npm run build` then `npm run preview`. Stop the other preview first if port 4174 is already occupied. Node 20.19+ or 22.12+ is required by Vite 7.

## Update content and PDF

Edit `src/content.json`: profile, projects, metrics, sources, `diviaPostCases`, experience, capabilities, tools and course completion. Metrics retain label, value, display, unit, period, attribution, source and note. Do not convert rounded K values into exact observations. Review the private register before adding claims. `src/App.tsx` controls the page; `src/DiviaPostResults.tsx` shows the selected post results; `src/Charts.tsx` the interactions; `src/PrintPortfolio.tsx` the PDF pages. `src/styles.css` and `src/print.css` control the corresponding layouts.

After content changes, build and start the production preview, then run `npm run pdf`. This uses a locally installed Chrome browser via Playwright and creates `output/pdf/Raihan_Modern_Portfolio.pdf`, also copying it into `public/documents/`. Run `npm run build` again so the production build includes the latest PDF. Inspect the ten exported pages before delivery. The original CV and campaign report must remain unchanged.

Run `npm test` against the production preview. Reports and captures are in `qa/` and `playwright-report/`. [TEST-REPORT.md](TEST-REPORT.md) describes measured results, visual review, and unavailable checks. Test helpers require the surrounding original evidence folders to verify unchanged document hashes.

## Later GitHub Pages deployment

The default build base is `/portfolio-updated/`, matching this GitHub Pages repository. All site and document assets use this path. The included GitHub Actions workflow automatically builds and publishes `dist/` to Pages on pushes to `main`.

The published address is `https://rehunss.github.io/portfolio-updated/`. `settings.publicSiteUrl` and `settings.publicDocumentBase` point to this address. PDFs use public links; they do not point to localhost.

## Files

- `dist/`: production build.
- `output/pdf/`: new portfolio PDF.
- `public/`: curated assets, official logos, licensed fonts, unchanged CV/report/certificate and new PDF.
- `asset-manifest.json`: transformations, provenance, dimensions and fingerprints.
- `private/evidence-register.json`: original documentation, confirmations, calculations and scope.
- `private/unresolved-claims.md`: excluded and qualified claims.
- `qa/`: reference captures, visual review, accessibility scans, performance and browser test results.
- `DESIGN.md`: design choices, tokens, behavior and reference adaptation.

`scripts/prepare_assets.py` is an initial local-source curation helper; it reads the previous portfolio and all three primary PDFs. Do not rerun it after editing the modern content model: it intentionally resets that model from the original app. `scripts/finalize-content.py` records source dimensions and font provenance. Keep this provenance pipeline separate from ordinary content editing.

## Additional Divia analytics

The August 12, 2026 screenshots add selected post results for the campus-transport carousel, campus-tour topic and Festival Budaya coverage. The account overview from the supplied Drive folder adds rounded TikTok post views of 401.1K and shares of 3.1K for June 1-July 29, with the comparison declines retained. Account totals and later post snapshots remain separate.

Public proof pages contain curated metric transcriptions in accessible HTML. Original new screenshots stay in the ignored local evidence folder. The PDF retains ten pages: page 2 highlights the transport and tour examples; page 3 retains platform totals and follower composition. New outcomes use team/account attribution. The August 5 Pamuka post is held out of the June-July internship case pending role/date confirmation.
