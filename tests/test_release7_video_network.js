// Release 7 pre-release DevTools-style network test (lawyer's step 4).
// Run: node tests/test_release7_video_network.js  (Flask app on 127.0.0.1:5055)
const { chromium } = require('playwright');
const BASE = process.env.KK_BASE || 'http://127.0.0.1:5055';
const VIDEO_HOSTS = /youtube\.com|youtube-nocookie\.com|ytimg\.com|googlevideo\.com|ggpht\.com/;
const PAGES = ['/', '/tools', '/tools/word-to-pdf', '/tools/merge-pdf', '/privacy'];
// RE (Reunion, EU) and XX (Cloudflare: unknown) added 11 Nov 2026 for R7-72.
// GI added 12 Nov 2026 (final legal opinion, B2).
const COUNTRIES = ['DE', 'GB', 'RE', 'XX', 'GI', 'US', 'PK'];
(async () => {
  const browser = await chromium.launch();
  const results = []; let failures = 0;
  for (const cc of COUNTRIES) {
    for (const path of PAGES) {
      const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': cc } });
      const page = await ctx.newPage();
      const reqs = []; const cspErrors = [];
      page.on('request', r => reqs.push(r.url()));
      page.on('console', m => { if (/Content Security Policy|Refused to/.test(m.text())) cspErrors.push(m.text()); });
      await page.goto(BASE + path, { waitUntil: 'load' });
      await page.mouse.wheel(0, 2000); // scroll like a visitor; lazy images load
      await page.waitForTimeout(6000);  // longer than the delayed tag loader
      const external = [...new Set(reqs.filter(u => !u.startsWith(BASE)).map(u => new URL(u).host))];
      const videoBefore = reqs.filter(u => VIDEO_HOSTS.test(u));
      const hasButton = await page.locator('.kk-video-play').count();
      const hasLink = await page.locator('a.kk-video--link').count();
      const label = hasButton ? (await page.locator('.kk-video-label').first().innerText()) : null;
      let iframeSrc = null, videoAfter = [];
      if (hasButton) {
        const n = reqs.length;
        await page.locator('.kk-video-play').first().click();
        await page.waitForTimeout(2500);
        iframeSrc = await page.locator('iframe.kk-video-frame').first().getAttribute('src');
        videoAfter = [...new Set(reqs.slice(n).filter(u => VIDEO_HOSTS.test(u)).map(u => new URL(u).host))];
      }
      const consentRegion = ['DE', 'GB', 'RE', 'XX', 'GI'].includes(cc);
      // Evidence for the legal test protocol: cookies and web storage after load.
      const cookies = (await ctx.cookies()).map(c => `${c.domain} ${c.name}`);
      const storage = await page.evaluate(() => ({ local: Object.keys(localStorage), session: Object.keys(sessionStorage) }));
      const adsense = reqs.some(u => /pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js/.test(u));
      const gtagReq = reqs.some(u => /googletagmanager\.com\/gtag\/js/.test(u));
      const ok = videoBefore.length === 0 && cspErrors.length === 0 &&
        (path === '/privacy' || (consentRegion ? (hasLink === 1 && hasButton === 0) : (hasButton === 1 && hasLink === 0))) &&
        (consentRegion ? (external.length === 0 && !adsense) : (!adsense && gtagReq)) &&
        (!hasButton || (iframeSrc && iframeSrc.startsWith('https://www.youtube-nocookie.com/embed/')));
      if (!ok) failures++;
      results.push({ cc, path, ok, external_before_click: external, video_requests_before_click: videoBefore.length,
                     player_button: hasButton, link_only: hasLink, label, iframeSrc, video_hosts_after_click: videoAfter, adsense_requested: adsense, google_tag_requested: gtagReq, csp_errors: cspErrors.length, csp_messages: cspErrors.slice(0, 3), cookies, storage });
      await ctx.close();
    }
  }
  // Global Privacy Control: a US visitor whose browser sends Sec-GPC must not get AdSense.
  {
    const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': 'US', 'Sec-GPC': '1' } });
    const page = await ctx.newPage(); const reqs = [];
    page.on('request', r => reqs.push(r.url()));
    await page.goto(BASE + '/tools/word-to-pdf', { waitUntil: 'load' });
    await page.waitForTimeout(3000);
    const adsense = reqs.some(u => /adsbygoogle\.js/.test(u));
    if (adsense) failures++;
    results.push({ cc: 'US + Sec-GPC', path: '/tools/word-to-pdf', ok: !adsense, adsense_requested: adsense });
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(results, null, 1));
  console.log(failures ? `FAILED: ${failures}` : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})();
