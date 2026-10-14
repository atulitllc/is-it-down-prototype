const R=document.body.dataset.root,SV=window.SERVICES;
const href=s=>s.page?R+'status/'+s.slug+'/':R+'category/'+s.cat+'/';
const mono=s=>`<span class="mono" style="--c:${s.color}">${s.name[0]}</span>`;
const q=document.getElementById('q'),ac=document.getElementById('ac');
if(q){let i=-1,m=[];const draw=()=>{const v=q.value.trim().toLowerCase();m=v?SV.filter(s=>s.name.toLowerCase().includes(v)||s.cat.includes(v)).slice(0,7):[];
ac.innerHTML=m.map((s,j)=>`<li class="${j==i?'on':''}"><a href="${href(s)}">${mono(s)}<span><b>${s.name}</b><br><small class="muted">${s.cat}${s.page?'':' · page soon'}</small></span></a></li>`).join('')||(v?'<li class="muted small" style="padding:10px">No match. Try another name.</li>':'');};
q.oninput=()=>{i=-1;draw()};q.onkeydown=e=>{if(e.key=='ArrowDown'){i=Math.min(i+1,m.length-1);draw();e.preventDefault()}if(e.key=='ArrowUp'){i=Math.max(i-1,0);draw();e.preventDefault()}};
document.getElementById('search').onsubmit=e=>{e.preventDefault();const s=m[Math.max(i,0)];if(s)location.href=href(s)};}
const rec=document.getElementById('recent');
if(rec){const l=JSON.parse(localStorage.getItem('df_recent')||'[]');rec.innerHTML=l.length?'<div class="svcs">'+l.map(r=>{const s=SV.find(x=>x.slug==r.slug);return `<a class="svc" href="${href(s)}">${mono(s)}<span><b>${s.name}</b><small>${r.ms} ms · ${new Date(r.t).toLocaleTimeString([], {hour:'numeric',minute:'2-digit'})}</small></span><i class="dot ok"></i></a>`}).join('')+'</div>':'<div class="empty-r"><b>Nothing checked yet</b><br><span class="small">Services you check appear here.</span></div>';}
function ping(cb){const t=performance.now(),img=new Image(),done=()=>cb(Math.round(performance.now()-t));img.onload=img.onerror=done;img.src='https://example.com/favicon.ico?t='+Date.now();}
const st=document.getElementById('status');
if(st){const slug=st.dataset.slug,b=document.getElementById('check'),v=document.getElementById('verdict');
const tz=Intl.DateTimeFormat().resolvedOptions().timeZone||'your region';document.getElementById('rg').textContent=tz.split('/').pop().replace(/_/g,' ');
b.onclick=()=>{b.textContent='Checking...';b.disabled=true;ping(ms=>{b.textContent='Check again';b.disabled=false;
document.getElementById('rt').textContent=ms+' ms';document.getElementById('lc').textContent=new Date().toLocaleTimeString([], {hour:'numeric',minute:'2-digit',second:'2-digit'});
v.innerHTML='<i class="dot ok"></i><span>Our check from your browser responded. See official status for service wide issues.</span>';
let l=JSON.parse(localStorage.getItem('df_recent')||'[]').filter(r=>r.slug!=slug);l.unshift({slug,ms,t:Date.now()});localStorage.setItem('df_recent',JSON.stringify(l.slice(0,6)));});};
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{document.querySelectorAll('.tab,.pane').forEach(x=>x.classList.toggle('on',x.dataset.t==t.dataset.t))});}
const cf=document.getElementById('cform');if(cf)cf.onsubmit=e=>{e.preventDefault();ping(ms=>document.getElementById('cres').textContent='Demo check: example.com answered in '+ms+' ms.')};
