// landing/main.js: general page logic for landing/index.html.
(function () {
  "use strict";

  // ---- iframe-aware link handling ----
  // When embedded in an iframe, links open in a new tab; standalone, they
  // navigate normally in the same tab.
  function is_embedded() {
    try {
      return window.self !== window.top;
    } catch (e) {
      // cross-origin parent access throws, which itself implies embedding
      return true;
    }
  }

  if (is_embedded()) {
    var links = document.querySelectorAll("a[href]");
    for (var i = 0; i < links.length; i++) {
      links[i].target = "_blank";
      links[i].rel = "noopener noreferrer";
    }
  }

  // ---- interactive interface preview (the mockup in the hero section) ----
  var app = document.getElementById("app");
  if (!app) return;

  // List / Grid switch in the bottom bar of the preview.
  var view_buttons = app.querySelectorAll("[data-view]");
  function set_view(view) {
    app.setAttribute("data-view", view);
    for (var j = 0; j < view_buttons.length; j++) {
      var active = view_buttons[j].getAttribute("data-view") === view;
      view_buttons[j].classList.toggle("on", active);
      view_buttons[j].setAttribute("aria-pressed", active ? "true" : "false");
    }
  }
  for (var b = 0; b < view_buttons.length; b++) {
    view_buttons[b].addEventListener("click", function (event) {
      set_view(event.currentTarget.getAttribute("data-view"));
    });
  }

  // A single click on an unread count marks the feed as read, as in NewsBlurMod itself.
  var badges = app.querySelectorAll(".badge");
  var unread_total = app.querySelector("[data-unread-total]");
  function mark_read(badge) {
    var count = parseInt(badge.textContent, 10) || 0;
    if (unread_total) {
      unread_total.textContent = Math.max(0, parseInt(unread_total.textContent, 10) - count);
    }
    if (badge.hasAttribute("data-current")) {
      var unread_rows = app.querySelectorAll(".story.unread");
      for (var r = 0; r < unread_rows.length; r++) unread_rows[r].classList.remove("unread");
    }
    badge.remove();
  }
  for (var k = 0; k < badges.length; k++) {
    badges[k].addEventListener("click", function (event) {
      mark_read(event.currentTarget);
    });
  }
})();
