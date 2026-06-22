import re, glob, os, hashlib, urllib.request, sys

pat = re.compile(r'https://images\.squarespace-cdn\.com/content/v1/[^\s"\'?\\]+\.(?:jpg|jpeg|png|webp|gif)', re.I)
urls = set()
for f in glob.glob('migration-notes/raw/*.html'):
    html = open(f, encoding='utf-8', errors='ignore').read()
    urls.update(pat.findall(html))
urls = sorted(urls)

outdir = 'migration-notes/assets/images'
os.makedirs(outdir, exist_ok=True)
ok = fail = skip = 0
log = open('migration-notes/assets/images/_download.log', 'w', encoding='utf-8')
for i, u in enumerate(urls, 1):
    h = hashlib.sha1(u.encode()).hexdigest()[:8]
    base = u.rsplit('/', 1)[-1]
    fn = '%s__%s' % (h, base)
    path = os.path.join(outdir, fn)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        skip += 1; continue
    try:
        req = urllib.request.Request(u + '?format=2500w', headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        open(path, 'wb').write(data)
        ok += 1
        log.write('OK\t%s\t%s\t%d bytes\n' % (fn, u, len(data)))
    except Exception as e:
        fail += 1
        log.write('FAIL\t%s\t%s\t%s\n' % (fn, u, e))
    if i % 50 == 0:
        print('progress %d/%d (ok=%d skip=%d fail=%d)' % (i, len(urls), ok, skip, fail), flush=True)
log.close()
print('DONE total=%d ok=%d skip=%d fail=%d' % (len(urls), ok, skip, fail), flush=True)
