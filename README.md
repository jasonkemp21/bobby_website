# Kennedy & Smith Mechanical website

Static site served by a Cloudflare Worker (`_worker.js` adds the preview password gate).

## Change something

1. Copy and settings are in `src/content.py`. The phone number, email, hours, PA registration number
   and Housecall Pro tokens are all in the `SITE` block at the top and feed every page.
2. Layout is in `src/build.py`, styles in `css/site.css`, behaviour in `js/site.js`.
3. Run `python3 src/build.py`. It rewrites the `.html` files, `sitemap.xml` and `robots.txt` in the repo root.
   Do not edit those by hand.

`python3 src/build.py --bundle` also writes `preview/index.html`, the whole site in one file,
for sharing somewhere that cannot load Housecall Pro. Booking buttons there open Housecall Pro in a new tab.

## View it locally

    python3 -m http.server 8095

Then open http://localhost:8095. Online booking and the request form load from Housecall Pro, so they need internet.

## Housecall Pro

- Every "Book online" button opens the Housecall Pro booking window on the page. If their script is blocked,
  the button falls back to the same booking page in a new tab.
- The contact page embeds the Housecall Pro lead form. Submissions land in Housecall Pro as leads.

## Before launch

- Work through `TO_CONFIRM` in `src/content.py` with the owner and delete the items as they are answered.
- Set `"preview": False` in `SITE`. That removes the checklist button and the noindex tag,
  and opens `robots.txt` to search engines.
- Remove the password gate: delete `main` and `run_worker_first` from `wrangler.jsonc`, or drop `_worker.js`.
- Replace the four stock photos in `img/` (run `node src/photos.mjs <folder>` to grade new ones the same way).

## Credits

County outlines on the service-area map: OpenStreetMap contributors (ODbL).
