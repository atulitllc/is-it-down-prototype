import json,os,html
B="DownFixer"
from atulit_gfx import icon,flogo,hero,THEME_HEAD,toggle,CREDIT,install_css
DOM={"discord":"discord.com","reddit":"reddit.com","chatgpt":"chatgpt.com","claude":"claude.ai","epic-games":"epicgames.com","coinbase":"coinbase.com","robinhood":"robinhood.com","github":"github.com","dropbox":"dropbox.com","figma":"figma.com","atlassian":"atlassian.com","duolingo":"duolingo.com"}
CATI={"social":"message-circle","ai":"sparkles","gaming":"gamepad-2","banking":"credit-card","work":"briefcase"}
CATC={"social":"#5865f2","ai":"#0F9D8A","gaming":"#f97316","banking":"#2563eb","work":"#a259ff"}
# Real services with public official Statuspage JSON APIs (checked Oct 13, 2026)
S=[("discord","Discord","social","#5865f2","https://discordstatus.com"),("reddit","Reddit","social","#ff4500","https://www.redditstatus.com"),
("chatgpt","ChatGPT (OpenAI)","ai","#10a37f","https://status.openai.com"),("claude","Claude","ai","#d97757","https://status.claude.com"),
("epic-games","Epic Games","gaming","#2a2a2a","https://status.epicgames.com"),
("coinbase","Coinbase","banking","#0052ff","https://status.coinbase.com"),("robinhood","Robinhood","banking","#00a85a","https://status.robinhood.com"),
("github","GitHub","work","#24292f","https://www.githubstatus.com"),("dropbox","Dropbox","work","#0061ff","https://status.dropbox.com"),("figma","Figma","work","#a259ff","https://status.figma.com"),
("atlassian","Atlassian (Jira, Confluence)","work","#0052cc","https://status.atlassian.com"),("duolingo","Duolingo","work","#58cc02","https://status.duolingo.com")]
PAGES=[x[0] for x in S]
CATS={"social":("Social","Chat and community apps"),"ai":("AI","Chat assistants"),"gaming":("Gaming","Game networks and launchers"),"banking":("Finance","Trading and crypto apps"),"work":("Work and learning","Code, files, design and learning apps")}
SD={k:{"slug":k,"name":n,"cat":c,"color":col,"page":True,"status":st,"domain":DOM[k]} for k,n,c,col,st in S}
PROB={"social":["Login","Messages not sending","App crashing"],"ai":["No response","Login","Slow answers"],"gaming":["Login","Server disconnects","Store"],"banking":["Login","App crashing","Transfers"],"work":["Login","Sync or upload","App crashing"]}
URL="https://downfixer.com/"  # canonical apex; SEO head tags are set by seo_site.py
def mono(s,big=False): return f'<span class="mono lg{" big" if big else ""}" style="--c:{s["color"]}">{flogo(s["domain"],s["name"],44 if big else 26,not big)}</span>'
def page(path,title,desc,crumbs,body,extra_ld=None,faq=None):
    d=path.count("/") if path else 0
    p="../"*d
    bl={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":URL+u} for i,(n,u) in enumerate(crumbs)]}
    org={"@context":"https://schema.org","@type":"Organization","name":B,"url":URL,"logo":URL+"img/brand/icon-512.png","parentOrganization":{"@type":"Organization","name":"Atulit"}}
    lds=[bl,org]+(extra_ld or [])
    ld="".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in lds)
    cr=" <span>/</span> ".join((f'<a href="{p}{u}">{html.escape(n)}</a>' if i<len(crumbs)-1 else f'<span aria-current="page">{html.escape(n)}</span>') for i,(n,u) in enumerate(crumbs))
    nav="".join(f'<a href="{p}category/{k}/">{icon(CATI[k],16)}{v[0]}</a>' for k,v in CATS.items())
    h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | {B}</title><meta name="description" content="{html.escape(desc)}"><meta name="robots" content="noindex, nofollow">{THEME_HEAD}
