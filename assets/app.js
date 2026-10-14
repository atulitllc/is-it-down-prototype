const R=document.body.dataset.root,SV=window.SERVICES;
const href=s=>s.page?R+'status/'+s.slug+'/':R+'category/'+s.cat+'/';
const mono=s=>`<span class="mono lg" style="--c:${s.color}"><img class="flogo" src="https://www.google.com/s2/favicons?domain=${s.domain}&sz=64" alt="${s.name} logo" width="26" height="26" loading="lazy"></span>`;
const q=document.getElementById('q'),ac=document.getElementById('ac');
if(q){let i=-1,m=[];const draw=()=>{const v=q.value.trim().toLowerCase();m=v?SV.filter(s=>s.name.toLowerCase().includes(v)||s.cat.includes(v)).slice(0,7):[];
ac.innerHTML=m.map((s,j)=>`<li class="${j==i?'on':''}"><a href="${href(s)}">${mono(s)}<span><b>${s.name}</b><br><small class="muted">${s.cat}${s.page?'':' · page soon'}</small></span></a></li>`).join('')||(v?'<li class="muted small" style="padding:10px">No match. Try another name.</li>':'');};
q.oninput=()=>{i=-1;draw()};q.onkeydown=e=>{if(e.key=='ArrowDown'){i=Math.min(i+1,m.length-1);draw();e.preventDefault()}if(e.key=='ArrowUp'){i=Math.max(i-1,0);draw();e.preventDefault()}};
document.getElementById('search').onsubmit=e=>{e.preventDefault();const s=m[Math.max(i,0)];if(s)location.href=href(s)};}
const rec=document.getElementById('recent');
if(rec){const l=JSON.parse(localStorage.getItem('df_recent')||'[]');rec.innerHTML=l.length?'<div class="svcs">'+l.map(r=>{const s=SV.find(x=>x.slug==r.slug);return `<a class="svc" href="${href(s)}">${mono(s)}<span><b>${s.name}</b><small>Viewed ${new Date(r.t).toLocaleTimeString([], {hour:'numeric',minute:'2-digit'})}</small></span></a>`}).join('')+'</div>':'<div class="empty-r"><b>Nothing checked yet</b><br><span class="small">Services you check appear here.</span></div>';}
const fmt=t=>new Date(t).toLocaleString([], {month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});
const IND={none:'ok',minor:'warn',major:'bad',critical:'bad',maintenance:'warn'};
const st=document.getElementById('status');
if(st){const slug=st.dataset.slug,api=st.dataset.api,b=document.getElementById('check'),v=document.getElementById('verdict');
const show=(d,fetched,snap)=>{v.innerHTML=`<i class="dot ${IND[d.status.indicator]||'idle'}"></i><span>${d.page.name} official status: ${d.status.description}${snap?' (saved snapshot)':''}</span>`;
document.getElementById('rt').textContent=d.status.description;document.getElementById('lc').textContent=fmt(d.page.updated_at);document.getElementById('rg').textContent=fmt(fetched);};
const snap=()=>fetch(R+'data/status.json',{cache:'no-store'}).then(r=>r.json()).then(j=>{const e=j.services[slug];if(e&&e.data)show(e.data,e.fetched_at,true);else throw 0}).catch(()=>{v.innerHTML='<i class="dot idle"></i><span>Could not load the official status. Use the status page link below.</span>'});
const live=()=>{b.textContent='Checking...';b.disabled=true;fetch(api,{cache:'no-store'}).then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>show(d,Date.now(),false)).catch(snap).finally(()=>{b.textContent='Check again';b.disabled=false;
let l=JSON.parse(localStorage.getItem('df_recent')||'[]').filter(r=>r.slug!=slug);l.unshift({slug,t:Date.now()});localStorage.setItem('df_recent',JSON.stringify(l.slice(0,6)));});};
b.onclick=live;live();
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{document.querySelectorAll('.tab,.pane').forEach(x=>x.classList.toggle('on',x.dataset.t==t.dataset.t))});}
