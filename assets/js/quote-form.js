/* نموذج طلب عرض السعر: تحقق من الحقول ← رسالة واتساب منسقة ← صفحة الشكر */
(function () {
  'use strict';
  var WA_NUMBER = '966548437382';

  document.querySelectorAll('[data-quote-form]').forEach(function (form) {
    function showError(name, show) {
      var el = form.querySelector('[data-error-for="' + name + '"]');
      var input = form.elements[name];
      if (el) el.hidden = !show;
      if (input) input.setAttribute('aria-invalid', show ? 'true' : 'false');
    }

    function normalizePhone(v) {
      // يقبل الأرقام العربية والإنجليزية، و +966 أو 966 أو 05
      v = String(v || '').replace(/[٠-٩]/g, function (d) { return String('٠١٢٣٤٥٦٧٨٩'.indexOf(d)); });
      v = v.replace(/[\s\-()]/g, '');
      if (v.indexOf('+966') === 0) v = '0' + v.slice(4);
      else if (v.indexOf('966') === 0) v = '0' + v.slice(3);
      return v;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Honeypot: البوتات تعبّي الحقل المخفي
      if (form.elements.website && form.elements.website.value) return;

      var f = form.elements;
      var phone = normalizePhone(f.phone.value);
      var checks = {
        name: f.name.value.trim().length >= 2,
        phone: /^05\d{8}$/.test(phone),
        from: f.from.value.trim().length >= 2,
        to: f.to.value.trim().length >= 2
      };
      var firstBad = null;
      Object.keys(checks).forEach(function (k) {
        showError(k, !checks[k]);
        if (!checks[k] && !firstBad) firstBad = f[k];
      });
      if (firstBad) { firstBad.focus(); return; }

      var services = Array.prototype.slice.call(form.querySelectorAll('input[name="services"]:checked'))
        .map(function (c) { return c.value; });

      var lines = [
        'السلام عليكم، أبغى عرض سعر نقل عفش:',
        '• الاسم: ' + f.name.value.trim(),
        '• الجوال: ' + phone,
        '• من: ' + f.from.value.trim(),
        '• إلى: ' + f.to.value.trim(),
        '• نوع السكن: ' + f.type.value + ' — الغرف: ' + f.rooms.value,
        '• الدور: ' + (f.floor.value === '' ? 'غير محدد' : f.floor.value) + ' — مصعد: ' + f.elevator.value
      ];
      if (f.date.value) lines.push('• التاريخ المتوقع: ' + f.date.value);
      lines.push('• الخدمات: ' + (services.length ? services.join('، ') : 'نقل فقط'));
      if (f.notes.value.trim()) lines.push('• ملاحظات: ' + f.notes.value.trim());
      lines.push('(من صفحة: ' + document.title + ')');

      var url = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));

      if (window.trackEvent) window.trackEvent('submit_quote', { services: services.join(',') });

      var win = window.open(url, '_blank');
      if (win) win.opener = null;
      // لو المتصفح منع النافذة، نفتح الواتساب في نفس الصفحة
      if (!win) { window.location.href = url; return; }
      window.location.href = '/thank-you/';
    });
  });
})();
