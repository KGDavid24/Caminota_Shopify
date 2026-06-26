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
- **`page-sample-cta.liquid`** — "Probează Caminota": image left + heading/body/button/footnote right. Olive button override, gold footnote.
- **`testimonial-quote.liquid`** — italic quote + author (author is regular-weight muted gold, not Bevan). Olive bg default.
- **`feature-rows.liquid`** — repeatable image/text rows (Moderne "Sisteme constructive"). Blocks: `image`/`image_asset`, `image_position`, `number` (inline with title), `title` (links via `link_url`), `subtitle` (underlined olive — color set inline due to style-block flakiness), `body` (justified semibold olive), `link_label`/`link_url` (gold button). Dividers between rows. Heading left-aligned.
- **`benefits-list.liquid`** — checklist (Moderne/Cărămidă benefits). `heading`/`lead`/`closing`, blocks of `text` (embed `<strong>` for bold phrases). `marker` = check/bullet/none, `marker`/`check_color`, `heading_color`/`text_color`. **Zigzag top divider** (`top_divider` + `divider_above_color`) — a Liquid-generated SVG sawtooth that bridges a cream section above into the olive section.
- **`link-list.liquid`** — heading + intro + link blocks (`label`, `url` → gold link if set else plain dark, `bold` checkbox). Used for Cărămidă "Resurse utile" / "Instrucțiuni".
- **`photo-gallery.liquid`** — **carousel**: large main image (`main_width`, `ratio`, object-fit contain) with `‹ ›` arrows + a scrolling thumbnail strip. Photo blocks (`image`/`image_asset`). JS: clicking a thumb/arrow moves the main image AND scrolls the thumb strip to keep the active thumb centered; active thumb gets a gold border. (Cărămidă gallery, 37 slides.)
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

### Page structure cheat-sheet
- **Case tradiționale:** page-intro hero (olive overlay 45, white text) → page-video (Arad interview, olive) → product-feature ×3 (Tencuiala white/img-left, Finisaj **gold bg + white text**/img-right, Vopsea white/img-left, 2 downloads) → page-sample-cta (Probează) → home-calc-cta → testimonial-quote (Dani, olive).
- **Case moderne:** page-intro hero (**bright image → white overlay ~40%, dark olive text, body semibold 600**) → home-calc-cta (cream) → feature-rows "Sisteme constructive" (5 systems, images right, item-1 title links to caramida page) → page-sample-cta (white) → benefits-list (olive bg, gold heading, white text, bullets, bold phrases, first item is the lead line; checks→bullets).
- **Cărămidă cu goluri și BCA:** page-intro hero (**brick image asset `caramida-hero.webp`, white overlay 35, olive text**) → link-list "Resurse utile" (cream) → link-list "Instrucțiuni" (cream) → **photo-gallery carousel** (37 slides, first = stratification diagram, cream) → benefits-list (olive, **zigzag top divider**, bullets, bold phrases) → page-sample-cta (white) → home-calc-cta "Calculează necesarul" (`button_position: top`, cream).
- **Cum Comand?:** all `rich-text` instances, single cream column: intro (centered h1 + interview link) → Pasul 1 split into two (`p1a` has the gold "Cere ofertă" button between paragraphs, `p1b` continues) → Pași 2–5 → meseriași → support. Then "**2.** Vrei să testezi" section is **white** (test/kit1/kit2): bold "Kit de încercare", floated bags image (`mostra-caminota-emag.jpg` from Files), Kerakoll line, "contactezi direct" → `/pages/contact`.
- **Contact:** single `contact-page` section (see §5).
- **Despre noi:** rich-text intro (white, centered h1 + **YouTube interview `o74TE1Tyeho`** + Adela Pârvu caption) → "Cum am început" (justify, founders photo `despre-vlad-andrei.webp` float-right, Ecobordei→facebook link) → "O tencuială pe cinste" (justify, bags `despre-saci.webp` float-**left** with `float_top:true` so heading sits beside it, max_width 1320, product names = bold gold links) → "Ultimii ani" (justify, `despre-ultimii.webp` float-right, max_width 960, `float_gap` 84, bold "iREBBELS", Coliba Verde→facebook, Plăci de paie→placidepaie.ro).

---

## 7. Outstanding work

### Pending links (deferred — see memory `caminota-pending-links`)
- **Cărămidă** Resurse/Instrucțiuni link URLs are empty (render as plain dark text). Should-be-links: Resurse items 2–4; Instrucțiuni 1.1, 1.2, 1.6. Wire when the client gives blog URLs / once blog posts are migrated.
- **Despre noi** product/system links use `/pages/...` best-guess handles (`/pages/case-moderne`, `/pages/caminota-tencuiala-cu-paie`, `/pages/caminota-finisaj-rustic`, `/pages/vopsea-de-var`) — may need `/products/` prefix; verify.
- **Cum Comand?** eMag links point to the Caminota brand page (don't have exact kit/Biocalce product URLs).

### Images served as theme assets (untracked — must be committed with the theme)
- Moderne systems: `case-moderne-timberframe.webp`, `case-moderne-panouri-paie.webp`, `case-moderne-hempcrete.webp`.
- Cărămidă: `caramida-hero.webp`, `caramida-gallery-00.webp … caramida-gallery-36.webp` (37 files; -00 is the stratification diagram).
- Despre noi: `despre-saci.webp`, `despre-vlad-andrei.webp`, `despre-ultimii.webp`.

### Admin tasks for the user (you can't do these)
- For each new page: create it in **Online Store → Pages**, fix the **handle** (Romanian diacritics produce wrong auto-handles), assign the **Theme template**.
- Upload remaining product/gallery images to **Files** (or keep the theme-asset approach).

### Pages still to build (from `migration-notes/site-inventory.md` scope: 6 products, ~10 content/legal pages, 15 blog posts)
- **Soluții** (`page.solu-ii.json` — still a stub).
- Product pages: `caminota-tencuiala-cu-paie`, `caminota-finisaj-rustic`, `caminota-izobarne`, `rogojina-de-stuf`, `vopsea-de-var`, `var-calcic-hidratat`.
- Case-moderne sub-pages (e.g. the other system detail pages besides Cărămidă), `case-moderne-1/2`.
- Legal: `termeni-si-conditii`, `politica-de-confidentialitate`, `politica-de-cookies`, FAQ.
- Blog (15 posts), `program-ambasadori`, `post-oferta`.
- The external ordering calculator at comenzi.caminota.ro (TBD whether to rebuild).

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

---

## 9. Quick orientation commands

```bash
# validate a page template (strip Shopify's /* */ header comment first)
python -c "import json,re; raw=open('templates/page.X.json',encoding='utf-8').read(); json.loads(re.sub(r'/\*.*?\*/','',raw,flags=re.DOTALL)); print('OK')"

# find a page's scraped text / structure
ls migration-notes/raw/txt/        # also check migration-notes/raw/*.txt
grep -noiE "<h[1-3][^>]*>[^<]+|youtube.com/embed/[A-Za-z0-9_-]+|section-background" migration-notes/raw/<page>.html

# download a live image into theme assets (then rename .png/.jpg -> .webp; Squarespace serves webp)
curl -s -L -o assets/<name>.webp "<squarespace-cdn-url>?format=1500w"
```

**Do not** start a dev/preview server. **Do not** edit logo/menu sizes. Match the original via the user's screenshots, section by section.
