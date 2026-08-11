// Section topic filter — filters .card elements by data-category.
(function () {
  var grid = document.querySelector(".card-grid");
  var bar = document.querySelector(".section-filter");
  if (!grid || !bar) return;
  var cards = grid.querySelectorAll(".card");
  var btns = bar.querySelectorAll(".filter-btn");
  btns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-filter");
      btns.forEach(function (b) { b.classList.toggle("active", b === btn); });
      cards.forEach(function (card) {
        var c = card.getAttribute("data-category") || "";
        card.style.display = (f === "all" || c === f) ? "" : "none";
      });
    });
  });
})();
