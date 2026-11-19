// Release 7 GPC / Consent Mode / AdSense deployment gate (adviser review, 12 Nov 2026).
// Run: node tests/test_release7_gpc_browser.js  (Flask app on 127.0.0.1:5055, or KK_BASE=...)
// Layers checked, as the adviser listed them:
//   1. Advertising code: no AdSense or other ad-network request.
//   2. GPC detection: navigator.globalPrivacyControl AND the Sec-GPC: 1 header.
//   3. Consent Mode: ad_storage, ad_user_data and ad_personalization end "denied".
//   4. Cookie settings: Advertising cannot be enabled while GPC applies.
// Scenarios: GPC before opening the site, outside and inside the consent regions,
// stored advertising consent from before GPC, navigation, direct tool pages, refresh.
const { chromium } = require('playwright');
const BASE = process.env.KK_BASE || 'http://127.0.0.1:5055';
const AD_HOSTS = /googlesyndication\.com|doubleclick\.net|googleadservices\.com|adservice\.google\.|launchnest\.io/;
const GPC_INIT = () => Object.defineProperty(Navigator.prototype, 'globalPrivacyControl', { get: () => true, configurable: true });

function finalAdConsent(dataLayer) {
  // Replays gtag('consent', 'default'|'update', {...}) in order (no region filter = applies everywhere).
  const st = {};
  for (const a of dataLayer) {
    if (a && a[0] === 'consent' && a[2] && !a[2].region) Object.assign(st, a[2]);
  }
  return { ad_storage: st.ad_storage, ad_user_data: st.ad_user_data, ad_personalization: st.ad_personalization };
}
function configuredIds(dataLayer) {
  return dataLayer.filter(a => a && a[0] === 'config').map(a => a[1]);
}
async function visit(ctx, path, opts = {}) {
  const page = await ctx.newPage();
  const reqs = []; page.on('request', r => reqs.push(r.url()));
  await page.goto(BASE + path, { waitUntil: 'load' });
  if (opts.before) await opts.before(page);
  await page.mouse.wheel(0, 1500);
  await page.waitForTimeout(opts.wait || 4500);
  const dl = await page.evaluate(() => (window.dataLayer || []).map(x => Array.from(x)));
  return { page, reqs, dl };
}

