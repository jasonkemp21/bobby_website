"""Site settings and page copy for Kennedy & Smith Mechanical.

Everything a non-developer is likely to change lives in SITE at the top.
Change it here, run `python3 src/build.py`, and every page updates.
"""

SITE = {
    "name": "Kennedy & Smith Mechanical",
    "domain": "https://kandsmechanical.com",
    # Used on every page.
    "phone_display": "(610) 212-6976",
    "phone_tel": "+16102126976",
    # PLACEHOLDER until confirmed.
    "email": "info@kandsmechanical.com",
    "hours": "Mon to Sat, 7 AM to 7 PM",
    "hours_schema": "Mo-Sa 07:00-19:00",
    # Pennsylvania registers home improvement contractors with the Attorney General
    # (number looks like PA123456) and it has to appear in advertising. Leave empty until known.
    "pa_hic": "",
    # Municipal licenses worth listing, e.g. "Philadelphia Master Plumber #12345". Empty until known.
    "other_licenses": [],
    # Housecall Pro
    "hcp_org": "Kennedy-and-Smith-Mechanical",
    "hcp_book_token": "a8d62a41ba21462caf2a9f9c9c8bf10e",
    "hcp_lead_token": "ab7ce96b4764422dad58e3566f36a950",
    # True while the owner is still reviewing: shows the checklist button, tells search engines to stay out.
    "preview": True,
}

# Shown in the preview checklist drawer. Delete items as Bobby answers them.
TO_CONFIRM = [
    ("Registration and licenses", "Pennsylvania has no statewide plumbing or HVAC license. What goes in the footer is the PA Home Improvement Contractor number (PA plus six digits) and any township or Philadelphia master plumber license. Both are blank for now."),
    ("What you offer", "The site sells plumbing, water heaters, heating and air conditioning. Confirm each one, and whether you take commercial jobs."),
    ("Emergency calls", "The site says to call any hour for emergencies. Confirm you answer after hours, or tell us the real cutoff."),
    ("Service area", "The site now leads with the Main Line and Delaware County, then Philadelphia. Confirm the towns and whether South Jersey should come back."),
    ("Maintenance plans", "Plan names, the $179 and $299 prices and every listed benefit are a draft. Edit or remove."),
    ("Hours and email", "Listed as Mon to Sat, 7 AM to 7 PM and info@kandsmechanical.com. Both are guesses."),
    ("Promises in the copy", "Insured, a price before work starts, same-day visits when the schedule allows, and cleanup before leaving. Strike anything you would not put in writing."),
    ("Reviews", "There are no testimonials on this build. The earlier ones were invented. Real Google reviews go in once the Business Profile is verified."),
    ("Photos", "The four photos are stock. Send pictures of the truck, the crew and finished jobs and they replace these."),
    ("About page", "Needs the real story: who owns it, how long you have been at it, where you are based."),
]

AREAS_SHORT = "the Main Line, Delaware County and Philadelphia"

