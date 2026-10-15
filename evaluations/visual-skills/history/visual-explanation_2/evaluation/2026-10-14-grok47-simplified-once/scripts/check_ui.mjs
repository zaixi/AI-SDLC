async (page) => {
  const requests = [];
  const dialogs = [];
  page.on('request', request => requests.push({url: request.url(), method: request.method()}));
  page.on('dialog', async dialog => { dialogs.push(dialog.message()); await dialog.dismiss(); });
  const buttons = await page.locator('button,[role="button"]').evaluateAll(elements => elements.map((e, index) => ({
    index, text: e.innerText, disabled: e.disabled ?? null, ariaDisabled: e.getAttribute('aria-disabled'),
    style: {color: getComputedStyle(e).color, background: getComputedStyle(e).backgroundColor,
      font: getComputedStyle(e).fontFamily, radius: getComputedStyle(e).borderRadius}
  })));
  for (const button of buttons) {
    const locator = page.locator('button,[role="button"]').nth(button.index);
    button.playwrightEnabled = await locator.isEnabled();
    if (button.playwrightEnabled) {
      await locator.click({timeout: 3000});
      await page.waitForTimeout(100);
    }
  }
  return {viewport: page.viewportSize(), buttons, requestsAfterClicks: requests, dialogs,
    textAfterClicks: await page.locator('body').innerText()};
}
