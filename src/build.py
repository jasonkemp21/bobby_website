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

from content import SITE, TO_CONFIRM, SERVICES, AREA_PAGES, ALSO_NEARBY, AREAS_SHORT  # noqa: E402
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

NAV = [("services", "Services"), ("maintenance-plans", "Maintenance plans"), ("service-areas", "Service areas"), ("about", "About"), ("contact", "Contact")]
NAV_GROUP = {s["slug"]: "services" for s in SERVICES}
NAV_GROUP.update({a["slug"]: "service-areas" for a in AREA_PAGES})
NAV_GROUP["emergency"] = "services"


def href(slug):
    return "index.html" if slug == "home" else slug + ".html"


def header(current):
    cur = NAV_GROUP.get(current, current)
    here = ' aria-current="page"'
    links = "".join(f'<a href="{href(s)}" data-nav="{s}"{here if s == cur else ""}>{t}</a>' for s, t in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="util"><div class="wrap util__in">
  <span>Serving {AREAS_SHORT}</span>
  <span class="util__r"><span>{SITE['hours']}</span><a href="emergency.html">Emergency? Call any hour</a></span>
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
    return f"""<footer class="foot"><div class="wrap">
  <div class="foot__grid">
    <div>
      <img class="foot__logo" src="img/ks-logo-light.webp" width="520" height="253" alt="Kennedy &amp; Smith Mechanical">
      <p>Locally owned plumbing, heating and cooling for {AREAS_SHORT}.</p>
      <p class="foot__lic">{"<br>".join(lic)}</p>
    </div>
    <div>
      <h4>Services</h4>
      <ul>{svc}<li><a href="emergency.html">Emergency service</a></li><li><a href="maintenance-plans.html">Maintenance plans</a></li></ul>
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
        <li><a class="foot__tel" href="{TEL_HREF}">{TEL}</a></li>
        <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        <li>{SITE['hours']}</li>
        <li>Emergency calls any hour</li>
      </ul>
      <p style="margin-top:16px">{book(cls="btn btn--red btn--sm")}</p>
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


def phead(crumbs, h1, lede, photo=None, buttons=True, red=False):
    trail = '<a href="index.html">Home</a>' + "".join(
        f' <span>/</span> <a href="{u}">{t}</a>' if u else f" <span>/</span> <span>{t}</span>" for t, u in crumbs)
    pic = f'<figure class="photo"><img src="img/{photo[0]}.webp" width="1200" height="900" alt="{E(photo[1])}"></figure>' if photo else ""
    btns = f'<div class="btns">{book()}{call()}</div>' if buttons else ""
    cls = "phead on-dark" + ("" if photo else " phead--plain") + (" phead--red" if red else "")
    return f"""<section class="{cls}"><div class="wrap phead__in">
  <div><nav class="crumb" aria-label="Breadcrumb">{trail}</nav><h1 class="h1">{h1}</h1><p class="lede">{lede}</p>{btns}</div>
  {pic}
</div></section>"""


STEPS = """<ol class="steps">
  <li><h3 class="h3">Book or call</h3><p>Pick a time online or call us. You get a confirmation by text or email.</p></li>
  <li><h3 class="h3">We find the cause</h3><p>The tech looks at the whole problem, explains it in plain words and gives you a price.</p></li>
  <li><h3 class="h3">You approve, we fix it</h3><p>Work starts when you say go. We test it, show you what we did and clean up.</p></li>
</ol>"""


def faq_block(faqs):
    items = "".join(f"<details><summary>{E(q)}</summary><div><p>{E(a)}</p></div></details>" for q, a in faqs)
    return f'<div class="faq">{items}</div>'


# ---------------------------------------------------------------- pages

def page_home():
    cards = ""
    for s in SERVICES:
        pts = "".join(f"<li>{p}</li>" for p in s["card_points"])
        cards += f'<a class="cat__c" href="{s["slug"]}.html">{icon(s["icon"], True)}<h3 class="h3">{s["name"]}</h3><p>{s["card"]}</p><ul>{pts}</ul><span class="more">{s["name"]}</span></a>'
    cards += f'<a class="cat__c" href="maintenance-plans.html">{icon("plan", True)}<h3 class="h3">Maintenance plans</h3><p>Yearly tune-ups and priority scheduling, so small problems get caught early.</p><ul><li>Annual tune-ups</li><li>Priority scheduling</li><li>Repair discounts</li></ul><span class="more">See the plans</span></a>'
    cards += f'<a class="cat__c is-red" href="emergency.html">{icon("alert", True)}<h3 class="h3">Emergency service</h3><p>Burst pipe, no heat, sewer backing up. Skip the form and call {TEL}.</p><span class="more">What to do right now</span></a>'
    return f"""<section class="hero on-dark"><div class="wrap hero__in">
  <div>
    <p class="label">Plumbing &middot; Heating &middot; Cooling</p>
    <h1 class="h1">Main Line &amp; Delco plumbing, heating and cooling</h1>
    <p class="lede">Kennedy &amp; Smith Mechanical is a locally owned shop serving {AREAS_SHORT}. You get a price before any work starts, and you can book the visit online in about a minute.</p>
    <div class="btns">{book()}{call()}</div>
    <ul class="hero__facts"><li>Registered and insured in PA</li><li>Price before work starts</li><li>Locally owned</li></ul>
  </div>
  <aside class="triage" aria-label="Start from the problem">
    <div class="triage__h">What's going on?</div>
    <a href="plumbing.html"><div>A leak, a clog or a drip<span>Plumbing repair</span></div></a>
    <a href="water-heaters.html"><div>No hot water<span>Water heaters</span></div></a>
    <a href="heating.html"><div>No heat or uneven heat<span>Furnaces and boilers</span></div></a>
    <a href="air-conditioning.html"><div>AC not cooling<span>Air conditioning</span></div></a>
    <a class="is-red" href="emergency.html"><div>It can't wait<span>Emergency service, call {TEL}</span></div></a>
  </aside>
</div></section>

<section class="strip"><div class="wrap strip__in">
  <div class="strip__c"><h3>Registered &amp; insured</h3><p>A Pennsylvania registered contractor. Proof of insurance on request.</p></div>
  <div class="strip__c"><h3>Price before work</h3><p>You see the number and approve it before we pick up a tool.</p></div>
  <div class="strip__c"><h3>Book online any time</h3><p>Pick a slot from your phone. Confirmation comes by text or email.</p></div>
  <div class="strip__c"><h3>Emergency calls</h3><p>Burst pipe or no heat in January. Call any hour.</p></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><p class="label">What we do</p><h2 class="h2">One shop for the pipes, the heat and the air</h2></div><p class="lede grey">Most houses around here are old enough that the plumbing and the heating are tangled together. It helps to call someone who works on both.</p></div>
  <div class="cat">{cards}</div>
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">How a service call works</p><h2 class="h2">Three steps, no surprises</h2></div></div>
  {STEPS}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><p class="label">Where we work</p><h2 class="h2">The Main Line, Delco and Philadelphia</h2></div><p class="lede grey">Our core area is Delaware County and the towns along the Main Line. We also work in Philadelphia and nearby parts of Montgomery and Chester counties.</p></div>
  <div class="area">
    {map_block()}
    <div class="towns">
      {towns_block(link=True)}
      <p><a class="more" href="service-areas.html">Full town list</a></p>
    </div>
  </div>
</div></section>

<section class="sec sec--shop"><div class="wrap split">
  <div>
    <p class="label">About the shop</p>
    <h2 class="h2">A local shop, not a call center</h2>
    <p class="lede grey" style="margin-top:16px">Kennedy &amp; Smith Mechanical is owner-operated. The person who quotes your job is the person responsible for getting it right.</p>
    <ul class="ticks"><li>A price you approve before work starts</li><li>Plain explanations of what failed and why</li><li>Drop cloths down and cleanup before we leave</li><li>Online booking with text and email confirmations</li></ul>
    <p style="margin-top:26px"><a class="more" href="about.html">About Kennedy &amp; Smith</a></p>
  </div>
  <figure class="photo"><img src="img/work-sink.webp" width="1200" height="900" alt="Plumber tightening a fitting under a kitchen sink" loading="lazy"></figure>
</div></section>

{book_band("Book a visit online", "Choose the service and a time that suits you. We confirm the appointment and send a reminder before we arrive.")}"""


def map_block():
    return f"""<div class="map">{area_map_svg()}
  <div class="map__key"><span><i style="background:#ead9bf"></i>Core area: Delaware County and the Main Line</span><span><i style="background:#fbfbfa"></i>Also served</span></div>
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
    rows += f'<a class="cat__c" href="maintenance-plans.html">{icon("plan", True)}<h3 class="h3">Maintenance plans</h3><p>A yearly membership that covers tune-ups for your plumbing, your heating and cooling, or both.</p><ul><li>Annual tune-ups</li><li>Priority scheduling</li><li>Repair discounts</li><li>We track the dates for you</li></ul><span class="more">See the plans</span></a>'
    rows += f'<a class="cat__c is-red" href="emergency.html">{icon("alert", True)}<h3 class="h3">Emergency service</h3><p>For a burst pipe, a sewer backup or no heat in freezing weather, call {TEL} at any hour. The page has steps to limit the damage while you wait.</p><span class="more">Emergency steps</span></a>'
    return phead([("Services", None)], "Plumbing, heating and cooling services", "Repairs, replacements and yearly maintenance for homes across " + AREAS_SHORT + ".") + f"""
<section class="sec"><div class="wrap"><div class="cat">{rows}</div></div></section>
<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">How a service call works</p><h2 class="h2">Three steps, no surprises</h2></div></div>
  {STEPS}
</div></section>
{book_band("Not sure which one you need?", "Describe the problem when you book or call. We will sort out the rest.")}"""


def page_service(s):
    handle = "".join(f"<li>{x}</li>" for x in s["handle"])
    signs = "".join(f"<div><dt>{E(t)}</dt><dd>{E(d)}</dd></div>" for t, d in s["signs"])
    others = "".join(f'<a href="{o["slug"]}.html"><h3 class="h3">{o["name"]}</h3><p>{o["card"]}</p><span class="more">{o["name"]}</span></a>' for o in SERVICES if o["slug"] != s["slug"])
    return phead([("Services", "services.html"), (s["name"], None)], s["h1"], s["lede"], s["photo"]) + f"""
<section class="sec"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">{s['name']}</p><h2 class="h2">{s['handle_h']}</h2></div></div>
  <ul class="sheet">{handle}</ul>
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">Know what you're looking at</p><h2 class="h2">{s['signs_h']}</h2></div></div>
  <dl class="signs">{signs}</dl>
  <div class="note" style="margin-top:40px"><h3 class="h3">{E(s['local'][0])}</h3><p>{E(s['local'][1])}</p></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">How a service call works</p><h2 class="h2">Three steps, no surprises</h2></div></div>
  {STEPS}
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">Common questions</p><h2 class="h2">{s['name']} questions</h2></div></div>
  {faq_block(s['faqs'])}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">Also from Kennedy &amp; Smith</p><h2 class="h2">Other services</h2></div></div>
  <div class="acards">{others}</div>
</div></section>

{book_band(s['cta'][0], s['cta'][1])}"""


def page_emergency():
    return f"""<section class="phead phead--plain phead--red on-dark"><div class="wrap phead__in"><div>
  <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> <span>/</span> <span>Emergency service</span></nav>
  <h1 class="h1">Something broken right now?</h1>
  <p class="lede">Don't fill out a form. Call, tell us what is happening, and we will tell you how fast we can be there.</p>
  <a class="emg-tel" href="{TEL_HREF}">{TEL}</a>
  <p style="margin:0;font-weight:600">Burst pipes, sewer backups, no heat, no hot water, flooding.</p>
</div></div></section>

<section class="sec"><div class="wrap">
  <div class="gas">
    <h3 class="h3">Smell gas? Leave first.</h3>
    <p>Get everyone out of the building. Don't touch light switches and don't use a phone inside. From outside, call 911 or your gas utility: <a href="tel:+18008414141">PECO 1-800-841-4141</a> in the suburbs, <a href="tel:+12152351212">PGW 215-235-1212</a> in Philadelphia. Call us after the utility has made it safe, and we will repair the line.</p>
  </div>
</div></section>

<section class="sec sec--shop" style="padding-top:0"><div class="wrap" style="padding-top:var(--gap)">
  <div class="sec-head"><div><p class="label">While you wait</p><h2 class="h2">What to do right now</h2></div><p class="lede grey">A few minutes of the right steps can save a ceiling, a floor or a furnace.</p></div>
  <div class="dos">
    <div><h3 class="h3">Burst or leaking pipe</h3><ol><li>Close the main water shutoff. It is usually where the line enters the basement, by the meter.</li><li>Open the lowest faucet in the house to drain what is left in the pipes.</li><li>If water is near outlets or the panel, switch off power to that area at the breaker.</li><li>Move what you can and start soaking up water.</li></ol></div>
    <div><h3 class="h3">Water heater leaking</h3><ol><li>Close the cold water valve on the pipe above the heater.</li><li>Gas unit: turn the dial on the gas valve to off. Electric unit: switch off its breaker.</li><li>If the tank is emptying onto the floor, run a hose from the drain valve to a floor drain or outside.</li></ol></div>
    <div><h3 class="h3">No heat</h3><ol><li>Check that the thermostat is set to heat and its batteries are good.</li><li>Check the furnace or boiler switch and its breaker.</li><li>Replace the filter if it is clogged.</li><li>In freezing weather, open cabinet doors under sinks and let faucets drip so pipes do not freeze.</li></ol></div>
    <div><h3 class="h3">Sewer backing up</h3><ol><li>Stop running water everywhere in the house. No flushing, no laundry, no dishwasher.</li><li>Keep children and pets away from the water.</li><li>Don't use chemical drain cleaner. It will not clear a main line and it makes the repair hazardous.</li></ol></div>
    <div><h3 class="h3">Frozen pipe</h3><ol><li>Close the main shutoff in case the pipe has already split.</li><li>Open the faucet the pipe feeds.</li><li>Warm the pipe gently with a hair dryer, starting at the faucet end. Never use an open flame.</li></ol></div>
    <div><h3 class="h3">Carbon monoxide alarm</h3><ol><li>Get everyone outside into fresh air.</li><li>Call 911 from outside.</li><li>Don't go back in or run the heat until the fire department clears the house. Then call us to find the cause.</li></ol></div>
  </div>
</div></section>

<section class="sec"><div class="wrap split">
  <div><p class="label">Not urgent?</p><h2 class="h2">Book a regular appointment</h2><p class="lede grey" style="margin-top:16px">If it can wait until business hours, booking online is the quickest way to get on the schedule.</p></div>
  <div class="btns">{book()}<a class="btn btn--line" href="services.html">See all services</a></div>
</div></section>

<section class="book" style="background:var(--red);border-top-color:var(--ink)"><div class="wrap book__in">
  <div><h2 class="h2">Still happening?</h2><p style="color:#fff">Stop reading and call.</p></div>
  <div class="book__act"><a class="book__tel" href="{TEL_HREF}"><small style="color:#fff">Emergency line</small>{TEL}</a></div>
</div></section>"""


def page_plans():
    def plan(tag, name, price, covers, blurb, items, main=False):
        return f"""<div class="plan{' plan--main' if main else ''}"><div class="plan__top"><p class="plan__tag">{tag}</p><h3 class="h2">{name}</h3><p class="plan__price">${price}<small>per year</small></p></div>
<div class="plan__body"><p><b>{covers}</b><br><span class="grey">{blurb}</span></p><ul class="ticks">{"".join(f"<li>{i}</li>" for i in items)}</ul><a class="btn{' btn--red' if main else ''}" href="contact.html">Ask about {name}</a></div></div>"""
    return phead([("Maintenance plans", None)], "Maintenance plans", "A yearly tune-up catches the worn part before it becomes a no-heat call. Two plans, billed once a year.") + f"""
<section class="sec"><div class="wrap">
  <div class="sec-head"><div><p class="label">Pick a plan</p><h2 class="h2">Two plans, one price each</h2></div><p class="lede grey">Both are billed yearly. Cancel whenever you like.</p></div>
  <div class="plans">
    {plan("One system", "Homeshield Basic", 179, "Covers your plumbing or your heating and cooling.", "For a home that needs one system looked after.", ["1 tune-up a year", "Priority scheduling", "No dispatch fee on service calls", "10% off repairs", "Yearly safety check", "We remind you when it is due"])}
    {plan("Whole house", "Homeshield Premium", 299, "Covers plumbing, heating and cooling.", "Heating checked in fall, cooling in spring, plumbing once a year.", ["2 tune-ups a year", "First in line for emergency calls", "No dispatch fee on service calls", "15% off repairs", "Yearly water heater flush", "Camera look at the main drain", "Transfers to the buyer if you sell"], main=True)}
  </div>
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">How it works</p><h2 class="h2">Sign up once, then we keep track</h2></div></div>
  <ol class="steps">
    <li><h3 class="h3">Sign up</h3><p>Ask us by phone or through the contact form. We set the plan up on your account.</p></li>
    <li><h3 class="h3">We schedule it</h3><p>When your tune-up is due we get in touch to book it. You don't have to remember.</p></li>
    <li><h3 class="h3">You get priority</h3><p>When something does break, plan members go to the front of the schedule.</p></li>
  </ol>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">What a tune-up covers</p><h2 class="h2">What we check</h2></div></div>
  <div class="trio">
    <div><h3 class="h3">Heating</h3><p>Burners, igniter and flame sensor, heat exchanger, safety controls, filter, and carbon monoxide at the unit. On boilers: pressure, expansion tank, circulators and radiator vents.</p></div>
    <div><h3 class="h3">Cooling</h3><p>Coils, capacitor and contactor, refrigerant pressures, condensate drain, and the temperature drop across the system.</p></div>
    <div><h3 class="h3">Plumbing</h3><p>Water pressure, shutoff valves, visible supply and drain lines, toilets, the sump pump, and the water heater's relief valve and anode.</p></div>
  </div>
</div></section>

{book_band("Want a plan?", "Tell us about your house and we will set you up with the one that fits.")}"""


def page_areas():
    cards = "".join(f'<a href="{a["slug"]}.html"><h3 class="h3">{a["name"]}</h3><p>{a["card"]}</p><span class="more">{a["name"]}</span></a>' for a in AREA_PAGES)
    return phead([("Service areas", None)], "Where we work", "Delaware County and the Main Line are home base. We also cover Philadelphia and nearby parts of Montgomery and Chester counties.") + f"""
<section class="sec"><div class="wrap">
  <div class="area">
    {map_block()}
    <div class="towns">
      {towns_block(link=True, full=True)}
      <div><h3>Also nearby</h3><p>{", ".join(ALSO_NEARBY)}. Not sure about your town? Call and ask.</p></div>
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
  <div class="sec-head sec-head--one"><div><p class="label">What we do here</p><h2 class="h2">Services {'on the Main Line' if a['slug'] == 'main-line' else 'in ' + a['name']}</h2></div></div>
  <div class="cat" style="grid-template-columns:repeat(auto-fit,minmax(250px,1fr))">{svc}</div>
</div></section>
{book_band("Need someone out?", "Book a visit online or call " + TEL + ".")}"""


def page_about():
    return phead([("About", None)], "About Kennedy &amp; Smith Mechanical", "A locally owned plumbing, heating and cooling shop serving " + AREAS_SHORT + ".", buttons=False) + f"""
<section class="sec"><div class="wrap split">
  <div>
    <p class="label">The shop</p>
    <h2 class="h2">Small on purpose</h2>
    <div class="grey" style="margin-top:18px">
      <p>Kennedy &amp; Smith Mechanical is owner-operated. There is no sales team and no call center. When you call, you reach the people who do the work.</p>
      <p>We fix plumbing, water heaters, heating and air conditioning in houses that are often older than anyone living in them. That takes patience and a willingness to figure out what is behind the wall before quoting a price.</p>
      <p>We would rather repair something properly than sell you a replacement you don't need, and we will say so when replacing really is the better call.</p>
    </div>
  </div>
  <figure class="photo"><img src="img/work-sink.webp" width="1200" height="900" alt="Plumber tightening a fitting under a kitchen sink" loading="lazy"></figure>
</div></section>

<section class="sec sec--shop"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">How we work</p><h2 class="h2">What you can expect</h2></div></div>
  <div class="trio">
    <div><h3 class="h3">A price first</h3><p>We look at the problem, tell you what it costs to fix, and wait for your go-ahead. The price you approve is the price you pay.</p></div>
    <div><h3 class="h3">Straight answers</h3><p>You hear what failed, why, and what your options are, including the cheap one.</p></div>
    <div><h3 class="h3">A clean job</h3><p>Drop cloths go down before tools come out, and we clean up before we leave.</p></div>
  </div>
  <div class="trio" style="margin-top:24px">
    <div><h3 class="h3">Easy to reach</h3><p>Book online at any hour. You get a confirmation and a reminder, and you can call with questions.</p></div>
    <div><h3 class="h3">Registered &amp; insured</h3><p>We are a registered Pennsylvania home improvement contractor and carry liability insurance. Ask and we will show you both.</p></div>
    <div><h3 class="h3">Local</h3><p>We work where we live: {AREAS_SHORT}.</p></div>
  </div>
</div></section>
{book_band("Let's get to work", "Book a visit online or call. Either way you will talk to someone who knows the trade.")}"""


def lead_form(bundle):
    if bundle:
        inner = f"""<div class="form__stand"><h3 class="h3">The request form goes here</h3><p class="grey">On the live site this box holds the Housecall Pro request form, and what a customer sends lands in Housecall Pro as a new lead. This preview cannot embed another site, so open the form in its own tab to see it.</p><a class="btn" href="{LEAD_URL}" target="_blank" rel="noopener">Open the request form</a></div>"""
    else:
        inner = f"""<iframe id="hcp-lead-iframe" title="Request service from Kennedy &amp; Smith Mechanical" src="{LEAD_URL}" loading="lazy"></iframe>
<p class="form__alt">Form not loading? <a href="{LEAD_URL}" target="_blank" rel="noopener">Open it in a new tab</a> or call {TEL}.</p>"""
    return f'<div class="form"><div class="form__h">Request service or a quote</div>{inner}</div>'


def page_contact(bundle):
    return phead([("Contact", None)], "Contact us", "Book a standard visit online. For a quote, a bigger project or a question, send the form or call.", buttons=False) + f"""
<section class="sec"><div class="wrap contact">
  <div>
    <dl class="clist">
      <div><dt>Phone</dt><dd><a href="{TEL_HREF}" style="color:var(--red)">{TEL}</a><small>Emergencies: call any hour</small></dd></div>
      <div><dt>Email</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a></dd></div>
      <div><dt>Hours</dt><dd>{SITE['hours']}</dd></div>
      <div><dt>Service area</dt><dd>Main Line, Delaware County, Philadelphia<small><a href="service-areas.html">See the map and town list</a></small></dd></div>
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
    return phead([("Request received", None)], "Thanks. We got it.", "Your request is in. Someone from Kennedy &amp; Smith will be in touch to confirm the details and set a time.", buttons=False) + f"""
<section class="sec"><div class="wrap">
  <div class="sec-head sec-head--one"><div><p class="label">What happens next</p><h2 class="h2">Three steps from here</h2></div></div>
  <ol class="steps">
    <li><h3 class="h3">We read it</h3><p>Requests are reviewed during business hours, {SITE['hours']}.</p></li>
    <li><h3 class="h3">We call or text</h3><p>We contact you at the number you gave to confirm the job and the time.</p></li>
    <li><h3 class="h3">We show up</h3><p>The tech arrives in the window you picked with what the job needs.</p></li>
  </ol>
  <div class="btns" style="margin-top:40px"><a class="btn" href="index.html">Back to home</a><a class="btn btn--line" href="services.html">Browse services</a></div>
  <div class="note" style="margin-top:40px"><h3 class="h3">Can't wait?</h3><p>If this turned into an emergency, call <a href="{TEL_HREF}"><b>{TEL}</b></a> now.</p></div>
</div></section>"""


# ---------------------------------------------------------------- assembly

def pages(bundle=False):
    out = [
        ("home", "Kennedy & Smith Mechanical | Plumbing, Heating & Cooling | Main Line & Delaware County",
         "Locally owned plumbing, heating and cooling for the Main Line, Delaware County and Philadelphia. A price before work starts. Book online.", page_home()),
        ("services", "Plumbing, Heating & Cooling Services | Kennedy & Smith Mechanical",
         "Plumbing, water heaters, heating, air conditioning, maintenance plans and emergency service for the Main Line, Delaware County and Philadelphia.", page_services()),
    ]
    out += [(s["slug"], s["title"], s["desc"], page_service(s)) for s in SERVICES]
    out += [
        ("emergency", "Emergency Plumber & No-Heat Service | Main Line & Delaware County | Kennedy & Smith Mechanical",
         "Burst pipe, sewer backup or no heat? Call Kennedy & Smith Mechanical at any hour. Steps to limit the damage while you wait.", page_emergency()),
        ("maintenance-plans", "Plumbing & HVAC Maintenance Plans | Kennedy & Smith Mechanical",
         "Yearly plumbing and HVAC maintenance plans with tune-ups, priority scheduling and repair discounts.", page_plans()),
        ("service-areas", "Service Areas | Main Line, Delaware County & Philadelphia | Kennedy & Smith Mechanical",
         "Kennedy & Smith Mechanical serves Delaware County, the Main Line, Philadelphia and nearby parts of Montgomery and Chester counties. Map and town list.", page_areas()),
    ]
    out += [(a["slug"], a["title"], a["desc"], page_area(a)) for a in AREA_PAGES]
    out += [
        ("about", "About | Kennedy & Smith Mechanical", "Kennedy & Smith Mechanical is a locally owned plumbing, heating and cooling shop serving the Main Line, Delaware County and Philadelphia.", page_about()),
        ("contact", "Contact & Request Service | Kennedy & Smith Mechanical", "Call, book online or send a request to Kennedy & Smith Mechanical.", page_contact(bundle)),
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
            "telephone": SITE["phone_tel"], "email": SITE["email"], "image": SITE["domain"] + "/img/share.jpg", "openingHours": SITE["hours_schema"],
            "areaServed": ["Delaware County, PA", "Main Line, PA", "Philadelphia, PA", "Montgomery County, PA", "Chester County, PA"],
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
    secs = "".join(f'<div data-page="{slug}" data-title="{E(title)}"{on if slug == "home" else ""}>' + "\n" + body + "\n</div>\n" for slug, title, _, body in all_pages)
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