(async () => {
  const browser = await chromium.launch();
  const results = []; let failures = 0;
  const check = (name, ok, detail) => { results.push({ name, ok, detail }); if (!ok) failures++; };

  // 1. US, GPC from the browser only, two pages (navigation) + refresh
  {
    const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': 'US' } });
    await ctx.addInitScript(GPC_INIT);
    for (const path of ['/', '/tools/word-to-pdf', '/tools/merge-pdf']) {
      const { page, reqs, dl } = await visit(ctx, path);
      const c = finalAdConsent(dl);
      check(`US navigator-GPC ${path}: no ad requests`, !reqs.some(u => AD_HOSTS.test(u)), reqs.filter(u => AD_HOSTS.test(u)));
      check(`US navigator-GPC ${path}: consent denied`, c.ad_storage === 'denied' && c.ad_user_data === 'denied' && c.ad_personalization === 'denied', c);
      check(`US navigator-GPC ${path}: Google Ads tag not configured`, !configuredIds(dl).includes('AW-18473004328'), configuredIds(dl));
      await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(1500);
      const dl2 = await page.evaluate(() => (window.dataLayer || []).map(x => Array.from(x)));
      check(`US navigator-GPC ${path}: after refresh still denied`, finalAdConsent(dl2).ad_storage === 'denied' && !configuredIds(dl2).includes('AW-18473004328'), finalAdConsent(dl2));
      await page.close();
    }
    await ctx.close();
  }
  // 2. US, GPC from the header only (server side)
  {
    const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': 'US', 'Sec-GPC': '1' } });
    const { reqs, dl } = await visit(ctx, '/tools/pdf-to-word');
    const c = finalAdConsent(dl);
    check('US Sec-GPC header: no ad requests', !reqs.some(u => AD_HOSTS.test(u)), reqs.filter(u => AD_HOSTS.test(u)));
    check('US Sec-GPC header: consent denied, no Ads tag', c.ad_storage === 'denied' && !configuredIds(dl).includes('AW-18473004328'), { c, ids: configuredIds(dl) });
    await ctx.close();
  }
  // 3. Control: US without GPC -> Ads tag configured, still no AdSense (switched off)
  {
    const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': 'US' } });
    const { reqs, dl } = await visit(ctx, '/tools/word-to-pdf');
    check('US no GPC (control): Ads tag configured', configuredIds(dl).includes('AW-18473004328'), configuredIds(dl));
    check('US no GPC (control): no AdSense request', !reqs.some(u => /googlesyndication\.com/.test(u)), null);
    await ctx.close();
  }
  // 4. DE (consent region) + GPC: banner, Advertising locked off, "Accept all" grants Analytics only
  for (const cc of ['DE', 'GB', 'CH', 'GI', 'XX']) {
    const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': cc } });
    await ctx.addInitScript(GPC_INIT);
    const { page } = await visit(ctx, '/tools/jpg-to-pdf', { wait: 800 });
    await page.click('#consent-choose');
    const locked = await page.evaluate(() => { const d = document.getElementById('consent-advertising'); return { disabled: d.disabled, checked: d.checked }; });
    const note = await page.locator('#consent-gpc-note').isVisible();
    check(`${cc} GPC: Advertising switch locked off`, locked.disabled && !locked.checked, locked);
    check(`${cc} GPC: GPC note shown`, note, note);
    await page.click('#consent-accept');
    await page.waitForTimeout(2500);
    const rec = await page.evaluate(() => JSON.parse(localStorage.getItem('kk_consent')));
    const dl = await page.evaluate(() => (window.dataLayer || []).map(x => Array.from(x)));
    check(`${cc} GPC: Accept all stores advertising=false`, rec && rec.analytics === true && rec.advertising === false, rec);
    check(`${cc} GPC: consent denied, no Ads tag`, finalAdConsent(dl).ad_storage === 'denied' && !configuredIds(dl).includes('AW-18473004328'), { c: finalAdConsent(dl), ids: configuredIds(dl) });
    await ctx.close();
  }
  // 5. DE: advertising accepted BEFORE GPC, then GPC switched on -> earlier "yes" not used
  {
    const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': 'DE' } });
    const p1 = await ctx.newPage();
    await p1.goto(BASE + '/tools/word-to-pdf', { waitUntil: 'load' });
    await p1.click('#consent-accept'); await p1.waitForTimeout(1500);
    const before = await p1.evaluate(() => JSON.parse(localStorage.getItem('kk_consent')));
    await p1.close();
    await ctx.addInitScript(GPC_INIT);
    const { page, reqs, dl } = await visit(ctx, '/tools/merge-pdf');
    const cur = await page.evaluate(() => window.__kkConsent.current());
    check('DE stored yes then GPC: stored record had advertising=true', before && before.advertising === true, before);
    check('DE stored yes then GPC: advertising now off', cur && cur.advertising === false, cur);
    check('DE stored yes then GPC: consent denied, no Ads tag', finalAdConsent(dl).ad_storage === 'denied' && !configuredIds(dl).includes('AW-18473004328'), { c: finalAdConsent(dl), ids: configuredIds(dl) });
    check('DE stored yes then GPC: no ad requests', !reqs.some(u => AD_HOSTS.test(u)), reqs.filter(u => AD_HOSTS.test(u)));
    await ctx.close();
  }

  console.log(JSON.stringify(results, null, 1));
  console.log(failures ? `FAILURES: ${failures} of ${results.length}` : `ALL PASSED (${results.length})`);
  await browser.close();
  process.exit(failures ? 1 : 0);
})();
