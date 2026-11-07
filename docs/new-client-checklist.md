# New Client Checklist

Work through this top to bottom for every client. Each step says who does it.

## A. Before the pitch (demo)

- [ ] **You:** pick a lead and collect name, phone, hours, services, 2–3 real reviews, photos (from their Google listing).
- [ ] **Claude:** "Make a demo for [business]…" Claude creates `clients/<slug>/site.json`, builds `sites/<slug>/`, and pushes to GitHub.
- [ ] **You (Netlify, first time per client):** create the Netlify site from GitHub (see section D). Name it `<slug>-demo`.
- [ ] **You:** send the demo link with the pitch.

## B. They said yes

- [ ] Send the proposal email (template 6) with the agreement, payment link and intake form link.
- [ ] Agreement signed.
- [ ] Launch fee paid.
- [ ] Intake form submitted (logo, photos, domain info, lead email).
- [ ] **Domain check, do this on day one:**
  - Where is the domain registered? Do we have login or delegate access?
  - Does their **email** run on this domain? If yes, never touch MX or email records.
  - Is it locked inside a website builder (Wix, Squarespace site plan, Landingsite…)? If so, start a transfer or nameserver change now. These can take days.
  - No domain yet? Buy it in Netlify (**Domains → Buy a domain**) so DNS and https are automatic.

## C. Build and launch

- [ ] **Claude:** update `site.json` with intake answers, add logo and photos to `clients/<slug>/assets/`, rebuild, push. Netlify updates on its own.
- [ ] Client reviews the live preview link and approves by email.
- [ ] **Netlify → Forms:** form detection is on, and the **contact** form is listed.
- [ ] **Netlify → Forms → Add notification → Email:** client's lead email, form `contact`. (Optionally add yourself too.)
- [ ] **Netlify → Domain management → Add a domain:** the client's domain.
- [ ] Add the DNS records Netlify shows at the client's registrar:
  - `A` · `@` · `75.2.60.5`
  - `CNAME` · `www` · `<netlify-site-name>.netlify.app`
  - Or switch nameservers to Netlify DNS if the registrar makes records awkward.
  - Delete only the old **website** records. Leave MX, TXT and email records alone.
- [ ] Wait for **DNS verified** and **HTTPS enabled** in Netlify.
- [ ] Test on a phone: page loads with the padlock, call button dials, form sends, and the client receives the email.
- [ ] Rename the Netlify site from `<slug>-demo` to `<slug>`.
- [ ] Send the launch email (template 8). Ask for a review and referrals.
- [ ] Set up monthly billing (autopay).

## D. Netlify setup for one client (from this GitHub repo)

One repository holds every client. Each client gets its own Netlify site that only publishes their folder.

1. Netlify → **Add new project → Import an existing project → GitHub**, then choose the `site-factory` repo.
2. Set:
   - **Base directory:** `sites/<slug>`
   - **Build command:** leave empty
   - **Publish directory:** `sites/<slug>` (or `.` if Netlify shows it relative to the base)
3. Deploy. From now on, every push that changes that client's folder updates their site automatically.
4. Optional, to stop other clients' changes from triggering a rebuild: **Project configuration → Build & deploy → Ignore builds**, command `git diff --quiet $CACHED_COMMIT_REF $COMMIT_REF -- .`

## E. Intake form (set up once)

1. Create one more Netlify site from the same repo with **base and publish directory `intake`**.
2. Netlify → **Forms → enable form detection**, then redeploy.
3. **Forms → Add notification → Email** to your own email, form `intake`.
4. Send `https://<your-intake-site>.netlify.app` to every new client.

## F. Monthly care

- [ ] Make requested text, price or hour changes (ask Claude, push).
- [ ] Check Netlify Forms for spam, and that form emails are arriving.
- [ ] Domain auto-renew is on (whoever holds it).
