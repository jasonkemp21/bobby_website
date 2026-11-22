"""Site settings and page copy for Kennedy & Smith Mechanical.

Everything a non-developer is likely to change lives in SITE at the top.
Change it here, run `python3 src/build.py`, and every page updates.
"""

SITE = {
    "name": "Kennedy & Smith Mechanical",
    "domain": "https://kandsmechanical.com",
    # Used on every page.
    "phone_display": "(610) 819-7789",
    "phone_tel": "+16108197789",
    "hours": "Mon to Fri, 6 AM to 8 PM",
    "hours_schema": "Mo-Fr 06:00-20:00",
    # Where the shop is based.
    "town": "Havertown",
    "state": "PA",
    # Pennsylvania registers home improvement contractors with the Attorney General
    # (number looks like PA123456) and it has to appear in advertising.
    "pa_hic": "PA162454",
    # Municipal licenses worth listing, e.g. "Master Plumber #12345". Empty until known.
    "other_licenses": [],
    # Housecall Pro
    "hcp_org": "Kennedy-and-Smith-Mechanical",
    "hcp_book_token": "a8d62a41ba21462caf2a9f9c9c8bf10e",
    "hcp_lead_token": "ab7ce96b4764422dad58e3566f36a950",
    # True while the owner is still reviewing: shows the checklist button, tells search engines to stay out.
    "preview": True,
}

# The two owners. Each has his own inbox: Bob takes plumbing and water, Joe takes heating and cooling.
# The first email is the one given to search engines as the business contact.
OWNERS = [
    {
        "name": "Bob Smith",
        "role": "Master plumber",
        "trade": "Plumbing and water",
        "does": "Water heaters, water filtration and softeners.",
        "email": "bob@kandsmechanical.com",
    },
    {
        "name": "Joe Kennedy",
        "role": "Senior HVAC technician",
        "trade": "Heating and cooling",
        "does": "Furnaces, boilers, central air, heat pumps and ductless systems.",
        "email": "joe@kandsmechanical.com",
    },
]

# Shown in the preview checklist drawer. Delete items as Bobby answers them.
TO_CONFIRM = [
    ("Registration number", "PA162454 is in the footer as the Pennsylvania Home Improvement Contractor number. Confirm that is what it is. If Bob wants his master plumber license number listed as well, send it."),
    ("Town lists", "The Delaware County and Main Line towns are our picks. Strike any town you do not want calls from."),
    ("What you install", "The service pages list softeners, carbon filters and salt-free conditioners; furnaces, boilers, central air, heat pumps and ductless; tank, tankless and heat pump water heaters. Strike anything you do not sell."),
    ("Water heater repairs", "The water heater page sells replacement only. Say so if you want repair calls too."),
    ("Promises in the copy", "Insured, a price before work starts, a water test before quoting treatment, old equipment taken away, and cleanup before leaving. Strike anything you would not put in writing."),
    ("Online booking menu", "The Book online button opens Housecall Pro. The services listed there should match the three on this site."),
    ("Reviews", "There are no testimonials on the site. Real Google reviews go in once the Business Profile verification clears."),
    ("Photos", "Every photo is one of your jobs. A picture of Bob and Joe, and one of the truck, would finish the About page. Town names for the photo captions would help too."),
]

AREAS_SHORT = "Delaware County and the Main Line"

