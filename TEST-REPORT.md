# Portfolio verification - October 6, 2026

The Apple-inspired website and matching ten-page PDF include the additional Divia analytics. The production build uses `/portfolio-updated/` and public PDF links target `https://rehunss.github.io/portfolio-updated/`.

## Final checks

- Production TypeScript and Vite build passed.
- All 15 Playwright checks passed in 2.0 minutes, using installed Chrome, one worker and no retries.
- Layouts at 390 x 844, 768 x 1024, 1440 x 900 and 1920 x 1080 passed: no horizontal overflow, broken loaded images, failed local requests, page errors or console errors.
- Automated WCAG 2 A/AA, 2.1 AA and 2.2 AA scans found zero violations at all four widths, in both original proof-dialog layouts and in the new metric excerpt dialog.
- Navigation, refresh, Back/Forward, mobile menu, 44px touch targets, skip link, keyboard focus, proof-dialog focus/Escape/return and reduced-motion preferences passed.
- All six new HTML evidence excerpts responded successfully. Selected post metrics, platform tabs, chart keyboard interactions, data tables and URL restoration passed.
- Original CV and TIRIZ campaign-report bytes still match their supplied originals.
- Shared print content retains ten pages, matching narratives and at least 8px clearance above every footer.

Raw browser results are retained locally in `qa/playwright-results.json`, accessibility scans in `qa/`, and the readable report in `playwright-report/`.

## Added Divia evidence

The 20 supplied screenshots and all three Drive subfolders were reviewed. The folder contains ten TikTok screenshots, an Instagram report and screenshot, and one LinkedIn XLS export. Its XLS fingerprint matches the existing local source; the LinkedIn CTR remains 65.0% (104 clicks / 160 impressions).

Selected post results use a screenshot snapshot of August 12, 2026 and team/account attribution:

| Example | TikTok | Instagram |
|---|---|---|
| Campus transport carousel | 9,898 views; 180 saves; 104 shares | Not supplied for this case |
| Campus tour | 9,745 views; 18 new followers; 12.5s average watch time | 3,765 views; 2,471 viewers; 6 follows |
| Meet The Ambassadors | 5,005 views; 302 likes; 22 shares | 3,444 views; 121 likes; 13.1s average watch time |

The account overview separately adds rounded TikTok post views of 401.1K and shares of 3.1K for June 1-July 29, 2026. Comparison declines of 20.0% and 23.1% remain visible. Post snapshots are not summed into account reach, and Instagram views and viewers remain distinct.

Six public HTML excerpts contain the relevant metrics, periods and attribution. Original new screenshots and private transcriptions remain in the ignored local evidence folder. The August 5 Pamuka post is held out of the June-July internship case pending role/date confirmation.

## Final PDF review

`output/pdf/Raihan_Modern_Portfolio.pdf` is ten landscape A4 pages, 7,827,258 bytes, with selectable text and 40 clickable links. Output, public download and production-build copies have the same SHA-256:

`9df45f3dc288a74dfec75d3dcb3e9b247c9b839dea2ad0e1cc7c92143964487e`

All ten exported pages were rendered with Poppler at 110dpi and inspected individually. No clipping or overlap was identified. Page 2 highlights the new transport and tour results; page 3 contains platform totals, comparison context and follower ages. PDF hyperlinks contain no localhost destinations or references to excluded new analytics JPEGs. Review renders are `qa/pdf/final-01.png` through `final-10.png`; the integrity result is `qa/pdf/final-audit.json`.

Previously requested transparent logo treatments, enlarged project marks, full-name PDF headers and the website navigation brand "Raihan" are preserved. The asset manifest has 77 curated entries, including six metric excerpts.

## Scope and repeat checks

This revision was verified in Chrome on Windows. Firefox, Safari, physical devices, email delivery and independent accessibility certification were not tested. Lighthouse performance was not remeasured; earlier measurements do not establish this revision's performance.

Build and start the production preview, then run `npm test`. After content/print changes, run `npm run pdf`, inspect all ten pages, then rebuild to include the updated PDF. Raw evidence, review output, local build folders and private files are excluded from the GitHub repository.
