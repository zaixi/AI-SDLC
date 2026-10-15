async (page) => page.evaluate(() => ({
  viewport: innerWidth,
  shapes: [...document.querySelectorAll('svg rect,svg line,svg polyline,svg path,svg circle,svg text,[class*="bar"]')].map(e => {
    const r = e.getBoundingClientRect();
    const style = getComputedStyle(e);
    return {tag: e.tagName, id: e.id, class: e.getAttribute('class'), text: e.textContent,
      attributes: Object.fromEntries([...e.attributes].map(a => [a.name, a.value])),
      screenBounds: {x:r.x,y:r.y,width:r.width,height:r.height},
      visible: style.display !== 'none' && style.visibility !== 'hidden', color:style.color,fill:style.fill,background:style.backgroundColor};
  })
}))