# Job photos. Every one is a Kennedy & Smith install. The files are made by src/jobphotos.py,
# which also strips the location data phones attach. "title" and "text" are the caption.
JOBS = {
    "boiler": {
        "alt": "Wall-hung high-efficiency boiler on a white board with new copper piping, two circulator pumps and an expansion tank",
        "title": "Boiler replacement",
        "text": "A wall-hung high-efficiency boiler with new copper piping, circulators and expansion tank.",
    },
    "furnace": {
        "alt": "New gas furnace and cooling coil in a basement, with new sheet metal ductwork and white vent piping",
        "title": "Furnace and coil",
        "text": "A new gas furnace and cooling coil tied into new sheet metal.",
    },
    "condensers": {
        "alt": "Two new outdoor heating and cooling units on raised pads over gravel beside a brick house",
        "title": "Two-system replacement",
        "text": "Both outdoor units replaced and set on raised pads over gravel.",
    },
    "ductless": {
        "alt": "Wall-mounted ductless mini-split unit high on a white wall",
        "title": "Ductless mini-split",
        "text": "Heating and cooling for one room on its own thermostat, with no ductwork.",
    },
    "water-heaters": {
        "alt": "Two new gas water heaters side by side in a closet, piped in copper with a shared expansion tank",
        "title": "Twin water heaters",
        "text": "Two gas tanks piped together in copper with a shared expansion tank.",
    },
    "water-heater": {
        "alt": "New gas water heater with copper connections and an expansion tank, the install date written on the label",
        "title": "Gas water heater",
        "text": "A new tank with copper connections and an expansion tank, dated the day it went in.",
    },
    "filtration": {
        "alt": "Whole-house water filtration tank and a sediment prefilter piped into the main water line beside a water heater",
        "title": "Whole-house filtration",
        "text": "A filtration system and sediment prefilter on the main water line.",
    },
    "ac-pair": {
        "shape": (1200, 900),  # the one wide photo; the rest are 1200 x 1500
        "alt": "Two outdoor air conditioning units on pads over white gravel beside a house",
        "title": "Central air replacement",
        "text": "Two outdoor units on new pads with fresh line sets and disconnects.",
    },
}

# The four photos in the home page's work row, each linking to its service page.
HOME_JOBS = [("boiler", "hvac-replacement"), ("condensers", "hvac-replacement"), ("water-heaters", "water-heaters"), ("filtration", "water-filtration")]

