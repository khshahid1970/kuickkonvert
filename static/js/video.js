// Release 7, WP8: click-to-play YouTube videos (lawyer's advice, 10 Nov 2026).
// Nothing is requested from YouTube or Google until the visitor presses the
// button; then the player loads from youtube-nocookie.com
// (privacy-enhanced mode). Not used for EEA/UK/CH visitors, who get a link.
(function () {
  "use strict";
  var ID = /^[A-Za-z0-9_-]{11}$/;
  document.querySelectorAll(".kk-video[data-yt]").forEach(function (box) {
    var btn = box.querySelector(".kk-video-play");
    if (!btn) { return; }
    btn.addEventListener("click", function () {
      var id = box.getAttribute("data-yt");
      if (!ID.test(id)) { return; }
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0&playsinline=1";
      f.title = box.getAttribute("data-title") || "KuickKonvert video";
      f.allow = "autoplay; encrypted-media; picture-in-picture";
      f.setAttribute("allowfullscreen", "");
      f.width = "360";
      f.height = "640";
      f.className = "kk-video-frame";
      btn.replaceWith(f);
    });
  });
})();
