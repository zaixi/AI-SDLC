async (page) => {
  const documentUrl = page.url();
  const blocked = [];
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  await page.route('**/*', route => {
    const request = route.request();
    const url = request.url();
    if (url === documentUrl || /^(data:|blob:|about:)/.test(url)) return route.continue();
    blocked.push({url, resourceType: request.resourceType()});
    return route.abort();
  });
  await page.reload();
  await page.evaluate(() => document.fonts.ready);
  const screenshot = `standalone-${page.viewportSize().width}.png`;
  await page.screenshot({path: '/review/' + screenshot, fullPage: true});
  return {blocked, errors, screenshot, text: await page.locator('body').innerText(),
    scrollWidth: await page.evaluate(() => document.documentElement.scrollWidth)};
}
