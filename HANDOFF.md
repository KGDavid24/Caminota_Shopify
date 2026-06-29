# Caminota — Shopify Migration Handoff

Everything a fresh session needs to continue this project. Read this top to bottom before touching anything.

---

## 1. Project at a glance

- **What:** Migrating **caminota.ro** (Romanian site selling natural clay/lime building materials — tencuieli de argilă) from **Squarespace** to a **Shopify Horizon** theme.
- **Where:** `C:\Projects\Caminota` (this is the theme root; it IS a Shopify theme directory).
- **Client relationship:** Agency job for a client. **Keep chat in English; site content stays Romanian** (with diacritics: ă â î ș ț).
- **Git:** branch `main`. Commit/push only when the user asks.

### Workflow (important)
- **Claude edits theme files locally → the user (client side) runs `shopify theme dev` to preview/debug → the client pushes per-feature and does all Shopify-admin work** (creating pages, assigning templates, uploading to Files, products, nav, metafields).
- The user reviews by sending **screenshots** and we iterate section-by-section. This screenshot loop is the primary way we match the original 1:1 — the raw scraped HTML has no computed styles, so screenshots are how we verify.
- **When comparing screenshots:** the user usually says which is the original ("first is original", etc.). You can also tell live-vs-ours by the **URL bar** (caminota.ro = original; 127.0.0.1:9292 = our dev preview). Do NOT assume by position.

