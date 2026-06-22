# Caminota — Squarespace → Shopify Migration Inventory

Source: https://www.caminota.ro/ (Romanian, single-language)
Target: Shopify Horizon theme (this repo)
Captured: 2026-06-22

> Workflow: Claude edits theme files locally → client runs `shopify theme dev` to verify/debug → client pushes per-feature and does any Shopify-editor / admin-side work (products, nav, metafields).

---

## 1. Navigation (main menu)

| Label | Old URL | Target type in Shopify |
|---|---|---|
| Acasă | `/` | Home (`templates/index.json`) |
| Case Tradiționale | `/case-traditionale` | Page |
| Case Moderne | `/case-moderne` | Page |
| Caminota Tencuială | `/caminota-tencuiala-cu-paie` | **Product** |
| Caminota Finisaj | `/caminota-finisaj-rustic` | **Product** |
| Caminota IzoBârne | `/caminota-izobarne` | **Product** |
| Vopsea de var | `/vopsea-de-var` (Kerakoll Biocalce Tinteggio) | **Product** |
| Rogojina de Stuf | `/rogojina-de-stuf` | **Product** |
| Var Stins | `/var-calcic-hidratat` | **Product** |
| Cum comand? | `/cum-comand` | Page |
| Articole Utile (Blog) | `/blog` | Blog |
| Întrebări frecvente | `/faq` | Page (accordion) |
| Instrucțiuni și fișe tehnice | `/instructiuni-tencuiala` | Page (downloads) |
| Despre noi | `/despre-noi` | Page |
| Contact | `/contact` | Page |

Note: there is a separate ordering subdomain / calculator at **comenzi.caminota.ro** ("material calculator" → producers call to confirm). Decide whether this stays external or gets rebuilt.

---

## 2. Products (6) — for Shopify catalog

1. **Caminota Tencuială cu Paie** — base plaster. Comp: argilă, nisip, fibre lignocelulozice. ~1.5 cm single layer, manual or mechanized. 15kg bags. Certified DIN 18947. ✅ full body in `raw/caminota-tencuiala-cu-paie.txt`
2. **Caminota Finisaj Rustic** — clay+sand finish coat. Benefits: natural, modern look, vapor-permeable, regulates humidity.
3. **Caminota IzoBârne** — predosed mortar for gaps between wooden logs. 15kg burlap sacks. Full spec table captured (granulation, density 900 kg/mc, λ 0.18–0.20 W/mK, etc.) + mixing/application steps.
4. **Vopsea de var** = *Kerakoll Biocalce Tinteggio* — natural lime paste paint (resold). Comp: var, ulei de pin. ~14 m²/4L in two coats, tintable. ✅ full body in `raw/vopsea-de-var.txt`
5. **Rogojina de Stuf** — reed mat plaster support, galvanized wire @10cm. Sizes 10×1.4 m and 10×1.6 m.
6. **Var Calcic Hidratat CL 90-S (Var Stins)** — hydrated lime, SR EN 459-1:2011. Mortar ratios 1:2–1:3.

Common across product pages:
- Sample-kit CTA via **eMAG** (1–2 day delivery); bulk delivered direct from factory.
- Contact block: Consultanță **0745 055 558** · Comenzi/livrări **0748 204 324** · contact@caminota.ro
- Downloadable technical sheet (PDF) + instructions per product.

---

## 3. Content pages

- **Despre noi** — H1 "Despre noi"; sections "Cum am început", "O tencuială pe cinste", "Ultimii ani". History: R&D w/ URBAN-INCERC 2013–2016; Ecobordei 8 experimental homes 2016–2020; natural materials from 2019; production Timișoara 2021; exports BG/GR/HU/MD; 1000+ B2C customers by summer 2024; iREBBELS 2023, straw boards 2024.
- **Case tradiționale** — sections "Tencuiala Caminota", "Finisajul Caminota".
- **Case moderne** — H1 "Tencuieli din argilă pentru case moderne"; 5 compatible construction systems; benefits list; CTA "Comandă o mostră de Caminota".
- **FAQ** — 8 Q&As captured verbatim-ish (see below). Build as accordion.
- **Cum comand** — ✅ full body in `raw/cum-comand.txt`. 5 steps (1 Ne trimiți proiectul → "Cere ofertă" form; 2 Te contactăm; 3 Calculăm cantitățile + ofertă; 4 Confirmi; 5 Livrare din fabrică pe palet) + test-kit section (eMAG kit = 25kg Tencuială + 5kg Finisaj, ~1 m²).
- **Instrucțiuni și fișe tehnice** — ⚠️ *not yet fetched* — PDF download hub.

