import { chromium } from '/runtime/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

const [action, input, output, width = '1280', height = '900'] = process.argv.slice(2);
if (!['screenshot', 'eval'].includes(action) || !input || !output) {
  console.log('Usage: node /tools/browser.mjs screenshot input.html|input.svg|input.mmd output.png [width height]\n       node /tools/browser.mjs eval input.html page-function.js\nThe eval file contains an async (page) => ... Playwright function. Network is unavailable.');
  process.exit(action === 'help' ? 0 : 1);
}
const browser = await chromium.launch({executablePath: '/runtime/chromium/chrome', headless: true, args: ['--no-sandbox']});
try {
  const page = await browser.newPage({viewport: {width: Number(width), height: Number(height)}});
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.route('**/*', route => /^(file:|data:|about:|blob:)/.test(route.request().url()) ? route.continue() : route.abort());
  if (input.endsWith('.mmd')) {
    await page.setContent('<!doctype html><meta charset="utf-8"><style>body{margin:24px;font-family:sans-serif}svg{max-width:none!important}</style><div id="diagram"></div>');
    await page.addScriptTag({path: '/tools/mermaid.min.js'});
    const source = await fs.readFile(input, 'utf8');
    await page.evaluate(async source => {
      mermaid.initialize({startOnLoad: false, securityLevel: 'strict'});
      const {svg} = await mermaid.render('diagram-output', source);
      document.querySelector('#diagram').innerHTML = svg;
      const element = document.querySelector('#diagram svg');
      const box = element.viewBox.baseVal;
      element.setAttribute('width', box.width);
      element.setAttribute('height', box.height);
      element.style.maxWidth = 'none';
    }, source);
  } else {
    await page.goto(pathToFileURL(input).href);
  }
  await page.evaluate(async () => {
    await document.fonts.ready;
    const animations = document.getAnimations().filter(a => a.effect?.getComputedTiming().iterations !== Infinity);
    await Promise.race([Promise.all(animations.map(a => a.finished.catch(() => {}))), new Promise(r => setTimeout(r, 2500))]);
  });
  if (action === 'eval') {
    const code = await fs.readFile(output, 'utf8');
    const fn = (0, eval)(`(${code})`);
    console.log(JSON.stringify({result: await fn(page), errors}));
  } else {
    const standaloneSvg = await page.evaluate(() => document.documentElement.localName === 'svg');
    if (standaloneSvg) {
      await page.locator(':root').screenshot({path: output});
    } else {
      await page.screenshot({path: output, fullPage: true});
    }
    const metrics = await page.evaluate(() => ({viewport: innerWidth, scrollWidth: document.documentElement.scrollWidth, text: document.body?.innerText ?? document.documentElement.textContent}));
    console.log(JSON.stringify({output, errors, ...metrics}));
  }
} finally {
  await browser.close();
}