SERVICES = [
    {
        "slug": "plumbing",
        "icon": "wrench",
        "name": "Plumbing",
        "card": "Leaks, clogs, fixtures, sump pumps, gas lines and repipes.",
        "card_points": ["Drain clearing", "Leak repair", "Fixtures and repipes"],
        "title": "Plumbing Repair & Installation | Main Line & Delaware County | Kennedy & Smith Mechanical",
        "desc": "Plumbing repair and installation on the Main Line, in Delaware County and in Philadelphia. Leaks, drains, fixtures, sump pumps, gas lines and repipes. Book online.",
        "h1": "Plumbing repair and installation",
        "lede": "Leaks, clogs, bad fixtures and worn-out pipes. We find the cause, give you a price, and fix it properly.",
        "photo": ("work-trap", "Plumber's hands tightening a drain trap under a sink"),
        "handle_h": "What we handle",
        "handle": [
            "Drain clearing", "Leak detection and repair", "Faucets, toilets and fixtures",
            "Garbage disposals", "Sump pumps and ejector pumps", "Gas line repair and installation",
            "Water service lines", "Repiping in copper and PEX", "Frozen and burst pipes",
            "Main sewer line service", "Shutoff valves and hose bibs", "Backflow preventers",
        ],
        "signs_h": "Signs it's time to call",
        "signs": [
            ("Several drains slow at once", "One slow sink is usually that sink. Several fixtures backing up together, or gurgling at the lowest drain in the house, points at the main sewer line."),
            ("A water bill that jumped", "With every tap off, watch the meter. If the dial still moves, water is leaving somewhere, often a running toilet or a line under the slab or yard."),
            ("Brown or rusty water", "Common in homes that still have galvanized steel pipe. The pipe rusts from the inside, pressure drops, and pinhole leaks follow."),
            ("Stains on a ceiling or wall", "Water travels along framing before it shows. The leak is rarely right above the stain, so it pays to trace it before opening anything."),
        ],
        "local": ("Older homes need a different approach", "Much of the housing on the Main Line and in eastern Delaware County went up before 1950. That means cast iron stacks, galvanized supply lines and the occasional lead service line. We check what is in the walls before we quote, so the price does not change halfway through."),
        "faqs": [
            ("Do I get a price before work starts?", "Yes. We look at the problem first, tell you what it will cost to fix, and start only after you say go."),
            ("My drain keeps clogging. Is something bigger wrong?", "If the same fixture clogs again and again, there is usually buildup or a bad slope in that branch line. If several fixtures back up together, the main line is the suspect, and a camera inspection will show whether it is roots, a belly in the pipe or a break."),
            ("Where is my main water shutoff?", "In most homes here it sits where the water line comes through the basement wall, near the meter. A round wheel handle turns clockwise to close. A lever handle closes with a quarter turn. Find it before you need it."),
            ("Do I need a permit?", "It depends on the job and the township. Swapping a faucet or toilet usually does not need one. Water heaters, gas lines and sewer work usually do. We tell you before we start."),
        ],
        "cta": ("Need a plumber?", "Book a visit online or call. Tell us what is happening and we will tell you when we can be there."),
    },
    {
        "slug": "water-heaters",
        "icon": "tank",
        "name": "Water heaters",
        "card": "Repair and replacement for tank, tankless and heat pump units.",
        "card_points": ["No hot water", "Leaking tanks", "Tankless upgrades"],
        "title": "Water Heater Repair & Replacement | Main Line & Delaware County | Kennedy & Smith Mechanical",
        "desc": "Water heater repair and replacement on the Main Line, in Delaware County and in Philadelphia. Tank, tankless and heat pump water heaters. Book online.",
        "h1": "Water heater repair and replacement",
        "lede": "No hot water, not enough of it, or a tank that has started to leak. We repair what can be repaired and replace what cannot.",
        "photo": None,
        "handle_h": "What we handle",
        "handle": [
            "Gas and electric tank heaters", "Tankless water heaters", "Heat pump water heaters",
            "Thermostats and heating elements", "Gas valves and thermocouples", "Anode rod replacement",
            "Tank flushing", "Expansion tanks", "Relief valves",
            "Recirculation pumps", "Gas line and venting changes", "Old unit removal",
        ],
        "signs_h": "Repair it or replace it?",
        "signs": [
            ("Water around the base", "If the tank itself is leaking, it is finished and needs replacing. If the water is coming from a fitting or the relief valve, that is often a repair."),
            ("Rumbling or popping", "Sediment has settled on the bottom and water is boiling under it. A flush can help. On an old tank it is a sign the end is close."),
            ("Hot water runs out fast", "On an electric unit, usually a failed lower element or thermostat. On gas, often a broken dip tube. Both are repairs."),
            ("The unit is past ten years", "Most tank heaters last eight to twelve years. Past that, a repair bill is better spent on a new unit, before it fails on a holiday weekend."),
        ],
        "local": ("Tank or tankless?", "A tankless unit heats water as you use it, hangs on the wall and can last around twenty years with yearly descaling. It also costs more up front and often needs a larger gas line and new venting. In a home with one or two bathrooms, a good tank is usually the better buy. We price both so you can compare."),
        "faqs": [
            ("How long does a water heater last?", "A tank unit typically lasts eight to twelve years. Tankless units can reach twenty with regular descaling. The serial number on the label tells you the build date."),
            ("What size do I need?", "For a tank, 40 gallons suits most homes with two or three people and 50 gallons suits four or five. Tankless units are sized by how many fixtures run at once."),
            ("Can you replace it the same day?", "Often, when it is a like-for-like swap and the schedule allows. Call early and tell us the fuel type and tank size from the label."),
            ("Why is the relief valve dripping?", "It opens when pressure or temperature gets too high. A steady drip can mean a failed valve, a missing or waterlogged expansion tank, or high water pressure. Do not cap it. Have it checked."),
        ],
        "cta": ("Out of hot water?", "Book online or call with the brand, fuel type and tank size from the label, and we will come prepared."),
    },
    {
        "slug": "heating",
        "icon": "flame",
        "name": "Heating",
        "card": "Furnaces, boilers, radiators and heat pumps, repaired and replaced.",
        "card_points": ["No-heat calls", "Boilers and radiators", "Fall tune-ups"],
        "title": "Heating, Furnace & Boiler Service | Main Line & Delaware County | Kennedy & Smith Mechanical",
        "desc": "Furnace, boiler and heat pump repair and replacement on the Main Line, in Delaware County and in Philadelphia. No-heat calls and fall tune-ups. Book online.",
        "h1": "Furnace, boiler and heat pump service",
        "lede": "No heat, uneven heat or a system that is on its last winter. We work on forced air, hot water and steam.",
        "photo": ("work-pipe", "Gloved hand turning a pipe wrench on a steel fitting"),
        "handle_h": "What we service",
        "handle": [
            "Gas furnaces", "Hot water boilers", "Steam boilers and radiators",
            "Heat pumps", "Thermostats and zone controls", "Circulator pumps and zone valves",
            "Igniters and flame sensors", "Blower motors", "Ductwork repair",
            "Radiator valves and vents", "Fall tune-ups and safety checks", "System replacement",
        ],
        "signs_h": "Signs it's time to call",
        "signs": [
            ("Short cycling", "The system starts, runs a minute or two and shuts off. Usual causes are a clogged filter, a dirty flame sensor or an overheating heat exchanger."),
            ("Banging radiators", "On a steam system, water is trapped where it should drain back. A radiator that has settled out of pitch or a half-closed valve is the usual cause."),
            ("One room stays cold", "On hot water heat, air in the radiator or a stuck zone valve. On forced air, a closed damper or a leaking duct run."),
            ("A carbon monoxide alarm", "Leave the house and call 911. Do not run the heat again until the system has been checked."),
        ],
        "local": ("We work on radiators", "Plenty of homes on the Main Line and in Delaware County still heat with hot water or steam, and not every company still services them. A boiler that is cared for can run for decades. We repair them, and we tell you plainly when replacing makes more sense."),
        "faqs": [
            ("Should I repair or replace my furnace?", "A gas furnace usually lasts fifteen to twenty years. If yours is past fifteen and the repair costs a large share of a new unit, replacing is usually the better use of the money. Younger than that, repair."),
            ("When should I get a tune-up?", "Early fall, before the first cold snap. Problems found in October are cheaper and easier than the same problems found on the coldest night of January."),
            ("Do heat pumps work in Pennsylvania winters?", "Current cold-climate heat pumps heat well through winters here. Many homeowners keep their furnace or boiler as backup for the coldest days."),
            ("What should I check before I call?", "Make sure the thermostat is set to heat and has fresh batteries, the furnace switch and breaker are on, and the filter is not clogged. If all of that is right, call."),
        ],
        "cta": ("Heat acting up?", "Book a visit online or call. If you have no heat at all, call."),
    },
    {
        "slug": "air-conditioning",
        "icon": "snow",
        "name": "Air conditioning",
        "card": "Central air and ductless systems, repaired, tuned and installed.",
        "card_points": ["Not cooling", "Ductless mini-splits", "Spring tune-ups"],
        "title": "Air Conditioning Repair & Installation | Main Line & Delaware County | Kennedy & Smith Mechanical",
        "desc": "Central air and ductless mini-split repair and installation on the Main Line, in Delaware County and in Philadelphia. Spring tune-ups. Book online.",
        "h1": "Air conditioning repair and installation",
        "lede": "Warm air from the vents, ice on the lines or a system that never shuts off. We repair central air and ductless systems and install new ones.",
        "photo": ("work-gauges", "Technician reading a digital gauge set on an HVAC unit"),
        "handle_h": "What we handle",
        "handle": [
            "Central air repair", "Ductless mini-splits", "Heat pump cooling",
            "Refrigerant leak checks", "Capacitors and contactors", "Condenser fan motors",
            "Frozen coils", "Clogged condensate drains", "Thermostats",
            "Spring tune-ups", "Ductwork repair", "System replacement",
        ],
        "signs_h": "Signs it's time to call",
        "signs": [
            ("Running but not cooling", "Check the filter and the outdoor unit's breaker first. If both are fine, the cause is often a failed capacitor or low refrigerant from a leak."),
            ("Ice on the copper lines", "Turn the system off and let it thaw. Ice means poor airflow or low refrigerant, and running it frozen can kill the compressor."),
            ("Water near the indoor unit", "The condensate drain is clogged. It is a quick fix if caught early and a ceiling repair if not."),
            ("A system from before 2010", "It probably runs on R-22, which has not been made in the US since 2020. Recharging one is expensive, so a leak is usually the point to replace."),
        ],
        "local": ("No ducts? That is common here", "Homes heated by radiators were built without ductwork. Ductless mini-splits cool them without tearing into plaster walls: one outdoor unit, a small line to each room, and each room on its own thermostat."),
        "faqs": [
            ("How often should AC be serviced?", "Once a year, in spring. A tune-up covers the coils, the drain, the electrical parts and the refrigerant pressures."),
            ("How long does a central air system last?", "Around twelve to fifteen years on average. Past that, efficiency drops and parts fail more often."),
            ("Can I add central air to a house with radiators?", "Yes, but the ductwork is the hard part. Ductless mini-splits or a high-velocity small-duct system are usually the better fit in an older home."),
            ("Why is one floor always hotter?", "Heat rises and most systems have one thermostat downstairs. Balancing dampers, a second zone or a ductless unit upstairs fixes it."),
        ],
        "cta": ("AC not keeping up?", "Book a visit online or call. Spring appointments go fast once the first hot week arrives."),
    },
]

