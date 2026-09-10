# Client onboarding

Work through this as a conversation. Where an answer is thin, push once — the
difference between a funnel that converts and one that looks templated is
almost entirely in how specific these answers are.

Record everything in `docs/client-brief.md` in the client's repo as you go, so
the context lives with the code.

## 1. What is this funnel for?

- **Services**, **training**, or **both**?

Both means one project with two routes. Only build the second if they genuinely
sell courses today — an aspirational training page with nothing behind it wastes
the visitor's click.

Whatever the answer, the funnel's goal is a booked consultation. That does not
change per client, and neither does the CTA label.

## 2. The business

- Trading name, as a customer would say it
- Legal entity name, for the footer copyright (often differs — ask, don't guess)
- City and state
- Phone, email, street address
- Facebook and Instagram URLs
- Do they have a Google Business Profile with a rating worth showing? Get the
  link and the review count.

Asking for a **screenshot of their current site's footer** is a good shortcut —
it usually has the address, phone and socials in one place. Verify what you read
rather than transcribing blindly; footers go stale.

## 3. Their website — ask for the URL, not just screenshots

This is the single highest-value question for visual fidelity.

With the live URL you can read exact colours and the actual font stack from
computed styles. A screenshot gives you an approximation of the colours and no
font information at all. Ask for both if you like — screenshots are useful for
layout reference — but the URL is what makes the brand match precise.

What to extract:

- The accent colour used for buttons and highlights
- Whether their headings use a serif or sans, and which one
- Their dark text colour, and their section background tints

If they have no website, ask for their Instagram and work from the palette in
their posts — and say plainly that you are approximating.

## 4. What they sell

**For a services funnel:** the two or three main services that a consultation
would lead to. Not their whole menu — the ones worth a conversation.

**For a training funnel:** the two or three main courses. Ask for the syllabus
or outline if one exists; condensing a real curriculum beats inventing modules,
and prospective students can tell the difference.

## 5. What actually happens in a consultation

This feeds the four numbered cards, and it is the question people rush. Slow
down here.

Ask them to walk you through a real consultation from the moment the client sits
down. Listen for the parts only they would say: what they look at first, what
they check before recommending anything, what they refuse to do, how they
explain pricing.

You need four distinct beats, each describable in about 20-25 words. If their
answer gives you three, ask what happens at the end. If it gives you six,
combine.

Good beats are concrete and slightly opinionated. Weak ones are generic
reassurance.

## 6. Images

Ask for these specifically. `references/images.md` has the dimensions and what
makes a good hero.

- **Logo** — ideally SVG, on a transparent background. A single dark colour
  works best; the header inverts it to white.
- **Hero photo** — the owner at work, ideally with a client or student. You need
  a square framing for desktop and a taller framing for mobile. One good
  original can usually produce both.
- **Four to six gallery photos** — real results for a services funnel; real
  classes for a training funnel.

Ask directly: **do they own these photos, and do they have consent from the
people in them?** Before/afters of faces are the common problem.

## 7. Reviews

Ask for real reviews, copied verbatim with the reviewer's name and roughly when
they were left. The Google Business Profile is the usual source.

If they have none yet, the reviews section stays hidden. That is fine and it is
the correct behaviour — do not fill it with invented testimonials to make the
page look complete. See the rules in SKILL.md.

For a training funnel, client reviews about treatments are **not** student
reviews. Do not carry them over even though every word is genuine; presenting a
treatment review as course feedback is misleading.

## 8. The booking link

The most-forgotten item, and the one that makes the funnel work.

Ask for the actual scheduler URL — Square, Vagaro, Calendly, Acuity, GoHighLevel,
whatever they use. Then open it and confirm it loads and lets someone pick a
time.

A contact form or an email address is not a scheduler. If that is genuinely all
they have, it can still work, but say so in the CTA microcopy so the visitor
knows a human will follow up rather than expecting a calendar.

Until you have a working link, leave it `null`. Disabled buttons are honest;
dead links are not.

## 9. Where it will live

- Do they have a domain or subdomain in mind?
- Is anything already pointing at an existing page that this will replace?

Worth knowing early: a Lovable project's live URL changes when you move to a
custom domain, and anything already linking to the old one breaks.