### Content source
- **No content handover from the client** except a logo folder (6 colorways). We source 100% of content ourselves from the live site.
- Scrape artifacts live in `migration-notes/` (raw HTML is gitignored):
  - `migration-notes/raw/*.html` — raw page HTML (curl'd).
  - `migration-notes/raw/txt/*.txt` and `migration-notes/raw/*.txt` — extracted page text (note: some txt files are in `raw/` not `raw/txt/`, e.g. `cum-comand.txt`).
  - `migration-notes/image-manifest.md`, `site-inventory.md`, `design-spec.md`, `assets/pdf/` (tech sheets/certs).
  - `extract.py` (stdlib HTMLParser) is the text extractor.
- **WebFetch truncates Squarespace's huge DOM** — use `curl` raw HTML for scraping.
- **Lazy-loaded images are NOT in the static HTML.** Squarespace galleries/banners inject some images via JS after load (e.g. the caramida gallery beyond ~9 shots, the despre-noi "Ultimii ani" photo). When an image can't be found in the HTML, ask the user to right-click → "Copy image address" on the live page. (Filenames can be misleading — the despre-noi fish-art photo is literally named `renovarea-unei-case-traditionale-din-chirpici.jpg`.)

---

## 2. Design tokens (global settings)

Defined in `config/settings_data.json` and `config/settings_schema.json`. Reference them in Liquid as `settings.brand_*`.

| Token | Hex | Use |
|---|---|---|
| `brand_olive` | `#606452` | body text, headings, footer bg, secondary buttons |
| `brand_cream` | `#f4f2e4` | alternating cream section background |
| `brand_gold` | `#b1a45a` | primary buttons, links, accents |
| `brand_green` | `#627434` | green accent / highlights |
| white | `#ffffff` | page bg, text on colored sections |

- **Fonts:** Headings **Bevan** (`var(--font-heading--family)`, chunky slab serif, **single weight 400 only** — no native bold; faux-bold via `font-weight:700` looks rough, avoid it). Body **Open Sans** (`var(--font-body--family)`), available weights **400 / 600 / 700** only.
- **Buttons:** square (radius 0). Primary = gold bg + white text; secondary "Află mai multe" = olive bg + white text. Horizon's `.button` is `display:block` full-width — to size it use `width: fit-content; margin-inline: auto` on the element.
- `color_palette.background` resolves to `#ffffff`.

---

## 3. Hard-won gotchas (read these or repeat past mistakes)

1. **Scoped `<style>` blocks are unreliable on the dev server.** `#shopify-section-{{ section.id }} .x { ... }` style blocks sometimes don't hot-apply (esp. dynamic values). For values that MUST apply (e.g. overlay color/opacity), **use inline `style=""` on the element**, or `assets/caminota.css`. Static structural CSS in the block is usually fine. (The page-intro overlay is inline for this reason.)
2. **The Shopify admin THEME EDITOR clobbers JSON.** When the client edits in the visual editor and pulls, it overwrites `templates/*.json`, `sections/*-group.json`, `config/*` with the editor's stored values, expanding all settings. **Keep durable work in Liquid (schema defaults), not in JSON.** Per-instance content unavoidably lives in JSON templates — accept that, it's recoverable.
3. **Uploaded Shopify filenames differ from scraped names.** Scraped images use underscores (`case_traditionale.jpg`); the client uploaded with hyphens (`case-traditionale.jpg`). A wrong `shopify://shop_images/<name>` ref **silently falls back** (blank image / fallback color, no error). Verify the actual filename in the editor's image-picker field before wiring.
4. **Shopify CLI temp-file bug:** `theme dev` hot-reload sometimes errors with "illegal characters" — workaround is restarting `shopify theme dev`. If the user "sees no change", suspect this.
5. **Never run a second `shopify theme dev`** (e.g. preview_start on port 9293) while the user's server (9292) is running — it causes "Failed to Upload Theme Files". Don't start preview servers; the user owns 9292.
6. **Range setting `default` (and any value) must be divisible by `step`** or the upload fails ("must be a step in the range"). Same for exceeding the range max (e.g. `content_width` can't exceed its `max`).
7. **`richtext` settings can't hold heading tags** (`<h2>` etc. get stripped) — only `<p>`, `<br>`, `<strong>`, `<em>`, `<a>`, `<ul>/<ol>/<li>`. For per-step headings, use one section instance per heading, or put `<strong>` for emphasis. **`text` settings DO output raw HTML** (Liquid `{{ }}` never escapes), so you can embed `<strong>`/`<a>` directly in a `text` setting value (editor shows the tags, but it renders).
8. **You (Claude) cannot create Shopify pages or upload to Files** — no Admin API access here, and the `shopify` CLI is theme-only. The user must, in admin: create the page, set its **handle** (watch Romanian diacritics — auto-generated handles differ), and assign the **Theme template**. Always remind them.
9. **Image-as-theme-asset trick:** Since you can't upload to Files, for images you need rendering NOW you can `curl` them into `assets/` and reference via `asset_url`. Sections that need this have an `image_asset` (filename) text setting that falls back when the Files `image` picker is blank. Squarespace serves **WebP regardless of extension** — download then rename to `.webp`. These assets push with the theme; the client can later move them to Files and set the picker (which takes precedence).

---

## 4. Architecture / conventions

- **Modular sections + snippets + blocks. No monolithic templates.** Each page is a `templates/page.<handle>.json` that orders reusable section instances.
- Section file pattern: `{%- liquid assign s = section.settings -%}`, then a `<style>` block scoped with `#shopify-section-{{ section.id }}`, then markup, then `{% schema %}`.
- Reusable sections take all editable text as schema `default`s (clobber-resistant). Background colors / per-instance content set in the page JSON.
- `assets/caminota.css` is the global override file (loaded last, after Horizon CSS). Header fixes, dropdown styling, benefits/partners image sizing live there.

---

## 5. Custom sections built (the toolkit)

All in `sections/`. Reuse these across pages.

- **`rich-text.liquid`** — the workhorse for prose pages. Settings: `heading` + `heading_tag` (h1–h4, headings never justify), `body` (richtext), `alignment` (left/center/justify), `max_width` (500–1400), `heading_color`, `background_color`, padding. Optional **button** (`button_label`/`button_link`, gold, centered). Optional **YouTube** (`youtube_id`, `video_width`, centered between heading and body). Optional **float image** (`float_image` Files OR `float_image_asset` filename fallback; `float_position` left/right; `float_top` checkbox = image starts at top so heading wraps beside it; `float_width` 160–760, capped at 65% of column; `float_caption`; `float_gap` px between image and text).
- **`page-intro.liquid`** — framed hero. Title + richtext body over a background image (`background_image` Files OR `background_asset` filename), with overlay (`overlay_color`/`overlay_opacity`, **inline-styled** so the slider works), `text_color`, `body_weight` (400/600/700), `body_size` px, `content_width`, `content_inset` (left margin to push text in), frame margin/corner-radius/min-height. Used as the hero on Tradiționale / Moderne / Cărămidă.
- **`page-video.liquid`** — YouTube embed + caption + sub-caption (richtext, gold links), olive bg by default. (Tradiționale testimonial video.)
- **`product-feature.liquid`** — heading + main image (`image`, `image_max_width`, left/right) + body + `composition` + `benefits` lines + up to 2 download links (gold) + a **gallery** (image blocks, columns/gap/ratio/side-margin). Color settings `heading_color`/`text_color`/`link_color` (for dark text on the gold Finisaj variant). Used 3× on Tradiționale.
- **`page-sample-cta.liquid`** — "Probează Caminota": image left + heading/body/button/footnote right. Olive button override, gold footnote. Now also has an **`image_asset`** fallback (so the eMAG `mostra-caminota-emag.webp` renders without a Files upload) and a **`body_alignment`** setting (left/justify; default left).
- **`testimonial-quote.liquid`** — italic quote + author (author is regular-weight muted gold, not Bevan). Olive bg default.
- **`feature-rows.liquid`** — repeatable image/text rows (Moderne "Sisteme constructive"). Blocks: `image`/`image_asset`, `image_position`, `number` (inline with title), `title` (links via `link_url`), `subtitle` (underlined olive — color set inline due to style-block flakiness), `body` (justified semibold olive), `link_label`/`link_url` (gold button). Dividers between rows. Heading left-aligned.
- **`benefits-list.liquid`** — checklist (Moderne/Cărămidă benefits). `heading`/`lead`/`closing`, blocks of `text` (embed `<strong>` for bold phrases). `marker` = check/bullet/none, `marker`/`check_color`, `heading_color`/`text_color`. **Zigzag top divider** (`top_divider` + `divider_above_color`) — a Liquid-generated SVG sawtooth that bridges a cream section above into the olive section.
- **`link-list.liquid`** — heading + intro + link blocks (`label`, `url` → gold link if set else plain dark, `bold` checkbox). Used for Cărămidă "Resurse utile" / "Instrucțiuni".
- **`link-cards.liquid`** — centered heading + responsive grid (`columns` 1–4, default 3) of image+caption-link **cards**. Each card block: `image` (Files) OR `image_asset` fallback, `label` (gold underlined caption link), `link`, `new_tab` checkbox. Image sits in a fixed-height box (`image_height`), object-fit contain (no crop, matches Squarespace). Both image and caption are anchors to the same target. `heading_tag` (h1–h3), `image_height`, `column_gap`/`row_gap`, `max_width`, bg/heading/link colors. Used for the **Fișe tehnice și instrucțiuni** page (8 cards). Stacks to 1 col on mobile.
- **`photo-gallery.liquid`** — **carousel**: large main image (`main_width`, `ratio`, object-fit contain) with `‹ ›` arrows + a scrolling thumbnail strip. Photo blocks (`image`/`image_asset`). JS: clicking a thumb/arrow moves the main image AND scrolls the thumb strip to keep the active thumb centered; active thumb gets a gold border. (Now used **only on Cărămidă**, 37 slides. Product pages use `photo-bento` instead.)

### Product-page & blog sections (added this session — all in `sections/`)
- **`product-detail.liquid`** — product-page top block. `heading`+`heading_tag`, optional `subtitle` (rendered in **Bevan**), product image (`image` Files OR `image_asset` fallback, `image_max_width`, left/right), `body` richtext + `body_alignment` (left/justify), `composition`/`benefits`/`extra_line` (raw-HTML text lines), up to 2 PDF download links, optional blog link, color settings, `content_width`.
- **`photo-bento.liquid`** — product galleries. Two layouts via `layout`: **bento** (mixed sizes — 4-col grid where every 5th/6th tile spans 2 cols) or **uniform** (equal tiles via centered flexbox so an incomplete last row centers; `columns` 2–8, `uniform_ratio`). `gap`, `side_padding` (0 = full-bleed), `max_width` (0 = full-bleed), square corners. **Click any tile → fullscreen lightbox** (‹ › arrows, counter, Esc/backdrop close, keyboard nav). Photo blocks (`image`/`image_asset`).
- **`reviews-google.liquid`** — embeds the SociableKit Google-reviews widget (`embed_id` default **`25510686`**). Renders white review cards on a configurable bg. Third-party `defer` script — verify on the real dev URL, not inside the admin editor's safe-mode preview.
- **`text-columns.liquid`** — N-column grid (one column per `column` block: `heading`+`heading_tag`+`body` richtext), top-aligned, stacks on mobile. (IzoBârne "Amestecarea cu apă" | "Instrucțiuni de aplicare" side-by-side.)
- **`spec-table.liquid`** — centered bordered 2-col table (`row` blocks: `label`/`value`), centered Bevan heading, optional centered gold footer link, `table_max_width`, `border_color`. (IzoBârne "Caracteristici tehnice".)
- **`article.liquid`** — prose section with a single **`html`** body setting (so it can hold `h2`/`h3` Bevan headings, lists, links, and native `<details>/<summary>` **clickable accordions** — caret rotates on open, divider rules). `body_alignment`, colors, `max_width`. (Var Calcic info/renovare articles.) **NOTE:** `html` settings do NOT run Liquid, so no `asset_url` inside — keep images in separate `photo-bento` rows.
- **`blog-listing.liquid`** — the blog index (`templates/blog.json` → this). 2-col card grid of `blog.articles` (featured image link, DD/MM/YYYY date, Bevan title, excerpt = `article.excerpt` else first ~40 words, gold "Read More"), paginated. Settings: `columns`, `posts_per_page`, `image_ratio`, `date_format`, `read_more_label`, gaps, colors.
- **`blog-post.liquid`** — the blog post page (`templates/article.json` → this). Centered meta line (date `%-d %b` + "Written By {{ article.author }}") **above** Bevan h1 title, then `{{ article.content }}`. No featured image at top (original doesn't show one). Styles content h2/h3 (Bevan), gold links, lists.
- **`contact-page.liquid`** + snippet **`snippets/contact-loc-card.liquid`** — the Contact page. A single **2-column CSS grid** (`align-items:start` so each grid row's two cards top-align), rendered in row-major order so columns stay aligned regardless of card height. Left col: title, gold contact card (phones/email), Moldova card, Bulgaria note, "Formular de contact" + a real `{% form 'contact' %}` (underline inputs, GDPR checkbox, gold submit). Right col: "Stoc materiale" + Bihor/Covasna/Tulcea cards. Location blocks have `column` (left/right), `region`, `company`/`company_url`, `address` (embed `<strong>` for the bold city), `phone`.
- **`home-*.liquid`** (hero, calc-cta, product-system, solutions, benefits, certifications, mission, partners) — the homepage sections (built earlier in the project).
  - **`home-calc-cta.liquid`** is reused as the "Solicită un calcul" / "Calculează necesarul" CTA on several pages. Settings include `button_position` (top = below heading / bottom = below text), `content_width`, `body_weight`, phone (omit by leaving phone fields blank), gold underlined phone link.
- **`caminota-footer.liquid`** — custom footer (replaces Horizon's block footer) in `sections/footer-group.json`. 4-col: contact+logo+social / nav / legal / decorative clay-smear image. Olive bg.

### Header notes (`sections/header.liquid`, `assets/caminota.css`)
- Dropdown menus restyled to a **compact white dropdown** (not Horizon's full-width mega-drawer): white bg, olive links, right-aligned, pulled up under the menu item via `margin-top: -32px`, opens leftward (`right:0`). All in `caminota.css`.
- Header forced to a **solid white background** (`.header__row--top { background:#fff !important }`) — it was rendering transparent over image heroes.
- Header height reduced via `.header-logo { min-height: 90px !important }` (the logo block had `min-height:145px` of dead space). **Do NOT change logo/wordmark/menu sizes — they're dialed in.**
- Cart/account icons hidden (no e-commerce chrome; ordering is via external calculator at comenzi.caminota.ro).

---

## 6. Pages — status

| Page | Template | Handle | Status |
|---|---|---|---|
| Home | `index.json` | — | Done |
| Case tradiționale | `page.case-traditionale.json` | `case-traditionale` | **Done** |
| Case moderne | `page.case-moderne.json` | `case-moderne` | **Done** |
| Cărămidă cu goluri și BCA | `page.caramida-cu-goluri-si-bca.json` | `caramida-cu-goluri-si-bca` | **Done except link URLs** |
| Cum Comand? | `page.cum-comand.json` | `cum-comand` | **Done** (links/eMag URLs are placeholders) |
| Contact | `page.contact.json` | `contact` | **Done** |
| Despre noi | `page.despre-noi.json` | `despre-noi` | **Done** |
| Soluții | `page.solu-ii.json` | `solu-ii` | **Stub (default main-page) — NOT built** |
| Tencuială cu Paie | `page.caminota-tencuiala-cu-paie.json` | `caminota-tencuiala-cu-paie` | **Done & reviewed** (PDF link TBD) |
| Finisaj Rustic | `page.caminota-finisaj-rustic.json` | `caminota-finisaj-rustic` | **Done & reviewed** (PDF link TBD) |
| IzoBârne | `page.caminota-izobarne.json` | `caminota-izobarne` | **Done & reviewed** (blog link TBD) |
| Vopseaua BioCalce | `page.vopsea-de-var.json` | `vopsea-de-var` | **Done & reviewed** (2 PDF links TBD) |
| Rogojina de stuf | `page.rogojina-de-stuf.json` | `rogojina-de-stuf` | **Done & reviewed** |
| Var Calcic Hidratat | `page.var-calcic-hidratat.json` | `var-calcic-hidratat` | **Done & reviewed** (PDF link TBD) |
| Fișe tehnice și instrucțiuni | `page.instructiuni-tencuiala.json` | `instructiuni-tencuiala` | **Built** — needs admin page + review (PDF/blog links provisional) |
| Blog index | `blog.json` | (Shopify blog) | **Built** — needs blog created in admin |
| Blog post | `article.json` | (Shopify articles) | **Built** — migrating posts (1 of 15 done) |

> **All 6 product pages were reviewed section-by-section against the originals and signed off.** Each has its OWN background theme — do NOT assume one palette:
> | Page | Detail + gallery bg | Gallery layout | Reviews |
> |---|---|---|---|
> | Tencuiala | cream `#f4f2e4` | bento (6) | gold |
> | Finisaj | **gold `#b1a45a`, white text** | bento (6) | cream |
> | IzoBârne | cream | uniform 4-col (8) | gold |
> | Vopsea | white, hero `image_max_width:520` | uniform 1×5 row, white bg | cream |
> | Rogojina | **gold, white text** | uniform 1×6 row, gold bg | none (no widget) |
> | Var Calcic | cream | uniform 4-col, interleaved | none (no widget) |
>
> **Reviews widget** (`reviews-google`, after Probează) is on **tencuiala / finisaj / izobarne / vopsea only** (not rogojina/var-calcic). Reviews bg is per-page (see table). Product-page Probença bodies are **justified**; bg white (except izobarne/varcalcic flows).
>
> **Product-page recipe:** `product-detail` → `photo-bento` → `page-sample-cta` → (`reviews-google`). **IzoBârne** inserts between detail & gallery: `text-columns` (2-col mixing|instructions) → `rich-text` (video `5N301dOMN64`) → `spec-table` (tech specs). **Var Calcic** is the most complex: detail → `article` (Informații utile, white, with `<details>` accordion) → `article` (Renovarea fațadelor, cream) → `article` (Ghid intro) → `photo-bento` 4 imgs → `article` (closing text) → `photo-bento` 7 imgs → `article` (2 paras) → `photo-bento` 3 imgs → Probează (no zigzag divider — user explicitly wanted it off).

### Page structure cheat-sheet
- **Case tradiționale:** page-intro hero (olive overlay 45, white text) → page-video (Arad interview, olive) → product-feature ×3 (Tencuiala white/img-left, Finisaj **gold bg + white text**/img-right, Vopsea white/img-left, 2 downloads) → page-sample-cta (Probează) → home-calc-cta → testimonial-quote (Dani, olive).
- **Case moderne:** page-intro hero (**bright image → white overlay ~40%, dark olive text, body semibold 600**) → home-calc-cta (cream) → feature-rows "Sisteme constructive" (5 systems, images right, item-1 title links to caramida page) → page-sample-cta (white) → benefits-list (olive bg, gold heading, white text, bullets, bold phrases, first item is the lead line; checks→bullets).
- **Cărămidă cu goluri și BCA:** page-intro hero (**brick image asset `caramida-hero.webp`, white overlay 35, olive text**) → link-list "Resurse utile" (cream) → link-list "Instrucțiuni" (cream) → **photo-gallery carousel** (37 slides, first = stratification diagram, cream) → benefits-list (olive, **zigzag top divider**, bullets, bold phrases) → page-sample-cta (white) → home-calc-cta "Calculează necesarul" (`button_position: top`, cream).
- **Cum Comand?:** all `rich-text` instances, single cream column: intro (centered h1 + interview link) → Pasul 1 split into two (`p1a` has the gold "Cere ofertă" button between paragraphs, `p1b` continues) → Pași 2–5 → meseriași → support. Then "**2.** Vrei să testezi" section is **white** (test/kit1/kit2): bold "Kit de încercare", floated bags image (`mostra-caminota-emag.jpg` from Files), Kerakoll line, "contactezi direct" → `/pages/contact`.
- **Contact:** single `contact-page` section (see §5).
- **Despre noi:** rich-text intro (white, centered h1 + **YouTube interview `o74TE1Tyeho`** + Adela Pârvu caption) → "Cum am început" (justify, founders photo `despre-vlad-andrei.webp` float-right, Ecobordei→facebook link) → "O tencuială pe cinste" (justify, bags `despre-saci.webp` float-**left** with `float_top:true` so heading sits beside it, max_width 1320, product names = bold gold links) → "Ultimii ani" (justify, `despre-ultimii.webp` float-right, max_width 960, `float_gap` 84, bold "iREBBELS", Coliba Verde→facebook, Plăci de paie→placidepaie.ro).

### Blog migration (in progress — see memory `caminota-shopify-files-urls`)
- The blog is **dynamic Shopify content**, not page templates. Client creates the blog + posts in admin; `blog-listing` / `blog-post` sections render them. Blog is the default **"News"** blog (handle `news`) → posts live at `/blogs/news/...`. (Internal links written `/blogs/sfaturi/...` need reconciling — either rename the blog handle to `sfaturi` or update those links.)
- **Per-post deliverable Claude produces:** paste-ready **content HTML** for the Content field (use the `</>` code view, NOT the visual editor — visual mode escapes the tags). Source from `migration-notes/raw/txt/blog__*.txt` for text BUT **the txt loses bold + links + image placement** — reconstruct those from the user's rendered screenshots of the original. The original posts have: **bold phrases** throughout, **product links** (`/pages/...`), and photos as **interspersed 2-col grids** (`<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:1.5rem 0;"><img …aspect-ratio:4/3…></div>`), not one gallery.
- **Wiring images:** client uploads gallery photos to **Content → Files**, then image URLs are constructable: base `https://cdn.shopify.com/s/files/1/1085/3561/1741/files/` + filename with `_`→`-` and `(1)`→`-281-29`. `?v=` is optional. Do NOT use the article-editor image uploader (adds a random UUID hash). Featured image is set per-post in admin (shows on listing card only).
- **Posts done:** (1) "Cerdacul cu Amintiri" (`blog__cerdacul-cu-amintiri`); (2) "Ce unelte folosim la tencuit cu sistemul Caminota" (handle `ce-unelte-folosim-la-tencuit-cu-sistemul-caminota`, date **4 Nov**) — content HTML in `migration-notes/blog-content/ce-unelte.html`. **Images already uploaded** to Files (in `migration-notes/assets/images-shopify/batch-01/03/04`, original sanitized names); the HTML points straight at the live CDN and all 24 cells resolve. Layout = per-section heading + intro + responsive auto-fit grid of image cards (img + bold tool name + description); original's bulleted lists + slideshow captions were merged/flattened (no JS carousel in pasted HTML). **One caveat:** the section-4 "Găleți gradate" photo (`galeata-gradata-pentru-mortar.jpeg`) collided with the section-1 `.jpg` after Shopify's `.jpeg→.jpg` normalization and reuses the section-1 image — confirm/replace if a distinct photo is wanted. 13 posts remain (see `migration-notes/raw/txt/blog__*.txt`). For each, client also sets: post **date** (so `%-d %b` shows the original date, e.g. "31 Mar") and **Author** = "Contact Caminota" to match the original byline.

---

## 7. Outstanding work

### Pending links (deferred — see memory `caminota-pending-links`)
- **Cărămidă** Resurse/Instrucțiuni link URLs are empty (render as plain dark text). Should-be-links: Resurse items 2–4; Instrucțiuni 1.1, 1.2, 1.6. Wire when the client gives blog URLs / once blog posts are migrated.
- **Despre noi** product/system links use `/pages/...` best-guess handles (`/pages/case-moderne`, `/pages/caminota-tencuiala-cu-paie`, `/pages/caminota-finisaj-rustic`, `/pages/vopsea-de-var`) — may need `/products/` prefix; verify.
- **Cum Comand?** eMag links point to the Caminota brand page (don't have exact kit/Biocalce product URLs).
- **Fișe tehnice și instrucțiuni**: the 4 fișă PDFs are now wired to **Shopify Files CDN URLs** (client uploaded; final). The 2 YouTube cards are final. Only the 2 blog cards (`/blogs/news/uscarea-pe-santier-timpii-de-prelucrare-tencuiala-lut`, `/blogs/news/ce-unelte-folosim-la-tencuit-cu-sistemul-caminota`) remain provisional — dead until those posts are migrated.

### Images served as theme assets (untracked — must be committed with the theme)
- Moderne systems: `case-moderne-timberframe.webp`, `case-moderne-panouri-paie.webp`, `case-moderne-hempcrete.webp`.
- Cărămidă: `caramida-hero.webp`, `caramida-gallery-00.webp … caramida-gallery-36.webp` (37 files; -00 is the stratification diagram).
- Despre noi: `despre-saci.webp`, `despre-vlad-andrei.webp`, `despre-ultimii.webp`.
- Product pages (heroes + galleries, all `image_asset` fallbacks): `tencuiala-hero.webp` + `tencuiala-gallery-00…05.webp`; `finisaj-hero.webp` + `finisaj-gallery-00…05.webp`; `vopsea-hero.webp` + `vopsea-gallery-00…04.webp`; `rogojina-hero.webp` + `rogojina-gallery-00…04.webp` + `rogojina-gallery-05.jpg` (this one is **JPEG** bytes — Squarespace served the original, not webp; kept `.jpg` extension so Shopify serves the right content-type); `izobarne-hero.webp` + `izobarne-gallery-00…07.webp`; `varcalcic-hero.webp` + `varcalcic-gallery-00…13.webp`. Shared eMAG sample image `mostra-caminota-emag.webp` (used in every product page's `page-sample-cta`).
- Fișe tehnice page: `instructiuni-00…07.webp` (8 card images, in card order: tencuiala bag, finisaj bag, izobârne bag, UD/USCAT wall, opening-sacks, trowel/mistrie, green-jacket applying, Biocalce bucket).
  - **Note:** `tencuiala-hero` also has a Files picker set by the client (`shopify://shop_images/t-fata.png`), which takes precedence over the asset fallback.
  - `page-sample-cta.liquid` gained an `image_asset` fallback setting (it previously had only a Files picker) so the eMAG sample image renders without a Files upload.

### Admin tasks for the user (you can't do these)
- For each new page: create it in **Online Store → Pages**, fix the **handle** (Romanian diacritics produce wrong auto-handles), assign the **Theme template**.
- Upload remaining product/gallery images to **Files** (or keep the theme-asset approach).

### Known tweaks pending review
- **Blog post in-content images render a bit small** vs the original — the `aspect-ratio:4/3` (and/or content `max_width`) in the pasted grid `<img>` inline styles needs bumping (try `1/1` or a taller ratio, or widen). These live in the pasted HTML, so it's a content edit (re-paste) — bake the fix into the per-post HTML going forward.

### Pages still to build (from `migration-notes/site-inventory.md` scope)
- **Blog: 14 of 15 posts remain** (post 1 "Cerdacul cu Amintiri" done). See blog-migration workflow above.
- **Soluții** (`page.solu-ii.json` — still a stub).
- Case-moderne sub-pages (other system detail pages besides Cărămidă), `case-moderne-1/2`.
- Legal: `termeni-si-conditii`, `politica-de-confidentialitate`, `politica-de-cookies`, FAQ.
- `program-ambasadori`, `post-oferta`.
- The external ordering calculator at comenzi.caminota.ro (TBD whether to rebuild).
- **Reconcile blog handle** (`news` vs `sfaturi`) across internal links (var-calcic "acest articol", Cărămidă pending links).

---

## 8. Persistent memory files

In `C:\Users\david\.claude\projects\C--Projects-Caminota\memory\` (auto-loaded each session via `MEMORY.md`):
- `caminota-migration` — project overview, workflow, scrape method, requested design changes.
- `caminota-architecture` — modular rule.
- `caminota-editor-pull-clobbers-config` — editor clobber gotcha.
- `caminota-image-filenames` — hyphen/underscore filename gotcha.
- `caminota-screenshot-order` — live-vs-ours by URL bar.
- `shopify-cli-tempfile-bug` — restart workaround.
- `caminota-pending-links` — the deferred Cărămidă links.
- `caminota-shopify-files-urls` — **Files CDN base + filename sanitization rules for wiring blog images** (avoid article-editor uploader). Critical for the blog migration.

---

## 9. Quick orientation commands

**No Python on this machine** (`python` → Microsoft Store stub). Validate template JSON with PowerShell instead:
```powershell
# validate a template JSON (strips Shopify's /* */ header comment first)
$raw = Get-Content "templates\page.X.json" -Raw -Encoding UTF8
ConvertFrom-Json ([regex]::Replace($raw, '/\*.*?\*/', '', 'Singleline')); "OK"

# validate a section's {% schema %} block
$s = Get-Content "sections\X.liquid" -Raw -Encoding UTF8
$m = [regex]::Match($s, '(?s)\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}')
ConvertFrom-Json $m.Groups[1].Value; "schema OK"
```
```bash
# find a page's scraped text / structure (Grep tool preferred over raw grep)
ls migration-notes/raw/txt/        # also check migration-notes/raw/*.txt
# download a live image into theme assets (then verify it's actually WEBP bytes — .JPG sources sometimes stay JPEG; rename to .jpg if so)
curl -s -L -o assets/<name>.webp "<squarespace-cdn-url>?format=1500w"
```

**Do not** start a dev/preview server (user owns 9292). **Do not** edit logo/menu sizes. **The user dislikes Python helper scripts and excessive token use — act directly, ask for missing inputs (e.g. CDN links) before producing large outputs.** Match the original via the user's screenshots, section by section.
