#!/usr/bin/env python3
"""Builds the Kennedy & Smith Mechanical site.

    python3 src/build.py            writes the pages into the repo root (what Cloudflare serves)
    python3 src/build.py --bundle   also writes preview/index.html, every page in one file,
                                    for places that cannot host several pages or load Housecall Pro

Copy and settings are in content.py. This file is layout only.
"""
import html
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import SITE, OWNERS, TO_CONFIRM, SERVICES, AREA_PAGES, AREAS_SHORT, JOBS, HOME_JOBS  # noqa: E402
from areamap import area_map_svg  # noqa: E402

BOOK_URL = f"https://book.housecallpro.com/book/{SITE['hcp_org']}/{SITE['hcp_book_token']}?v2=true"
LEAD_URL = f"https://book.housecallpro.com/lead-form/{SITE['hcp_org']}/{SITE['hcp_lead_token']}"
HCP_SCRIPT = f"https://online-booking.housecallpro.com/script.js?token={SITE['hcp_book_token']}&orgName={SITE['hcp_org']}"
FONTS = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&display=swap"
TEL = SITE["phone_display"]
TEL_HREF = "tel:" + SITE["phone_tel"]
E = html.escape

ICONS = {
    "wrench": '<path d="M15.2 3.6a4.6 4.6 0 0 0-4.3 6.2L4 16.7V20h3.3l6.9-6.9a4.6 4.6 0 0 0 6.2-4.3l-3 1.1-2.1-2.1z"/>',
    "tank": '<rect x="7" y="3" width="10" height="16"/><path d="M9 19v2M15 19v2M10 7h4"/><path d="M12 10.5c1.1 1.3 1.7 2.1 1.7 3a1.7 1.7 0 0 1-3.4 0c0-.9.6-1.7 1.7-3z"/>',
    "hvac": '<rect x="4" y="4" width="16" height="16"/><circle cx="12" cy="12" r="5"/><path d="M12 7v10M7 12h10"/>',
    "drop": '<path d="M12 3.5l4.2 6.2a5.2 5.2 0 1 1-8.4 0z"/>',
    "flame": '<path d="M12 3c.6 3.2 5 5.2 5 10.2A5 5 0 0 1 7 13.2c0-1.9.9-3.1 2-4.1.1 1.8.9 2.9 2 3 .2-3-.6-5.400 1-9.100z"/>',
    "snow": '<path d="M12 2.5v19M3.800 7.200l16.400 9.600M20.200 7.200L3.800 16.800"/><path d="M9.500 4.500L12 7l2.500-2.500M9.500 19.500L12 17l2.500 2.500"/>',
    "alert": '<path d="M12 3.500L21.500 20h-19z"/><path d="M12 10v4.500M12 17v.600"/>',
    "plan": '<rect x="4" y="5" width="16" height="15"/><path d="M4 10h16M8 3v4M16 3v4M9 15l2 2 4-4"/>',
    "phone": '<path d="M5 4h4l2 5-2.600 1.600a11 11 0 0 0 5 5L15 13l5 2v4c0 .600-.400 1-1 1A15 15 0 0 1 4 5c0-.600.400-1 1-1z"/>',
    "cal": '<rect x="4" y="5" width="16" height="15"/><path d="M4 10h16M8 3v4M16 3v4"/>',
}


def icon(name, box=False):
    svg = f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9">{ICONS[name]}</svg>'
    return f'<span class="ico">{svg}</span>' if box else svg


def book(label="Book online", cls="btn btn--red"):
    return f'<a class="{cls}" href="{BOOK_URL}" data-book target="_blank" rel="noopener">{label}</a>'


def call(cls="btn btn--line", label=None):
    return f'<a class="{cls}" href="{TEL_HREF}">{icon("phone")}{label or "Call " + TEL}</a>'


# ---------------------------------------------------------------- shared chrome

NAV = [("services", "Services"), ("service-areas", "Service areas"), ("about", "About"), ("contact", "Contact")]
NAV_GROUP = {s["slug"]: "services" for s in SERVICES}
NAV_GROUP.update({a["slug"]: "service-areas" for a in AREA_PAGES})
BASE = f"{SITE['town']}, {SITE['state']}"


def href(slug):
    return "index.html" if slug == "home" else slug + ".html"


