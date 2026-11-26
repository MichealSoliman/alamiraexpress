# -*- coding: utf-8 -*-
"""
مولّد الصفحات الجديدة (لا يُرفع على الاستضافة).
يأخذ صفحة قائمة كـ "قشرة" (الهيدر والفوتر والـ Schema الموحد حرفياً)
ويستبدل فقط: الميتا، Schema الخاص بالصفحة، مسار التنقل، <main>، ونص رسالة واتساب.

الاستخدام (من جذر المشروع):
    python _seo/gen.py
المحتوى موجود في _seo/pages_*.py — كل صفحة بمحتوى فريد خاص بها.
"""
import json, re, sys, os, html, urllib.parse, importlib.util
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://alamiraexpress.com"
SHELLS = {
    "area": "areas/al-salamah/index.html",
    "route": "routes/jeddah-to-taif/index.html",
    "blog": "blog/moving-checklist-jeddah/index.html",
    "service": "services/dyna/index.html",
}
ARROW = '<span aria-hidden="true" class="text-slate-400">←</span>'


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    full = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def ld(obj):
    body = json.dumps(obj, ensure_ascii=False, indent=2)
    body = "\n".join("  " + l for l in body.split("\n"))
    return '  <script type="application/ld+json">\n' + body + "\n  </script>\n"


def wa(text):
    return urllib.parse.quote(text, safe="")


def shell_parts(kind):
    s = read(SHELLS[kind])
    # الأزرار داخل main (نعيد استخدامها كما هي)
    main = re.search(r"<main id=\"main\">.*?</main>", s, re.S).group(0)
    hero_btns = re.search(r'<div class="mt-8 flex flex-col gap-3 sm:flex-row">.*?</div>', main, re.S)
    cta_btns = re.search(r'<div class="mt-8 justify-center flex flex-col gap-3 sm:flex-row">.*?</div>', main, re.S)
    old_wa = Counter(re.findall(r"wa\.me/966548437382\?text=([^\"&]+)", s)).most_common(1)[0][0]
    return s, hero_btns.group(0) if hero_btns else "", cta_btns.group(0) if cta_btns else "", old_wa


def related(items, label):
    lis = "\n".join(
        f'          <li><a href="{h}" class="route-card min-h-[52px] text-[15px]">{t}{ARROW}</a></li>' for h, t in items
    )
    return f'''    <aside class="section-sm container-site" aria-label="{label}">
      <div class="max-w-3xl">
        <h2 class="mb-5 text-xl">{label}</h2>
        <ul class="grid gap-3 sm:grid-cols-2">
{lis}
        </ul>
      </div>
    </aside>
'''


def faq_html(title, faqs):
    items = "\n".join(
        f'''          <details class="faq-item">
            <summary>{q}</summary>
            <div><p>{a}</p></div>
          </details>''' for q, a in faqs
    )
    return f'''    <section class="section-sm container-site" aria-labelledby="faq-title">
      <div class="max-w-3xl">
        <h2 id="faq-title" class="mb-6">{title}</h2>
        <div class="faq-list">
{items}
        </div>
      </div>
    </section>
'''


