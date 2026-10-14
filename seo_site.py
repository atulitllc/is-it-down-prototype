"""DownFixer SEO config. INDEXABLE gates robots meta and sitemap for the whole site."""
import os, re, shutil, sys
INDEXABLE = False
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT); import seo
LOGOS = "/workspace/atulit-logos/downfixer"

def crumbs(ctx):
    ce = seo.crumbs_el(ctx["soup"]); return [seo.norm(a.get_text()) for a in ce.find_all("a")] if ce else []

def hook(ctx):
    p, s, paths = ctx["path"], ctx["soup"], ctx["paths"]
    seg = p.strip("/").split("/") if p else []
    if p == "": return dict(titles=["Is It Down or Just You? Live Checks & Fixes"])
    if seg[0] == "status" and len(seg) == 2:
        n = re.sub(r"^Is (.*) down\?$", r"\1", ctx["h1"]); n = re.sub(r"^Is (.*) Down Right Now\? Status & Fixes$", r"\1", n)
        t = f"Is {n} Down Right Now? Status & Fixes"
        rel = [q for q in paths if q.startswith(f"fix/{seg[1]}/")] + [q for q in paths if q.startswith("status/") and q != p]
        return dict(titles=[t, f"Is {n} Down Right Now? Status"], h1=t, related=rel[:8],
                    desc=f"Is {n} down right now? Run a live check from your browser, open the official {n} status page, and follow fixes for web, iPhone and Android.")
    if seg[0] == "fix":
        n = crumbs(ctx)[1] if len(crumbs(ctx)) > 1 else seg[1]
        rel = [q for q in paths if q.startswith(f"fix/{seg[1]}/") and q != p] + [f"status/{seg[1]}/", "errors/500/"] + [q for q in paths if q.startswith("fix/") and q.endswith(f"/{seg[2]}/") and q != p]
        return dict(titles=[ctx["h1"], f"{n} {seg[2].replace('-', ' ').title()} Fixes"], related=rel[:8])
    if seg[0] == "errors":
        return dict(titles=["Error 500 Internal Server Error: What It Means", "Error 500: What It Means"], related=[q for q in paths if q.endswith("/error-500/")][:8])
    if seg[0] == "check":   # /check?url= tool page: noindex, canonical to hub
        return dict(index=False, canonical="", titles=["Check Any Site"], desc="Run a quick demo check of any website from your own browser. One check never proves a site is down for everyone, so also read the official status page.")
    if seg[0] == "category":
        t = f"{ctx['h1'].replace(' status', '').replace(' Apps Status: Is It Down?', '')} Apps Status: Is It Down?"
        return dict(titles=[t], h1=t)
    if p == "fixes/":
        t = "Fixes Guide: What to Try When an App Is Not Working"
        return dict(titles=[t, "Fixes Guide: When an App Is Not Working"], h1=t)
    return dict(titles=[ctx["h1"]])

def build():
    for a, b in [("favicon.svg", "favicon.svg"), ("favicon-32.png", "favicon-32.png"), ("icon-180.png", "apple-touch-icon.png"), ("icon-512.png", "icon-512.png")]:
        shutil.copy(f"{LOGOS}/{a}", f"{ROOT}/img/brand/{b}")
    site = seo.Site(ROOT, "DownFixer", "downfixer.com", "is-it-down-prototype", INDEXABLE, "Oct 13, 2026", "2026-10-13",
        "Independent status checks by Atulit. Not affiliated with any service listed. Status read from official status pages.",
        f"{LOGOS}/wordmark-1200.png", "img/brand/icon-512.png",
        ["Official status pages.", "Updated Oct 13, 2026.", "From DownFixer.", "Not affiliated with any service listed.", "Free and independent.", "No fake counts.", "Live official status.", "Fixes for web, iPhone and Android."], hook)
    return seo.run(site)
if __name__ == "__main__": build()