def header(current):
    cur = NAV_GROUP.get(current, current)
    here = ' aria-current="page"'
    links = "".join(f'<a href="{href(s)}" data-nav="{s}"{here if s == cur else ""}>{t}</a>' for s, t in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="util"><div class="wrap util__in">
  <span>Serving {AREAS_SHORT}</span>
  <span class="util__r"><span>{SITE['hours']}</span><a href="about.html">Owner-operated in {BASE}</a></span>
</div></div>
<header class="head"><div class="wrap head__in">
  <a class="logo" href="index.html"><img src="img/ks-logo.webp" width="520" height="253" alt="Kennedy &amp; Smith Mechanical"></a>
  <nav class="nav" id="nav" aria-label="Main">{links}</nav>
  <div class="head__cta">
    <a class="tel" href="{TEL_HREF}"><small>Call us</small><b>{TEL}</b></a>
    {book(cls="btn btn--red btn--sm")}
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</div></header>"""


def footer():
    lic = []
    if SITE["pa_hic"]:
        lic.append(f"PA Home Improvement Contractor #{E(SITE['pa_hic'])}")
    elif SITE["preview"]:
        lic.append("PA Home Improvement Contractor # to be added")
    lic += [E(x) for x in SITE["other_licenses"]]
    lic.append("Insured")
    svc = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    areas = "".join(f'<li><a href="{a["slug"]}.html">{a["name"]}</a></li>' for a in AREA_PAGES)
    mails = "".join(f'<li><a href="mailto:{o["email"]}">{o["email"]}</a><span class="foot__sub">{o["trade"]}</span></li>' for o in OWNERS)
    return f"""<footer class="foot"><div class="wrap">
  <div class="foot__grid">
    <div>
      <img class="foot__logo" src="img/ks-logo-light.webp" width="520" height="253" alt="Kennedy &amp; Smith Mechanical">
      <p>Owner-operated plumbing and HVAC, based in {SITE['town']}. Serving {AREAS_SHORT}.</p>
      <p class="foot__lic">{"<br>".join(lic)}</p>
    </div>
    <div>
      <h4>Services</h4>
      <ul>{svc}</ul>
    </div>
    <div>
      <h4>Service areas</h4>
      <ul>{areas}<li><a href="service-areas.html">Full map and town list</a></li></ul>
      <h4 style="margin-top:22px">Company</h4>
      <ul><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li></ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul>
        <li><a href="{TEL_HREF}">{TEL}</a></li>
        {mails}
        <li>{SITE['hours']}</li>
        <li>{BASE}</li>
      </ul>
    </div>
  </div>
  <div class="foot__base"><span>&copy; <span data-year>2026</span> Kennedy &amp; Smith Mechanical</span><span>Online booking by Housecall Pro. Site by Adaptive AI Services.</span></div>
</div></footer>
<div class="mobar"><a href="{TEL_HREF}">{icon("phone")}Call</a><a href="{BOOK_URL}" data-book target="_blank" rel="noopener">{icon("cal")}Book online</a></div>"""


def preview_drawer():
    if not SITE["preview"]:
        return ""
    items = "".join(f"<li><div><b>{E(t)}</b><span>{E(d)}</span></div></li>" for t, d in TO_CONFIRM)
    return f"""<button class="pv-btn" type="button" data-pv-open>Preview build <b>{len(TO_CONFIRM)} to confirm</b></button>
<div class="pv" id="pv" hidden>
  <div class="pv__panel" role="dialog" aria-modal="true" aria-labelledby="pv-h">
    <div class="pv__top"><div><p class="label">Preview build</p><h2 class="h3" id="pv-h">Before this goes live</h2></div><button class="pv__x" type="button" data-pv-close aria-label="Close">&times;</button></div>
    <p class="grey small">This list is only on the preview. It comes off when the site launches. Each item is something only the owner can answer.</p>
    <ol>{items}</ol>
  </div>
</div>"""


def book_band(h, p):
    return f"""<section class="book"><div class="wrap book__in">
  <div><p class="label label--tan">Schedule service</p><h2 class="h2">{h}</h2><p>{p}</p></div>
  <div class="book__act">
    {book()}
    <a class="book__tel" href="{TEL_HREF}"><small>Or call</small>{TEL}</a>
    <p class="book__by">Online booking runs on Housecall Pro</p>
  </div>
</div></section>"""


# ---------------------------------------------------------------- job photos

def job_img(key, sizes, lazy=True):
    """One of the owners' job photos (see JOBS in content.py), in two sizes."""
    j = JOBS[key]
    w, h = j.get("shape", (1200, 1500))
    lz = ' loading="lazy"' if lazy else ""
    return (f'<img src="img/job-{key}.webp" srcset="img/job-{key}-600.webp 600w, img/job-{key}.webp 1200w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{E(j["alt"])}"{lz}>')


def job_cap(key):
    j = JOBS[key]
    return f'<b>{E(j["title"])}</b><span>{E(j["text"])}</span>'


def jobs_grid(keys, links=None):
    """A ruled row of captioned job photos. With links, each cell goes to a service page."""
    sizes = "(max-width: 700px) 50vw, 300px" if len(keys) > 3 else "(max-width: 700px) 100vw, 400px"
    cells = ""
    for i, k in enumerate(keys):
        fig = f'<figure>{job_img(k, sizes)}<figcaption>{job_cap(k)}</figcaption></figure>'
        cells += f'<a class="job" href="{links[i]}.html">{fig}</a>' if links else f'<div class="job">{fig}</div>'
    return f'<div class="jobs jobs--{len(keys)}">{cells}</div>'


def phead(crumbs, h1, lede, photo=None, buttons=True):
    trail = '<a href="index.html">Home</a>' + "".join(
        f' <span>/</span> <a href="{u}">{t}</a>' if u else f" <span>/</span> <span>{t}</span>" for t, u in crumbs)
    pic = f'<figure class="photo photo--tall">{job_img(photo, "(max-width: 860px) 90vw, 420px", lazy=False)}</figure>' if photo else ""
    btns = f'<div class="btns">{book()}{call()}</div>' if buttons else ""
    cls = "phead on-dark" + ("" if photo else " phead--plain")
    return f"""<section class="{cls}"><div class="wrap phead__in">
  <div><nav class="crumb" aria-label="Breadcrumb">{trail}</nav><h1 class="h1">{h1}</h1><p class="lede">{lede}</p>{btns}</div>
  {pic}
</div></section>"""


STEPS_HEAD = '<div class="sec-head sec-head--one"><div><p class="label">How a job goes</p><h2 class="h2">Three steps, no surprises</h2></div></div>'
STEPS = """<ol class="steps">
  <li><h3 class="h3">Book or call</h3><p>Pick a time online or call. One of us comes out and looks at what you have now.</p></li>
  <li><h3 class="h3">You get a price</h3><p>We explain the options in plain words and price each one. Nothing starts until you say go.</p></li>
  <li><h3 class="h3">We install it</h3><p>An owner does the work, tests it, shows you how it runs and takes the old equipment away.</p></li>
</ol>"""


def faq_block(faqs):
    items = "".join(f"<details><summary>{E(q)}</summary><div><p>{E(a)}</p></div></details>" for q, a in faqs)
    return f'<div class="faq">{items}</div>'


# ---------------------------------------------------------------- pages

def page_home():
    bob, joe = OWNERS
    cards = ""
    for s in SERVICES:
        pts = "".join(f"<li>{p}</li>" for p in s["card_points"])
        cards += f'<a class="cat__c" href="{s["slug"]}.html">{icon(s["icon"], True)}<h3 class="h3">{s["name"]}</h3><p>{s["card"]}</p><ul>{pts}</ul><span class="more">{s["name"]}</span></a>'
    triage = "".join(f'<a href="{s["slug"]}.html"><div>{s["triage"][0]}<span>{s["triage"][1]}</span></div></a>' for s in SERVICES)
    return f"""<section class="hero on-dark"><div class="wrap hero__in">
  <div>
    <p class="label">{BASE} &middot; Delaware County &middot; The Main Line</p>
    <h1 class="h1">Heating, cooling and water systems, installed by the owners</h1>
    <p class="lede">Kennedy &amp; Smith Mechanical is {bob['name']}, a master plumber, and {joe['name']}, a senior HVAC technician. We replace heating and cooling systems, install water heaters and fit water filtration and softeners in homes across {AREAS_SHORT}.</p>
    <div class="btns">{book()}{call()}</div>
    <ul class="hero__facts"><li>PA contractor #{E(SITE['pa_hic'])}</li><li>Owner-operated</li><li>Price before work starts</li></ul>
  </div>
  <aside class="triage" aria-label="Start from what you need">
    <div class="triage__h">What do you need?</div>
    {triage}
    <a class="is-red" href="{TEL_HREF}"><div>Rather talk it through?<span>Call {TEL}, {SITE['hours']}</span></div></a>
  </aside>
</div></section>

<section class="strip"><div class="wrap strip__in">
  <div class="strip__c"><h3>Owner-operated</h3><p>Bob or Joe prices your job and does the work.</p></div>
  <div class="strip__c"><h3>Registered &amp; insured</h3><p>PA Home Improvement Contractor #{E(SITE['pa_hic'])}.</p></div>
  <div class="strip__c"><h3>Price before work</h3><p>You see the number and approve it before we pick up a tool.</p></div>
  <div class="strip__c"><h3>Book online any time</h3><p>Pick a slot from your phone. Confirmation comes by text or email.</p></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><p class="label">What we do</p><h2 class="h2">A short list, done properly</h2></div><p class="lede grey">We are a two-man shop, so we stick to the installs we do best: heating and cooling systems, water heaters and water treatment.</p></div>
  <div class="cat">{cards}</div>
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head"><div><p class="label">Our work</p><h2 class="h2">Every photo here is a job we did</h2></div><p class="lede grey">No stock pictures. These are our own installs, in customers' homes.</p></div>
  {jobs_grid([k for k, _ in HOME_JOBS], [s for _, s in HOME_JOBS])}
</div></section>

<section class="sec"><div class="wrap">
  {STEPS_HEAD}
  {STEPS}
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head"><div><p class="label">Where we work</p><h2 class="h2">Delaware County and the Main Line</h2></div><p class="lede grey">We are based in {SITE['town']} and work in the towns around us, across Delaware County and out along the Main Line.</p></div>
  <div class="area">
    {map_block()}
    <div class="towns">
      {towns_block(link=True)}
      <p><a class="more" href="service-areas.html">Full town list</a></p>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap split">
  <div>
    <p class="label">About the shop</p>
    <h2 class="h2">Two owners, no call center</h2>
    <p class="lede grey" style="margin-top:16px">Bob is a master plumber and Joe is a senior HVAC technician. They started Kennedy &amp; Smith in {SITE['town']} to take on fewer jobs and do each one properly.</p>
    <ul class="ticks"><li>You deal with an owner from the first call to the finished job</li><li>A price you approve before work starts</li><li>Plain talk about your options, and no upselling</li><li>Drop cloths down and cleanup before we leave</li></ul>
    <p style="margin-top:26px"><a class="more" href="about.html">About Kennedy &amp; Smith</a></p>
  </div>
  <figure class="photo">{job_img("ac-pair", "(max-width: 860px) 90vw, 540px")}</figure>
</div></section>

{book_band("Book a visit online", "Choose the service and a time that suits you. We confirm the appointment and send a reminder before we arrive.")}"""


def map_block():
    return f"""<div class="map">{area_map_svg()}
  <div class="map__key"><span><i style="background:#ead9bf"></i>Where we work: Delaware County and the Main Line</span><span><i class="map__home"></i>Home base: {SITE['town']}</span></div>
</div>"""


def towns_block(link=False, full=False):
    out = ""
    for a in AREA_PAGES:
        towns = a["towns"] if full else a["towns"][:9]
        more = "" if full or len(a["towns"]) <= 9 else " and more"
        lk = f'<a href="{a["slug"]}.html">About this area</a>' if link else ""
        out += f'<div><h3>{a["name"]}{lk}</h3><p>{", ".join(towns)}{more}.</p></div>'
    return out


def page_services():
    rows = ""
    for s in SERVICES:
        rows += f"""<a class="cat__c" href="{s['slug']}.html">{icon(s['icon'], True)}<h3 class="h3">{s['name']}</h3><p>{s['lede']}</p><ul>{"".join(f"<li>{x}</li>" for x in s['handle'][:5])}</ul><span class="more">{s['name']}</span></a>"""
    return phead([("Services", None)], "What we install", "Three kinds of jobs, each one done start to finish by the owners, for homes across " + AREAS_SHORT + ".") + f"""
<section class="sec"><div class="wrap"><div class="cat">{rows}</div></div></section>
<section class="sec sec--shop"><div class="wrap">
  {STEPS_HEAD}
  {STEPS}
</div></section>
{book_band("Not sure which one you need?", "Describe what is going on when you book or call. We will sort out the rest.")}"""


def page_service(s):
    handle = "".join(f"<li>{x}</li>" for x in s["handle"])
    signs = "".join(f"<div><dt>{E(t)}</dt><dd>{E(d)}</dd></div>" for t, d in s["signs"])
    others = "".join(f'<a href="{o["slug"]}.html"><h3 class="h3">{o["name"]}</h3><p>{o["card"]}</p><span class="more">{o["name"]}</span></a>' for o in SERVICES if o["slug"] != s["slug"])
    if s["side"]:
        # one more job photo, set beside the list of signs
        signs_html = f"""<div class="split split--top"><dl class="signs signs--stack">{signs}</dl>
    <div><figure class="photo photo--tall">{job_img(s['side'], "(max-width: 860px) 90vw, 540px")}</figure><p class="cap">{job_cap(s['side'])}</p></div></div>"""
    else:
        signs_html = f'<dl class="signs">{signs}</dl>'
    blocks = [
        f"""<div class="sec-head sec-head--one"><div><p class="label">{s['name']}</p><h2 class="h2">{s['handle_h']}</h2></div></div>
  <ul class="sheet">{handle}</ul>""",
        f"""<div class="sec-head sec-head--one"><div><p class="label">Know what you're looking at</p><h2 class="h2">{s['signs_h']}</h2></div></div>
  {signs_html}
  <div class="note" style="margin-top:40px"><h3 class="h3">{E(s['local'][0])}</h3><p>{E(s['local'][1])}</p></div>""",
    ]
    if s["jobs"]:
        blocks.append(f"""<div class="sec-head sec-head--one"><div><p class="label">Our work</p><h2 class="h2">{s['jobs_h']}</h2></div></div>
  {jobs_grid(s['jobs'])}""")
    blocks += [
        f"""{STEPS_HEAD}
  {STEPS}""",
        f"""<div class="sec-head sec-head--one"><div><p class="label">Common questions</p><h2 class="h2">{s['faq_h']}</h2></div></div>
  {faq_block(s['faqs'])}""",
        f"""<div class="sec-head sec-head--one"><div><p class="label">Also from Kennedy &amp; Smith</p><h2 class="h2">Other services</h2></div></div>
  <div class="acards">{others}</div>""",
    ]
    # white and grey bands alternate down the page, however many blocks this service has
    body = "\n\n".join(f'<section class="sec{" sec--shop" if i % 2 else ""}"><div class="wrap">\n  {b}\n</div></section>' for i, b in enumerate(blocks))
    return phead([("Services", "services.html"), (s["name"], None)], s["h1"], s["lede"], s["photo"]) + "\n" + body + "\n\n" + book_band(s["cta"][0], s["cta"][1])


def page_areas():
    cards = "".join(f'<a href="{a["slug"]}.html"><h3 class="h3">{a["name"]}</h3><p>{a["card"]}</p><span class="more">{a["name"]}</span></a>' for a in AREA_PAGES)
    return phead([("Service areas", None)], "Where we work", f"We are based in {SITE['town']} and work across Delaware County and the towns along the Main Line.") + f"""
<section class="sec"><div class="wrap">
  <div class="area">
    {map_block()}
    <div class="towns">
      {towns_block(link=True, full=True)}
      <div><h3>Not sure about your town?</h3><p>If you are near the edge of the map, call {TEL} and ask.</p></div>
    </div>
  </div>
</div></section>
<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">Area by area</p><h2 class="h2">Different towns, different houses</h2></div></div>
  <div class="acards">{cards}</div>
</div></section>
{book_band("In our area?", "Book online or call. If you are just outside the map, call anyway and we will tell you straight.")}"""


def page_area(a):
    facts = "".join(f"<div><dt>{E(t)}</dt><dd>{E(d)}</dd></div>" for t, d in a["facts"])
    svc = ""
    for s in SERVICES:
        svc += f'<a class="cat__c" href="{s["slug"]}.html">{icon(s["icon"], True)}<h3 class="h3">{s["name"]}</h3><p>{s["card"]}</p><span class="more">{s["name"]}</span></a>'
    return phead([("Service areas", "service-areas.html"), (a["name"], None)], a["h1"], a["lede"]) + f"""
<section class="sec"><div class="wrap split split--top">
  <div>
    <p class="label">{a['name']}</p>
    <h2 class="h2">What the houses are like</h2>
    <div class="grey" style="margin-top:18px">{"".join(f"<p>{E(p)}</p>" for p in a['body'])}</div>
  </div>
  <div class="towns"><div><h3>Towns and neighborhoods</h3><p>{", ".join(a['towns'])}.</p></div>
    <dl class="facts">{facts}</dl>
  </div>
</div></section>
<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">What we do here</p><h2 class="h2">Services {a['where']}</h2></div></div>
  <div class="cat">{svc}</div>
</div></section>
{book_band("Need someone out?", "Book a visit online or call " + TEL + ".")}"""


def page_about():
    bob, joe = OWNERS
    crew = "".join(f'<div><p class="crew__role">{E(o["role"])}</p><h3 class="h2">{E(o["name"])}</h3><p>{E(o["does"])}</p><p><a href="mailto:{o["email"]}">{o["email"]}</a></p></div>' for o in OWNERS)
    return phead([("About", None)], "About Kennedy &amp; Smith Mechanical", f"A two-man, owner-operated plumbing and HVAC company based in {SITE['town']}, Pennsylvania.", buttons=False) + f"""
<section class="sec"><div class="wrap split">
  <div>
    <p class="label">The shop</p>
    <h2 class="h2">Two owners, both on the tools</h2>
    <div class="grey" style="margin-top:18px">
      <p>Kennedy &amp; Smith Mechanical is {bob['name']} and {joe['name']}. Bob is a master plumber. Joe is a senior HVAC technician. They started the company in {SITE['town']}, and they still do the work themselves.</p>
      <p>It is two people on purpose. A small shop can take fewer jobs and give each one the time it needs, and that was the reason for starting one.</p>
      <p>When you call, you talk to an owner. The same person looks at the job, prices it and installs it. Nobody here is paid to sell you more than you need.</p>
      <p>They work in the towns they live in, often for people they know, and they would like to keep it that way.</p>
    </div>
  </div>
  <div><figure class="photo photo--tall">{job_img("boiler", "(max-width: 860px) 90vw, 540px")}</figure><p class="cap">{job_cap("boiler")}</p></div>
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">Who you will deal with</p><h2 class="h2">The owners</h2></div></div>
  <div class="crew">{crew}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">How we work</p><h2 class="h2">What you can expect</h2></div></div>
  <div class="trio">
    <div><h3 class="h3">A price first</h3><p>We look at the job, tell you what it costs and wait for your go-ahead. The price you approve is the price you pay.</p></div>
    <div><h3 class="h3">Straight answers</h3><p>You hear what your options are, including the cheaper one, and what we would do in our own house.</p></div>
    <div><h3 class="h3">A clean job</h3><p>Drop cloths go down before tools come out, and we clean up before we leave.</p></div>
  </div>
  <div class="trio" style="margin-top:24px">
    <div><h3 class="h3">Easy to reach</h3><p>Book online at any hour, or call {SITE['hours']}. You get a confirmation and a reminder.</p></div>
    <div><h3 class="h3">Registered &amp; insured</h3><p>Pennsylvania Home Improvement Contractor #{E(SITE['pa_hic'])}. We carry liability insurance and will show you proof if you ask.</p></div>
    <div><h3 class="h3">Local</h3><p>Based in {SITE['town']}. We work across {AREAS_SHORT}.</p></div>
  </div>
</div></section>
{book_band("Let's get to work", "Book a visit online or call. Either way you will be talking to an owner.")}"""


def lead_form(bundle):
    if bundle:
        inner = f"""<div class="form__stand"><h3 class="h3">The request form goes here</h3><p class="grey">On the live site this box holds the Housecall Pro request form, and what a customer sends lands in Housecall Pro as a new lead. This preview cannot embed another site, so open the form in its own tab to see it.</p><a class="btn" href="{LEAD_URL}" target="_blank" rel="noopener">Open the request form</a></div>"""
    else:
        inner = f"""<iframe id="hcp-lead-iframe" title="Request service from Kennedy &amp; Smith Mechanical" src="{LEAD_URL}" loading="lazy"></iframe>
<p class="form__alt">Form not loading? <a href="{LEAD_URL}" target="_blank" rel="noopener">Open it in a new tab</a> or call {TEL}.</p>"""
    return f'<div class="form"><div class="form__h">Request service or a quote</div>{inner}</div>'


def page_contact(bundle):
    mails = ""
    for i, o in enumerate(OWNERS):
        gap = ' style="margin-top:12px"' if i else ""
        mails += f'<dd{gap}><a href="mailto:{o["email"]}">{o["email"]}</a><small>{o["trade"]}: {o["name"]}</small></dd>'
    return phead([("Contact", None)], "Contact us", "Pick a time online and one of us will come out to price the job. If you have a question first, send the form, call or email.", buttons=False) + f"""
<section class="sec"><div class="wrap contact">
  <div>
    <dl class="clist">
      <div><dt>Phone</dt><dd><a href="{TEL_HREF}" style="color:var(--red)">{TEL}</a></dd></div>
      <div><dt>Email</dt>{mails}</div>
      <div><dt>Hours</dt><dd>{SITE['hours']}</dd></div>
      <div><dt>Service area</dt><dd>{AREAS_SHORT}<small><a href="service-areas.html">See the map and town list</a></small></dd></div>
      <div><dt>Based in</dt><dd>{BASE}</dd></div>
    </dl>
    <div style="margin-top:28px;display:grid;gap:12px;justify-items:start">
      <h3 class="h3">Know what you need?</h3>
      <p class="grey">Skip the form and pick a time.</p>
      {book()}
    </div>
  </div>
  {lead_form(bundle)}
</div></section>"""


def page_thanks():
    return phead([("Request received", None)], "Thanks. We got it.", "Your request is in. Bob or Joe will be in touch to confirm the details and set a time.", buttons=False) + f"""
<section class="sec"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">What happens next</p><h2 class="h2">Three steps from here</h2></div></div>
  <ol class="steps">
    <li><h3 class="h3">We read it</h3><p>Requests are reviewed during business hours, {SITE['hours']}.</p></li>
    <li><h3 class="h3">We call or text</h3><p>We contact you at the number you gave to confirm the job and the time.</p></li>
    <li><h3 class="h3">We show up</h3><p>One of us arrives in the window you picked to look at the job and price it.</p></li>
  </ol>
  <div class="btns" style="margin-top:40px"><a class="btn" href="index.html">Back to home</a><a class="btn btn--line" href="services.html">Browse services</a></div>
  <div class="note" style="margin-top:40px"><h3 class="h3">Rather talk now?</h3><p>Call <a href="{TEL_HREF}"><b>{TEL}</b></a>, {SITE['hours']}.</p></div>
</div></section>"""


# ---------------------------------------------------------------- assembly

def pages(bundle=False):
    out = [
        ("home", "Kennedy & Smith Mechanical | HVAC Replacement, Water Heaters & Water Treatment | Delaware County & Main Line",
         "Owner-operated plumbing and HVAC company in Havertown, PA. Heating and cooling replacement, water heaters, and water filtration and softeners for Delaware County and the Main Line. Book online.", page_home()),
        ("services", "Services | HVAC Replacement, Water Heaters & Water Treatment | Kennedy & Smith Mechanical",
         "Heating and cooling system replacement, water heater replacement, and water filtration and softeners for homes in Delaware County and on the Main Line.", page_services()),
    ]
    out += [(s["slug"], s["title"], s["desc"], page_service(s)) for s in SERVICES]
    out += [
        ("service-areas", "Service Areas | Delaware County & the Main Line | Kennedy & Smith Mechanical",
         "Kennedy & Smith Mechanical is based in Havertown and serves Delaware County and the Main Line. Map and town list.", page_areas()),
    ]
    out += [(a["slug"], a["title"], a["desc"], page_area(a)) for a in AREA_PAGES]
    out += [
        ("about", "About | Kennedy & Smith Mechanical", "Kennedy & Smith Mechanical is Bob Smith, a master plumber, and Joe Kennedy, a senior HVAC technician: a two-man, owner-operated company based in Havertown, PA.", page_about()),
        ("contact", "Contact & Request Service | Kennedy & Smith Mechanical", "Call, email, book online or send a request to Kennedy & Smith Mechanical in Havertown, PA.", page_contact(bundle)),
        ("thanks", "Thanks | Kennedy & Smith Mechanical", "Your request was received.", page_thanks()),
    ]
    return out


def canonical(slug):
    return SITE["domain"] + ("/" if slug == "home" else "/" + slug)


def schema(slug):
    blocks = []
    if slug == "home":
        biz = {
            "@context": "https://schema.org", "@type": ["Plumber", "HVACBusiness"], "name": SITE["name"], "url": SITE["domain"] + "/",
            "telephone": SITE["phone_tel"], "email": OWNERS[0]["email"], "image": SITE["domain"] + "/img/share.jpg", "openingHours": SITE["hours_schema"],
            "address": {"@type": "PostalAddress", "addressLocality": SITE["town"], "addressRegion": SITE["state"], "addressCountry": "US"},
            "areaServed": ["Delaware County, PA", "Main Line, PA"],
            "founder": [{"@type": "Person", "name": o["name"], "jobTitle": o["role"]} for o in OWNERS],
            "potentialAction": {"@type": "ReserveAction", "target": BOOK_URL, "name": "Book online"},
        }
        blocks.append(biz)
    for s in SERVICES:
        if s["slug"] == slug:
            blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]})
    return "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>\n' for b in blocks)


