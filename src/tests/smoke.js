// Smoke test: opens every route of the built site, checks JS errors, an h1 and horizontal overflow.
// Usage:  node tests/smoke.js index.html      (needs: npm i playwright)
const {chromium}=require('playwright');const path=require('path');
const file=path.resolve(process.argv[2]||'index.html');
(async()=>{
  const b=await chromium.launch();const errs=[];let n=0;
  for(const [w,label] of [[1280,'desktop'],[400,'mobile']]){
    const p=await (await b.newContext({viewport:{width:w,height:900}})).newPage();
    p.on('pageerror',e=>errs.push(`${label} pageerror: ${e.message}`));
    await p.goto('file://'+file);await p.waitForTimeout(300);
    const routes=await p.evaluate(()=>window.ACADEMY.routes());
    for(const r of routes){
      await p.goto('file://'+file+'#'+r);await p.waitForTimeout(80);n++;
      const res=await p.evaluate(()=>({h1:document.querySelectorAll('main h1,#main h1,h1').length,over:document.documentElement.scrollWidth-window.innerWidth}));
      if(!res.h1)errs.push(`${label} ${r}: no h1`);
      if(res.over>1)errs.push(`${label} ${r}: horizontal overflow ${res.over}px`);
    }
  }
  await b.close();
  console.log(`${n} pages checked`);
  if(errs.length){console.log(errs.join('\n'));process.exit(1)}console.log('OK');
})();
