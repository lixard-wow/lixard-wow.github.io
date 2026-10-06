(function () {
  var KEY = "lixard-theme";
  var THEMES = ["classic", "workbench", "ledger"];
  var root = document.documentElement;

  function current() {
    var theme = root.getAttribute("data-theme");
    return THEMES.indexOf(theme) >= 0 ? theme : "classic";
  }

  function paint() {
    var theme = current();
    var buttons = document.querySelectorAll("[data-theme-pick]");
    for (var i = 0; i < buttons.length; i++) {
      var on = buttons[i].getAttribute("data-theme-pick") === theme;
      buttons[i].setAttribute("aria-pressed", on ? "true" : "false");
    }
  }

  function pick(theme) {
    root.setAttribute("data-theme", theme);
    try { localStorage.setItem(KEY, theme); } catch (e) {}
    paint();
  }

  var buttons = document.querySelectorAll("[data-theme-pick]");
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function () {
      pick(this.getAttribute("data-theme-pick"));
    });
  }
  paint();
})();
