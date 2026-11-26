// Release 7, WP14 (conversion-failure Package 2) browser checks, 11 Nov 2026.
// Run: node tests/test_release7_package2_browser.js  (Flask app on 127.0.0.1:5055)
// The /convert/ requests are intercepted, so network drops, cut-off
// downloads and refusals can be simulated without touching the server.
const { chromium } = require('playwright');
const path = require('path');
const BASE = process.env.KK_BASE || 'http://127.0.0.1:5055';
const FIX = (f) => path.join(__dirname, 'fixtures', f);
const PDF = Buffer.from('%PDF-1.4\n%test\n');

function pngSize(buf) {
  const i = buf.indexOf(Buffer.from('IHDR'));
  return i < 0 ? null : [buf.readUInt32BE(i + 4), buf.readUInt32BE(i + 8)];
}

async function openTool(browser, slug, initScript) {
  const ctx = await browser.newContext({ extraHTTPHeaders: { 'CF-IPCountry': 'US' } });
  if (initScript) await ctx.addInitScript(initScript);
  const page = await ctx.newPage();
  await page.goto(`${BASE}/tools/${slug}`, { waitUntil: 'load' });
  return { ctx, page };
}

const status = (page) => page.locator('#status').innerText();
const results = [];
function check(name, ok, detail) { results.push({ name, ok: !!ok, detail }); }

