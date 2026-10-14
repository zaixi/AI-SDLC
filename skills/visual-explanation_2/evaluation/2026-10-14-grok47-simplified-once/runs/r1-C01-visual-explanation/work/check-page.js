module.exports = async (page) => {
  const result = {};
  for (const [name, w, h] of [['desk', 1280, 900], ['phone', 390, 844]]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('file:///work/answer.html', { waitUntil: 'load' });
    result[name] = await page.evaluate(() => {
      const doc = document.documentElement;
      const sc = document.querySelector('svg.scatter').closest('.diagram-container');
      const bars = document.querySelector('svg.bars').closest('.diagram-container');
      const sr = document.querySelector('svg.scatter').getBoundingClientRect();
      return {
        pageOverflow: doc.scrollWidth > doc.clientWidth + 2,
        scrollW: doc.scrollWidth,
        clientW: doc.clientWidth,
        scatterScrolls: sc.scrollWidth > sc.clientWidth + 2,
        barsScrolls: bars.scrollWidth > bars.clientWidth + 2,
        scatterW: Math.round(sr.width),
        h1: document.querySelector('h1').textContent,
        external: [...document.querySelectorAll('script, link, img')].map(n => n.src || n.href).filter(Boolean)
      };
    });
    await page.screenshot({ path: `/tmp/${name}.png`, fullPage: true });
  }
  return result;
};
