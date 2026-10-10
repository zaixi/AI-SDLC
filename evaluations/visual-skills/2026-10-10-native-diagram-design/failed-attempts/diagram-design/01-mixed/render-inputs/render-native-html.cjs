const fs = require('fs');
const {createRequire} = require('module');
const req = createRequire('/opt/render-tools/package.json');
const puppeteer = req('puppeteer-core');

(async () => {
  const [input, outputPrefix] = process.argv.slice(2);
  const browser = await puppeteer.launch({executablePath:'/usr/bin/chromium', args:['--no-sandbox','--disable-setuid-sandbox']});
  const page = await browser.newPage();
  const blocked = [];
  try {
    await page.setJavaScriptEnabled(false);
    await page.setViewport({width:1600,height:1000,deviceScaleFactor:1});
    await page.setRequestInterception(true);
    page.on('request', request => {
      const url = request.url();
      if(url.startsWith('file:') || url.startsWith('data:')) request.continue();
      else { blocked.push(url); request.abort(); }
    });
    await page.goto('file://'+input, {waitUntil:'load',timeout:30000});
    await page.screenshot({path:outputPrefix+'-desktop.png',fullPage:true});
    const svgs = await page.$$('svg');
    const diagrams = [];
    for(let i=0;i<svgs.length;i++) {
      const bounds = await svgs[i].boundingBox();
      if(!bounds || bounds.width<100 || bounds.height<60) continue;
      const filename = outputPrefix+'-svg'+(i+1)+'.png';
      await svgs[i].screenshot({path:filename});
      const geometry = await svgs[i].evaluate(el => ({viewBox:el.getAttribute('viewBox'),title:el.querySelector('title')?.textContent||null,fonts:[...new Set([...el.querySelectorAll('text')].map(t=>getComputedStyle(t).fontFamily))],textCount:el.querySelectorAll('text').length}));
      diagrams.push({index:i+1,file:filename.split('/').pop(),bounds,geometry});
    }
    await page.setViewport({width:390,height:844,deviceScaleFactor:1});
    await page.screenshot({path:outputPrefix+'-mobile.png',fullPage:true});
    const mobile = await page.evaluate(() => ({viewport:innerWidth,pageWidth:document.documentElement.scrollWidth,localScrollers:[...document.querySelectorAll('*')].filter(e=>e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflowX==='auto').map(e=>({tag:e.tagName,width:e.clientWidth,scrollWidth:e.scrollWidth}))}));
    fs.writeFileSync(outputPrefix+'-browser.json',JSON.stringify({viewport:[1600,1000],javascript:'disabled',blockedRequests:blocked,diagrams,mobile},null,2)+'\n');
    console.log(JSON.stringify({status:'passed',diagrams:diagrams.length,desktop:outputPrefix.split('/').pop()+'-desktop.png',mobile:outputPrefix.split('/').pop()+'-mobile.png'}));
  } finally { await browser.close(); }
})().catch(e=>{console.error(String(e));process.exitCode=1;});
