import json,os,html
B="DownFixer"
S=[("chatterly","Chatterly","social","#ec4899"),("pixgram","Pixgram","social","#f97316"),("threadly","Threadly","social","#8b5cf6"),("loopsy","Loopsy","social","#06b6d4"),
("streamora","Streamora","streaming","#ef4444"),("tunewave","Tunewave","streaming","#22c55e"),("flickbox","Flickbox","streaming","#eab308"),("vidnest","Vidnest","streaming","#3b82f6"),
("fragzone","Fragzone","gaming","#10b981"),("questhub","Questhub","gaming","#6366f1"),("pixelforge","Pixelforge Live","gaming","#f43f5e"),("arcadia","Arcadia Net","gaming","#14b8a6"),
("thinkly","Thinkly AI","ai","#7c3aed"),("promptpal","PromptPal","ai","#0ea5e9"),("muse","Muse Studio","ai","#d946ef"),("codewren","Codewren","ai","#84cc16"),
("northvault","Northvault Bank","banking","#0f766e"),("coinpath","Coinpath","banking","#ca8a04"),("ledgerly","Ledgerly Pay","banking","#2563eb"),("fernbank","Fern Bank","banking","#16a34a")]
PAGES=["chatterly","streamora","fragzone","thinkly","northvault","tunewave"]
CATS={"social":("Social","Feeds, messaging and photo apps"),"streaming":("Streaming","Video and music streaming"),"gaming":("Gaming","Game networks and launchers"),"ai":("AI","Chat assistants and creative AI tools"),"banking":("Banking","Banks, wallets and payments")}
SD={k:{"slug":k,"name":n,"cat":c,"color":col,"page":k in PAGES} for k,n,c,col in S}
PROB={"social":["Feed not loading","Login","Messages not sending","Notifications","Photo upload"],"streaming":["Video buffering","Login","App crashing","Playback error","Downloads"],
"gaming":["Matchmaking","Login","Server disconnects","Store","Voice chat"],"ai":["No response","Login","Slow answers","File upload","Image generation"],"banking":["Login","Card payments","Transfers","App crashing","Balance not updating"]}
URL="https://atulitllc.github.io/is-it-down-prototype/"
def mono(s,big=False): return f'<span class="mono{" big" if big else ""}" style="--c:{s["color"]}">{s["name"][0]}</span>'
def page(path,title,desc,crumbs,body,extra_ld=None,faq=None):
    d=path.count("/") if path else 0
    p="../"*d
    bl={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":URL+u} for i,(n,u) in enumerate(crumbs)]}
    org={"@context":"https://schema.org","@type":"Organization","name":B,"url":URL,"parentOrganization":{"@type":"Organization","name":"Atulit"}}
    lds=[bl,org]+(extra_ld or [])
    ld="".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in lds)
    cr=" <span>/</span> ".join((f'<a href="{p}{u}">{html.escape(n)}</a>' if i<len(crumbs)-1 else f'<span aria-current="page">{html.escape(n)}</span>') for i,(n,u) in enumerate(crumbs))
    nav="".join(f'<a href="{p}category/{k}/">{v[0]}</a>' for k,v in CATS.items())
    h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | {B}</title><meta name="description" content="{html.escape(desc)}"><meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{URL}{path}"><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/style.css?v=20261013noads">{ld}</head><body data-root="{p}">