def build(p):
    kind = p["kind"]
    s, hero_btns, cta_btns, old_wa = shell_parts(kind)
    url = f"{DOMAIN}/{p['path']}/"
    new_wa = wa(p["wa"]) if p.get("wa") else old_wa
    hero_btns = hero_btns.replace(old_wa, new_wa)
    cta_btns = cta_btns.replace(old_wa, new_wa)

    # ---------- head ----------
    title, desc = p["title"], p["desc"]
    head = f'''<title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">

  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="{'article' if kind == 'blog' else 'website'}">
  <meta property="og:locale" content="ar_SA">
  <meta property="og:site_name" content="الأميرة إكسبريس لنقل العفش بجدة">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://alamiraexpress.com/assets/images/og/og-default.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
{f'  <meta property="article:published_time" content="{p["date"]}">{chr(10)}' if kind == 'blog' else ''}  <meta name="twitter:card" content="summary_large_image">

  '''
    s = re.sub(r"<title>.*?(?=<meta name=\"theme-color\")", lambda m: head, s, count=1, flags=re.S)

    # ---------- page schemas ----------
    crumbs = [("الرئيسية", f"{DOMAIN}/")] + [(n, DOMAIN + h) for n, h in p["crumbs"]] + [(p["crumb"], url)]
    schemas = ld({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)],
    })
    if kind == "blog":
        schemas += ld({
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": strip(p["h1"]), "description": desc, "inLanguage": "ar-SA",
            "url": url, "mainEntityOfPage": url,
            "datePublished": p["date"], "dateModified": p["date"],
            "image": "https://alamiraexpress.com/assets/images/og/og-default.jpg",
            "author": {"@type": "Organization", "name": "الأميرة إكسبريس لنقل العفش بجدة", "url": "https://alamiraexpress.com/about/"},
            "publisher": {"@id": "https://alamiraexpress.com/#business"},
        })
    else:
        default_area = {"@type": "City", "name": "جدة"}
        if kind == "area":
            default_area = {"@type": "Place", "name": f'{p["crumb"]}، جدة', "containedInPlace": {"@type": "City", "name": "جدة"}}
        svc = {"@context": "https://schema.org", "@type": "Service", "name": p["service_name"],
               "description": desc,
               "serviceType": p.get("service_type", "نقل عفش وأثاث"), "url": url,
               "provider": {"@id": "https://alamiraexpress.com/#business"},
               "areaServed": p.get("area_served", default_area)}
        schemas += ld(svc)
    if p.get("faqs"):
        schemas += ld({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in p["faqs"]],
        })
    # كل ما بعد Schema الشركة حتى </head>
    m = re.search(r'("@id": "https://alamiraexpress.com/#business".*?</script>\n)(.*?)(</head>)', s, re.S)
    s = s[: m.start(2)] + schemas + s[m.start(3):]

    # ---------- nav current ----------
    s = s.replace(' aria-current="true"', "")
    nav_target = {"area": "/areas/", "route": "/routes/", "blog": "/blog/"}.get(kind)
    if nav_target:
        s = s.replace(f'<a href="{nav_target}" class="nav-link">', f'<a href="{nav_target}" class="nav-link" aria-current="true">', 1)

    # ---------- breadcrumbs ----------
    bc = "\n".join(f'      <li><a href="{h}">{n}</a></li>' for n, h in [("الرئيسية", "/")] + p["crumbs"])
    bc += f'\n      <li><span aria-current="page">{p["crumb"]}</span></li>'
    s = re.sub(r'(<nav aria-label="مسار التنقل"[^>]*>\s*<ol>).*?(</ol>)', lambda m: m.group(1) + "\n" + bc + "\n    " + m.group(2), s, count=1, flags=re.S)

    # ---------- main ----------
    eyebrow = f'      <p class="eyebrow">{p["eyebrow"]}</p>\n' if p.get("eyebrow") else ""
    if kind == "blog":
        hero = f'''    <section class="page-hero">
{eyebrow}      <h1 class="max-w-3xl">{p["h1"]}</h1>
      <p class="lead">{p["lead"]}</p>
    </section>
    <div class="container-site"><div class="divider"></div></div>
    <!-- ⚠️ الشركة: يُفضّل أن يكون الكاتب شخصاً حقيقياً من الفريق باسمه — حدّث author في الـ Schema أيضاً -->
    <p class="container-site pt-6 text-sm text-slate-500">فريق الأميرة إكسبريس · <time datetime="{p["date"]}">{p["date_ar"]}</time></p>
'''
    else:
        hero = f'''    <section class="page-hero">
{eyebrow}      <h1>{p["h1"]}</h1>
      <p class="lead">{p["lead"]}</p>
      {hero_btns}
      <ul class="checks"><li>معاينة مجانية</li><li>ضمان ضد التلف</li><li>حضور في نفس اليوم</li><li>متاحون 24 ساعة</li></ul>
    </section>
    <div class="container-site"><div class="divider"></div></div>
'''
    review = "    <!-- راجع مع فريق الشركة: تفاصيل الحي والأحياء القريبة المذكورة -->\n" if kind == "area" else ""
    body = f'''{review}    <div class="section-sm container-site">
      <div class="prose-ar">
{p["body"].strip(chr(10))}
      </div>
    </div>
'''
    faq = faq_html(p["faq_title"], p["faqs"]) if p.get("faqs") else ""
    rel = related(p["related"], p.get("related_label", "صفحات ذات صلة"))
    cta = f'''    <section class="section container-site">
      <div class="cta-box">
        <h2>{p["cta_h"]}</h2>
        <p>{p["cta_p"]}</p>
      {cta_btns}
      </div>
    </section>
'''
    main = '<main id="main">\n' + hero + body + faq + rel + cta + "  </main>"
    s = re.sub(r"<main id=\"main\">.*?</main>", lambda m: main, s, count=1, flags=re.S)

    # ---------- whatsapp (sticky bar + floating) ----------
    s = s.replace(old_wa, new_wa)
    import photos
    s = photos.inject(s, p["path"])
    write(f"{p['path']}/index.html", s)
    return p["path"]


def load_pages():
    pages = []
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in sorted(os.listdir(here)):
        if fn.startswith("pages_") and fn.endswith(".py"):
            spec = importlib.util.spec_from_file_location(fn[:-3], os.path.join(here, fn))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            pages += mod.PAGES
    return pages


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    only = sys.argv[1:]
    for p in load_pages():
        if only and p["path"] not in only:
            continue
        print("built", build(p))
