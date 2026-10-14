async (page) => {
  const cards = await page.locator('article.card').evaluateAll((nodes) =>
    nodes.map((node) => {
      const button = node.querySelector('button.save');
      const style = getComputedStyle(button);
      return {
        state: node.querySelector('.state-name')?.textContent?.trim(),
        doc: node.querySelector('.doc-name')?.textContent?.trim(),
        label: button.textContent.trim(),
        disabled: button.disabled,
        hint: node.querySelector('.hint')?.textContent?.trim(),
        color: style.color,
        background: style.backgroundColor,
        cursor: style.cursor,
      };
    })
  );
  const layout = await page.evaluate(() => ({
    viewport: innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    columns: getComputedStyle(document.querySelector('.states')).gridTemplateColumns,
  }));
  return { cards, layout };
}