FAQ questions: (1) Cum știu dacă sistemul Caminota e pentru casa mea? (2) La ce temperaturi se pot aplica? (3) Procedura de uscare pe șantier (4) Cum trebuie să fie un perete? (5) Cum se aplică produsele? (6) Pot aplica eu (nemeseriaș)? (7) De unde cumpăr? (8) Putem tencui băi și bucătării?

---

## 4. Footer / contact data

Company: **Caminota** (production in Timișoara)
- Consultanță materiale: **0745 055 558**
- Comenzi / livrări: **0748 204 324**
- Email: **contact@caminota.ro**

Warehouses / pickup points:
1. **Bihor** — Route Logistic SRL, Nr. 312, Borș · 0721 284 285
2. **Covasna** — Euroconstruct SRL, str. Bem Jozsef 18A (DN11), Târgu Secuiesc · 0788 323 012
3. **Tulcea** — Moisache-Elania SRL, str. Principală nr. 125, Slava Rusă · 0766 484 971
4. **Rep. Moldova** — Eveco Construction, șos. Hincești km 8, Ialoveni · +373 782 08 008
- Export BG/GR: SEVAREX Ltd., info@sevarex.com · +49 176 44472284

Social (official brand accounts):
- Facebook: https://www.facebook.com/caminota.tencuiala
- Instagram: https://www.instagram.com/caminota.ro/
- YouTube: https://www.youtube.com/channel/UCUZEgaD4mEhxEDQs7XBLyMQ

eMAG store:
- Brand store: https://www.emag.ro/tencuieli-decorative-soclu/brand/caminota/c?ref=bc
- Test kit (25kg Tencuială + 5kg Finisaj): https://www.emag.ro/kit-testare-sistem-caminota-25-kg-tencuiala-si-5-kg-finisaj-cam-01/pd/DVPBTFMBM/

Legal: Termeni și condiții, Politica de confidențialitate, Politica cookies (all captured in `raw/txt/`).
Note: other Facebook URLs in HTML are partners/distributors (Moisache, ReCult, Coliba Verde, etc.), not the brand — ignore for footer.

---

## 5. Homepage section order (to rebuild in index.json)

1. Hero — "caminota" / "Case care inspiră." → **change image to cracked clay (client to send variants next week)**
2. CTA — "Solicită un calcul personalizat" / button "Cere ofertă" / phone 0745055558
3. Product showcase — 3 natural certified products
4. Solutions — Case tradiționale / Case moderne
5. Benefits — "Caminota pentru oameni și case"
6. Footer

---

## 6. Client-requested design adjustments

- [ ] **Typography**: reduce H1–H4 sizes + tighten spacing so more text fits per screen (less whitespace). Proposed H1 56→40, H2 48→32, H3 32→24, H4 24→20; body line-height loose→normal; trim section padding. → `config/settings_data.json`.
- [ ] **Hero image**: replace with cracked-clay texture (client sends variants next week).

---

## 7. Technical sheets & instruction hub (`/instructiuni-tencuiala`)

H1: "Fișe tehnice și instrucțiuni". Downloads/links:
- Fișă tehnică - Tencuială cu Paie → `/s/-Fisa-tehnica-Caminota-Tencuiala-082024-brbb.pdf`
- Fișă tehnică - Caminota Finisaj → `/s/-Fisa-tehnica-Caminota-Finisaj-052023-copy.pdf`
- Procedura de uscare (blog) → `/blog/uscarea-pe-santier-timpii-de-prelucrare-tencuiala-lut`
- Cum desfacem sacii de rafie (YouTube short) → `youtube.com/shorts/eWMzUTR-WVA`
- Ce unelte folosim (blog) → `/blog/ce-unelte-folosim-la-tencuit-cu-sistemul-caminota`
- Fișă tehnică - Kerakoll Biocalce Tinteggio → `/s/-Fisa-tehnica-Kerakoll-Biocalce-Tinteggio.pdf`
- Instrucțiuni video Kerakoll → `youtube.com/watch?v=WfzIrGjaxKI`
- Fișă tehnică - Izolație termică plăci de paie SSH Terra → `/s/SSH-System-teljesitmenynyilatkozatRo.pdf`

> These PDFs/assets must be re-uploaded to Shopify Files and relinked after migration.

---

## 8. Blog (Articole Utile) — 15 posts captured

Full text in `migration-notes/raw/txt/blog__*.txt`. Posts:
beneficiile-sistemului-caminota · ce-unelte-folosim-la-tencuit-cu-sistemul-caminota · cerdacul-cu-amintiri · curarea-pereilor-de-pmnt-zugrvii-cu-var · decizii-renovare-pereti-case-traditionale · finisaje-naturale-pentru-case-noi · ghid-pregatire-tencuire-santier-caramida-bca · planificarea-lucrarilor-renovare-casa-veche · renovare-case-lemn-barne-izolare-umplere-goluri · renovarea-casei-frusina · renovarea-caselor-vechi-de-chirpici · tencuit-mecanizat-argila-caramida-bca · texturi-caminota-rustic-fin · tipuri-de-finisaje · uscarea-pe-santier-timpii-de-prelucrare