<link rel="canonical" href="{URL}{path}"><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="{p}img/brand/favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}img/brand/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="{p}img/brand/icon-180.png"><link rel="stylesheet" href="{p}assets/style.css?v=20261013logos">{ld}</head><body data-root="{p}">
<header class="top"><div class="wrap row"><a class="logo" href="{p or './'}"><img src="{p}img/brand/wordmark.svg" alt="{B}" height="34"></a><nav>{nav}<a href="{p}fixes/">{icon("wrench",16)}Fixes</a><a href="{p}how-we-check/">{icon("shield-check",16)}How we check</a></nav>{toggle()}</div></header>
<div class="wrap">{"" if not path else f'<nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>'}
{body}</div>
<footer><div class="wrap row"><div><a class="logo" href="{p or './'}"><img src="{p}img/brand/wordmark.svg" alt="{B}" height="30"></a><p class="muted">Independent status checks by Atulit. Not affiliated with any service listed.</p></div>
<div class="flinks"><a href="{p}about/">About</a><a href="{p}how-we-check/">How we check</a><a href="{p}fixes/">Fixes guide</a></div></div><p class="wrap small muted credit">{CREDIT}</p></footer>
<script>window.SERVICES={json.dumps(list(SD.values()))};</script><script src="{p}assets/app.js"></script></body></html>'''
    os.makedirs(path or ".",exist_ok=True); open((path or "")+"index.html","w").write(h)
def card(s,p):
    href=f'{p}status/{s["slug"]}/' if s["page"] else f'{p}category/{s["cat"]}/'
    return f'<a class="svc" href="{href}">{mono(s)}<span><b>{s["name"]}</b><small>{CATS[s["cat"]][0]}{"" if s["page"] else " · page soon"}</small></span><span class="st">{icon("activity",16)}<i class="dot" data-k="{s["slug"]}" title="Checking status"></i></span></a>'
# HOME
chips="".join(f'<a class="chip" href="category/{k}/">{icon(CATI[k],15)} {v[0]}</a>' for k,v in CATS.items())
pop="".join(card(SD[k],"") for k in PAGES)
body=f'''<section class="hero hs"><div><p class="eyebrow"><span class="pulse"></span> Live official status from public status pages</p><h1>Is it down,<br>or is it just you?</h1>
<p class="lead">Search an app to see what its official status page says right now, with the time it was last updated, plus fixes from official help docs.</p>
<form class="search" id="search" autocomplete="off" role="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><input id="q" placeholder="Try Discord, ChatGPT, GitHub..." aria-label="Search services"><button>Check</button><ul id="ac" role="listbox"></ul></form>
<div class="chips">{chips}</div></div><div class="hgfx">{hero("downfixer")}</div></section>
<div class="grid2"><main><h2 class="secdeco" style="--c:#0F9D8A"><span class="ibadge soft">{icon("activity",20)}</span>Popular checks</h2><div class="svcs">{pop}</div><script>fetch('data/status.json',{{cache:'no-store'}}).then(r=>r.json()).then(j=>{{const M={{none:['ok','Up and working'],minor:['warn','Minor issues'],maintenance:['warn','Maintenance'],major:['bad','Major outage'],critical:['bad','Major outage']}};document.querySelectorAll('.svcs .dot[data-k]').forEach(d=>{{const e=j.services[d.dataset.k];if(e&&e.data){{const m=M[e.data.status.indicator];if(m){{d.classList.add(m[0]);d.title=m[1]}}}}}})}}).catch(()=>{{}})</script>
<h2 class="secdeco" style="--c:#0E2A3F"><span class="ibadge soft">{icon("clock",20)}</span>Recently checked</h2><p class="muted small">Stored only on this device.</p><div id="recent"></div>
<h2 class="secdeco" style="--c:#0F9D8A"><span class="ibadge soft">{icon("layers",20)}</span>Browse by category</h2><div class="cats">{"".join(f'<a href="category/{k}/" class="catcard" style="--c:{CATC[k]}"><span class="ibadge sm">{icon(CATI[k],18)}</span><b>{v[0]}</b><span>{v[1]}</span></a>' for k,v in CATS.items())}</div></main>
<aside><div class="box"><span class="ibadge sm" style="--c:#0F9D8A">{icon("shield-check",18)}</span><h3>Honest data only</h3><p class="small muted">We never show invented report counts. Charts stay empty until real reports arrive.</p><a href="how-we-check/">How we check</a></div></aside></div>'''
page("","Is It Down or Just You? Live Checks & Fixes","Check if popular apps are down for everyone or just you, run a live check from your own browser, and get step by step fixes for web, iPhone and Android.",[("Home","")],body,[{"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":URL+f"status/{k}/","name":SD[k]["name"]} for i,k in enumerate(PAGES)]}])
# SERVICE
APPLE_CLOSE="https://support.apple.com/en-us/109359"; APPLE_UPD="https://support.apple.com/en-us/102629"; GPLAY="https://support.google.com/googleplay/answer/7513003?hl=en"
def fixes(s):
    n=s["name"]
    return {"iPhone":[(f"If {n} is frozen, close it: from the Home Screen swipe up from the bottom and pause, find the app, then swipe up on its preview. Reopen it.",APPLE_CLOSE),
    ("Update the app: open the App Store, tap your photo at the top, tap App Updates, then Update.",APPLE_UPD)],
    "Android":[("Check your Wi-Fi or mobile data connection. A strong connection, ideally Wi-Fi, is best.",GPLAY),
    ("Check storage: open Settings, tap Storage. Less than 1 GB free can stop apps from updating.",GPLAY),
    ("Check for Android system updates in Settings.",GPLAY)],
    "Web":[(f"Open the official {n} status page to see if the problem is on their side.",s["status"])]}
def stepli(v): return "".join(f'<li>{x} <a class="small" href="{u}" rel="nofollow">Source</a></li>' for x,u in v)
for k in PAGES:
    s=SD[k];n=s["name"];c=s["cat"];p="../../"
    pr=PROB[c]
    chipsr="".join(f'<button type="button" class="chip pick" data-v="{x}">{x}</button>' for x in pr)
    fx=fixes(s)
    tabs="".join(f'<button class="tab{" on" if i==0 else ""}" data-t="{t}">{t}</button>' for i,t in enumerate(fx))
    panes="".join(f'<ol class="steps pane{" on" if i==0 else ""}" data-t="{t}">'+stepli(v)+"</ol>" for i,(t,v) in enumerate(fx.items()))
    rel="".join(card(x,p) for x in SD.values() if x["cat"]==c and x["slug"]!=k)
    faqq=[(f"Is {n} down right now?",f"This page reads the official {n} status page and shows what it reports, with the time {n} last updated it. Press Check now to fetch it again. We do not collect user reports, so we show none."),(f"Why does {n} work for others but not me?","Local issues such as cache, network or an outdated app are the most common cause. Try the fixes for your device.")]
    faqh="".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faqq)
    body=f'''<div class="grid2"><main>
