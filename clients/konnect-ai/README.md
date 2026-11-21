# konnectai.org

Source for Konnect AI's own site (`sites/konnect-ai/`).

- `index.html` is hand-built. Sections between `<!--NAME-->` markers are filled in by the generator.
- `pages.py` builds every other page, the shared header/footer, sitemap, robots.txt and redirects.
  Run it after any change: `python3 clients/konnect-ai/pages.py`

## Prospect pages (konnectai.org/for/<slug>/)

A personal page for each prospect, with their name, a pre-set system diagram and a pre-filled cost calculator. Hidden from Google.

1. Copy `prospects/sample-insurance.json` to `prospects/<business-slug>.json`.
2. Fill in `business`, `first_name`, `industry` (one of the industry page file names), `note`,
   the starting `system` (inputs: form, phone, email, text, chat, social · ai: qualify, answer, collect, docs ·
   outcomes: crm, book, alert, follow, report, review) and calculator defaults.
3. Run `python3 clients/konnect-ai/pages.py`, commit and push.
4. Send the link `https://konnectai.org/for/<business-slug>/`.

Or just ask Claude: "Make a prospect page for [business], [first name], [industry]."

## Founder photo and video

Add `sites/konnect-ai/assets/tristan.jpg` (square, at least 400×400) and/or `assets/tristan.mp4`, then run the generator. They appear in the founder section automatically.
