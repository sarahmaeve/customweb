/* Client-side ledger behaviour for the Consulting Occultist index:
   live text search with a violet highlighter, a date-range filter (relative
   presets or an explicit year range), and a newest/oldest sort toggle.

   The pure helpers below are exported for Node tests (tools/test_app.js); the
   DOM wiring runs only in a browser. */

'use strict';

function escapeHtml(s) {
  return s.replace(/[&<>]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c];
  });
}

// Wrap every case-insensitive occurrence of `needle` in `raw` with <mark>,
// escaping the surrounding text. Returns an HTML string.
function markHTML(raw, needle) {
  if (!needle) return escapeHtml(raw);
  var low = raw.toLowerCase(), out = '', i = 0, n = needle.length, k;
  while ((k = low.indexOf(needle, i)) !== -1) {
    out += escapeHtml(raw.slice(i, k)) + '<mark>' + escapeHtml(raw.slice(k, k + n)) + '</mark>';
    i = k + n;
  }
  return out + escapeHtml(raw.slice(i));
}

// ISO date (YYYY-MM-DD) `days` before `now` (defaults to today). UTC, so it is
// stable across time zones and testable.
function isoDaysAgo(days, now) {
  var d = now ? new Date(now.getTime()) : new Date();
  d.setUTCDate(d.getUTCDate() - days);
  return d.toISOString().slice(0, 10);
}

// Is ISO date `iso` within [min, max]? An empty bound is open; an empty date
// matches only when the range is fully open.
function inRange(iso, min, max) {
  if (!iso) return !min && !max;
  if (min && iso < min) return false;
  if (max && iso > max) return false;
  return true;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { escapeHtml: escapeHtml, markHTML: markHTML, isoDaysAgo: isoDaysAgo, inRange: inRange };
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLedger);
  } else {
    initLedger();
  }
}

function initLedger() {
  var q = document.getElementById('q'),
      list = document.getElementById('list'),
      count = document.getElementById('count'),
      empty = document.getElementById('empty'),
      sortBtn = document.getElementById('sort'),
      presets = document.getElementById('presets'),
      fromSel = document.getElementById('from'),
      toSel = document.getElementById('to'),
      entries = [].slice.call(list.querySelectorAll('.entry')),
      TOTAL = entries.length,
      asc = false,                 // false = newest first (default)
      rangeMin = '', rangeMax = ''; // inclusive ISO bounds; '' = unbounded

  // cache the title's plain text so highlighting can rebuild it (segments carry
  // their own data-raw from the server)
  entries.forEach(function (e) {
    var t = e.querySelector('.title');
    t.setAttribute('data-raw', t.textContent);
  });

  function applyMarks(e, needle) {
    var t = e.querySelector('.title'), seg = e.querySelector('.seg');
    t.innerHTML = markHTML(t.getAttribute('data-raw'), needle);
    seg.innerHTML = markHTML(seg.getAttribute('data-raw'), needle);
  }

  function highlightPreset(kind) {
    [].forEach.call(presets.children, function (b) {
      b.classList.toggle('on', b.dataset.preset === kind);
    });
  }

  function run() {
    var s = q.value.trim().toLowerCase(), shown = 0;
    entries.forEach(function (e) {
      var hit = (!s || e.getAttribute('data-text').indexOf(s) !== -1)
                && inRange(e.getAttribute('data-iso'), rangeMin, rangeMax);
      e.style.display = hit ? '' : 'none';
      if (hit) { shown++; applyMarks(e, s); }
    });
    empty.style.display = shown ? 'none' : 'block';
    count.textContent = (shown === TOTAL) ? (TOTAL + ' entries') : (shown + ' of ' + TOTAL + ' entries');
  }

  function setPreset(kind) {
    fromSel.value = ''; toSel.value = '';       // presets and year range are exclusive
    if (kind === 'month') { rangeMin = isoDaysAgo(31); rangeMax = ''; }
    else if (kind === 'year') { rangeMin = isoDaysAgo(365); rangeMax = ''; }
    else { rangeMin = ''; rangeMax = ''; }
    highlightPreset(kind);
    run();
  }

  function setYearRange() {
    var f = fromSel.value, t = toSel.value;
    rangeMin = f ? f + '-01-01' : '';
    rangeMax = t ? t + '-12-31' : '';
    highlightPreset((!f && !t) ? 'all' : null);  // only "All" lights up when unbounded
    run();
  }

  function resort() {
    var arr = entries.slice().sort(function (a, b) {
      var x = a.getAttribute('data-iso'), y = b.getAttribute('data-iso');
      return asc ? (x < y ? -1 : x > y ? 1 : 0) : (x < y ? 1 : x > y ? -1 : 0);
    });
    var frag = document.createDocumentFragment();
    arr.forEach(function (e) { frag.appendChild(e); });
    list.appendChild(frag);
  }

  q.addEventListener('input', run);
  sortBtn.addEventListener('click', function () {
    asc = !asc; resort();
    sortBtn.innerHTML = '<span class="arw" aria-hidden="true">' + (asc ? '&uarr;' : '&darr;') + '</span>'
                      + (asc ? 'Oldest first' : 'Newest first');
  });
  presets.addEventListener('click', function (ev) {
    var b = ev.target.closest('button');
    if (b) setPreset(b.dataset.preset);
  });
  fromSel.addEventListener('change', setYearRange);
  toSel.addEventListener('change', setYearRange);
}