<section class="status" id="status" data-slug="{k}" data-api="{s["status"]}/api/v2/status.json">{mono(s,True)}<div class="st"><p class="eyebrow">{CATS[c][0]} status</p><h1>Is {n} down?</h1><p class="small muted">Not affiliated with {n}. Status below is what {n} publishes on its own status page.</p>
<p class="verdict" id="verdict"><i class="dot idle"></i><span id="vt">Loading the official status...</span></p>
<div class="metrics"><div><small>Official status</small><b id="rt">--</b></div><div><small>Status page updated</small><b id="lc">--</b></div><div><small>We fetched it</small><b id="rg">--</b></div></div>
<div class="act"><button class="btn" id="check">Check now</button><a class="btn ghost" href="{p}fix/{k}/app-crashing/">Top fixes</a></div>
<p class="small muted">Source: <a href="{s["status"]}" rel="nofollow">{s["status"].split("//")[1]}</a> (public Statuspage API). Times show in your time zone. If it says operational but the app fails for you, the problem may be on your side.</p></div></section>
<section class="panel"><div class="ph"><h2>User reports, last 24 hours</h2><span class="tag">Not collected yet</span></div>
<p class="small muted"><b>No user reports shown.</b> We do not collect user reports yet, so we show no counts and no chart.</p></section>

