async page => {
  const observations = {};
  for (const [mode, port] of [['reference',18076], ['candidate',18077]]) {
    const base = 'http://127.0.0.1:'+port;
    const views = {};
    const errors = [];
    page.on('pageerror', err => errors.push(err.message));
    async function observe(name) {
      await page.waitForFunction(() => document.querySelector('#report')?.innerText.trim().length > 10);
      await page.evaluate(() => document.fonts.ready);
      views[name] = await page.evaluate(async () => {
        const content = ['.site-nav','#report','#status','#periods'].map(sel => document.querySelector(sel)?.innerHTML).join('\n');
        const digest = await crypto.subtle.digest('SHA-256',new TextEncoder().encode(content));
        return {sha256:Array.from(new Uint8Array(digest),v=>v.toString(16).padStart(2,'0')).join(''), textLength:document.querySelector('#report').innerText.length};
      });
    }
    await page.goto(base); await observe('latest');
    await page.screenshot({path:mode+'-updates.png',animations:'disabled'});
    await page.locator('.site-nav summary').first().click();
    if (!await page.locator('.site-nav details[open]').count()) throw Error('Court menu did not open');
    await observe('openMenu');
    await page.keyboard.press('Escape');
    await page.locator('[data-days="30"]').click(); await observe('dateFilter');
    await page.locator('#site-query').fill('Broward'); await page.locator('#site-query').press('Enter');
    await page.getByRole('heading',{name:'Search results'}).waitFor(); await observe('search');
    await page.goto(base+'/directory.html');await observe('directory');
    await page.screenshot({path:mode+'-directory.png',animations:'disabled'});
    const id = await page.evaluate(async()=>{const p=await (await fetch('assets/current-archive.json')).json(); const a=await (await fetch('assets/'+p.archive)).json(); return a.issues[a.issues.length-1].id;});
    await page.goto(base+'/?issue='+encodeURIComponent(id));await observe('historicalIssue');
    if(errors.length)throw Error(errors.join('\n'));
    observations[mode]=views;
  }
  if(JSON.stringify(observations.reference)!==JSON.stringify(observations.candidate))throw Error('Rendered states differ');
  return observations;
}
