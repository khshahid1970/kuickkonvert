/* KuickKonvert consent manager (added 11 Oct 2026).
 *
 * Loaded ONLY on pages served to visitors in the EEA, UK and Switzerland
 * (consent_required in app.py, from Cloudflare's CF-IPCountry). Everyone else
 * gets exactly the pages they got before this file existed.
 *
 * base.html runs first, in a nonce'd inline <script>: it defines gtag(), sets
 * ONE global Consent Mode default with all four storage types 'denied' (no
 * 'region' list -- see the comment in base.html for why), optionally
 * gtag('set','ads_data_redaction',true), and puts the settings from config.py
 * in window.__kkConsentConfig. This file then:
 *
 *  1. Reads the visitor's consent record from localStorage ("kk_consent"):
 *     {"v": CONSENT_VERSION, "ts": "YYYY-MM-DDTHH:MM:SSZ",
 *      "analytics": true|false, "advertising": true|false}
 *     Nothing else is stored; nothing is sent to our server. A missing,
 *     unreadable, old-format ('granted'/'denied'), other-version or expired
 *     record counts as "no choice" and the banner is shown.
 *  2. With a valid record: gtag('consent','update', <all four values>) and
 *     only then gtag('js') + gtag('config') -- so every consent value is in
 *     place before the Google tag can process anything -- and the tag is
 *     lazy-loaded as before (first tap/scroll/key, or 3 s after load).
 *     With no valid record: nothing is loaded; the banner waits for a choice.
 *  3. Analytics -> analytics_storage. Advertising -> ad_storage, ad_user_data,
 *     ad_personalization.
 *  4. CONSENT_MODE_TYPE "basic" (shipped default, 11 Oct 2026) is strict PER
 *     CATEGORY: gtag('config','G-K0VJLC113K') only with Analytics consent,
 *     gtag('config','AW-18473004328') only with Advertising consent, and the
 *     gtag.js library is requested only when at least one is granted (with
 *     the id of a granted product). With both refused nothing is requested
 *     from Google at all. "advanced": after any choice both IDs are
 *     configured and the library loads; refused categories stay 'denied'
 *     (Consent Mode then governs what Google may still receive).
 *     Each ID is configured at most once per page: a later upgrade (Cookie
 *     settings) configures the newly granted ID; a downgrade never configures
 *     anything and cannot un-configure an ID already configured on the page
 *     (consent for it is set to 'denied' instead).
 *  5. When a category ends up refused, that category's first-party Google
 *     cookies are deleted (only those names; host and parent domains,
 *     path=/): Analytics _ga, _ga_*; Advertising _gcl_au, _gcl_aw, _gcl_dc,
 *     _gcl_gb, _gcl_gs, _gcl_ag, _gac_*.
 *  6. LaunchNest badge: LAUNCHNEST_CONSENT_REGIONS "text_link" -> base.html
 *     renders a plain text link, nothing to do here; "advertising" -> the
 *     image's data-src is turned into src only with Advertising consent.
 *
 * Every storage access is wrapped in try/catch: if localStorage is blocked the
 * visitor's choice applies to the current page only and the banner is shown
 * again on the next page. ES5 on purpose (no build step, old browsers).
 */
