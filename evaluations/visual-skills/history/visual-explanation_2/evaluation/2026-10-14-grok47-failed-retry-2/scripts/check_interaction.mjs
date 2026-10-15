async (page) => {
  const manual = null;
  const controls = await page.locator('input,select,button').evaluateAll(elements => elements.map((e, index) => ({
    index, tag: e.tagName, type: e.type, id: e.id, name: e.name, min: e.min, max: e.max, value: e.value,
    label: [...(e.labels || [])].map(l => l.innerText).join(' '), text: e.innerText,
    options: e.tagName === 'SELECT' ? [...e.options].map(o => ({value: o.value, text: o.text})) : undefined
  })));
  const values = c => c.options?.map(o => Number(o.value)).sort((a,b) => a-b).join(',');
  const baseCandidates = controls.filter(c => values(c) === '1,2,3' || (Number(c.min) === 1 && Number(c.max) === 3));
  const retryCandidates = controls.filter(c => values(c) === '0,1,2,3,4,5' || (c.min === '0' && c.max === '5'));
  const baseControl = manual?.base || (baseCandidates.length === 1 ? baseCandidates[0] : null);
  const retryControl = manual?.retry || (retryCandidates.length === 1 ? retryCandidates[0] : null);
  if (!baseControl || !retryControl) {
    return {status: 'needs_manual_control_mapping', controls, text: await page.locator('body').innerText()};
  }
  async function set(control, value) {
    if (control.buttons) {
      await page.locator('input,select,button').nth(control.buttons[value]).click();
      return;
    }
    const locator = page.locator('input,select,button').nth(control.index);
    if (control.tag === 'SELECT') {
      await locator.selectOption(String(value));
    } else if (control.type === 'range') {
      await locator.focus();
      await locator.press('Home');
      for (let step = Number(control.min); step < value; step++) await locator.press('ArrowRight');
    } else {
      await locator.fill(String(value));
      await locator.press('Tab');
    }
  }
  const runs = [];
  for (const [b, n] of [[2,3],[2,5],[1,5],[3,4],[3,0]]) {
    await set(baseControl, b);
    await set(retryControl, n);
    await page.waitForTimeout(350);
    await page.evaluate(async () => {
      const animations = document.getAnimations().filter(a => a.effect?.getComputedTiming().iterations !== Infinity);
      await Promise.race([Promise.all(animations.map(a => a.finished.catch(() => {}))), new Promise(resolve => setTimeout(resolve, 2500))]);
    });
    const times = [0];
    for (let i=1;i<=n;i++) times.push(times.at(-1)+Math.min(b*2**(i-1),10));
    const viewport = page.viewportSize().width;
    const screenshot = `interaction-${viewport}-b${b}-n${n}.png`;
    await page.screenshot({path:'/review/'+screenshot,fullPage:true});
    const state = await page.evaluate(() => ({
      text: document.body.innerText,
      controls: [...document.querySelectorAll('input,select')].map(e => ({id:e.id,name:e.name,value:e.value})),
      svg: [...document.querySelectorAll('svg')].map(e => e.outerHTML),
      canvasCount: document.querySelectorAll('canvas').length
    }));
    runs.push({b,n,viewport,expected_times:times,expected_total:times.at(-1),screenshot,...state});
  }
  return {status:'operated',controls,manual_mapping:manual,runs};
}
