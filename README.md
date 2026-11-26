# موقع الأميرة إكسبريس لنقل العفش بجدة

موقع ثابت: HTML + Tailwind CSS + JavaScript عادي. بدون Frameworks.

## المعاينة محلياً
```
python -m http.server 8000
```
ثم افتح http://localhost:8000 (المسارات تبدأ من الجذر `/assets/...` فلا تعمل بفتح الملف مباشرة).

## بناء ملف CSS (بعد أي تعديل في الكلاسات)
```
build.cmd
```
أو: `tailwindcss.exe -c tailwind.config.js -i assets/css/input.css -o assets/css/style.css --minify`

## تعديل البيانات
الهيدر والفوتر والشريط الثابت والـ Schema مكتوبين بنفس النص حرفياً في كل الصفحات.
لأي تعديل: استخدم **البحث والاستبدال في كل الملفات** في VS Code (`Ctrl+Shift+H`):

| البيان | القيمة الحالية |
|---|---|
| الجوال (عرض) | `0548437382` |
| الجوال (دولي) | `+966548437382` |
| واتساب | `966548437382` |
| الدومين | `https://alamiraexpress.com` |

وعدّل نفس الشي في `_templates/base.html` (القالب المرجعي للصفحات الجديدة).

## بيانات ناقصة يجب إكمالها قبل/بعد الإطلاق
- **الأسعار:** جدول `/prices/index.html` (الخانات `[__ – __ ريال]`) + نفس الأرقام في `assets/js/price-calculator.js` (الحاسبة تعرض «يبدأ من 250 ريال» فقط لحين إدخالها).
- **الشروط:** `/terms/index.html` — العربون، سياسة الإلغاء، شروط الضمان.
- **من نحن:** قصة الشركة، اسم المدير وصورته، صور الفريق والسيارات والمستودع.
- **السجل التجاري:** عند استخراجه أضفه للفوتر و `"identifier"` في Schema.
- **Google Business والسوشيال:** أضف `"hasMap"` و `"sameAs"` في Schema، وقسم «تابعنا» في الفوتر.
- **Google Analytics:** ضع المعرف في `GA_ID` داخل `assets/js/analytics.js`.
- **كاتب المقالات:** يفضل شخص حقيقي باسمه (المدونة حالياً باسم فريق الشركة).
- **الصور:** صور حقيقية بصيغة WebP في `assets/images/` (الهيرو، الخدمات، الأحياء) + صورة مشاركة OG حقيقية.
- **صفحات الأحياء:** راجع الأحياء المجاورة والتفاصيل المحلية مع الفريق (عليها تعليق `راجع` في الكود).

## الرفع على الاستضافة
ارفع كل الملفات **ما عدا**: `_templates/`، `_seo/`، `assets/images/gallery/` (الصور الأصلية — المستخدم منها نسخ WebP في `assets/images/work/`)، `tailwindcss.exe`، `tailwind.config.js`، `build.cmd`، `README.md`، `assets/css/input.css`.
- Cloudflare Pages / Netlify: يستخدمون `_headers` و `_redirects`.
- استضافة Apache عادية: تستخدم `.htaccess`.

بعد الرفع: سجّل الموقع في Google Search Console و Bing Webmaster وارفع `sitemap.xml`.
عند إضافة صفحة جديدة: انسخ `_templates/base.html` (أو أضف بياناتها في `_seo/pages_*.py` وشغّل `python _seo/gen.py`)، ثم `python _seo/sitemap.py`، وأضف رابطها في صفحة فهرس مناسبة (لا صفحات يتيمة).

خطة SEO وخريطة الكلمات المفتاحية: `_seo/SEO-PLAN.md`.