(function () {
  'use strict';
  var cfg = window.__kkConsentConfig || {};
  var VERSION = String(cfg.version || '');
  var MAX_AGE_MS = (Number(cfg.maxAgeDays) > 0 ? Number(cfg.maxAgeDays) : 365) * 86400000;
  var MODE = cfg.mode === 'advanced' ? 'advanced' : 'basic';
  var BADGE = cfg.badge === 'advertising' ? 'advertising' : 'text_link';
  var KEY = 'kk_consent';
  var TAG_BASE = 'https://www.googletagmanager.com/gtag/js?id=';
  var GA_ID = 'G-K0VJLC113K';
  var ADS_ID = 'AW-18473004328';

  function gtag() {
    if (typeof window.gtag === 'function') window.gtag.apply(window, arguments);
  }

  // ---- consent record -----------------------------------------------------
  function readRecord() {
    var raw = null;
    try { raw = window.localStorage.getItem(KEY); } catch (e) { return { state: 'unavailable' }; }
    if (raw === null) return { state: 'none' };
    if (raw === 'granted' || raw === 'denied') return { state: 'legacy' };
    var rec;
    try { rec = JSON.parse(raw); } catch (e) { return { state: 'invalid' }; }
    if (!rec || typeof rec !== 'object' || typeof rec.analytics !== 'boolean' ||
        typeof rec.advertising !== 'boolean' || typeof rec.ts !== 'string') {
      return { state: 'invalid' };
    }
    if (rec.v !== VERSION) return { state: 'version' };
    var t = Date.parse(rec.ts);
    if (isNaN(t) || t > Date.now() + 86400000) return { state: 'invalid' };
    if (Date.now() - t > MAX_AGE_MS) return { state: 'expired' };
    return { state: 'valid', choice: { analytics: rec.analytics, advertising: rec.advertising } };
  }

  function writeRecord(choice) {
    var rec = {
      v: VERSION,
      ts: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
      analytics: !!choice.analytics,
      advertising: !!choice.advertising
    };
    try { window.localStorage.setItem(KEY, JSON.stringify(rec)); return true; } catch (e) { return false; }
  }

  function consentValues(choice) {
    var a = choice.analytics ? 'granted' : 'denied';
    var d = choice.advertising ? 'granted' : 'denied';
    return { 'analytics_storage': a, 'ad_storage': d, 'ad_user_data': d, 'ad_personalization': d };
  }

  // ---- Google tag -----------------------------------------------------------
  var configured = {};      // per tag ID: configured on this page?
  var jsSent = false;
  var loaded = false;
  var libraryId = null;     // the id= used for the gtag.js library request
  var lazyRegistered = false;

  // Tag IDs a choice allows: basic = only the granted products; advanced = both.
  function wantedIds(choice) {
    if (MODE === 'advanced') return [GA_ID, ADS_ID];
    var ids = [];
    if (choice.analytics) ids.push(GA_ID);
    if (choice.advertising) ids.push(ADS_ID);
    return ids;
  }

  function tagAllowed(choice) { return wantedIds(choice).length > 0; }

  // Configure every allowed ID not yet configured on this page (never undoes one).
  function configureFor(choice) {
    var ids = wantedIds(choice);
    for (var i = 0; i < ids.length; i++) {
      if (configured[ids[i]]) continue;
      if (!jsSent) { jsSent = true; gtag('js', new Date()); }
      configured[ids[i]] = true;
      gtag('config', ids[i]);
      if (!libraryId) libraryId = ids[i];
    }
  }

  function loadGoogleTag() {
    if (loaded || !libraryId) return;
    loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = TAG_BASE + libraryId;
    document.head.appendChild(s);
  }

  function registerLazyLoad() {
    if (lazyRegistered) return;
    lazyRegistered = true;
    ['pointerdown', 'keydown', 'touchstart', 'scroll'].forEach(function (ev) {
      window.addEventListener(ev, loadGoogleTag, { once: true, passive: true });
    });
    window.addEventListener('load', function () { setTimeout(loadGoogleTag, 3000); });
  }

  // ---- first-party cookies ---------------------------------------------------
  var ADS_NAMES = ['_gcl_au', '_gcl_aw', '_gcl_dc', '_gcl_gb', '_gcl_gs', '_gcl_ag'];
  function isAnalyticsCookie(n) { return n === '_ga' || n.indexOf('_ga_') === 0; }
  function isAdsCookie(n) { return ADS_NAMES.indexOf(n) !== -1 || n.indexOf('_gac_') === 0; }

  function deleteCookies(matches) {
    var names = [];
    try {
      names = document.cookie.split(';').map(function (x) {
        return x.split('=')[0].trim();
      }).filter(function (n) { return n && matches(n); });
    } catch (e) { return; }
    if (!names.length) return;
    var parts = location.hostname.split('.');
    var domains = [];
    for (var i = 0; i <= parts.length - 2; i++) {
      var d = parts.slice(i).join('.');
      domains.push(d, '.' + d);
    }
    var gone = '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    names.forEach(function (n) {
      try {
        document.cookie = n + gone;
        domains.forEach(function (dm) { document.cookie = n + gone + '; domain=' + dm; });
      } catch (e) { /* ignore */ }
    });
  }

  // ---- LaunchNest badge (only in "advertising" mode) -------------------------
  function applyBadge(choice) {
    if (BADGE !== 'advertising') return;
    var el = document.getElementById('launchnest-badge');
    if (!el || !el.getAttribute('data-src')) return;
    if (choice && choice.advertising) {
      if (!el.getAttribute('src')) el.setAttribute('src', el.getAttribute('data-src'));
    } else if (el.getAttribute('src')) {
      el.removeAttribute('src');
    }
  }

  // ---- state + choices ---------------------------------------------------------
  var record = readRecord();
  var current = record.state === 'valid' ? record.choice : null;
  var opener = null;

  if (current) {
    gtag('consent', 'update', consentValues(current));
    if (tagAllowed(current)) { configureFor(current); registerLazyLoad(); }
  }

  function choose(choice) {
    current = { analytics: !!choice.analytics, advertising: !!choice.advertising };
    var stored = writeRecord(current);
    gtag('consent', 'update', consentValues(current));   // before config / tag load
    if (!current.analytics) deleteCookies(isAnalyticsCookie);
    if (!current.advertising) deleteCookies(isAdsCookie);
    applyBadge(current);
    if (tagAllowed(current)) { configureFor(current); loadGoogleTag(); }
    closeBanner();
    return stored;
  }

  // ---- banner UI -------------------------------------------------------------------
  function $(id) { return document.getElementById(id); }

  function setPanel(open) {
    var panel = $('consent-panel');
    var btn = $('consent-choose');
    if (!panel) return;
    panel.hidden = !open;
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      var a = $('consent-analytics');
      var d = $('consent-advertising');
      if (a) a.checked = !!(current && current.analytics);
      if (d) d.checked = !!(current && current.advertising);
    }
  }

  function openBanner(withPanel, focusTarget) {
    var b = $('consent-banner');
    if (!b) return;
    b.hidden = false;
    setPanel(!!withPanel);
    if (focusTarget) focusTarget.focus();
  }

  function closeBanner() {
    var b = $('consent-banner');
    if (!b) return;
    var hadFocus = b.contains(document.activeElement);
    b.hidden = true;
    setPanel(false);
    if (hadFocus && opener && document.body.contains(opener)) opener.focus();
    opener = null;
  }

  function wire() {
    var b = $('consent-banner');
    applyBadge(current);
    var on = function (id, fn) { var el = $(id); if (el) el.addEventListener('click', fn); };
    on('consent-accept', function () { choose({ analytics: true, advertising: true }); });
    on('consent-reject', function () { choose({ analytics: false, advertising: false }); });
    on('consent-choose', function () {
      var panel = $('consent-panel');
      var open = panel && panel.hidden;
      setPanel(open);
      if (open && $('consent-analytics')) $('consent-analytics').focus();
    });
    on('consent-save', function () {
      var a = $('consent-analytics');
      var d = $('consent-advertising');
      choose({ analytics: !!(a && a.checked), advertising: !!(d && d.checked) });
    });
    on('cookie-settings', function (ev) {
      opener = ev.currentTarget;
      openBanner(true, b);
    });
    if (!current) openBanner(false, null);
  }

  // Read-only hook: static/js/main.js reads mode + current() to decide which
  // events it may send in basic mode; the site's tests read it too. Frozen,
  // and current() returns a copy, so other code can't change the choice
  // through it.
  window.__kkConsent = Object.freeze({
    state: record.state,
    mode: MODE,
    current: function () { return current ? { analytics: current.analytics, advertising: current.advertising } : null; }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else {
    wire();
  }
})();
