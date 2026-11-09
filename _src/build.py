import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/lixard-wow/"
CF = "https://www.curseforge.com/projects/"

ADDONS = [
    dict(name="LixardUI", status="dev", repo="LixardUI", cf=None, guide="lixardui/", cmd="/lui", game="Retail · Forever",
         desc="A complete replacement for the game's interface in one look: unit, party and raid frames, action bars, bags, chat, minimap, world map and quest tracker, tooltips, info bars, skins for Blizzard's windows and an addon manager."),
    dict(name="Plateau", status="beta", repo="Plateau", cf="1749349", guide="plateau/", cmd="/plt", game="Retail · Forever",
         desc="Fast, readable enemy nameplates built for Midnight's addon rules. Cast bars that follow your interrupt, threat colors for your role, enemy type colors, and a settings window where you click and drag a live sample plate."),
    dict(name="Keyfolio", status="released", repo="Keyfolio", cf="1769983", guide=None, cmd="/kf", game="Retail",
         desc="Every character's Mythic+ week in one window: Great Vault, keystone, best runs, crests, raid lockouts, weekly quests, currencies and gold, plus your party's keys and dungeon loot."),
    dict(name="Profession Knowledge Treasures", status="released", repo="ProfessionKnowledgeTreasures", cf="1488283", guide="profession-knowledge-treasures/", cmd="/pkt", game="Retail",
         desc="Routes you to every profession knowledge treasure in Midnight for your own professions, moves the waypoint on as you loot, suggests portals, and walks you through the Darkmoon Faire quests."),
    dict(name="CharacterStats", status="released", repo="CharacterStats", cf="1386469", guide="characterstats/", cmd="/cs", game="Retail · Forever · MoP Classic",
         desc="Your item level and stats in a small on-screen panel, a stat list and gear details on the character window, and a quick way to share your stats in chat."),
    dict(name="HealerMana", status="released", repo="HealerMana", cf="1647742", guide="healermana/", cmd="/healermana", game="Retail",
         desc="The mana of every healer in your group or raid in one small display, so you can see who is running low before the pull."),
    dict(name="SmartAssist", status="released", repo="SmartAssist", cf="1508635", guide="smart-assist/", cmd="/smartassist", game="Retail",
         desc="Keeps your Misdirection, Tricks of the Trade or Power Infusion macro pointed at the right player, switching to the tank by itself when you join a group."),
    dict(name="Auto Expansion Filter", status="released", repo="AutoExpansionFilter", cf="1450270", guide="auto-expansion-filter/", cmd="/aef", game="Retail",
         desc="Ticks “Current Expansion Only” for you every time you open the Auction House or the Crafting Orders browser."),
    dict(name="Spellscript", status="dev", repo="Spellscript", cf=None, guide=None, cmd="/sps", game="Retail",
         desc="A macro editor that checks your macro as you type, explains every line in plain English, shows what it would do right now, keeps every version, and has a library of popular macros for each spec."),
    dict(name="Pub", status="dev", repo="Pub", cf=None, guide=None, cmd="/pub", game="Retail · Forever",
         desc="A friends window that shows who is free to play right now, remembers every character your Battle.net friends play, and keeps a history of everyone you've grouped with."),
    dict(name="ErrorLens", status="dev", repo="ErrorLens", cf=None, guide=None, cmd="/errorlens", game="Retail · Forever",
         desc="A cleaner error window for BugGrabber: search, filters, ignore, copying that stays safe when an error repeats, and a one-click wipe."),
    dict(name="FocusControl", status="dev", repo="FocusControl", cf=None, guide=None, cmd="/fc", game="Retail · Forever",
         desc="Builds a focus-and-mark macro and an interrupt-your-focus macro for your class, set up per character."),
    dict(name="Debrief", status="dev", repo="Debrief", cf=None, guide=None, cmd="/debrief", game="Retail",
         desc="A post-fight coach: after a pull, boss or key it compares your presses with SimulationCraft's priority list, with a timeline, graphs, an opener check and concrete tips."),
    dict(name="Ultimate Keystone Reminder", status="dev", repo="UltimateKeystoneReminder", cf=None, guide=None, cmd="/ukr", game="Retail",
         desc="Shows your party's keystones, reminds you to change your key after a dungeon, and lists whose key fits the dungeon on ready check."),
    dict(name="QuietDungeon", status="dev", repo="QuietDungeon", cf=None, guide=None, cmd="/quietdungeon", game="Retail",
         desc="Hides Blizzard's popups, banners and toasts while you're inside a dungeon."),
    dict(name="CraftersMark", status="dev", repo="CraftersMark", cf=None, guide=None, cmd=None, game="Retail",
         desc="Finds crafters for an item and predicts the crafting quality you'll get, including inspiration chances."),
    dict(name="Fieldtest", status="dev", repo="Fieldtest", cf=None, guide=None, cmd="/ft", game="Retail · Forever",
         desc="In-game test checklists for any addon: tick what works, note what doesn't, then copy the results or save a log."),
]