<section class="panel"><h2>How to fix {n}</h2><div class="tabs">{tabs}</div>{panes}<p class="small"><a href="{p}fixes/">Full fixes guide</a></p></section>
<section class="panel"><h2>Questions</h2>{faqh}</section></main>
<aside><div class="box"><h3>Official status</h3><p class="small muted">Check what {n} says about its own systems.</p><a class="btn ghost full" href="{s["status"]}" rel="nofollow">{n} status page</a></div>
<div class="box"><h3>Related services</h3><div class="svcs one">{rel}</div></div></aside></div>'''
    fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqq]}
    page(f"status/{k}/",f"Is {n} Down? Official Status + Our Live Check",f"Official {n} status, our live {n} status check, fixes.",[("Home",""),(CATS[c][0],f"category/{c}/"),(n,f"status/{k}/")],body,[fq])
# CATEGORY
for c,(t,d) in CATS.items():
    items=[x for x in SD.values() if x["cat"]==c]
    body=f'<h1>{t} status</h1><p class="lead">{d}. Pick a service to run a check.</p><div class="chips">'+"".join(f'<a class="chip{" on" if k==c else ""}" href="../{k}/">{v[0]}</a>' for k,v in CATS.items())+f'</div><div class="grid2"><main><div class="svcs">{"".join(card(x,"../../") for x in items)}</div></main></div>'
    page(f"category/{c}/",f"{t} status",d,[("Home",""),(t,f"category/{c}/")],body,[{"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"name":x["name"]} for i,x in enumerate(items)]}])
# FIXES
G=[("Start here",["Run Check now on the service page. If the check passes and there are no reports, the problem is likely on your side.","Try another device or network to isolate the cause."]),
("Web browsers",["Hard refresh with Ctrl Shift R or Cmd Shift R.","Disable extensions or use a private window.","Clear cookies for that site only.","Check your date and time are set automatically."]),
("iPhone and iPad",["Force close the app and reopen it.","Toggle Airplane Mode.","Update the app and iOS.","Settings, General, Transfer or Reset, Reset Network Settings as a last resort."]),
("Android",["Force stop the app and clear its cache.","Toggle mobile data and WiFi.","Update from Google Play.","Restart the phone in safe mode to test for conflicts."]),
("Network and router",["Restart your router and modem, wait 30 seconds.","Change DNS to your provider default or a public resolver.","Turn off VPN or proxy temporarily."])]
body='<h1>Fixes guide</h1><p class="lead">Step by step fixes that work for most apps when it is just you.</p><p class="small muted">These are general troubleshooting tips, not official steps from any one service. For sourced steps, see each service fix page. Last checked Oct 13, 2026.</p><div class="grid2"><main>'+"".join(f'<section class="panel"><h2>{h}</h2><ol class="steps on">'+"".join(f"<li>{x}</li>" for x in l)+"</ol></section>" for h,l in G)+'</main></div>'
body=body.replace('</main></div>','<section class="panel"><h2>Fixes by service</h2><ul>'+"".join(f'<li><a href="../status/{k}/">{SD[k]["name"]} status</a> · <a href="../fix/{k}/app-crashing/">app crashing</a> · <a href="../fix/{k}/android-not-updating/">Android updates</a> · <a href="../fix/{k}/error-500/">error 500</a></li>' for k in PAGES)+'</ul><p><a href="../errors/500/">Error 500 explained</a></p></section></main></div>')
page("fixes/","Fixes guide","Fix apps that are not working.",[("Home",""),("Fixes guide","fixes/")],body)
page("errors/500/","Error 500 Internal Server Error: What It Means","",[("Home",""),("Fixes guide","fixes/"),("Error 500","errors/500/")],'<div class="prose"><h1>Error 500 Internal Server Error: What It Means</h1><p class="lead">An HTTP 500 error means the server hit an unexpected problem while handling your request. It is almost always on the service side, not your device.</p><ol class="steps on"><li>Wait two minutes, then reload the page.</li><li>Check the service status page here or the official status page.</li><li>Sign out and back in, or try a private window.</li><li>If it keeps happening, contact the service through its official help channels.</li></ol><h2>Service specific pages</h2><ul>'+"".join(f'<li><a href="../../fix/{k}/error-500/">{SD[k]["name"]} error 500</a></li>' for k in PAGES)+'</ul><p><a href="../../fixes/">Full fixes guide</a></p></div>')
page("about/","About","About "+B,[("Home",""),("About","about/")],f'<div class="prose"><h1>About {B}</h1><p class="lead">{B} is an Atulit project that helps you work out in seconds whether an app is down for everyone or just for you.</p><p>We plan to fund the site with clearly labeled ads once it has real traffic. Ads will never sit inside status widgets. We are not affiliated with the services listed.</p><p>We publish only real data. If nobody has reported a problem, you will see an empty chart, not an invented number.</p></div>')
page("how-we-check/","How we check","Methodology",[("Home",""),("How we check","how-we-check/")],'<div class="prose"><h1>How we check</h1><p class="lead">We show what each service says on its own public status page. Nothing is estimated.</p><div class="steps3"><div class="box"><b>1. Live from your browser</b><p class="small">Each status page fetches the service\'s public Statuspage API (for example discordstatus.com/api/v2/status.json) when you open it or press Check now.</p></div><div class="box"><b>2. Snapshot every 15 minutes</b><p class="small">A scheduled GitHub Action saves the same official JSON to data/status.json, so the last known status shows even if the live fetch fails. Each entry keeps its real fetch time.</p></div><div class="box"><b>3. Fixes from official docs</b><p class="small">Device fixes come from Apple Support and Google Play Help, with a source link on each step.</p></div></div><h2>What we never do</h2><ul><li>Show estimated or placeholder report counts. We do not collect user reports.</li><li>Back fill outage history before tracking began.</li></ul><p class="small muted">Last checked Oct 13, 2026.</p></div>')
open(".nojekyll","w").write("")

ISS=[("app-crashing","App crashing or frozen","iPhone"),("android-not-updating","App not updating","Android")]
for k in PAGES:
    s=SD[k];n=s["name"]
    for slug,iss,plat in ISS:
        st=fixes(s)[plat]
        body=f'<div class="prose"><h1>{n} not working? {len(st)} fixes for {iss} ({plat})</h1><p class="small muted">General device steps from official {"Apple Support" if plat=="iPhone" else "Google Play Help"} docs. They apply to most apps, not {n} only. Not affiliated with {n}. Last checked Oct 13, 2026.</p><section class="panel"><ol class="steps on">'+stepli(st)+f'</ol><p class="small">First check the <a href="{s["status"]}" rel="nofollow">official {n} status page</a>.</p></section><p><a href="../../../status/{k}/">Back to {n} status</a> · <a href="../error-500/">{n} error 500</a> · <a href="../../../errors/500/">Error 500 explained</a></p></div>'
        ht={"@context":"https://schema.org","@type":"HowTo","name":f"Fix {n} {iss}","step":[{"@type":"HowToStep","text":x} for x,u in st]}
        page(f"fix/{k}/{slug}/",f"{n} Not Working? {len(st)} Fixes for {iss} ({plat})",f"Fixes for {n} {iss}.",[("Home",""),(n,f"status/{k}/"),(iss,f"fix/{k}/{slug}/")],body,[ht])
    body=f'<div class="prose"><h1>{n} error 500: what it means and how to fix it</h1><p>Error 500 means {n} servers hit an unexpected problem. It is usually on their side. Check the official status, wait a few minutes, then retry.</p><ol class="steps on"><li>Reload after 2 minutes.</li><li>Check <a href="../../../status/{k}/">{n} status</a>.</li><li>Sign out and back in.</li><li>If it keeps happening, contact {n} through its official help channels only.</li></ol><p>Related: <a href="../android-not-updating/">Android update fixes</a> · <a href="../app-crashing/">App crashing</a> · <a href="../../../errors/500/">What error 500 means on any site</a></p></div>'
    page(f"fix/{k}/error-500/",f"{n} Error 500: What It Means & How to Fix It",f"{n} error 500 explained.",[("Home",""),(n,f"status/{k}/"),("Error 500",f"fix/{k}/error-500/")],body)

import seo_site; seo_site.build()
install_css("assets/style.css",""".hero.hs{display:grid;grid-template-columns:1.25fr 1fr;gap:30px;align-items:center;text-align:left}.hs .lead{margin-left:0}.hs .search{margin:0}.hs .chips{justify-content:flex-start}.hs .chip{display:inline-flex;align-items:center;gap:6px}.hs .chip .ic{opacity:.7}
.mono.lg{background:#fff;border:1px solid #e5e7eb}.svc .mono{flex:none;display:grid}.svc .st{flex:none;flex-direction:row;display:flex;align-items:center;gap:6px;color:#94a3b8}
.catcard{gap:4px}.catcard .ibadge{margin-bottom:6px}.catcard:hover{text-decoration:none;border-color:var(--c)}.box .ibadge{margin-bottom:8px}.credit{margin-top:6px;padding-bottom:16px}
@media(max-width:860px){.hero.hs{grid-template-columns:1fr}.hgfx{order:-1}.hgfx .hero-gfx{max-width:260px}.hero.hs h1{font-size:44px}}
html[data-theme=dark] .sample{background:#2a2410;color:#fcd34d}
""")

