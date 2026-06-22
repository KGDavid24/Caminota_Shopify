import re, sys
from html.parser import HTMLParser

SKIP = {'script','style','noscript','svg','head'}
BLOCK = {'h1','h2','h3','h4','h5','h6','p','li','td','th','blockquote','div','section'}

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip=0; self.out=[]; self.cur=[]; self.tag_stack=[]
    def handle_starttag(self,t,a):
        if t in SKIP: self.skip+=1
        if t in ('br',): self.cur.append('\n')
        if t in BLOCK and self.cur:
            self.flush()
        if t in ('h1','h2','h3','h4'): self.tag_stack.append(t)
    def handle_endtag(self,t):
        if t in SKIP and self.skip: self.skip-=1
        if t in BLOCK: self.flush(t)
    def flush(self,t=None):
        txt=''.join(self.cur).strip()
        self.cur=[]
        if txt:
            pre=''
            if self.tag_stack:
                lvl=self.tag_stack[-1]; pre={'h1':'# ','h2':'## ','h3':'### ','h4':'#### '}.get(lvl,'')
            self.out.append(pre+txt)
        if t in ('h1','h2','h3','h4') and self.tag_stack: self.tag_stack.pop()
    def handle_data(self,d):
        if not self.skip:
            self.cur.append(d)

html=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
# isolate main content region if present
m=re.search(r'<main\b.*?</main>', html, re.S|re.I)
if m: html=m.group(0)
p=Extract(); p.feed(html)
seen=set(); lines=[]
for l in p.out:
    l=re.sub(r'\s+',' ',l).strip()
    if len(l)<2: continue
    if l in seen: continue
    seen.add(l); lines.append(l)
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(lines))