PUBLIC = {"Plateau", "CharacterStats", "HealerMana", "SmartAssist", "ProfessionKnowledgeTreasures", "AutoExpansionFilter"}

TAG = {"released": ("Released", "tag-released"), "beta": ("Beta", "tag-beta"), "dev": ("In development", "tag-dev")}

GH_ICON = '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
CF_ICON = '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M1 5h9.5c1.2-1.6 3-2.4 5.5-2.5v1.8c-1.6.1-2.4.6-3 1.4.9.8 1.4 1.9 1.4 3.2 0 1.7-1 3-2.6 3.6v1.5H4.2V12c-1.5-.6-2.3-1.7-2.5-3.4H1z"/></svg>'
ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 8h9M8.5 4l4 4-4 4"/></svg>'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&amp;family=Source+Sans+3:wght@400;600;700&amp;family=JetBrains+Mono&amp;display=swap" rel="stylesheet">'


def header(current):
    nav = [("/#addons", "Addons"), ("/#install", "Install"), (GH, "GitHub")]
    links = "".join(f'<a href="{h}"{" aria-current=page" if l == current else ""}>{l}</a>' for h, l in nav)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><span class="slit" aria-hidden="true"></span><span class="brand-name">Lixard</span><span class="brand-sub">WoW addons</span></a>
    <nav class="site-nav" aria-label="Site">{links}</nav>
  </div>
  <div class="scutes" aria-hidden="true"></div>
</header>'''


FOOTER = '''<footer class="site-footer">
  <div class="wrap">
    <p>Made by Lixard &middot; <a href="https://github.com/lixard-wow">github.com/lixard-wow</a></p>
    <p>World of Warcraft is a trademark of Blizzard Entertainment. These addons are not affiliated with or endorsed by Blizzard.</p>
  </div>
</footer>'''


def page(title, desc, body, current=None, script=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="color-scheme" content="dark">
{FONTS}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css?v=5">
</head>
<body>
{header(current)}
{body}
{FOOTER}
{script}
</body>
</html>
'''


def card(a):
    label, cls = TAG[a["status"]]
    name = html.escape(a["name"])
    title = f'<a href="/{a["guide"]}">{name}</a>' if a["guide"] else name
    meta = [f'<li>{a["game"]}</li>']
    if a["cmd"]:
        meta.append(f'<li><code>{a["cmd"]}</code></li>')
    links = []
    if a["guide"]:
        links.append(f'<a class="btn btn-main" href="/{a["guide"]}">Guide {ARROW}</a>')
    if a["repo"] in PUBLIC:
        links.append(f'<a class="btn" href="{GH}{a["repo"]}">{GH_ICON} GitHub</a>')
    if a["cf"]:
        links.append(f'<a class="btn" href="{CF}{a["cf"]}">{CF_ICON} CurseForge</a>')
    return f'''      <article class="addon panel" data-status="{a["status"]}">
        <span class="slit marker" aria-hidden="true"></span>
        <div class="addon-top"><h3>{title}</h3><span class="tag {cls}">{label}</span></div>
        <ul class="meta">{"".join(meta)}</ul>
        <p>{html.escape(a["desc"])}</p>
        <div class="links">{"".join(links)}</div>
      </article>'''


def home():
    counts = {k: sum(1 for a in ADDONS if a["status"] == k) for k in TAG}
    filters = [("all", "All", len(ADDONS))] + [(k, TAG[k][0], counts[k]) for k in ("released", "beta", "dev")]
    fbtn = "".join(f'<li><button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}<span class="count">{n}</span></button></li>' for k, l, n in filters)
    cards = "\n".join(card(a) for a in ADDONS)
    body = f'''<main id="main">
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow"><span class="slit" aria-hidden="true"></span>World of Warcraft addons</p>
      <h1>Addons by Lixard</h1>
      <p class="lede">Free addons for retail World of Warcraft and WoW Forever, from single-job tools to a complete interface. Every one is open on GitHub; the released ones are also on CurseForge.</p>
    </div>
  </section>

  <div class="wrap">
    <div class="section-head" id="addons"><h2>The addons</h2></div>
    <ul class="filters" aria-label="Show">{fbtn}</ul>
    <div class="addon-grid">
{cards}
    </div>

    <div class="section-head" id="install"><h2>Installing</h2></div>
    <div class="install">
      <div class="panel"><h3><span class="num">1</span>CurseForge app</h3><p>For released addons: search the name in the World of Warcraft section and click Install. Updates arrive by themselves.</p></div>
      <div class="panel"><h3><span class="num">2</span>From GitHub</h3><p>On the addon's GitHub page click <strong>Code</strong>, then <strong>Download ZIP</strong>, and copy the addon folders from the zip into <code>_retail_\\Interface\\AddOns</code>.</p></div>
      <div class="panel"><h3><span class="num">3</span>In game</h3><p>Restart the game the first time, then tick the addon in the AddOns list on the character screen. After updates, <code>/reload</code> is enough.</p></div>
    </div>
  </div>
</main>'''
    script = '''<script>
document.querySelectorAll(".filters button").forEach(function (b) {
  b.addEventListener("click", function () {
    var f = b.dataset.filter;
    document.querySelectorAll(".filters button").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
    document.querySelectorAll(".addon").forEach(function (c) { c.hidden = f !== "all" && c.dataset.status !== f; });
  });
});
</script>'''
    return page("Lixard's WoW Addons", "Free World of Warcraft addons by Lixard, with guides and GitHub links.", body, "Addons", script)


