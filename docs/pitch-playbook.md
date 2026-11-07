# Pitch Playbook

The method: **build the demo first, then pitch with the link.** A business owner who sees their own name on a finished site decides in minutes. A description of a site gets "send me some info."

---

## 1. Find leads (30 minutes = 20 leads)

Search Google Maps for a trade plus a town: "plumber Troy MI", "hair salon Royal Oak", "auto repair Ferndale".

Good targets:

| Signal | Why it matters |
|---|---|
| **No website** in their Google listing | Easiest yes. Everyone knows they need one. |
| Site looks old or broken on a phone | Open it on your phone. If you pinch to zoom, so do their customers. |
| Site is a free builder subdomain (`.wixsite.com`, `.godaddysites.com`) | Looks unprofessional; they know it. |
| **Lots of good reviews** (30+ at 4.5★+) | They have customers and money, and the site will have real proof on it. |
| Owner-operated (name in the business, owner replies to reviews) | You can reach the decision maker directly. |

Skip: franchises (corporate controls the site), businesses with a modern site, and listings with very few reviews.

Track leads in a spreadsheet: business, owner name, phone, email, current site, review count, status, demo link, next follow-up date.

## 2. Build the demo (20–40 minutes each)

Grab from their Google listing: name, phone, address, hours, services, 2–3 real reviews (first name + initial), photos.

Then ask Claude:

> Make a demo site for [Business] in [City]. Phone [..], hours [..], services [..]. Use these reviews: [..]. Brand color [from their logo or sign].

Deploy it to a free Netlify link like `smith-plumbing-demo.netlify.app`. Leave the form notification pointed at **you** until they buy.

Only use reviews and photos that are really theirs, and say "demo" in the pitch so nothing is misread as their official site.

## 3. Reach out

Best order: **walk in or call** (highest response), then text, then email. Use the templates in `email-templates.md`.

### Phone / walk-in script

> Hi, is this [Owner]? This is [Your name], I build websites for local businesses here in [Area].
>
> I was looking at [Business] on Google. You've got [87] reviews, which is great, but [you don't have a website / your site is hard to use on a phone]. So I went ahead and built you one. Can I text you the link? It takes 30 seconds to look at.
>
> *(After they look)*
>
> What do you think? Anything you'd change?
>
> It's ready to go live on your own web address. It includes the contact form that sends leads straight to your phone and email, and I handle hosting and updates. It's [$X] to launch and [$Y] a month. If you want it, I can have it live this week.

### Handling objections

| They say | You say |
|---|---|
| "I get all my work from word of mouth." | "That's great. When someone gets your name from a friend, the first thing they do is Google you. This makes sure what they find closes the deal." |
| "I already have a website." | "Totally. Pull it up on your phone next to this one. Which would you call?" |
| "It's too expensive." | "One extra job a month covers it. We can also start with the launch-only package and skip the monthly." |
| "My nephew is building me one." | "No problem. Keep this link. If it's not done in a month, call me and this one goes live the same day." |
| "Send me some info." | "Sure. The best info is the site itself. I'll text you the link now and check back Thursday. Does that work?" |
| "I need to think about it." | "Of course. What would you need to see to say yes?" (Then answer that.) |

## 4. Follow up

Most yeses happen on the 2nd–4th touch.

| Day | Action |
|---|---|
| 0 | Call or visit, send demo link |
| 2 | Text: "Did you get a chance to look?" |
| 5 | Email follow-up #1 |
| 10 | Call again |
| 20 | Final email: "Taking the demo down Friday unless you want it." |

## 5. Pricing (starting point; adjust for your market)

| Package | Price | Includes |
|---|---|---|
| **Starter** | $500–$800 launch + $49/mo | One-page site, contact form to email, domain connection, hosting, small text updates |
| **Growth** | $1,200–$1,800 launch + $99/mo | Everything in Starter + booking link, Google Business Profile tune-up, review request link, monthly updates |
| **Konnect AI add-on** | quoted | AI chat or voice agent, missed-call text back, lead follow-up automation |

Rules of thumb: collect the launch fee **before** going live, put the monthly fee on autopay, and offer a small discount for paying 12 months upfront.

## 6. After the sale

Follow `new-client-checklist.md`. Ask every happy client for:
1. A Google review of **your** business.
2. Two referrals: "Who else do you know who needs this?"