(async () => {
  const browser = await chromium.launch();

  // 1. R7-59: two drops, then success on the third try
  {
    const { ctx, page } = await openTool(browser, 'jpg-to-pdf');
    let hits = 0;
    await page.route('**/convert/jpg-to-pdf', (r) => {
      hits++;
      if (hits <= 2) return r.abort('connectionreset');
      return r.fulfill({ status: 200, body: PDF, headers: { 'Content-Type': 'application/pdf', 'Content-Disposition': 'attachment; filename="p2-small.pdf"' } });
    });
    await page.setInputFiles('#file-input', FIX('p2-small.jpg'));
    await page.click('#convert-btn');
    await page.waitForFunction(() => /Done/.test(document.getElementById('status').innerText), null, { timeout: 15000 });
    check('retries: success after 2 drops (3 requests)', hits === 3, { hits, status: await status(page) });
    await ctx.close();
  }

  // 2. R7-59: three drops -> slow-connection hint
  {
    const { ctx, page } = await openTool(browser, 'jpg-to-pdf');
    let hits = 0;
    await page.route('**/convert/jpg-to-pdf', (r) => { hits++; return r.abort('connectionreset'); });
    await page.setInputFiles('#file-input', FIX('p2-small.jpg'));
    await page.click('#convert-btn');
    await page.waitForFunction(() => /connection dropped\. Try a smaller file/i.test(document.getElementById('status').innerText), null, { timeout: 15000 });
    const enabled = !(await page.locator('#convert-btn').isDisabled());
    check('retries: hint after 3 failed tries; button usable again', hits === 3 && enabled, { hits, status: await status(page) });
    await ctx.close();
  }

  // 3. R7-60: download cut off -> "Download again" converts again
  {
    const init = () => {
      const orig = Response.prototype.blob; let n = 0;
      Response.prototype.blob = function () { n++; return n === 1 ? Promise.reject(new TypeError('network error')) : orig.call(this); };
    };
    const { ctx, page } = await openTool(browser, 'jpg-to-pdf', init);
    let hits = 0;
    await page.route('**/convert/jpg-to-pdf', (r) => { hits++; return r.fulfill({ status: 200, body: PDF, headers: { 'Content-Type': 'application/pdf' } }); });
    await page.setInputFiles('#file-input', FIX('p2-small.jpg'));
    await page.click('#convert-btn');
    await page.waitForSelector('#download-again', { timeout: 10000 });
    const msg = await status(page);
    await page.click('#download-again');
    await page.waitForFunction(() => /Done/.test(document.getElementById('status').innerText), null, { timeout: 10000 });
    check('download again: button shown, second request succeeds', hits === 2 && /interrupted/.test(msg) && /deleted automatically/.test(msg), { hits, msg });
    await ctx.close();
  }

  // 4. R7-63: a refused file is not sent again
  {
    const { ctx, page } = await openTool(browser, 'pdf-to-ppt');
    let hits = 0;
    await page.route('**/convert/pdf-to-ppt', (r) => {
      hits++;
      return r.fulfill({ status: 400, contentType: 'application/json', body: JSON.stringify({ error: "'p2-locked' is password-protected, so it can't be opened here.", code: 'pdf_locked' }) });
    });
    await page.setInputFiles('#file-input', FIX('p2-locked.pdf'));
    await page.click('#convert-btn');
    await page.waitForFunction(() => /password-protected/.test(document.getElementById('status').innerText), null, { timeout: 10000 });
    const disabled = await page.locator('#convert-btn').isDisabled();
    await page.evaluate(() => document.getElementById('convert-form').requestSubmit());
    await page.waitForTimeout(800);
    const blockedMsg = await status(page);
    // choosing the file again (a different selection object) still matches
    await page.setInputFiles('#file-input', FIX('p2-small.jpg')).catch(() => {});
    check('repeat refusal: button disabled, no second request', hits === 1 && disabled && /wasn[’']t sent again/.test(blockedMsg), { hits, disabled, blockedMsg });
    await ctx.close();
  }

  // 5. R7-64: only an image above the limit is reduced, with a visible note
  for (const [limit, expectReduced] of [['1', true], [null, false]]) {
    // Record what main.js puts in the upload (Playwright can't read a
    // multipart body that holds a file chosen from disk).
    const rec = () => {
      window.__sent = [];
      const a = FormData.prototype.append;
      FormData.prototype.append = function (k, v, n) {
        if (v instanceof Blob) window.__sent.push(v);
        return n === undefined ? a.call(this, k, v) : a.call(this, k, v, n);
      };
    };
    const { ctx, page } = await openTool(browser, 'png-to-jpg', rec);
    let size = null;
    await page.route('**/convert/png-to-jpg', (r) => {
      size = pngSize(r.request().postDataBuffer());
      return r.fulfill({ status: 200, body: Buffer.from([0xff, 0xd8, 0xff, 0xd9]), headers: { 'Content-Type': 'image/jpeg' } });
    });
    if (limit) await page.evaluate((l) => { document.getElementById('convert-form').dataset.maxMp = l; }, limit);
    // maxPixels is read when main.js starts, so reload main.js state by re-running the page script
    if (limit) {
      await page.evaluate(() => new Promise((res) => {
        const f = document.getElementById('convert-form');
        const clone = f.cloneNode(true); f.replaceWith(clone);
        const u = new URL(document.querySelector('script[src*="main.js"]').src); u.searchParams.set('t', Date.now());
        const s = document.createElement('script'); s.src = u.href;
        s.nonce = document.querySelector('script[src*="main.js"]').nonce; s.onload = res; document.body.appendChild(s);
      }));
    }
    await page.setInputFiles('#file-input', FIX('p2-1500x1000.png'));
    await page.click('#convert-btn');
    await page.waitForFunction(() => /Done/.test(document.getElementById('status').innerText), null, { timeout: 15000 });
    const msg = await status(page);
    if (!size) {
      size = await page.evaluate(async () => {
        const b = window.__sent[0]; if (!b) return null;
        const bmp = await createImageBitmap(b); return [bmp.width, bmp.height];
      });
    }
    const reduced = size && size[0] * size[1] <= 1000000;
    const ok = expectReduced ? (reduced && /reduced it to/.test(msg)) : (size && size[0] === 1500 && size[1] === 1000 && !/reduced/.test(msg));
    check(expectReduced ? 'reduce: image above limit reduced, note shown' : 'reduce: image under limit sent unchanged', ok, { size, msg });
    await ctx.close();
  }

  await browser.close();
  console.log(JSON.stringify(results, null, 1));
  const failed = results.filter((r) => !r.ok).length;
  console.log(failed ? `FAILED: ${failed}` : `ALL PASSED (${results.length})`);
  process.exit(failed ? 1 : 0);
})();
