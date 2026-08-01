/* System A — live inquiry box. One component, driven entirely by data
   attributes on the form; queries the dataset's own ArcGIS FeatureServer. */
(function () {
  'use strict';
  document.querySelectorAll('.inquiry-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = form.querySelector('.inquiry-input').value.trim();
      var results = form.parentElement.querySelector('.inquiry-results');
      if (!q) { return; }
      results.hidden = false;
      results.innerHTML = '<p class="inquiry-status">Searching…</p>';

      var base = form.getAttribute('data-inquiry-url') || '';
      var search = form.getAttribute('data-inquiry-search') || '';
      var field = form.getAttribute('data-inquiry-field') || '';
      var extra = (form.getAttribute('data-inquiry-extra') || '').split('|').filter(Boolean);
      var query = base + (base.endsWith('/FeatureServer') ? '/0' : '') + '/query';

      var esc = q.replace(/'/g, "''");
      var params = new URLSearchParams();
      params.set('where', "UPPER(" + search + ") LIKE UPPER('%" + esc + "%')");
      params.set('f', 'geojson');
      params.set('outFields', [search, field].concat(extra).join(','));
      params.set('resultRecordCount', '6');

      fetch(query + '?' + params.toString())
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var feats = (data && data.features) || [];
          if (!feats.length) {
            results.innerHTML = '<p class="inquiry-status">No records found for “' + q +
              '”. Try a street name like “NW 23rd” or a fuller address.</p>';
            return;
          }
          var html = '<p class="inquiry-status">' + feats.length + ' record' +
            (feats.length > 1 ? 's' : '') + ' found:</p><ul class="inquiry-list">';
          feats.forEach(function (f) {
            var p = f.properties || f.attributes || {};
            var val = p[field] != null && p[field] !== '' ? p[field] : '—';
            var pieces = ['<strong>' + val + '</strong>'];
            extra.forEach(function (k) {
              if (p[k] != null && p[k] !== '') { pieces.push(k + ': ' + p[k]); }
            });
            html += '<li>' + pieces.join(' · ') + '</li>';
          });
          html += '</ul>';
          results.innerHTML = html;
        })
        .catch(function () {
          results.innerHTML = '<p class="inquiry-status">Lookup failed — the city service may be busy. Try again in a moment.</p>';
        });
    });
  });
})();