AREA_PAGES = [
    {
        "slug": "main-line",
        "name": "The Main Line",
        "title": "Main Line Plumber & HVAC | Ardmore, Bryn Mawr, Wayne, Paoli | Kennedy & Smith Mechanical",
        "desc": "Plumbing, heating and cooling for Main Line homes from Narberth and Ardmore through Bryn Mawr, Wayne and Paoli. Book online.",
        "h1": "Plumbing, heating and cooling on the Main Line",
        "lede": "From Narberth and Ardmore out through Bryn Mawr, Villanova, Wayne and Paoli.",
        "card": "Stone colonials, radiators and ninety-year-old pipe. Narberth to Malvern.",
        "towns": ["Narberth", "Merion", "Bala Cynwyd", "Wynnewood", "Ardmore", "Haverford", "Bryn Mawr", "Gladwyne", "Rosemont", "Villanova", "Radnor", "St. Davids", "Wayne", "Devon", "Berwyn", "Paoli", "Malvern"],
        "body": [
            "The Main Line is named for the Pennsylvania Railroad's main line west out of Philadelphia, and most of its housing followed the tracks between about 1890 and 1940. Stone colonials, Tudors and twins from those years are well built and full of original mechanical systems.",
            "That usually means hot water or steam radiators instead of ducts, cast iron drain stacks, and galvanized or brass supply lines that are near the end of their life. Work in these homes goes better when the plan accounts for plaster walls, slate roofs and finished basements before anything is opened up.",
        ],
        "facts": [
            ("Townships", "Lower Merion and Narberth in Montgomery County, Haverford and Radnor in Delaware County, and Tredyffrin, Easttown and Willistown in Chester County. Each one sets its own permit rules."),
            ("Water", "Mostly Aqua Pennsylvania, which is headquartered in Bryn Mawr."),
            ("Gas and electric", "PECO. Their gas emergency line is 1-800-841-4141."),
            ("Common calls", "Boiler and radiator service, ductless cooling for homes without ducts, galvanized pipe replacement, sump pumps and sewer laterals under old trees."),
        ],
    },
    {
        "slug": "delaware-county",
        "name": "Delaware County",
        "title": "Delaware County Plumber & HVAC | Havertown, Springfield, Media | Kennedy & Smith Mechanical",
        "desc": "Plumbing, heating and cooling across Delaware County, PA: Havertown, Drexel Hill, Upper Darby, Springfield, Broomall, Newtown Square, Media and more. Book online.",
        "h1": "Plumbing, heating and cooling in Delaware County",
        "lede": "Havertown, Drexel Hill and Upper Darby through Springfield, Broomall, Newtown Square and Media.",
        "card": "Twins in Drexel Hill, postwar singles in Springfield, newer homes out past Media.",
        "towns": ["Havertown", "Drexel Hill", "Upper Darby", "Lansdowne", "Clifton Heights", "Springfield", "Morton", "Swarthmore", "Wallingford", "Media", "Broomall", "Newtown Square", "Ridley Park", "Folsom", "Aston", "Glen Mills", "Garnet Valley"],
        "body": [
            "Delco housing changes as you head west. The eastern end, around Upper Darby, Drexel Hill and Lansdowne, is twins and rowhomes from the 1920s through the 1940s, most with basement boilers and shared walls. Springfield, Broomall and Havertown filled in after the war with singles, capes and split-levels on forced air.",
            "Past Media, in Glen Mills and Garnet Valley, the homes are newer and larger, often with two or more HVAC zones and finished basements that depend on a sump pump. We work across all of it.",
        ],
        "facts": [
            ("Water", "Aqua Pennsylvania in most towns. Chester Water Authority serves parts of the southern and western county."),
            ("Gas and electric", "PECO. Their gas emergency line is 1-800-841-4141."),
            ("Permits", "Handled by each township or borough. We tell you up front if your job needs one."),
            ("Common calls", "Water heater replacement, boiler service in older twins, main drain clogs, sump pumps, and AC that struggles on the second floor."),
        ],
    },
    {
        "slug": "philadelphia",
        "name": "Philadelphia",
        "title": "Philadelphia Plumber & HVAC | West Philly, Roxborough, Manayunk | Kennedy & Smith Mechanical",
        "desc": "Plumbing, heating and cooling in Philadelphia, including Overbrook, Wynnefield, West Philadelphia, Roxborough, Manayunk and East Falls. Book online.",
        "h1": "Plumbing, heating and cooling in Philadelphia",
        "lede": "Overbrook, Wynnefield and West Philadelphia up through Manayunk, Roxborough and the Northwest.",
        "card": "Rowhomes, tight basements and shared stacks, mostly on the west side of the city.",
        "towns": ["Overbrook", "Wynnefield", "West Philadelphia", "University City", "East Falls", "Manayunk", "Roxborough", "Mt. Airy", "Chestnut Hill", "Center City", "South Philadelphia"],
        "body": [
            "Philadelphia is a rowhome city, and rowhomes have their own rules. Basements are narrow, the water heater and boiler share a corner, drain stacks run inside party walls, and there is nowhere to stage equipment except the sidewalk.",
            "A lot of city plumbing is a century old, with plenty of lead and galvanized service lines still in the ground. We plan the job around the house, protect the floors on the way in and out, and clean up before we leave.",
        ],
        "facts": [
            ("Water", "Philadelphia Water Department."),
            ("Gas", "Philadelphia Gas Works. Their emergency line is 215-235-1212."),
            ("Electric", "PECO."),
            ("Permits", "Issued by the city's Department of Licenses and Inspections. Philadelphia has its own plumbing code and its own contractor licenses."),
        ],
    },
]

ALSO_NEARBY = ["King of Prussia", "Conshohocken", "Plymouth Meeting", "Lafayette Hill", "West Chester", "Exton"]
