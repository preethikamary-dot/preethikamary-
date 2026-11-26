// Renders the HTML files produced by build.py into print PDFs and images.
// Usage: node render.js build/jobs.json
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  for (const j of jobs) {
    const url = 'file://' + path.resolve(j.html);
    if (j.type === 'pdf') {
      const page = await browser.newPage();
      await page.goto(url, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      await page.pdf({
        path: j.out,
        width: j.width + 'in',
        height: j.height + 'in',
        printBackground: true,
        margin: { top: 0, right: 0, bottom: 0, left: 0 },
        preferCSSPageSize: true,
      });
      await page.close();
    } else {
      const page = await browser.newPage({
        viewport: { width: j.vw, height: j.vh },
        deviceScaleFactor: j.scale || 1,
      });
      await page.goto(url, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      const opts = { path: j.out, fullPage: false };
      if (j.out.endsWith('.jpg')) { opts.type = 'jpeg'; opts.quality = 92; }
      if (j.transparent) opts.omitBackground = true;
      await page.screenshot(opts);
      await page.close();
    }
    console.log('wrote', j.out);
  }
  await browser.close();
})();