Blog taxonomy: category "Tutoriale"; tags incl. #tehnologie, "curatare pereti var", "renovare casa veche".

---

## 9. PDF / document assets (downloaded → `migration-notes/assets/pdf/`)

11 files secured locally (Squarespace `/s/` + static1 paths die after migration → re-upload to Shopify Files):
Fișă tehnică Tencuială · Fișă tehnică Finisaj · Fișă tehnică Kerakoll Biocalce Tinteggio · Agrement Tehnic TNA-FUN (+ full version) · Certificat ISO 9001 (ECO LIVING PROJECT 2025) · ECOLIVING PROJECT URS · Fișă tehnică Var Calcic CL90-S · Listă verificare Pregătire cărămidă/BCA · Poster CATCAR33 · Culori Kerakoll.

**Embedded YouTube videos** (channel UCUZEgaD4mEhxEDQs7XBLyMQ) — ~20 across pages/blog, e.g. embeds 1CQUo4fbiFY, 4et0aNoTQgg, 5N301dOMN64, BjDLfOgRnPk, FJBZua2gxJQ, KMjb3YrHRIY, KSH0Irdbiiw, RI-yJalu3fg, fOLEE3MrFBk, gOOnZ8swAEo, m6P_yEooYLc, tsGZMhlWvyQ; shorts eWMzUTR-WVA, ABbHU1aUJw8, E_NZmncpMUs, aRN6cJeZJkg; watch YBNZwwjxtNw, IwN63zuN1eE, WfzIrGjaxKI, tvIjrrI2Qpc. (grep `youtube` in `raw/*.html` for per-page mapping.)

---

## 10. Capture status — COMPLETE

> There is **no content handover from the client** — the "handover" was the logo folder only. We source 100% of content ourselves. Method: `curl` raw HTML → `migration-notes/extract.py` (WebFetch truncates Squarespace's DOM; raw parse does not).

Artifacts produced:
- `migration-notes/raw/txt/*.txt` — full text of all 32 pages (products, content, legal, blog).
- `migration-notes/image-manifest.md` — 473 unique content images, grouped per page. SEO filenames double as alt text.
- `migration-notes/assets/pdf/*` — 9 downloaded PDFs.
- `migration-notes/raw/` (gitignored) — source HTML + sitemap.

Draft/duplicate pages in sitemap (captured for reference, likely don't carry over): `home` & `home-1` (homepage variants), `case-moderne-1`, `case-moderne-2` (dupes of case-moderne), `blog/blog-post-title-one-c2wl7` (Squarespace placeholder post).

All **483 images downloaded** to `migration-notes/assets/images/` (full res via `?format=2500w`, 247 MB, 0 failures, all validated as real PNG/JPEG). Filenames are `<urlhash>__<original-name>`; `image-manifest.md` maps each back to its page.

**Upload-ready set → `migration-notes/assets/images-shopify/` (477 files, split into `batch-01`..`batch-05`).** Renamed to unique, Shopify-safe, descriptive slugs (page-slug-based for the 49 that had generic names like `0.jpg`). Mapping in **`migration-notes/image-upload-map.csv`**: `shopify_filename, shopify_url, original_filename, used_on_pages, primary_page, suggested_alt, source_url`.

**Uploaded to Shopify Files — store CDN prefix:** `https://cdn.shopify.com/s/files/1/1085/3561/1741/files/`. Our sanitized filenames match Shopify's exactly (verified), so `shopify_url` = prefix + `shopify_filename` for all 477 (version `?v=` param omitted — canonical URL resolves to latest). In theme Liquid prefer `{{ 'filename.jpg' | file_url }}` over hardcoding the CDN path; use the full URL for image-picker/editor selection and reference.

⚠️ **6 images excluded** → `assets/_excluded-template-stock/` — Squarespace *template demo stock* (from a foreign site ID `5ec321c2…`: "Aro Ha" retreat photos, "Trade 151" stock, a placeholder). They only appeared on the draft `home-1` and stub `program-ambasadori` pages, never on real content. Do **not** upload them.

Remaining decisions (not blockers):
- Keep comenzi.caminota.ro calculator external vs rebuild in Shopify.
- Extra pages: `program-ambasadori` (ambassador program), `caramida-cu-goluri-si-bca` (construction-system detail), `post-oferta` (thank-you page) — decide if they carry into the new site.
