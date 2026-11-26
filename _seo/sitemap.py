# -*- coding: utf-8 -*-
# يعيد بناء sitemap.xml من كل صفحات index.html (ما عدا thank-you). lastmod = تاريخ آخر تعديل للملف.
import glob, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
EXCLUDE = {"thank-you", "_templates", "_seo"}
urls = []
for f in sorted(glob.glob("**/index.html", recursive=True)):
    d = os.path.dirname(f).replace("\\", "/")
    if d.split("/")[0] in EXCLUDE:
        continue
    loc = "https://alamiraexpress.com/" + (d + "/" if d else "")
    mod = datetime.date.fromtimestamp(os.path.getmtime(f)).isoformat()
    urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n  </url>")
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
open("sitemap.xml", "w", encoding="utf-8", newline="\n").write(xml)
print(len(urls), "urls")
