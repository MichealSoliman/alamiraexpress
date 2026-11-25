/* حاسبة تكلفة نقل العفش التقريبية
   ------------------------------------------------------------
   ⚠️ للشركة: كل الأسعار هنا null لحين إدخال الأرقام الحقيقية.
   ما دام السعر null، الحاسبة تعرض "يبدأ من 250 ريال" فقط ولا تخترع أرقاماً.
   اكتب كل نطاق بالشكل [أقل, أعلى] بالريال — ونفس الأرقام في جدول /prices/ .
   ------------------------------------------------------------ */
var PRICES = {
  minimum: 250,
  // نقل داخل جدة شامل الفك والتركيب الأساسي (تقدير استرشادي)
  base: {
    studio: [400, 650],
    apt23:  [650, 1100],
    apt45:  [1000, 1600],
    villa:  [1600, 3000]
  },
  // إضافة لكل دور بدون مصعد (للدور الثاني فما فوق)
  perFloorNoElevator: [50, 100],
  // خدمات إضافية
  extras: {
    assembly: [0, 0],      // الفك والتركيب الأساسي مشمول في الباقة
    packing:  [200, 450],
    storage:  [350, 700]   // شهرياً
  },
  // إضافة النقل من جدة إلى مدينة (فوق سعر الأساس)
  routes: {
    jeddah:  [0, 0],
    makkah:  [250, 400],
    taif:    [400, 650],
    yanbu:   [700, 1100],
    madinah: [850, 1350],
    riyadh:  [1750, 2700],
    dammam:  [2350, 3500]
  }
};

(function () {
  'use strict';
  var form = document.querySelector('[data-price-calculator]');
  if (!form) return;
  var out = form.querySelector('[data-calc-result]');
  var note = form.querySelector('[data-calc-note]');
  var waBtn = form.querySelector('[data-calc-whatsapp]');
  var used = false;

  var LABELS = {
    studio: 'غرفة / استوديو', apt23: 'شقة 2–3 غرف', apt45: 'شقة 4–5 غرف', villa: 'فيلا / دبلكس',
    jeddah: 'داخل جدة', makkah: 'جدة ← مكة المكرمة', taif: 'جدة ← الطائف', yanbu: 'جدة ← ينبع',
    madinah: 'جدة ← المدينة المنورة', riyadh: 'جدة ← الرياض', dammam: 'جدة ← الدمام'
  };

  function add(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
  function fmt(n) { return Math.round(n / 10) * 10; }

  function calc() {
    var f = form.elements;
    var type = f.type.value, scope = f.scope.value;
    var floor = Math.max(0, parseInt(f.floor.value, 10) || 0);
    var noElevator = f.elevator.value === 'no';
    var range = PRICES.base[type];
    var ok = !!range && !!PRICES.routes[scope];

    if (ok) {
      range = add(range, PRICES.routes[scope]);
      if (noElevator && floor > 1) {
        if (!PRICES.perFloorNoElevator) ok = false;
        else range = add(range, [PRICES.perFloorNoElevator[0] * (floor - 1), PRICES.perFloorNoElevator[1] * (floor - 1)]);
      }
      ['assembly', 'packing', 'storage'].forEach(function (k) {
        if (!ok || !f[k].checked) return;
        if (!PRICES.extras[k]) ok = false; else range = add(range, PRICES.extras[k]);
      });
    }

    if (ok) {
      out.textContent = 'من ' + fmt(Math.max(range[0], PRICES.minimum)) + ' إلى ' + fmt(range[1]) + ' ريال تقريباً';
      note.textContent = 'تقدير استرشادي — السعر النهائي يتحدد بعد المعاينة المجانية.';
    } else {
      out.textContent = 'يبدأ من ' + PRICES.minimum + ' ريال';
      note.textContent = 'أرسل التفاصيل على واتساب ونرد عليك بسعر دقيق بعد المعاينة المجانية.';
    }

    var extras = [];
    if (f.assembly.checked) extras.push('فك وتركيب');
    if (f.packing.checked) extras.push('تغليف كامل');
    if (f.storage.checked) extras.push('تخزين');
    var msg = [
      'السلام عليكم، أبغى السعر النهائي لنقل عفش:',
      '• ' + LABELS[type] + ' — ' + LABELS[scope],
      '• الدور: ' + floor + ' — مصعد: ' + (noElevator ? 'لا' : 'نعم'),
      '• الخدمات: ' + (extras.length ? extras.join('، ') : 'نقل فقط'),
      '• التقدير في الموقع: ' + out.textContent
    ].join('\n');
    waBtn.href = 'https://wa.me/966548437382?text=' + encodeURIComponent(msg);

    if (!used && window.trackEvent) { used = true; window.trackEvent('use_calculator'); }
  }

  form.addEventListener('change', calc);
  form.addEventListener('input', calc);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
})();
