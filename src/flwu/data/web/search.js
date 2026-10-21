/* Public text is always inserted as text, never executed as markup. */
'use strict';
// Current county supplements never enter explicit issue or date-range views.
// Pure selection function also exercised in Node without a browser/DOM.
function countyDirectoryView(snapshot, search, supplements, savedContacts) {
  const query = new URLSearchParams(search);
  const historical = ['issue','from','to'].some(key=>query.has(key));
  const entries = new Map((snapshot?.directory||[]).map(person=>[person.id,person]));
  const contacts = {...savedContacts};
  const applied = historical ? [] : supplements;
  // Explicit county-scoped refreshes keep differing offices/assignments separate.
  // Remove only their county memberships from an older shared identity.
  const scopedCounties = new Map();
  for (const supplement of applied) for (const person of supplement.people) {
    if (person.legacy_person_id) scopedCounties.set(person.legacy_person_id,
      [...new Set([...(scopedCounties.get(person.legacy_person_id)||[]),...person.counties])]);
  }
  for (const [id,counties] of scopedCounties) {
    const saved=entries.get(id);
    if (!saved) continue;
    const remaining=saved.counties.filter(county=>!counties.includes(county));
    if (!remaining.length) { entries.delete(id); delete contacts[id]; }
    else entries.set(id,{...saved,counties:remaining,court_ids:(saved.court_ids||[]).filter(group=>
      !counties.some(county=>group==='county_'+county.toLowerCase().replace(/[^a-z0-9]+/g,'_')))});
  }
  const current = new Map();
  const union = (a,b) => [...new Map([...a,...b].map(x=>[JSON.stringify(x),x])).entries()].sort(([a],[b])=>a.localeCompare(b)).map(([,x])=>x);
  for (const supplement of applied) {
    for (const person of supplement.people) {
      const previous = current.get(person.id);
      let merged = {...person, source_observations:[person.source_observation]};
      const saved = entries.get(person.id);
      if (!previous && saved) {
        // An explicitly reconciled identity refreshes contacts without removing
        // another county's existing membership. Historical views bypass this.
        for (const key of ['counties','court_ids']) merged[key]=union(saved[key]||[],person[key]||[]);
      }
      if(previous){
        merged = {...previous};
        for(const key of ['counties','court_ids','sources','contact_notes'])merged[key]=union(previous[key],person[key]);
        merged.source_observations=union(previous.source_observations,[person.source_observation]);
        merged.source_observation=merged.source_observations[0];
      }
      current.set(person.id,merged);
      entries.set(person.id,merged);
      contacts[person.id]=merged.contacts;
    }
  }
  return {entries:[...entries.values()],contacts,applied};
}
function matchesDirectoryCourt(person,court,circuitCounties){
  if(!court)return true;
  const courtId=court.group_id;
  if((person.court_ids||[]).includes(courtId))return true;
  if(courtId.startsWith('clerk_')&&!person.source_observation)return person.counties.includes(court.label.replace(/ County$/, ''));
  if(circuitCounties[courtId])return person.counties.some(c=>circuitCounties[courtId].includes(c));
  return false;
}
if (typeof module !== 'undefined' && module.exports) module.exports={countyDirectoryView,matchesDirectoryCourt};
if (typeof document !== 'undefined') (async () => {
  document.querySelectorAll('.site-nav details').forEach(menu=>menu.addEventListener('toggle',()=>{if(menu.open)document.querySelectorAll('.site-nav details').forEach(other=>{if(other!==menu&&!other.contains(menu)&&!menu.contains(other))other.open=false;});}));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){const menus=[...document.querySelectorAll('.site-nav details[open]')];const menu=menus.reverse().find(m=>m.contains(document.activeElement))||menus[0];if(menu){menu.open=false;menu.querySelector('summary').focus();}}});
  document.addEventListener('focusin',event=>{document.querySelectorAll('.site-nav details[open]').forEach(menu=>{if(!menu.contains(event.target))menu.open=false;});});
  if(document.body.dataset.page==='about')return;
  const loading = document.getElementById('status');
  loading.hidden=false;
  loading.textContent='Loading updates and personnel…';
  const controls=[...document.querySelectorAll('#period-form input, #period-form button, [data-days], #latest')];
  controls.forEach(control=>control.disabled=true);
  let data;
  try {
    const response=await fetch(document.getElementById('archive-data').href);
    if(!response.ok)throw new Error('Archive request failed');
    data=await response.json();
  } catch(error) {
    loading.textContent='Updates and personnel could not be loaded. Please reload the page to try again.';
    loading.setAttribute('role','alert');
    return;
  }
  controls.forEach(control=>control.disabled=false);
  const isDirectory = document.body.dataset.page === 'directory';
  const sections = [['statutes','Statutes'],['case_law','Case Law'],['procedural_rules','Procedural Rules'],['local_rules','Local Rules']];
  const from = document.getElementById('from'), to = document.getElementById('to');
  const report = document.getElementById('report'), status = document.getElementById('status');
  const periods = document.getElementById('periods');
  const node = (tag, text, cls) => {const e=document.createElement(tag); if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;};
  const period = i => `${i.window_start} – ${i.window_end}`;
  const publicationDate = i => new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'long',day:'numeric'}).format(new Date(i.published_at));
  // Newest revision for each period; direct issue URLs retain older revisions.
  const seen=new Set();
  const issues=data.issues.filter(i=>{const k=period(i);if(seen.has(k))return false;seen.add(k);return true;});
  function filterRows(start,end){return issues.filter(i=>i.window_start<=end && i.window_end>=start);}
  function summary(text, isCaseLaw){
    if(!isCaseLaw)return node('p',text,'summary');
    const body=node('div',undefined,'case-body');
    let value, extra;
    // Source text stays text. A continuation line belongs to the preceding label.
    text.split('\n').forEach(line=>{
      const match=line.match(/^\s*(Holding|Disposition|Author):\s*(.*)$/);
      if(match){
        const fact=node('div',undefined,'case-fact');
        fact.append(node('span',match[1],'case-label'));
        value=node('span',match[2]);extra=null;fact.append(value);body.append(fact);
      }else if(!line){value=null;extra=null;}
      else if(value)value.append('\n'+line);
      else{if(!extra){extra=node('p',undefined,'case-extra');body.append(extra);}else extra.append('\n');extra.append(line);}
    });
    return body;
  }
  function citations(parent,refs){
    const sources=[...new Map(refs.map(c=>[c.url,c])).values()];
    const line=node('p');line.append(sources.length===1?'Source: ':'Sources: ');
    sources.forEach((c,n)=>{if(n)line.append(' · ');const a=node('a',c.label.split(' · ')[0]);a.href=c.url;line.append(a);});parent.append(line);
  }
  function render(selected, description){
    report.replaceChildren();periods.replaceChildren();status.textContent=description;status.hidden=!description;
    if(!selected.length){
      const view=countyDirectoryView(null,location.search,data.county_directories||[],{});
      if(isDirectory&&view.applied.length){renderDirectory(null);return;}
      report.append(node('p',issues.length?'No published updates match this period. This does not establish that no legal changes occurred.':'No reviewed updates have been published yet.'));return;}
    const list=node('ul');
    selected.forEach(i=>{const li=node('li'),a=node('a',period(i));const q=new URLSearchParams({issue:i.id}),court=new URLSearchParams(location.search).get('court');if(court)q.set('court',court);a.href='?'+q;a.addEventListener('click',e=>{if(e.button===0&&!e.metaKey&&!e.ctrlKey&&!e.shiftKey&&!e.altKey){e.preventDefault();navigate(a.getAttribute('href'));report.focus();}});li.append(a);list.append(li);});
    if(selected.length>1)periods.append(list);
    if(isDirectory){renderDirectory(selected[0]);return;}
    for(const [key,title] of sections){
      const section=node('details',undefined,'update-section');section.id='section-'+key;
      if(key==='case_law'||location.hash==='#section-'+key)section.open=true;
      const heading=node('h2',title),toggle=node('summary');toggle.append(heading);section.append(toggle);
      const content=node('div',undefined,'section-content');
      if(selected.some(issue=>issue.sections[key].status==='incomplete'))content.append(node('p','Research is incomplete; missing findings do not establish no changes.','notice'));
      if(selected.every(issue=>issue.sections[key].status==='reviewed'&&!issue.sections[key].items.length))content.append(node('p','No items included in this reviewed section.','meta'));
      selected.forEach(issue=>{
        const part=issue.sections[key];
        part.items.forEach(item=>{const article=node('article');if(key==='case_law')article.className='case-law-entry';article.append(node('h3',item.title));
          const dates=[];if(item.publication_date)dates.push(`Published: ${item.publication_date}`);if(item.effective_date)dates.push(`Effective: ${item.effective_date}`);if(item.legal_status!=='unknown')dates.push(item.legal_status);
          if(item.inclusion_basis==='opening_baseline')dates.push('Opening evidence baseline');
          if(item.inclusion_basis==='effective')dates.push('Included for its stated effective date');
          if(dates.length)article.append(node('p',dates.join(' · '),'meta'));
          const detail=summary(item.summary,key==='case_law');article.append(detail);
          citations(key==='case_law'?detail:article,item.citations);content.append(article);
        });
      });section.append(content);report.append(section);
    }
  }
  function renderDirectory(snapshot){
    const courtId=new URLSearchParams(location.search).get('court');
    const court=(data.courts||[]).find(c=>c.group_id===courtId);
    const directory=node('section',undefined,'directory');directory.id='directory';
    const view=countyDirectoryView(snapshot,location.search,data.county_directories||[],snapshot?data.directory_contacts[snapshot.id]:{});
    directory.append(node('h2',court?court.label+' — Personnel': 'All covered courts — Personnel'));
    if(courtId&&!court){directory.append(node('p','This court is not in the covered directory.'));report.append(directory);return;}
    const circuitCounties={circuit_fourth:['Duval','Clay','Nassau'],circuit_seventh:['Putnam','St. Johns'],circuit_eighth:['Baker','Union']};
    for(const supplement of data.county_directories||[]){
      for(const group of supplement.courts.filter(c=>c.group_id.startsWith('circuit_'))){
        circuitCounties[group.group_id]=[...new Set([...(circuitCounties[group.group_id]||[]),supplement.county])];
      }
    }
    const matches=person=>matchesDirectoryCourt(person,court,circuitCounties);
    if(courtId&&circuitCounties[courtId])directory.append(node('p','Personnel serving the covered counties within this circuit, including county-court and clerk contacts.'));
    const entries=view.entries.filter(matches).sort((a,b)=>(a.counties.join(', ')+' '+a.name).localeCompare(b.counties.join(', ')+' '+b.name));
    view.applied.filter(s=>!courtId||s.courts.some(c=>c.group_id===courtId)).forEach(s=>{
      const date=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'long',day:'numeric'}).format(new Date(s.through_capture.recorded_at));
      directory.append(node('p',`${s.county} directory observation: ${date}${s.review_status==='pending'?' · Review draft':''}.`));
      if(s.coverage_note)directory.append(node('p',s.coverage_note));
    });
    if(!entries.length)directory.append(node('p','No personnel records for this court are available in this saved snapshot.'));
    else {
      const table=node('table');table.className='personnel-table';
      const headers=['Personnel','Court / County','Chambers / Office','Judicial Assistant'];
      const thead=node('thead'),head=node('tr');headers.forEach(label=>{const th=node('th',label);th.scope='col';head.append(th);});thead.append(head);table.append(thead);
      const tbody=node('tbody');
      entries.forEach(person=>{
        const row=node('tr');row.id='person-'+person.id;const cells=headers.map(label=>{const td=node('td');td.dataset.label=label;row.append(td);return td;});
        const name=node('strong',person.name);
        if(person.profile_url){const a=node('a');a.href=person.profile_url;a.append(name);cells[0].append(a);}else cells[0].append(name);
        cells[0].append(node('p',person.kind==='clerk'?'Clerk':person.kind==='judge'?'Judge':person.kind));
        if(person.procedure_url){const a=node('a','Procedures');a.href=person.procedure_url;const p=node('p');p.append(a);cells[0].append(p);}
        if(person.contact_status==='not_verified')cells[0].append(node('p','Individual contacts not verified.'));
        if(person.contact_notes?.length){
          const notes=node('details');notes.append(node('summary','Contact differences'));
          for(const item of person.contact_notes){const p=node('p');p.append(node('strong',item.title+': '),item.text);notes.append(p);}
          cells[0].append(notes);
        }
        const courtLabels=(person.court_ids||[]).map(id=>(data.courts||[]).find(c=>c.group_id===id)?.label).filter(Boolean);
        [...new Set([...courtLabels,...person.counties.map(c=>c+' County')])].forEach(text=>cells[1].append(node('p',text)));
        const display=view.contacts[person.id];
        function contactLines(cell,rows,empty){
          if(!rows.length){cell.append(node('p',empty));return;}
          const notes=rows.some(item=>item.type==='note')?node('details'):null;
          if(notes)notes.append(node('summary','Contact notes'));
          rows.forEach(item=>{
            const p=node('p',undefined,item.type==='address'?'contact-address':'contact-line');
            if(item.type==='address'){
              p.append(node('strong',item.label));
              item.lines.forEach(text=>p.append(node('span',text)));
            }else{
              if(item.label!=='Name')p.append(node('strong',item.label+': '));
              item.lines.forEach((text,index)=>{
                if(index)p.append(node('br'));
                if(item.href){const a=node('a',text);a.href=item.href;p.append(a);}else p.append(document.createTextNode(text));
              });
            }
            if(item.type==='note')notes.append(p);else cell.append(p);
          });
          if(notes)cell.append(notes);
        }
        contactLines(cells[2],display.office,'Not published');
        contactLines(cells[3],display.assistant,['clerk','Clerk','Court administration'].includes(person.kind)?'Not applicable':'Not published');
        tbody.append(row);
      });table.append(tbody);directory.append(table);
    }
    report.append(directory);
  }
  function searchArchive(query){
    report.replaceChildren();periods.replaceChildren();
    const terms=query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    const matches=value=>terms.every(t=>value.toLocaleLowerCase().includes(t));
    const list=node('ul');let count=0;
    const add=(title,href,detail)=>{const li=node('li'),a=node('a',title);a.href=href;li.append(a,node('p',detail,'meta'));list.append(li);count++;};
    if(terms.length){
      issues.forEach(issue=>sections.forEach(([key,label])=>issue.sections[key].items.forEach(item=>{
        if(matches([item.title,item.summary,label].join(' ')))add(item.title,'./?'+new URLSearchParams({issue:issue.id})+'#section-'+key,label+' · '+period(issue));
      })));
      const latest=issues[0];
      const view=countyDirectoryView(latest,'',data.county_directories||[],latest?data.directory_contacts[latest.id]:{});
      view.entries.forEach(person=>{
        if(matches(JSON.stringify([person.name,person.counties,person.assignment,person.contacts])))add(person.name,'directory.html#person-'+encodeURIComponent(person.id),person.counties.join(', ')+' · Current directory');
      });
    }
    status.hidden=false;status.textContent=count+' search result'+(count===1?'':'s')+' for “'+query+'”';
    report.append(node('h2','Search results'),node('p','Search covers saved updates and the current personnel directory.'));
    if(count)report.append(list);else report.append(node('p','No matches. Try a surname, county, or fewer keywords.'));
  }
  function validDate(value){return /^\d{4}-\d{2}-\d{2}$/.test(value)&&!Number.isNaN(Date.parse(value+'T00:00:00Z'))&&new Date(value+'T00:00:00Z').toISOString().slice(0,10)===value;}
  function route(){
    const error=document.getElementById('date-error');error.hidden=true;error.textContent='';
    from.removeAttribute('aria-invalid');to.removeAttribute('aria-invalid');
    const updateQuery=new URLSearchParams(location.search);updateQuery.delete('q');document.getElementById('updates-link').href='./'+(updateQuery.size?'?'+updateQuery:'');
    const allQuery=new URLSearchParams(location.search);allQuery.delete('court');allQuery.delete('q');
    document.getElementById('directory-link').href='directory.html'+(allQuery.size?'?'+allQuery:'');
    document.querySelectorAll('[data-court]').forEach(link=>{const q=new URLSearchParams(allQuery);q.set('court',link.dataset.court);link.href='directory.html?'+q;});
    const query=new URLSearchParams(location.search);document.getElementById('site-query').value=query.get('q')||'';if(query.has('q')){searchArchive(query.get('q').slice(0,200));return;}const start=query.get('from'),end=query.get('to'),id=query.get('issue');
    if(id){const issue=data.issues.find(i=>i.id===id);from.value=issue?.window_start||'';to.value=issue?.window_end||'';render(issue?[issue]:[],issue?`Update: ${period(issue)}`:'The requested update was not found.');return;}
    if(start!==null||end!==null){from.value=start||'';to.value=end||'';if(!validDate(start||'')||!validDate(end||'')||start>end){const message='Enter a valid date range with From on or before Through.';error.textContent=message;error.hidden=false;if(!validDate(start||'')||start>end)from.setAttribute('aria-invalid','true');if(!validDate(end||'')||start>end)to.setAttribute('aria-invalid','true');render([],message);return;}const selected=filterRows(start,end);render(selected,`${selected.length} update${selected.length===1?'':'s'} for ${start} – ${end}`);return;}
    const latest=issues[0];from.value=latest?.window_start||'';to.value=latest?.window_end||'';render(latest?[latest]:[],latest?`Latest update: ${publicationDate(latest)}`:'');
  }
  function navigate(search){const q=new URLSearchParams(search),court=new URLSearchParams(location.search).get('court');if(court)q.set('court',court);history.pushState(null,'',location.pathname+(q.size?'?'+q:''));route();}
  document.getElementById('period-form').addEventListener('submit',e=>{e.preventDefault();navigate('?'+new URLSearchParams({from:from.value,to:to.value}));document.querySelector('[aria-invalid="true"]')?.focus();});
  document.getElementById('latest').addEventListener('click',()=>navigate(''));
  document.querySelectorAll('[data-days]').forEach(button=>button.addEventListener('click',()=>{
    // Calendar days in the reporting timezone, including today. UTC arithmetic
    // on that date avoids shortening or extending a range across DST changes.
    const parts=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
    const part=type=>parts.find(p=>p.type===type).value;
    const end=`${part('year')}-${part('month')}-${part('day')}`;
    const start=new Date(end+'T00:00:00Z');start.setUTCDate(start.getUTCDate()-Number(button.dataset.days)+1);
    navigate('?'+new URLSearchParams({from:start.toISOString().slice(0,10),to:end}));
  }));
  addEventListener('popstate',route);route();if(location.hash){const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target){target.tabIndex=-1;target.focus();target.scrollIntoView();}}
})();
