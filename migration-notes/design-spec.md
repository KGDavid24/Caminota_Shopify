# Caminota — Design Spec (from live site inspection, 2026-06-22)

Captured by inspecting computed styles on https://www.caminota.ro/. This is the visual target for the Horizon rebuild.

## Typography
- **Headings:** `Bevan` (chunky slab serif, Google Font), weight 400, normal letter-spacing. All H1–H4 use it.
  - H1 (hero "caminota") 60px · section titles ~42px · hero tagline 24px · line-height ~1.2–1.3
- **Body:** `Open Sans`, weight 400. Paragraphs ~18–22px, line-height ~1.8 (loose). Buttons Open Sans 600.

## Color palette
| Token | RGB | Hex | Use |
|---|---|---|---|
| Dark olive (text) | 96,100,82 | **#606452** | body text, headings, secondary buttons, footer bg |
| Cream | 244,242,228 | **#F4F2E4** | alternating section background |
| Gold / mustard | 177,164,90 | **#B1A45A** | primary buttons, links, colored benefits-section bg |
| Green accent | 98,116,52 | **#627434** | tagline "Case care inspiră.", highlights |
| White | 255,255,255 | **#FFFFFF** | page bg, text on colored sections |

## Buttons (square, no border-radius)
- **Primary** (Cere ofertă / Comandă o mostră / Download): bg `#B1A45A` gold, white text, Open Sans 600, padding ~18px 30px, radius 0.
- **Secondary** (Află mai multe): bg `#606452` dark olive, white text, radius 0.

## Homepage section-by-section layout
1. **Hero** — cream bg, **left**: dark "caminota" (Bevan 60px) + green "Case care inspiră." + dict-style definition paragraph. **Right**: 4-tile image **collage** (olive-green block, terracotta clay trowel-smear, cracked-earth tile, sandy tile). NOT white-text-over-fullbleed.
2. **"Solicită un calcul personalizat"** — cream, centered Bevan title, gold "Cere ofertă" button, centered intro (first line bold), gold phone link 0745055558.
3. **3-products band** — cream/warm bg, product-bags photo left, text right (certifications: Agrement Tehnic, ISO 9001, DIN 18947 SII), gold "Comandă o mostră Caminota prin eMag*" button + footnote.
4. **"Caminota face casă bună cu"** — centered Bevan title; two cards (image → **gold** Bevan heading → body → **olive** "Află mai multe" button): Case tradiționale, Case moderne.
5. **"Caminota pentru oameni și case"** — **solid gold-olive (#B1A45A) background**, white line-icons + white text. Two groups of 3: "Pentru oameni" (climat plăcut / ocrotește natura / ușor de aplicat) and "Pentru case" (lasă pereții să respire / ocrotește casa / întreține siguranța).
6. **"Certificări și alte tehnicalități"** — 3 light cards w/ Bevan heading + gold button: Fișe tehnice (Link), Agrement tehnic (Download), Certificat ISO 9001:2015 (Download).
7. **Misiune** — full-bleed misty-mountains photo + dark overlay, centered white Bevan "Misiune", two white paragraphs w/ bold highlights.
8. **Parteneri** — logo row: Climate-KIC / Funded by EU, INCD INCERC, ecoliving, SEVAREX.
9. **Footer** — dark olive (#606452) bg, white "caminota" logo, contact (0745 055 558, 0748 204 324, contact@caminota.ro w/ gold links), 3 link columns (Blog/FAQ/Instrucțiuni/Contact/Despre noi · Termeni/Confidențialitate/Cookies/ANPC), social icons (YT/FB/IG/email), decorative clay-smear bottom-right.

## Header / nav
Cream/white bg. Left: "C" monogram + "caminota" wordmark (Bevan, dark olive). Right nav **grouped into dropdowns**: Acasă · Soluții ▾ · Produse ▾ · Cum Comand? · Utile ▾ · Despre Noi · Contact. (My earlier flat 15-item nav was wrong — it's condensed.)

## Implementation notes
- Set theme heading font → Bevan, body font → Open Sans (verify both in Shopify font library; else add @font-face via Google Fonts).
- Define color scheme(s) in settings_data.json: cream/olive/gold/green. Likely need 3 schemes: light (cream+olive text), gold (benefits block), dark (footer).
- Buttons: square corners globally.