def parse(slug):
    raw = open(os.path.join(HERE, "guides", slug + ".html"), encoding="utf-8").read()
    head, body = raw.split("-->", 1)
    meta = {}
    for line in head.replace("<!--meta", "").strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    toc = re.findall(r'<section id="([^"]+)"[^>]*data-toc="([^"]+)"', body)
    return meta, toc, body.strip()


def guide(a):
    slug = a["guide"].strip("/")
    meta, toc, body = parse(slug)
    label, cls = TAG[a["status"]]
    acts = []
    if a["repo"] in PUBLIC:
        acts.append(f'<a class="btn btn-main" href="{GH}{a["repo"]}">{GH_ICON} GitHub</a>')
    cf = meta.get("curseforge", "none")
    if cf and cf != "none" and a["status"] != "dev":
        acts.append(f'<a class="btn{"" if acts else " btn-main"}" href="{CF}{cf}">{CF_ICON} CurseForge</a>')
    if any(t[0] == "install" for t in toc):
        acts.append('<a class="btn" href="#install">How to install</a>')
    facts = [("Command", f'<code>{html.escape(meta["command"])}</code>' if meta.get("command") and meta["command"] != "none" else None),
             ("Game", html.escape(meta.get("game", ""))),
             ("Version", html.escape(meta.get("version", "")) if a["status"] != "dev" else None),
             ("Language", "English")]
    facts_html = "".join(f"<li><span>{k}</span>{v}</li>" for k, v in facts if v)
    toc_html = "".join(f'<li><a href="#{i}">{html.escape(l)}</a></li>' for i, l in toc)
    page_body = f'''<main id="main">
  <section class="guide-hero">
    <div class="wrap">
      <p class="eyebrow"><span class="slit" aria-hidden="true"></span>User guide <span class="tag {cls}" style="margin-left:6px">{label}</span></p>
      <h1>{html.escape(meta["title"])}</h1>
      <p class="lede">{html.escape(meta["lede"])}</p>
      <div class="actions">{"".join(acts)}</div>
      <ul class="facts">{facts_html}</ul>
    </div>
  </section>
  <div class="wrap guide">
    <aside class="toc"><nav aria-label="On this page"><p>On this page</p><ol>{toc_html}</ol></nav></aside>
    <div class="guide-body">
{body}
    </div>
  </div>
</main>'''
    script = '''<script>
var links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
var secs = links.map(function (a) { return document.querySelector(a.getAttribute("href")); });
function mark() {
  var i = 0;
  secs.forEach(function (s, n) { if (s && s.getBoundingClientRect().top < 140) i = n; });
  links.forEach(function (a, n) { a.classList.toggle("on", n === i); });
}
addEventListener("scroll", mark, { passive: true }); mark();
</script>'''
    return slug, page(meta["title"] + " guide · Lixard's WoW Addons", meta["lede"], page_body, None, script)


def notfound():
    body = '''<main id="main"><section class="hero"><div class="wrap">
      <p class="eyebrow"><span class="slit" aria-hidden="true"></span>404</p>
      <h1>Page not found</h1>
      <p class="lede">That page doesn't exist. Some guides moved when the site was redone.</p>
      <div class="actions" style="margin-top:22px"><a class="btn btn-main" href="/">All addons</a></div>
    </div></section></main>'''
    return page("Page not found · Lixard's WoW Addons", "Page not found.", body)


OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline=chr(10)).write(text)

write("index.html", home())
write("404.html", notfound())
n = 0
for a in ADDONS:
    if a["guide"] and os.path.exists(os.path.join(HERE, "guides", a["guide"].strip("/") + ".html")):
        slug, text = guide(a)
        write(os.path.join(slug, "index.html"), text)
        n += 1
print("ok", len(ADDONS), "addons,", n, "guides ->", OUT)
