(function () {
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  function isOpen() {
    return nav.classList.contains("nav-open");
  }

  // F15: the open mobile menu is an overlay. Keep keyboard focus within the
  // toggle + its links while it is open (SC 2.4.3 / 2.4.11: focus must not fall
  // behind the overlay), allow Escape and an outside tap to close it, and
  // return focus to the toggle on close. Only engages on mobile, where
  // .nav-open is used; on desktop the menu is always visible and nav-open is
  // never set, so none of this runs.
  function focusables() {
    return [toggle].concat(
      Array.prototype.slice.call(nav.querySelectorAll("a"))
    );
  }

  function open() {
    nav.classList.add("nav-open");
    toggle.setAttribute("aria-expanded", "true");
    var links = nav.querySelectorAll("a");
    if (links.length) links[0].focus();
  }

  function close(returnFocus) {
    if (!isOpen()) return;
    nav.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    if (returnFocus) toggle.focus();
  }

  toggle.addEventListener("click", function () {
    if (isOpen()) {
      close(true);
    } else {
      open();
    }
  });

  // Close when a link is chosen (navigation / in-page anchor).
  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      close(false);
    });
  });

  // Escape closes and returns focus to the toggle; Tab is trapped while open.
  document.addEventListener("keydown", function (e) {
    if (!isOpen()) return;
    if (e.key === "Escape" || e.key === "Esc") {
      close(true);
      return;
    }
    if (e.key === "Tab") {
      var f = focusables();
      if (!f.length) return;
      var first = f[0];
      var last = f[f.length - 1];
      var active = document.activeElement;
      if (e.shiftKey && active === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && active === last) {
        e.preventDefault();
        first.focus();
      } else if (f.indexOf(active) === -1) {
        e.preventDefault();
        first.focus();
      }
    }
  });

  // An outside tap/click closes the menu (without stealing focus).
  document.addEventListener("click", function (e) {
    if (!isOpen()) return;
    if (nav.contains(e.target) || toggle.contains(e.target)) return;
    close(false);
  });
})();
