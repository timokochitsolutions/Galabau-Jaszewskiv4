(function () {
  var d = document, root = d.documentElement;

  // Kopfzeile beim Scrollen
  var top = d.querySelector('.top');
  function onScroll() { if (top) top.classList.toggle('scrolled', window.scrollY > 20); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobiles Menü
  var burger = d.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = d.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    d.querySelectorAll('.mobile a').forEach(function (a) {
      a.addEventListener('click', function () { d.body.classList.remove('menu-open'); });
    });
  }

  // Einblenden beim Scrollen (Inhalt bleibt ohne JS sichtbar)
  var els = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
    // Sicherheitsnetz: nach 2,5 s alles zeigen, was im Sichtbereich liegt oder darüber
    setTimeout(function () {
      els.forEach(function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in');
      });
    }, 2500);
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  // Anfrageformular: erzeugt eine fertige Nachricht für WhatsApp oder E-Mail
  d.querySelectorAll('form.anfrage').forEach(function (form) {
    function text() {
      var g = function (n) { var f = form.elements[n]; return f ? f.value.trim() : ''; };
      var lines = ['Anfrage über die Website', ''];
      if (g('leistung')) lines.push('Leistung: ' + g('leistung'));
      if (g('name')) lines.push('Name: ' + g('name'));
      if (g('telefon')) lines.push('Telefon: ' + g('telefon'));
      if (g('ort')) lines.push('Ort: ' + g('ort'));
      if (g('nachricht')) { lines.push(''); lines.push(g('nachricht')); }
      return lines.join('\n');
    }
    function valid() {
      var ok = form.elements['name'].value.trim() && form.elements['telefon'].value.trim();
      var err = form.querySelector('.err');
      if (err) err.style.display = ok ? 'none' : 'block';
      return ok;
    }
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    form.querySelectorAll('[data-send]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!valid()) return;
        var t = encodeURIComponent(text());
        if (btn.getAttribute('data-send') === 'wa') {
          window.open('https://wa.me/' + form.getAttribute('data-wa') + '?text=' + t, '_blank', 'noopener');
        } else {
          window.location.href = 'mailto:' + form.getAttribute('data-mail') +
            '?subject=' + encodeURIComponent('Anfrage ' + (form.elements['leistung'].value || 'Garten')) + '&body=' + t;
        }
      });
    });
  });

  // Scroll-Fortschritt, Parallax im Bildband, schwebender Anfrage-Knopf
  var prog = d.createElement('div'); prog.className = 'prog'; d.body.appendChild(prog);
  var qbg = d.querySelector('.quote-bg'), fab = d.querySelector('.fab');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var tick = false;
  function frame() {
    tick = false;
    var max = d.documentElement.scrollHeight - window.innerHeight;
    prog.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
    if (qbg && !reduce) {
      var r = qbg.parentNode.getBoundingClientRect();
      if (r.bottom > 0 && r.top < window.innerHeight) {
        var t = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
        qbg.style.transform = 'translate3d(0,' + (t * -8).toFixed(2) + '%,0)';
      }
    }
    if (fab) {
      var form = d.querySelector('form.anfrage'), near = false;
      if (form) { var fr = form.getBoundingClientRect(); near = fr.top < window.innerHeight && fr.bottom > 0; }
      fab.classList.toggle('on', window.scrollY > 700 && !near && window.scrollY < max - 500);
    }
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();

  // Lightbox für die Referenzen
  var links = [].slice.call(d.querySelectorAll('a.lb'));
  if (links.length) {
    var box = d.createElement('div'); box.className = 'lbx'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Bildansicht');
    box.innerHTML = '<button class="x" aria-label="Schließen">&times;</button><button class="pv" aria-label="Vorheriges Bild">&#8592;</button><img alt=""><button class="nx" aria-label="Nächstes Bild">&#8594;</button><p></p>';
    d.body.appendChild(box);
    var im = box.querySelector('img'), cap = box.querySelector('p'), cur = 0, last = null;
    function show(i) {
      cur = (i + links.length) % links.length;
      im.src = links[cur].getAttribute('href');
      im.alt = cap.textContent = links[cur].getAttribute('data-cap') || '';
    }
    function close() { box.classList.remove('on'); d.body.style.overflow = ''; if (last) last.focus(); }
    links.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        e.preventDefault(); last = a; show(i); box.classList.add('on'); d.body.style.overflow = 'hidden'; box.querySelector('.x').focus();
      });
    });
    box.querySelector('.x').addEventListener('click', close);
    box.querySelector('.pv').addEventListener('click', function () { show(cur - 1); });
    box.querySelector('.nx').addEventListener('click', function () { show(cur + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    d.addEventListener('keydown', function (e) {
      if (!box.classList.contains('on')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
  }

  // Jahr im Footer
  var y = d.getElementById('jahr');
  if (y) y.textContent = new Date().getFullYear();
})();
