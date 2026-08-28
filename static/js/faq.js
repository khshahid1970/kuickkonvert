(function () {
  // Single-open FAQ accordion: opening one question closes any other that
  // was already open, so the page can never grow past "one extra answer's
  // height" no matter how many items a visitor clicks through. Built on
  // the native <details>/<summary> toggle event rather than a hover-popup
  // or tooltip, so keyboard and screen-reader users -- and anyone on a
  // touch device, where "hover" has no real equivalent -- get the same
  // behavior as a mouse user.
  var items = document.querySelectorAll(".faq-item");
  if (!items.length) return;

  items.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      items.forEach(function (other) {
        if (other !== item) other.open = false;
      });
    });
  });
})();
