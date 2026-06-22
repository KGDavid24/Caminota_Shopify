import re, glob, os

pages = {}
allimg = set()
pat = re.compile(r'https://images\.squarespace-cdn\.com/content/v1/[^\s"\'?\\]+\.(?:jpg|jpeg|png|webp|gif)', re.I)

for f in sorted(glob.glob('migration-notes/raw/*.html')):
    name = os.path.basename(f)[:-5].replace('__', '/')
    html = open(f, encoding='utf-8', errors='ignore').read()
    seen = []
    for u in pat.findall(html):
        if u not in seen:
            seen.append(u); allimg.add(u)
    if seen:
        pages[name] = seen

with open('migration-notes/image-manifest.md', 'w', encoding='utf-8') as out:
    out.write('# Caminota image manifest (content images, deduped)\n\n')
    out.write('Total unique content images: %d\n\n' % len(allimg))
    for name in sorted(pages):
        out.write('## %s (%d)\n' % (name, len(pages[name])))
        for u in pages[name]:
            out.write('- %s\n' % u)
        out.write('\n')

print('unique content images:', len(allimg))
print('pages with images:', len(pages))