def head(slug, title, desc, bundle=False):
    robots = '<meta name="robots" content="noindex, nofollow">\n' if (SITE["preview"] or slug == "thanks") else ""
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}<link rel="canonical" href="{canonical(slug)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(SITE['name'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical(slug)}">
<meta property="og:image" content="{SITE['domain']}/img/share.jpg">
<meta name="theme-color" content="#101113">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="css/site.css">
{schema(slug)}"""


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build_site():
    all_pages = pages()
    for slug, title, desc, body in all_pages:
        doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(slug, title, desc)}</head>
<body>
{header(slug)}
<main id="main">
{body}
</main>
{footer()}
{preview_drawer()}
<script async src="{HCP_SCRIPT}"></script>
<script src="js/site.js" defer></script>
</body>
</html>
"""
        write(os.path.join(ROOT, href(slug)), doc)
    # a page dropped from the list above must not stay behind in the folder Cloudflare serves
    keep = {href(slug) for slug, *_ in all_pages}
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html") and name not in keep:
            os.remove(os.path.join(ROOT, name))
            print("removed retired page:", name)
    # search engine files
    if SITE["preview"]:
        robots = "User-agent: *\nDisallow: /\n"
    else:
        robots = f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n"
    write(os.path.join(ROOT, "robots.txt"), robots)
    urls = "".join(f"  <url><loc>{canonical(s)}</loc></url>\n" for s, *_ in all_pages if s != "thanks")
    write(os.path.join(ROOT, "sitemap.xml"), f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print(f"site: {len(all_pages)} pages")


def build_bundle():
    """Every page in one document, switched by the address hash. No Housecall Pro script or iframe:
    booking buttons open Housecall Pro in a new tab instead."""
    all_pages = pages(bundle=True)
    on = ' class="is-on"'
    secs = "".join(f'<div data-page="{slug}" data-group="{NAV_GROUP.get(slug, slug)}" data-title="{E(title)}"{on if slug == "home" else ""}>' + "\n" + body + "\n</div>\n" for slug, title, _, body in all_pages)
    slug, title, desc, _ = all_pages[0]
    doc = f"""<!DOCTYPE html>
<html lang="en" data-bundle>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kennedy &amp; Smith Mechanical site preview</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
{header("home")}
<main id="main">
{secs}</main>
{footer()}
{preview_drawer()}
<script src="js/site.js" defer></script>
</body>
</html>
"""
    out = os.path.join(ROOT, "preview")
    if os.path.isdir(out):
        shutil.rmtree(out)
    write(os.path.join(out, "index.html"), doc)
    for d in ("css", "js", "img"):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(out, d))
    print(f"bundle: preview/index.html, {len(all_pages)} pages")


if __name__ == "__main__":
    build_site()
    if "--bundle" in sys.argv:
        build_bundle()