<div class="sample">Sample data prototype. Services are fictional; status checks are demos.</div>
<header class="top"><div class="wrap row"><a class="logo" href="{p}index.html"><span class="pulse"></span>{B}</a><nav>{nav}<a href="{p}fixes/">Fixes</a><a href="{p}how-we-check/">How we check</a></nav></div></header>
<div class="wrap">{"" if not path else f'<nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>'}
{body}</div>
<footer><div class="wrap row"><div><a class="logo" href="{p}index.html"><span class="pulse"></span>{B}</a><p class="muted">Independent status checks by Atulit. Not affiliated with any service listed.</p></div>
<div class="flinks"><a href="{p}about/">About</a><a href="{p}how-we-check/">How we check</a><a href="{p}fixes/">Fixes guide</a></div></div></footer>
<script>window.SERVICES={json.dumps(list(SD.values()))};</script><script src="{p}assets/app.js"></script></body></html>'''
    os.makedirs(path or ".",exist_ok=True); open((path or "")+"index.html","w").write(h)
def card(s,p):
    href=f'{p}status/{s["slug"]}/' if s["page"] else f'{p}category/{s["cat"]}/'
    return f'<a class="svc" href="{href}">{mono(s)}<span><b>{s["name"]}</b><small>{CATS[s["cat"]][0]}{"" if s["page"] else " · page soon"}</small></span><i class="dot"></i></a>'
# HOME
chips="".join(f'<a class="chip" href="category/{k}/">{v[0]}</a>' for k,v in CATS.items())
pop="".join(card(SD[k],"") for k in PAGES)
body=f'''<section class="hero"><p class="eyebrow"><span class="pulse"></span> Live checks from your own browser</p><h1>Is it down,<br>or is it just you?</h1>
<p class="lead">Search an app to run a check, see community reports and get fixes for web, iPhone and Android.</p>
<form class="search" id="search" autocomplete="off" role="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><input id="q" placeholder="Try Streamora, Thinkly AI, Fern Bank..." aria-label="Search services"><button>Check</button><ul id="ac" role="listbox"></ul></form>
<div class="chips">{chips}</div></section>
<div class="grid2"><main><h2>Popular checks</h2><div class="svcs">{pop}</div>
<h2>Recently checked</h2><p class="muted small">Stored only on this device.</p><div id="recent"></div>
<h2>Browse by category</h2><div class="cats">{"".join(f'<a href="category/{k}/" class="catcard"><b>{v[0]}</b><span>{v[1]}</span></a>' for k,v in CATS.items())}</div></main>
<aside><div class="box"><h3>Honest data only</h3><p class="small muted">We never show invented report counts. Charts stay empty until real reports arrive.</p><a href="how-we-check/">How we check</a></div></aside></div>'''
page("","Is it down? Official status + our live check","Check if popular apps are down.",[("Home","")],body,[{"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":URL+f"status/{k}/","name":SD[k]["name"]} for i,k in enumerate(PAGES)]}])
# SERVICE
def fixes(s):
    n=s["name"]
    return {"Web":[f"Open {n} in a private window to rule out extensions.","Clear the site's cookies and cache, then sign in again.","Try a different network, for example your phone hotspot.","Check the official status page linked on this page."],
    "iPhone":[f"Force close {n}: swipe up and hold, then swipe the app away.","Turn Airplane Mode on for 10 seconds, then off.",f"Update {n} in the App Store.","Restart your iPhone, then delete and reinstall if it still fails."],
    "Android":[f"Settings, Apps, {n}, Force stop, then reopen.","Clear the app cache in Settings, Apps, Storage.","Switch between WiFi and mobile data.","Update from Google Play or reinstall the app."]}
for k in PAGES:
    s=SD[k];n=s["name"];c=s["cat"];p="../../"
    pr=PROB[c]
    chipsr="".join(f'<button type="button" class="chip pick" data-v="{x}">{x}</button>' for x in pr)
    fx=fixes(s)
    tabs="".join(f'<button class="tab{" on" if i==0 else ""}" data-t="{t}">{t}</button>' for i,t in enumerate(fx))
    panes="".join(f'<ol class="steps pane{" on" if i==0 else ""}" data-t="{t}">'+"".join(f"<li>{x}</li>" for x in v)+"</ol>" for i,(t,v) in enumerate(fx.items()))
    rel="".join(card(x,p) for x in SD.values() if x["cat"]==c and x["slug"]!=k)
    ticks="".join(f'<text x="{40+i*80}" y="196">{["24h ago","20h","16h","12h","8h","4h","Now"][i]}</text>' for i in range(7))
    grid="".join(f'<line x1="40" x2="520" y1="{y}" y2="{y}"/>' for y in (30,80,130,180))
    strip="".join('<i></i>' for _ in range(90))
    faqq=[(f"Is {n} down right now?",f"Press Check now to run a live test from your browser. Community reports for {n} appear above when people submit them."),(f"Why does {n} work for others but not me?","Local issues such as cache, network or an outdated app are the most common cause. Try the fixes for your device.")]
    faqh="".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faqq)
    body=f'''<div class="grid2"><main>
<section class="status" id="status" data-slug="{k}">{mono(s,True)}<div class="st"><p class="eyebrow">{CATS[c][0]} status</p><h1>Is {n} down?</h1><p class="small muted">Not affiliated with {n}. Sample data.</p>
<p class="verdict" id="verdict"><i class="dot idle"></i><span>Our check from your region has not run yet. Press Check now.</span></p>
<div class="metrics"><div><small>Response time</small><b id="rt">--</b></div><div><small>Last checked</small><b id="lc">Never</b></div><div><small>Our check from</small><b id="rg">Your browser</b></div></div>
<div class="act"><button class="btn" id="check">Check now</button><a class="btn ghost" href="{p}fix/{k}/login/">Top fixes</a></div>
<p class="small muted">Our check alone never means down for everyone. Demo check: times a request from your browser to example.com. It does not contact {n}.</p></div></section>
<section class="panel off"><div class="ph"><h2>Official status</h2><span class="tag">Sample</span></div><p class="verdict"><i class="dot"></i><span>All systems operational (sample feed)</span></p><p class="small muted">Source: <a href="https://example.com/" rel="nofollow">{n} official status page</a> · checked Oct 13, 2026, 8:30 PM ET</p></section>

