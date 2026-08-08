// MapLibre renderer for Civic Data, Explained — token-free.
// Finds [data-maplibre-geojson] containers, fetches the source's own
// keyless GeoJSON (FeatureServer query / SODA endpoint), renders with
// MapLibre GL + a free OSM raster basemap. No Mapbox token, no iframes,
// no org-gated viewers (the OKC fix: render THEIR data on OUR page).
(function () {
  var containers = document.querySelectorAll("[data-maplibre-geojson]");
  if (!containers.length) return;

  function loadScript(src, cb) {
    var s = document.createElement("script");
    s.src = src;
    s.onload = cb;
    document.head.appendChild(s);
  }

  loadScript("https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js", function () {
    containers.forEach(function (el) {
      var url = el.getAttribute("data-maplibre-geojson");
      var title = el.getAttribute("data-maplibre-title") || "Live data map";
      var color = el.getAttribute("data-maplibre-color") || "#1f77b4";

      fetch(url)
        .then(function (r) { return r.json(); })
        .then(function (geojson) {
          var fc = geojson.type === "FeatureCollection" ? geojson
            : { type: "FeatureCollection", features: geojson.features || [geojson] };
          if (!fc.features || !fc.features.length) {
            el.innerHTML = '<p style="padding:1rem;font-size:13px;color:#666">No features returned from the source service.</p>';
            return;
          }
          var map = new maplibregl.Map({
            container: el,
            style: {
              version: 8,
              sources: {
                osm: { type: "raster", tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"], tileSize: 256, attribution: "© OpenStreetMap contributors" },
                data: { type: "geojson", data: fc }
              },
              layers: [
                { id: "osm", type: "raster", source: "osm" },
                { id: "data-fill", type: "fill", source: "data", paint: { "fill-color": color, "fill-opacity": 0.35 }, filter: ["==", ["geometry-type"], "Polygon"] },
                { id: "data-line", type: "line", source: "data", paint: { "line-color": color, "line-width": 1.5 } },
                { id: "data-point", type: "circle", source: "data", paint: { "circle-color": color, "circle-radius": 4 } }
              ]
            },
            attributionControl: { compact: true }
          });
          map.on("load", function () {
            try {
              var b = map.getSource("data").getBounds ? null : null;
              var coords = [];
              fc.features.forEach(function (f) {
                if (!f.geometry) return;
                if (f.geometry.type === "Point") coords.push(f.geometry.coordinates);
                else if (f.geometry.coordinates) flattenCoords(f.geometry.coordinates, coords);
              });
              if (coords.length) {
                var lons = coords.map(function (c) { return c[0]; });
                var lats = coords.map(function (c) { return c[1]; });
                map.fitBounds([[Math.min.apply(null, lons), Math.min.apply(null, lats)],
                              [Math.max.apply(null, lons), Math.max.apply(null, lats)]], { padding: 30 });
              }
            } catch (e) { /* fit-bounds best-effort */ }
          });
        })
        .catch(function (err) {
          el.innerHTML = '<p style="padding:1rem;font-size:13px;color:#b00">Map failed to load: ' + err.message + '</p>';
        });
    });
  });

  function flattenCoords(coords, out) {
    // handles Polygon/MultiPolygon/LineString nesting
    if (typeof coords[0] === "number") { out.push(coords); return; }
    coords.forEach(function (c) { flattenCoords(c, out); });
  }
})();
