# -*- coding: utf-8 -*-
"""
صور الأعمال الحقيقية (assets/images/work/) وأماكنها في الصفحات.
- IMAGES: الملف ← (النص البديل alt، التعليق، العرض، الارتفاع)
- PAGES: مسار الصفحة ← قائمة الصور
inject(html, path) يضيف/يحدّث قسم الصور بين <!-- photos --> و <!-- /photos --> (آمن للتكرار).

تشغيل على كل الصفحات:  python _seo/photos.py
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGES = {
    "thallaja-mughallafa": ("ثلاجة مغلفة بالكامل بالاسترتش الأزرق قبل نقلها من الشقة", "ثلاجة مغلفة وجاهزة للنقل"),
    "dolab-mafkuk-mughallaf": ("قطع دولاب مفكوك ومغلفة بالاسترتش داخل صالة الشقة قبل التحميل", "دولاب بعد الفك والتغليف"),
    "ajhiza-kahrabaiya-mughallafa": ("أجهزة كهربائية مغلفة بالاسترتش وموضوعة على قاعدة لحمايتها أثناء النقل", "أجهزة كهربائية مغلفة"),
    "ghassala-mughallafa": ("غسالة ملابس مغلفة من كل الجهات بالاسترتش قبل نقلها", "غسالة مغلفة قبل النقل"),
    "athath-mughallaf-lil-takhzeen": ("ألواح أثاث ومراتب مغلفة ومرصوصة بعناية للتخزين", "أثاث مغلف ومرتب للتخزين"),
    "saloon-villa-athath-mughallaf": ("صالة فيلا بعد تغليف كل الأثاث بالاسترتش استعداداً للنقل", "صالة فيلا بعد التغليف الكامل"),
    "tawilat-mughallafa-murqqama": ("طاولات دائرية وقطع أثاث مغلفة وعليها ملصقات مرقمة لتسهيل التركيب", "ترقيم القطع لتسهيل التركيب"),
    "tawilat-sufra-mughallafa": ("طاولة سفرة مغلفة سطحها بالاسترتش لحمايته من الخدش", "طاولة سفرة مغلفة"),
    "majlis-villa-mughallaf": ("كنب مجلس فاخر مغلف بالاسترتش داخل فيلا قبل نقله", "مجلس فيلا مغلف بالكامل"),
    "kanab-villa-mughallaf": ("كنب وكراسي صالة مغلفة بالاسترتش في فيلا", "كنب صالة مغلف"),
    "karasi-sufra-murqqama": ("كراسي سفرة مغلفة وعليها أرقام لترتيبها بعد النقل", "كراسي سفرة مغلفة ومرقمة"),
    "maraya-alwah-mughallafa": ("مرآة كبيرة وألواح دولاب مغلفة بطبقات من الاسترتش", "مرايا وألواح مغلفة بطبقات"),
    "athath-mughallaf-mamar-shaqqa": ("أثاث مغلف ومصفوف في ممر الشقة جاهز للتحميل", "أثاث شقة جاهز للتحميل"),
    "kanab-shaqqa-mughallaf": ("كنب مغلف بالاسترتش في صالة شقة قبل النقل", "كنب شقة مغلف"),
    "athath-shaqqa-jahiz-lil-naql": ("أثاث شقة مغلف ومجمع في غرفة واحدة قبل التحميل", "أثاث مجمع قبل التحميل"),
    "karasi-mughallafa": ("كراسي مغلفة ومرصوصة فوق بعضها لتوفير المساحة في السيارة", "كراسي مغلفة ومرصوصة"),
    "saloon-athath-murqqam": ("صالة كبيرة فيها أثاث مغلف وعليه ملصقات مرقمة", "أثاث مغلف ومرقم"),
    "sarir-mughallaf": ("لوح سرير مغلف بالاسترتش ومسنود على الجدار", "لوح سرير مغلف"),
    "qaat-villa-athath-mughallaf": ("قاعة فيلا واسعة بكامل أثاثها المغلف قبل النقل", "قاعة فيلا قبل النقل"),
    "ghurfat-nawm-mafkuka-mughallafa": ("غرفة نوم بعد فك الدولاب والسرير وتغليف القطع", "غرفة نوم بعد الفك"),
    "alwah-dolab-sarir-mughallafa": ("ألواح دولاب وسرير بعد الفك والتغليف بالاسترتش", "ألواح الدولاب بعد الفك"),
    "tahmeel-afsh-sayyara-mughlaqa": ("عفش مغلف ومرصوص داخل سيارة نقل مغلقة", "التحميل في سيارة مغلقة"),
    "taqm-kanab-mughallaf": ("طقم كنب مغلف بالاسترتش وجاهز للنقل", "طقم كنب مغلف"),
    "kanab-saloon-mughallaf": ("كنب صالة طويل مغلف بالاسترتش تحت الثريا", "كنب صالة مغلف"),
}

VILLA = ["majlis-villa-mughallaf", "qaat-villa-athath-mughallaf", "kanab-villa-mughallaf", "saloon-villa-athath-mughallaf",
         "kanab-saloon-mughallaf", "saloon-athath-murqqam", "maraya-alwah-mughallafa"]
FLAT = ["athath-mughallaf-mamar-shaqqa", "kanab-shaqqa-mughallaf", "athath-shaqqa-jahiz-lil-naql", "ghurfat-nawm-mafkuka-mughallafa",
        "dolab-mafkuk-mughallaf", "taqm-kanab-mughallaf", "tawilat-sufra-mughallafa", "karasi-mughallafa", "sarir-mughallaf",
        "alwah-dolab-sarir-mughallafa"]
VILLA_AREAS = ["al-shati", "al-mohammadiyah", "al-khalidiyah", "al-zahra", "al-basateen", "al-naeem", "obhur-al-shamaliyah",
               "obhur-al-janubiyah", "al-sawari", "al-yaqout", "al-murjan", "al-nahdah", "al-harazat", "al-hamra", "al-sanabel", "al-samer"]

PAGES = {
    "services/moving-furniture-jeddah": ["saloon-villa-athath-mughallaf", "athath-mughallaf-mamar-shaqqa", "tahmeel-afsh-sayyara-mughlaqa"],
    "services/dismantling-assembly": ["ghurfat-nawm-mafkuka-mughallafa", "alwah-dolab-sarir-mughallafa", "dolab-mafkuk-mughallaf"],
    "services/packing": ["karasi-sufra-murqqama", "ajhiza-kahrabaiya-mughallafa", "maraya-alwah-mughallafa"],
    "services/storage": ["maraya-alwah-mughallafa", "alwah-dolab-sarir-mughallafa"],
    "services/dyna": ["athath-shaqqa-jahiz-lil-naql", "karasi-mughallafa"],
    "services/cheap-furniture-moving": ["taqm-kanab-mughallaf", "kanab-shaqqa-mughallaf"],
    "services": ["majlis-villa-mughallaf", "ghurfat-nawm-mafkuka-mughallafa", "tahmeel-afsh-sayyara-mughlaqa"],
    "about": ["saloon-villa-athath-mughallaf", "tawilat-mughallafa-murqqama", "ghurfat-nawm-mafkuka-mughallafa"],
    "prices": ["athath-mughallaf-mamar-shaqqa", "qaat-villa-athath-mughallaf"],
    "blog/moving-fridge-washing-machine": ["thallaja-mughallafa", "ghassala-mughallafa", "ajhiza-kahrabaiya-mughallafa"],
    "blog/how-to-pack-furniture": ["karasi-sufra-murqqama", "tawilat-mughallafa-murqqama", "karasi-mughallafa"],
    "blog/moving-without-elevator": ["alwah-dolab-sarir-mughallafa", "athath-mughallaf-mamar-shaqqa"],
    "blog/renting-dyna-jeddah": ["tahmeel-afsh-sayyara-mughlaqa"],
    "blog/moving-checklist-jeddah": ["saloon-athath-murqqam", "tawilat-sufra-mughallafa"],
    "blog/choose-moving-company-jeddah": ["kanab-villa-mughallaf"],
    "blog/best-time-to-move-jeddah": ["qaat-villa-athath-mughallaf"],
}
_ROUTE_EXTRA = ["saloon-athath-murqqam", "tawilat-mughallafa-murqqama", "maraya-alwah-mughallafa", "ajhiza-kahrabaiya-mughallafa", "karasi-mughallafa", "majlis-villa-mughallaf"]


def photos_for(path):
    if path in PAGES:
        return PAGES[path]
    parts = path.split("/")
    if len(parts) == 2 and parts[0] == "routes":
        i = sum(map(ord, parts[1])) % len(_ROUTE_EXTRA)
        return ["tahmeel-afsh-sayyara-mughlaqa", _ROUTE_EXTRA[i]]
    if len(parts) == 2 and parts[0] == "areas":
        pool = VILLA if parts[1] in VILLA_AREAS else FLAT
        i = sum(map(ord, parts[1])) % len(pool)
        a, b = pool[i], pool[(i + 3) % len(pool)]
        return [a, b]
    return []


def _size(name):
    from PIL import Image
    with Image.open(os.path.join(ROOT, "assets/images/work", name + ".webp")) as im:
        return im.size


def figure(name):
    alt, cap = IMAGES[name]
    w, h = _size(name)
    return (f'          <figure class="photo">\n'
            f'            <img src="/assets/images/work/{name}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">\n'
            f'            <figcaption>{cap}</figcaption>\n'
            f'          </figure>')


def block(names, title="صور من نقلاتنا"):
    figs = "\n".join(figure(n) for n in names)
    return (f'    <!-- photos -->\n'
            f'    <section class="section-sm container-site" aria-labelledby="photos-title">\n'
            f'      <h2 id="photos-title" class="mb-5 text-xl">{title}</h2>\n'
            f'      <div class="photo-grid">\n{figs}\n      </div>\n'
            f'    </section>\n'
            f'    <!-- /photos -->\n')


def inject(s, path):
    s = re.sub(r"    <!-- photos -->.*?<!-- /photos -->\n", "", s, flags=re.S)
    names = photos_for(path)
    if not names:
        return s
    main = re.search(r'<main id="main">.*?</main>', s, re.S)
    seg = main.group(0)
    for marker in ['    <section class="section-sm container-site" aria-labelledby="faq-title">',
                   '    <aside class="section-sm container-site"',
                   '    <section class="section container-site">']:
        i = seg.find(marker)
        if i != -1:
            break
    else:
        i = seg.rfind("  </main>")
    seg = seg[:i] + block(names) + seg[i:]
    return s[:main.start()] + seg + s[main.end():]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    n = 0
    for f in glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True):
        rel = os.path.relpath(os.path.dirname(f), ROOT).replace(os.sep, "/")
        if rel.startswith("_") or rel == ".":
            continue
        s = open(f, encoding="utf-8").read()
        o = inject(s, rel)
        if o != s:
            open(f, "w", encoding="utf-8", newline="\n").write(o); n += 1
    print("pages with photos:", n)