SERVICES = [
    {
        "slug": "hvac-replacement",
        "icon": "hvac",
        "name": "HVAC replacement",
        "card": "New furnaces, boilers, central air, heat pumps and ductless systems.",
        "card_points": ["Furnaces and boilers", "Central air and heat pumps", "Ductless mini-splits"],
        "triage": ("Furnace, boiler or AC on its last legs", "Heating and cooling replacement"),
        "title": "Furnace, Boiler & AC Replacement | Delaware County & Main Line | Kennedy & Smith Mechanical",
        "desc": "Furnace, boiler, central air, heat pump and ductless system replacement in Delaware County and on the Main Line. Sized to the house and installed by the owners. Book online.",
        "h1": "Heating and cooling system replacement",
        "lede": "When the furnace, boiler or air conditioner is at the end of its life, we size the new system to the house, install it ourselves and take the old one away.",
        "photo": "furnace",
        "handle_h": "What we replace and install",
        "handle": [
            "Gas furnaces", "Hot water boilers", "High-efficiency wall-hung boilers",
            "Central air conditioners", "Heat pumps", "Ductless mini-splits",
            "Air handlers and coils", "Ductwork changes for the new system", "Boiler piping and circulators",
            "Thermostats and zone controls", "Venting and condensate drains", "Old equipment removal",
        ],
        "signs_h": "Signs it's time to replace",
        "signs": [
            ("The system is past its expected life", "A gas furnace usually lasts fifteen to twenty years and central air twelve to fifteen. A boiler that has been looked after can go longer. Past those ages, parts fail more often and efficiency drops."),
            ("The repair bills keep coming", "One repair on a ten-year-old system is normal. A second and a third inside a couple of years means the next bill is better spent on new equipment."),
            ("An air conditioner that runs on R-22", "Most systems put in before 2010 use R-22 refrigerant, which has not been made in the US since 2020. Recharging one is expensive, so a leak is usually the point to replace."),
            ("Rooms that never get comfortable", "Sometimes that is the ductwork, or one thermostat in the wrong place. Sometimes the equipment was the wrong size from the day it went in. We check before we quote, so the new system does not inherit the old problem."),
        ],
        "side": None,
        "jobs_h": "Heating and cooling installs",
        "jobs": ["boiler", "condensers", "ductless"],
        "local": ("No ducts? That is common here", "A lot of homes in Delaware County and on the Main Line were built with radiators and never had ductwork. That does not rule out air conditioning. Ductless mini-splits heat and cool room by room through a small line to an outdoor unit, with no plaster to tear out. And when the boiler itself is due, a wall-hung high-efficiency boiler gives back floor space in the basement."),
        "faq_h": "Replacement questions",
        "faqs": [
            ("Should I repair or replace?", "If the system is past fifteen years and the repair costs a large share of a new unit, replacing is usually the better use of the money. Younger than that, a repair usually makes more sense, and we will say so before we quote a replacement."),
            ("How long does a replacement take?", "A furnace or air conditioner swap is usually done in a day. A boiler, a full heating and cooling system or new ductwork can take two or three days. We give you the schedule before we start."),
            ("How do you decide what size system I need?", "By the house, not by the label on the old unit. We look at the square footage, the insulation, the windows and the existing ducts or radiators. Equipment that is too big turns on and off constantly, wears out sooner and leaves the house clammy in summer."),
            ("Do heat pumps work in Pennsylvania winters?", "Current cold-climate heat pumps heat well through winters here. Many homeowners keep their furnace or boiler as backup for the coldest days."),
            ("Do I need a permit?", "Usually, for new heating and cooling equipment. Each township and borough handles its own. We tell you what your job needs before we start."),
        ],
        "cta": ("System on its last legs?", "Book a visit online or call. We will look at what you have and price the replacement."),
    },
    {
        "slug": "water-heaters",
        "icon": "tank",
        "name": "Water heaters",
        "card": "Tank, tankless and heat pump water heaters, replaced and installed.",
        "card_points": ["Leaking or failed tanks", "Tankless upgrades", "Gas and electric"],
        "triage": ("Water heater leaking or running out", "Water heater replacement"),
        "title": "Water Heater Replacement & Installation | Delaware County & Main Line | Kennedy & Smith Mechanical",
        "desc": "Water heater replacement in Delaware County and on the Main Line. Gas, electric, tankless and heat pump water heaters, installed by a master plumber. Book online.",
        "h1": "Water heater replacement",
        "lede": "A tank that is leaking, rumbling or past ten years old. We replace it with the right size and type, pipe it in properly and take the old one away.",
        "photo": "water-heaters",
        "handle_h": "What we install",
        "handle": [
            "Gas tank water heaters", "Electric tank water heaters", "Tankless water heaters",
            "Heat pump water heaters", "Expansion tanks", "Relief valves and drain pans",
            "Gas line and venting changes", "New shutoffs and copper connections", "Old unit removal",
        ],
        "signs_h": "Signs it's time to replace",
        "signs": [
            ("Water around the base", "If the tank itself is leaking, it is finished. Shut the cold water valve above the heater and call. Water from a fitting or the relief valve is a different problem, and we will tell you which one you have."),
            ("Rumbling or popping", "Sediment has settled on the bottom and water is boiling under it. On an old tank it is a sign the end is close."),
            ("Rusty hot water", "If only the hot side runs brown, the inside of the tank is probably corroding, and a leak usually follows."),
            ("The unit is past ten years", "Most tank heaters last eight to twelve years. Past that, it is cheaper to replace one on your schedule than on a holiday weekend."),
        ],
        "side": "water-heater",
        "jobs_h": None,
        "jobs": [],
        "local": ("Tank or tankless?", "A tankless unit heats water as you use it, hangs on the wall and can last around twenty years with yearly descaling. It also costs more up front and often needs a larger gas line and new venting. In a home with one or two bathrooms, a good tank is usually the better buy. We price both so you can compare."),
        "faq_h": "Water heater questions",
        "faqs": [
            ("How long does a water heater last?", "A tank unit typically lasts eight to twelve years. Tankless units can reach twenty with regular descaling. The serial number on the label tells you the build date."),
            ("What size do I need?", "For a tank, 40 gallons suits most homes with two or three people and 50 gallons suits four or five. Tankless units are sized by how many fixtures run at once."),
            ("How long does the install take?", "A like-for-like tank swap usually takes a few hours. Switching to tankless or changing the fuel takes longer, because the gas line, venting or wiring often has to change."),
            ("Why does a new heater need an expansion tank?", "Water expands as it heats. In a house with a check valve or pressure reducer on the main, that pressure has nowhere to go, and it wears on the tank and the fixtures. A small expansion tank takes it up."),
        ],
        "cta": ("Water heater on its way out?", "Book online or call with the fuel type and tank size from the label, and we will come prepared."),
    },
    {
        "slug": "water-filtration",
        "icon": "drop",
        "name": "Water filtration and softeners",
        "card": "Whole-house filters, softeners and conditioners, matched to your water.",
        "card_points": ["Hard water and scale", "Chlorine taste and smell", "Whole-house systems"],
        "triage": ("Hard water, spots or a bad taste", "Water filtration and softeners"),
        "title": "Water Filtration & Water Softener Installation | Delaware County & Main Line | Kennedy & Smith Mechanical",
        "desc": "Whole-house water filtration and water softener installation in Delaware County and on the Main Line. We test your water first, then fit the system to it. Book online.",
        "h1": "Water filtration and softeners",
        "lede": "Scale on the fixtures, spots on the dishes, or water that smells like a pool. We test your water, then install a system that fits what is in it.",
        "photo": "filtration",
        "handle_h": "What we install",
        "handle": [
            "Water softeners", "Whole-house carbon filtration", "Sediment prefilters",
            "Salt-free conditioners", "Combined filter and conditioner systems", "Water testing before we quote",
            "Bypass and shutoff valves", "Drain line connections", "Old system removal",
        ],
        "signs_h": "Signs your water needs attention",
        "signs": [
            ("White crust on faucets and shower heads", "That is scale: calcium and magnesium left behind when hard water dries. The same crust builds up inside the water heater, where you cannot see it."),
            ("Spots on glasses and soap that will not lather", "Both point to hardness. A softener takes the minerals out. A salt-free conditioner leaves them in the water but keeps them from sticking to surfaces."),
            ("A chlorine taste or smell", "Public water is disinfected with chlorine. A whole-house carbon filter takes the taste and the smell out at every tap, the shower included."),
            ("Orange stains or grit in the faucet screens", "Usually iron or sediment, more common on well water and in homes with old galvanized pipe. A sediment filter catches grit. Iron needs its own treatment, which is one reason we test first."),
        ],
        "side": None,
        "jobs_h": None,
        "jobs": [],
        "local": ("We test before we quote", "Most homes in Delaware County and on the Main Line get their water from Aqua Pennsylvania, and hardness changes with the town and the source. A home on a private well is a different job again. We test the water at your tap and fit the system to the result, so you do not pay for treatment you do not need."),
        "faq_h": "Water treatment questions",
        "faqs": [
            ("Softener or filter: which one do I need?", "They do different jobs. A softener deals with hardness, the minerals behind scale and spots. A carbon filter deals with chlorine taste and smell. Plenty of homes want both, and a combined system handles the two in one install."),
            ("Does a softener make the water salty?", "No. The salt cleans the softener's resin and is rinsed down the drain. Softening does add a small amount of sodium to the water, more when the water started out harder. If that matters in your house, ask us about a salt-free system."),
            ("How much upkeep is there?", "A softener needs salt added to its brine tank, usually every month or two. Sediment cartridges are changed on a schedule that depends on your water and how much you use. Tank-style carbon filters run for years between media changes."),
            ("Where does it go, and how long does it take?", "Where the main water line comes into the house, usually in the basement near the meter and the water heater. It needs a drain close by and, for most systems, an outlet. Most installs are finished the same day."),
        ],
        "cta": ("Tired of hard water?", "Book a visit online or call. We will test your water and price the options."),
    },
]

