# Site Factory

Build, launch and manage websites for local businesses from one repository.

```
clients/<slug>/site.json   ← each client's details (the only file you normally edit)
clients/<slug>/assets/     ← their logo and photos
sites/<slug>/              ← the finished website (generated; this is what Netlify publishes)
sites/konnect-ai/          ← Konnect AI's own site (hand-built, not generated)
intake/                    ← client intake form (deploy once, send the link to every new client)
docs/                      ← pitch playbook, email templates, client agreement, checklist
build.mjs                  ← turns site.json into a website
```

## Make a new client site

The easy way: ask Claude.

> New client: [Business] in [City]. Phone …, email …, hours …, services …, reviews …, brand color …. Make the site and push it.

By hand:

```bash
cp -r clients/_example clients/smith-plumbing
# edit clients/smith-plumbing/site.json
node build.mjs smith-plumbing
git add -A && git commit -m "Add Smith Plumbing" && git push
```

Then create the client's Netlify site once (see `docs/new-client-checklist.md`, section D). After that, every push updates their site automatically.

Rebuild everyone after a template change: `node build.mjs --all`

## What every generated site includes

- Mobile-first layout with a sticky call button on phones, plus light and dark mode
- Hero, services, why-us, reviews, service area and hours, FAQ, contact form
- Netlify contact form with phone/email validation and spam protection; set the email alert per client
- Optional online booking button
- Local business SEO data (schema.org) for Google
- Brand color, 4 font styles (`modern`, `classic`, `friendly`, `bold`), optional logo and hero photo

## site.json reference

See `clients/_example/site.json` for every option. Required: `business.name`, `business.phone`. Leave out any section (`reviews`, `faq`, `why`, `services`) to hide it.

Icons for services and why-us: `wrench drop bolt home leaf sun snow hammer paint car tooth scissors paw heart shield clock star chat calendar truck dollar spark check phone pin mail`.

## Docs

- `docs/pitch-playbook.md`: finding leads, call script, objections, follow-up schedule, pricing
- `docs/email-templates.md`: cold email, follow-ups, proposal, domain access, launch, review request
- `docs/client-agreement.md`: website services agreement template (have a lawyer review it once)
- `docs/new-client-checklist.md`: step by step from demo to launch, including Netlify and DNS
