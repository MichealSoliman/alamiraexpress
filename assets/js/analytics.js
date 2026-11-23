/* التتبع: أحداث click_call / click_whatsapp / submit_quote / use_calculator
   ------------------------------------------------------------
   ⚠️ ضع معرف GA4 (مثل G-XXXXXXXXXX) في GA_ID لتفعيل Google Analytics.
   ما دام فارغاً: لا يُحمَّل أي سكربت خارجي ولا يظهر شريط الكوكيز.
   GA لا يُحمَّل إلا بعد موافقة الزائر (نظام حماية البيانات الشخصية PDPL).
   ------------------------------------------------------------ */
(function () {
  'use strict';
  var GA_ID = '';
  var KEY = 'ae_consent';

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  window.trackEvent = function (name, params) {
    params = params || {};
    params.page_path = location.pathname;
    params.page_title = document.title;
    if (window.gtag) window.gtag('event', name, params);
    else window.dataLayer.push({ event: name, params: params });
  };

  // تتبع أزرار الاتصال والواتساب في كل الصفحات
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-track]');
    if (a) window.trackEvent(a.getAttribute('data-track'));
  });

  if (!GA_ID) return;

  function loadGA() {
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  var choice = null;
  try { choice = localStorage.getItem(KEY); } catch (err) {}
  if (choice === 'yes') { loadGA(); return; }
  if (choice === 'no') return;

  // شريط موافقة صغير أسفل الصفحة (فوق الشريط الثابت في الجوال) — لا يغطي المحتوى
  var bar = document.createElement('div');
  bar.setAttribute('role', 'region');
  bar.setAttribute('aria-label', 'الموافقة على ملفات تعريف الارتباط');
  bar.className = 'fixed inset-x-2 bottom-20 z-50 mx-auto max-w-xl rounded-xl border border-slate-200 bg-white p-4 text-sm shadow-lg lg:bottom-4';
  bar.innerHTML = '<p>نستخدم أداة تحليلات لتحسين الموقع. <a href="/privacy/">سياسة الخصوصية</a></p>' +
    '<div class="mt-3 flex gap-2"><button type="button" class="btn-primary" data-c="yes">موافق</button>' +
    '<button type="button" class="btn-outline" data-c="no">رفض</button></div>';
  bar.addEventListener('click', function (e) {
    var v = e.target.getAttribute && e.target.getAttribute('data-c');
    if (!v) return;
    try { localStorage.setItem(KEY, v); } catch (err) {}
    bar.remove();
    if (v === 'yes') loadGA();
  });
  window.addEventListener('load', function () { document.body.appendChild(bar); });
})();
