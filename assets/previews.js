document.querySelectorAll("[data-group]").forEach(function (group) {
  var targets = document.querySelectorAll(group.getAttribute("data-group"));
  group.querySelectorAll("button[data-set]").forEach(function (button) {
    button.addEventListener("click", function () {
      var attr = button.getAttribute("data-set");
      var value = button.getAttribute("data-value");
      targets.forEach(function (target) { target.setAttribute(attr, value); });
      group.querySelectorAll('button[data-set="' + attr + '"]').forEach(function (other) {
        other.setAttribute("aria-pressed", other === button ? "true" : "false");
      });
    });
  });
});
