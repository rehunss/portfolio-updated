# Raihan's adventure portfolio

An English, recruiter-facing portfolio with original 16-bit scenery, native scrolling, a game-style chapter menu, three interactive data views, and curated proof. Scroll from the creative town through continuous underground scenery to the core. Ready for public deployment through the included GitHub Pages workflow.

## Run

Use Node.js 22.12+ or a supported newer version. Open a terminal in this `website` folder:

```powershell
npm install
npm run dev
```

Open the local address printed in the terminal. Development normally uses `http://127.0.0.1:5173/`.

```powershell
npm run build
node scripts/serve-production.mjs
```

The production preview is `http://127.0.0.1:4173/portfolio-preview/`. The preview server has gzip compression for text assets, matching normal static-host delivery. This deliberately exercises a subdirectory. Stop a server with Ctrl+C.

The build also creates static HTML for the profile, projects, final chart values and document links. React adds the interactive controls after hydration. Motion features load in a separate chunk.

## Update content

- Edit `src/content.json`. Projects, metric labels, values, units, reporting periods, attribution and source IDs are shared with the PDF. Do not combine periods or change a metric definition just to simplify a headline.
- Experience records contain the organization context, contribution, outcome, genuine logo and concise highlights. `toolGroups` holds Google Workspace, Microsoft Office and Canva, including their real app icons. User-confirmed revision figures are distinguished from original-source analytics in the private register; public experience copy contains no CV-source caveats.
- Logos use transparent, high-resolution variants. Microsoft Office and Canva use native SVG; Google apps use 1024px PNG. Organization marks are 1254–3222px wide, except wide wordmarks optimized to 1600px. The HIMA master is an AI-assisted restoration of the available 281px genuine mark; its original remains preserved. See `asset-manifest.json` for provenance. For a changed SVG app mark, also replace its transparent 512px `-pdf.png` print render.
- Keep source originals in the surrounding evidence folders. Add only curated, suitable public proof to `public/proof`. Preserve full-size originals; `public/assets` contains optimized display previews.
- Record new claims and any conflicts in `private/evidence-register.json` and `private/unresolved-claims.md`. `private/` is excluded from version control and the public build.
- Rebuild both the website and PDF when content changes. Check values against the source, including source page numbers. The supplied CV stays unchanged until its owner supplies a replacement.

## Rebuild the portfolio PDF

Python 3.12+ is suitable. Install the small document dependencies, then run the builder:

```powershell
py -m pip install -r scripts/requirements.txt
py scripts/build_pdf.py
```

The builder reads the same JSON content and embeds licensed fonts from the installed font packages. It writes `output/pdf/Raihan_Adventure_Portfolio.pdf` and synchronizes `public/documents/Raihan_Adventure_Portfolio.pdf`. It produces 10 A4 landscape pages with selectable text, native chart labels and clickable links. Source screenshots remain documentary material. Rebuild the website after rebuilding the PDF so `dist/` receives the latest document.

Render with Poppler after meaningful edits and inspect all pages. `qa/pdf-links.json` inventories link destinations. `scripts/build_register.py` regenerates the private claim register and hashes the original folder files.

The local audit helpers require the surrounding original evidence folders and private source snapshots. They are separate from the website and PDF build. `scripts/export_linkedin_excerpt.py` produces a clearly labeled transcription of three selected original XLS rows, with a source fingerprint. The existing public excerpt is already included; no private workbook is required to run the site.

## Test

```powershell
npx playwright test --project=chromium
```

The Chromium configuration uses installed Google Chrome. The complete suite tests four screen sizes, plus the browser-comment viewport (766 × 652), native history, project refresh links, keyboard/dialog focus, chart definitions, data tables, tap/focus details, motion preferences, original CV/report bytes, PDF downloads, experience/app content, continuous camera movement across the landing boundary, proportional logos and readable full-size photos, missing assets, overflow and axe accessibility checks. It expects the production preview above.

Optional engines, when downloads are available:

```powershell
npx playwright install firefox webkit
npx playwright test --project=firefox --project=webkit
```

See `TEST-REPORT.md` for actual results and limits. An automated accessibility pass is supported by visual and keyboard checks; it is not a certification of full WCAG conformance.

## Handoff files

`output/packages/` contains an editable source archive, a ready-to-upload production archive, and a separate private evidence-audit archive. The production archive contains only `dist/`. The source archive excludes private source snapshots, dependencies and transient test files. Representative screenshots and the measured results are included in the source archive. Keep the private audit archive out of public hosting.

## Deploy

Push this repository to GitHub with its default branch named `main`. The included `.github/workflows/deploy.yml` builds the static website and deploys `dist/` to GitHub Pages after each push. In the repository, choose **Settings → Pages → Build and deployment → GitHub Actions** if Pages asks for a publishing source. The live address will be `https://<account>.github.io/<repository>/`.

The default Vite base is relative (`./`), so the build supports a GitHub Pages project path. The workflow publishes only the generated `dist/` folder; local evidence registers, QA screenshots and source archives are excluded. Do not upload the evidence archive, private register, node_modules or source trackers. Existing Drive permissions are unchanged. Public proof and requested document downloads are served from the site itself.

For a custom deployment path, set `VITE_BASE_PATH` before building, for example:

```powershell
$env:VITE_BASE_PATH='/Portofolio/'
npm run build
```
## Structure and licenses

- `src/`: editable React, TypeScript, content and design tokens.
- `public/`: public assets, genuine organization/app logos, curated proof, original CV, complete TIRIZ report, certificate and new portfolio PDF.
- `artwork/`: reusable original generated PNGs; no documentary evidence is generated.
- `asset-manifest.json`: generated decoration versus real evidence and display previews.
- `private/`: audit register, source snapshots, conflicts and actual search scope.
- `qa/`: browser screenshots, axe results, PDF renders, performance and test reports.
- `output/`: final PDF and packaged source/build.

Silkscreen and Source Sans 3 are self-hosted under the SIL Open Font License; copies are in `public/licenses/`. Design references informed menu affordances; all illustrations and interface composition are original. Installed design-taste-frontend, web-interface-guidelines, design-md-reference and playwright-cli skills were used with the explicit 16-bit brief taking precedence over generic aesthetics.

## Underground scenery

`src/EarthWorld.tsx` controls one fixed, continuous town-to-core panorama behind the entire page, including the landing section. `public/assets/continuous-world-sharp-4x.webp` connects the sky and town directly to the soil below. One camera transform travels through topsoil, sedimentary rock, crust, upper/lower mantle and outer/inner core without switching background images. Distances are deliberately compressed for a game. Worms occur near the surface, fossils in sedimentary rock, quartz/gold and a fictional miner's chest in the crust, and diamonds/peridotite in the upper mantle. No gems or fossils appear in the core.

Standalone discovery panels, the depth-facts control and the decorative footer sentence were removed in the browser-comment revision. The full TIRIZ report remains linked inside its case study and proof dialog. Motion off uses still scenes that change at layer boundaries and retains every content/control. Experience logos are compact beside larger organization labels; full original photos are uncropped and clickable. The 10-page PDF uses the real supplied portrait and print-friendly backgrounds and is unchanged by this layout-only revision.

Reusable original PNGs and prompts are in `artwork/`. Optimized WebP files are in `public/assets/`. The asset manifest records generated decoration, genuine evidence, brand-mark origins and official app-icon endpoints. Fikomnex uses its organizer's BEM Fikom mark with an explicit organizer label.