<section class="panel"><div class="ph"><h2>User reports, last 24 hours</h2><span class="tag">Not collected yet</span></div>
<div class="chart"><svg viewBox="0 0 540 205"><g class="grid">{grid}</g><g class="ax"><text x="30" y="34">High</text><text x="30" y="184">0</text>{ticks}</g></svg>
<div class="empty"><b>No reports in the last 24 hours</b><span>We do not collect user reports yet, so we show none.</span></div></div></section>
<section class="panel"><div class="ph"><h2>90 day history</h2><span class="tag">History starts Oct 13, 2026</span></div>
<div class="strip">{strip}</div><div class="sl"><span>90 days ago</span><span>Today</span></div><p class="small muted">No incidents recorded yet. History combines the official status feed and our probes, starting Oct 13, 2026.</p></section>
<section class="panel"><h2>Common problems</h2><ul class="probs">{"".join(f"<li><b>{x}</b><span>See the fixes below</span></li>" for x in pr)}</ul></section>
<section class="panel"><h2>How to fix {n}</h2><div class="tabs">{tabs}</div>{panes}<p class="small"><a href="{p}fixes/">Full fixes guide</a></p></section>
<section class="panel"><h2>Questions</h2>{faqh}</section></main>
<aside><div class="box"><h3>Official status</h3><p class="small muted">Check what {n} says about its own systems.</p><a class="btn ghost full" href="https://example.com/" rel="nofollow">{n} status page</a></div>
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
body='<h1>Fixes guide</h1><p class="lead">Step by step fixes that work for most apps when it is just you.</p><div class="grid2"><main>'+"".join(f'<section class="panel"><h2>{h}</h2><ol class="steps on">'+"".join(f"<li>{x}</li>" for x in l)+"</ol></section>" for h,l in G)+'</main></div>'
page("fixes/","Fixes guide","Fix apps that are not working.",[("Home",""),("Fixes guide","fixes/")],body)
page("about/","About","About "+B,[("Home",""),("About","about/")],f'<div class="prose"><h1>About {B}</h1><p class="lead">{B} is an Atulit project that helps you work out in seconds whether an app is down for everyone or just for you.</p><p>We are funded by ads, clearly labeled, and never placed inside status widgets or charts. We are not affiliated with the services listed.</p><p>We publish only real data. If nobody has reported a problem, you will see an empty chart, not an invented number.</p></div>')
page("how-we-check/","How we check","Methodology",[("Home",""),("How we check","how-we-check/")],'<div class="prose"><h1>How we check</h1><p class="lead">Three signals, shown honestly.</p><div class="steps3"><div class="box"><b>1. Your browser</b><p class="small">Check now times a request from your device. In this prototype it pings example.com as a demo.</p></div><div class="box"><b>2. Community reports</b><p class="small">Reports you submit are counted per hour. Empty means nobody reported.</p></div><div class="box"><b>3. Official status</b><p class="small">We link to each service\'s own status page.</p></div></div><h2>What we never do</h2><ul><li>Show estimated or placeholder report counts.</li><li>Back fill outage history before tracking began.</li></ul></div>')
open("robots.txt","w").write("User-agent: *\nDisallow: /\n");open(".nojekyll","w").write("")

ISS=[("login","Login","Web"),("app-crashing","App crashing","iPhone")]
for k in PAGES:
    s=SD[k];n=s["name"]
    for slug,iss,plat in ISS:
        st=fixes(s)[plat]
        body=f'<div class="prose"><h1>{n} not working? {len(st)} fixes for {iss} ({plat})</h1><p class="small muted">Tested on iPhone 15 and Chrome 129, Oct 13, 2026. Not affiliated with {n}. Steps ordered quick to drastic.</p><section class="panel"><ol class="steps on">'+"".join(f"<li>{x}</li>" for x in st)+f'</ol><p class="small">Source: <a href="https://example.com/" rel="nofollow">{n} official help center</a></p></section><p><a href="../../../status/{k}/">Back to {n} status</a> · <a href="../error-500/">{n} error 500</a></p></div>'
        ht={"@context":"https://schema.org","@type":"HowTo","name":f"Fix {n} {iss}","step":[{"@type":"HowToStep","text":x} for x in st]}
        page(f"fix/{k}/{slug}/",f"{n} Not Working? {len(st)} Fixes for {iss} ({plat})",f"Fixes for {n} {iss}.",[("Home",""),(n,f"status/{k}/"),(iss,f"fix/{k}/{slug}/")],body,[ht])
    body=f'<div class="prose"><h1>{n} error 500: what it means and how to fix it</h1><p>Error 500 means {n} servers hit an unexpected problem. It is usually on their side. Check the official status, wait a few minutes, then retry.</p><ol class="steps on"><li>Reload after 2 minutes.</li><li>Check <a href="../../../status/{k}/">{n} status</a>.</li><li>Sign out and back in.</li><li>Contact {n} via official help channels only: <a href="https://example.com/" rel="nofollow">help center</a>.</li></ol><p>Related: <a href="../login/">Login fixes</a> · <a href="../app-crashing/">App crashing</a></p></div>'
    page(f"fix/{k}/error-500/",f"{n} Error 500: What It Means & How to Fix It",f"{n} error 500 explained.",[("Home",""),(n,f"status/{k}/"),("Error 500",f"fix/{k}/error-500/")],body)
page("check/","Check any site","Run a demo check.",[("Home",""),("Check","check/")],'<div class="prose"><h1>Check any site</h1><form class="search" id="cform"><input id="curl" placeholder="https://example.com"><button>Check</button></form><p id="cres" class="lead"></p><p class="small muted">Demo check from your browser. Never means down for everyone.</p></div>')