AREA_PAGES = [
    {
        "slug": "delaware-county",
        "name": "Delaware County",
        "where": "in Delaware County",
        "title": "Delaware County HVAC Replacement, Water Heaters & Water Treatment | Kennedy & Smith Mechanical",
        "desc": "Heating and cooling replacement, water heaters and water treatment across Delaware County, PA: Havertown, Drexel Hill, Springfield, Broomall, Newtown Square, Media and more. Book online.",
        "h1": "HVAC, water heaters and water treatment in Delaware County",
        "lede": "Our home county. Havertown, Drexel Hill and Upper Darby through Springfield, Broomall, Newtown Square and Media.",
        "card": "Home base. Twins in Drexel Hill, postwar singles in Springfield, newer homes out past Media.",
        "towns": ["Havertown", "Drexel Hill", "Upper Darby", "Lansdowne", "Clifton Heights", "Springfield", "Morton", "Swarthmore", "Wallingford", "Media", "Broomall", "Newtown Square", "Ridley Park", "Folsom", "Aston", "Glen Mills", "Garnet Valley"],
        "body": [
            "Delco housing changes as you head west. The eastern end, around Upper Darby, Drexel Hill and Lansdowne, is twins and rowhomes from the 1920s through the 1940s, most with a boiler in the basement and shared walls. Springfield, Broomall and Havertown filled in after the war with singles, capes and split-levels on forced air.",
            "Past Media, in Glen Mills and Garnet Valley, the homes are newer and larger, often with two or more heating and cooling systems. We are based in Havertown and work across all of it.",
        ],
        "facts": [
            ("Water", "Aqua Pennsylvania in most towns. Chester Water Authority serves parts of the southern and western county. Hardness varies, so we test before recommending treatment."),
            ("Gas and electric", "PECO. Their gas emergency line is 1-800-841-4141."),
            ("Permits", "Handled by each township or borough. We tell you up front if your job needs one."),
            ("Common jobs", "Furnace and central air replacements, new boilers in older twins, water heaters, and softeners or whole-house filters."),
        ],
    },
    {
        "slug": "main-line",
        "name": "The Main Line",
        "where": "on the Main Line",
        "title": "Main Line HVAC Replacement, Water Heaters & Water Treatment | Kennedy & Smith Mechanical",
        "desc": "Heating and cooling replacement, water heaters and water treatment for Main Line homes from Narberth and Ardmore through Bryn Mawr, Wayne and Paoli. Book online.",
        "h1": "HVAC, water heaters and water treatment on the Main Line",
        "lede": "From Narberth and Ardmore out through Bryn Mawr, Villanova, Wayne and Paoli.",
        "card": "Stone colonials and radiator heat, from Narberth out to Malvern.",
        "towns": ["Narberth", "Merion", "Bala Cynwyd", "Wynnewood", "Ardmore", "Haverford", "Bryn Mawr", "Gladwyne", "Rosemont", "Villanova", "Radnor", "St. Davids", "Wayne", "Devon", "Berwyn", "Paoli", "Malvern"],
        "body": [
            "The Main Line is named for the Pennsylvania Railroad's main line west out of Philadelphia, and most of its housing followed the tracks between about 1890 and 1940. Stone colonials, Tudors and twins from those years are well built and full of original mechanical systems.",
            "That usually means hot water or steam radiators instead of ducts, a boiler in the basement and no easy path for central air. A replacement in one of these homes goes better when the plan accounts for plaster walls, slate roofs and finished basements before anything is opened up.",
        ],
        "facts": [
            ("Townships", "Lower Merion and Narberth in Montgomery County, Haverford and Radnor in Delaware County, and Tredyffrin, Easttown and Willistown in Chester County. Each one sets its own permit rules."),
            ("Water", "Mostly Aqua Pennsylvania, which is headquartered in Bryn Mawr. Hardness varies, so we test before recommending treatment."),
            ("Gas and electric", "PECO. Their gas emergency line is 1-800-841-4141."),
            ("Common jobs", "Boiler replacements, ductless systems for homes without ducts, water heaters, and whole-house filtration."),
        ],
    },
]
