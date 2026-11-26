# -*- coding: utf-8 -*-
"""
تقوية محتوى الصفحات الموجودة: يضيف أقساماً وأسئلة شائعة في أماكن محددة.
المحتوى في _seo/exp_*.py — كل ملف فيه EXP = { "مسار/الصفحة": {"sections": [...], "faqs": [...]}, ... }
  sections: (قبل_عنوان_H2 أو None للنهاية، معرف، HTML)
  faqs: [(سؤال، جواب)] — تُضاف للصفحة ولـ FAQPage Schema معاً (وتُنشأ إن لم توجد).
آمن للتكرار: كل إضافة محاطة بعلامات <!-- x:ID --> وتُستبدل عند إعادة التشغيل.
التشغيل: python _seo/expand.py   (يُشغَّل بعد gen.py لأن gen.py يعيد كتابة الصفحات المولّدة)
"""
import os, re, sys, json, html, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def load():
    exp = {}
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in sorted(os.listdir(here)):
        if fn.startswith("exp_") and fn.endswith(".py"):
            spec = importlib.util.spec_from_file_location(fn[:-3], os.path.join(here, fn))
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            for k, v in mod.EXP.items():
                exp.setdefault(k, {"sections": [], "faqs": []})
                exp[k]["sections"] += v.get("sections", [])
                exp[k]["faqs"] += v.get("faqs", [])
    return exp


def prose_end(s):
    i = s.index('<div class="prose-ar">')
    return s.index("\n      </div>\n    </div>", i)


def add_sections(s, sections, path):
    for before, sid, body in sections:
        s = re.sub(rf"\n?        <!-- x:{sid} -->.*?<!-- /x:{sid} -->", "", s, flags=re.S)
        block = f"\n        <!-- x:{sid} -->\n{body.strip(chr(10))}\n        <!-- /x:{sid} -->"
        if before == "__first__":   # قبل أول عنوان في المحتوى (ملخص في البداية)
            i = s.index('<div class="prose-ar">')
            j = s.index("\n        <h2", i)
            s = s[:j] + block + s[j:]
        elif before:
            m = re.search(r"\n        <h2[^>]*>" + re.escape(before) + r"</h2>", s)
            if not m:
                raise SystemExit(f"[{path}] heading not found: {before}")
            s = s[:m.start()] + block + s[m.start():]
        else:
            j = prose_end(s)
            s = s[:j] + block + s[j:]
    return s


def faq_items(faqs):
    return "\n".join(f'''          <details class="faq-item">
            <summary>{q}</summary>
            <div><p>{a}</p></div>
          </details>''' for q, a in faqs)


def add_faqs(s, faqs, path):
    s = re.sub(r"\n          <!-- xf -->.*?<!-- /xf -->", "", s, flags=re.S)
    s = re.sub(r"\n    <!-- xfaq -->.*?<!-- /xfaq -->", "", s, flags=re.S)
    s = re.sub(r'  <script type="application/ld\+json" data-x="faq">.*?</script>\n', "", s, flags=re.S)
    if not faqs:
        return s
    if 'class="faq-list"' in s:
        i = s.index('class="faq-list"')
        j = s.index("\n        </div>\n      </div>\n    </section>", i)
        s = s[:j] + "\n          <!-- xf -->\n" + faq_items(faqs) + "\n          <!-- /xf -->" + s[j:]
    else:
        sec = f'''
    <!-- xfaq -->
    <section class="section-sm container-site" aria-labelledby="faq-title">
      <div class="max-w-3xl">
        <h2 id="faq-title" class="mb-6">أسئلة شائعة</h2>
        <div class="faq-list">
{faq_items(faqs)}
        </div>
      </div>
    </section>
    <!-- /xfaq -->'''
        main = s[s.index('<main id="main">'):s.index("</main>")]
        for marker in ["\n    <!-- photos -->", "\n    <aside class=", '\n    <section class="section container-site">']:
            k = main.find(marker)
            if k != -1:
                break
        k += s.index('<main id="main">')
        s = s[:k] + sec + s[k:]
    # schema
    names = {strip(q) for q, _ in faqs}
    new_q = [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]
    m = None
    for m2 in re.finditer(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', s, re.S):
        obj = json.loads(m2.group(1))
        if obj.get("@type") == "FAQPage":
            m = m2; break
    if m:
        obj["mainEntity"] = [q for q in obj["mainEntity"] if q["name"] not in names] + new_q
        body = json.dumps(obj, ensure_ascii=False, indent=2)
        s = s[:m.start()] + '<script type="application/ld+json">\n' + "\n".join("  " + l for l in body.split("\n")) + "\n  </script>" + s[m.end():]
    else:
        obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": new_q}
        body = json.dumps(obj, ensure_ascii=False, indent=2)
        tag = '  <script type="application/ld+json" data-x="faq">\n' + "\n".join("  " + l for l in body.split("\n")) + "\n  </script>\n"
        s = s.replace("</head>", tag + "</head>", 1)
    return s


def apply(path, spec):
    f = os.path.join(ROOT, path, "index.html")
    s = open(f, encoding="utf-8").read()
    s = add_sections(s, spec["sections"], path)
    s = add_faqs(s, spec["faqs"], path)
    open(f, "w", encoding="utf-8", newline="\n").write(s)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    exp = load()
    only = sys.argv[1:]
    for path, spec in exp.items():
        if only and path not in only:
            continue
        apply(path, spec)
    print("expanded", len(exp) if not only else len(only), "pages")
