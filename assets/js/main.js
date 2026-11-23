/* الأميرة إكسبريس — تفاعلات الواجهة فقط (لا يُحقن أي محتوى مهم هنا) */
(function () {
  'use strict';

  /* ---------- قائمة الجوال ---------- */
  var menuBtn = document.querySelector('[data-menu-toggle]');
  var menu = document.getElementById('mobile-menu');

  function setMenu(open) {
    if (!menuBtn || !menu) return;
    menu.hidden = !open;
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'إغلاق القائمة' : 'فتح القائمة');
    menuBtn.querySelector('[data-icon-open]').classList.toggle('hidden', open);
    menuBtn.querySelector('[data-icon-close]').classList.toggle('hidden', !open);
  }

  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () {
      setMenu(menu.hidden);
    });
  }

  /* ---------- قائمة الخدمات المنسدلة (ديسكتوب) ---------- */
  var dropdowns = document.querySelectorAll('[data-dropdown]');

  function setDropdown(dd, open) {
    var btn = dd.querySelector('[data-dropdown-toggle]');
    var list = document.getElementById(btn.getAttribute('aria-controls'));
    list.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
    var icon = btn.querySelector('svg');
    if (icon) icon.classList.toggle('rotate-180', open);
  }

  dropdowns.forEach(function (dd) {
    var btn = dd.querySelector('[data-dropdown-toggle]');
    btn.addEventListener('click', function () {
      setDropdown(dd, btn.getAttribute('aria-expanded') !== 'true');
    });
    // يُغلق عند خروج التركيز بالكيبورد من القائمة
    dd.addEventListener('focusout', function (e) {
      if (!dd.contains(e.relatedTarget)) setDropdown(dd, false);
    });
  });

  // إغلاق عند الضغط خارجها
  document.addEventListener('click', function (e) {
    dropdowns.forEach(function (dd) {
      if (!dd.contains(e.target)) setDropdown(dd, false);
    });
  });

  // Escape يغلق كل القوائم ويعيد التركيز لزرها
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    dropdowns.forEach(function (dd) {
      var btn = dd.querySelector('[data-dropdown-toggle]');
      if (btn.getAttribute('aria-expanded') === 'true') {
        setDropdown(dd, false);
        btn.focus();
      }
    });
    if (menu && !menu.hidden) {
      setMenu(false);
      menuBtn.focus();
    }
  });

  // إغلاق قائمة الجوال عند التحويل لمقاس الديسكتوب
  var mq = window.matchMedia('(min-width: 1024px)');
  var onMq = function (e) { if (e.matches) setMenu(false); };
  if (mq.addEventListener) mq.addEventListener('change', onMq);

  /* ---------- الخريطة: لا تُحمَّل إلا عند الضغط ----------
     الاستخدام في HTML:
     <button type="button" data-lazy-map="https://www.google.com/maps/embed?pb=..." data-map-title="موقع الأميرة إكسبريس على الخريطة">
       <img src="/assets/images/map-placeholder.webp" alt="..." width="..." height="..." loading="lazy">
     </button>
  */
  document.querySelectorAll('[data-lazy-map]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var iframe = document.createElement('iframe');
      iframe.src = btn.getAttribute('data-lazy-map');
      iframe.title = btn.getAttribute('data-map-title') || 'خريطة الموقع';
      iframe.loading = 'lazy';
      iframe.referrerPolicy = 'no-referrer-when-downgrade';
      iframe.className = 'h-full w-full border-0';
      iframe.setAttribute('allowfullscreen', '');
      btn.replaceWith(iframe);
    }, { once: true });
  });

  /* ---------- سنة الحقوق ---------- */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = String(new Date().getFullYear());
})();
