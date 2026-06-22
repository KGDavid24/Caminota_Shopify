import re, glob, os, hashlib, shutil, csv, unicodedata

# 1. Build url -> ordered list of pages, from raw HTML
pat = re.compile(r'https://images\.squarespace-cdn\.com/content/v1/[^\s"\'?\\]+\.(?:jpg|jpeg|png|webp|gif)', re.I)
url_pages = {}
for f in sorted(glob.glob('migration-notes/raw/*.html')):
    page = os.path.basename(f)[:-5].replace('__', '/')
    html = open(f, encoding='utf-8', errors='ignore').read()
    seen = set()
    for u in pat.findall(html):
        if u in seen:
            continue
        seen.add(u)
        url_pages.setdefault(u, []).append(page)

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

GENERIC = re.compile(r'^(\d+|image-asset|layer-?\d+|p\d+|img-?\d+-wa\d+|dsc-?\d+|untitled|[0-9a-f]{6,})$')

def humanize(slug):
    t = slug.replace('-', ' ').strip()
    return t[:1].upper() + t[1:] if t else t

srcdir = 'migration-notes/assets/images'
dstdir = 'migration-notes/assets/images-shopify'
os.makedirs(dstdir, exist_ok=True)

# deterministic order: by url
rows = []
used = {}
for u in sorted(url_pages):
    h = hashlib.sha1(u.encode()).hexdigest()[:8]
    orig = u.rsplit('/', 1)[-1]
    local = '%s__%s' % (h, orig)
    localpath = os.path.join(srcdir, local)
    if not os.path.exists(localpath):
        continue
    name, ext = os.path.splitext(orig)
    ext = ext.lower()
    pages = url_pages[u]
    primary = pages[0]
    base_slug = slugify(name)
    if not base_slug or GENERIC.match(base_slug):
        base_slug = slugify(primary.replace('/', '-'))
        descriptive = False
    else:
        descriptive = True
    clean = base_slug + ext
    n = 1
    while clean in used:
        n += 1
        clean = '%s-%02d%s' % (base_slug, n, ext)
    used[clean] = local
    shutil.copy2(localpath, os.path.join(dstdir, clean))
    alt = humanize(base_slug) if descriptive else humanize(slugify(primary.replace('/', '-')))
    rows.append({
        'shopify_filename': clean,
        'original_filename': orig,
        'used_on_pages': '; '.join(pages),
        'primary_page': primary,
        'suggested_alt': alt,
        'source_url': u,
    })

with open('migration-notes/image-upload-map.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['shopify_filename', 'original_filename', 'used_on_pages', 'primary_page', 'suggested_alt', 'source_url'])
    w.writeheader()
    w.writerows(rows)

print('clean files written:', len(rows))
print('unique clean names:', len(used))
print('descriptive vs page-derived:', sum(1 for r in rows if slugify(os.path.splitext(r['original_filename'])[0]) and not GENERIC.match(slugify(os.path.splitext(r['original_filename'])[0]))), 'descriptive')
