---
name: beauty-consultation-funnel
description: Build a consultation funnel landing page for a beauty business — salon, PMU artist, lash tech, barber, aesthetician, hairstylist, med spa, nail studio — or a training funnel for their courses, using GBR Consulting's Lovable + GitHub template. Use this whenever someone wants to create, replicate, set up or clone a funnel or landing page for a beauty client; whenever a new beauty client is being onboarded; whenever Lovable and a client landing page come up together; and when editing an existing funnel built from this template (swapping hero photos, updating copy, changing the booking link, adding real reviews). Also use it when someone asks how our funnels are structured or why a funnel looks the way it does.
---

# Beauty consultation funnel

Every funnel we build has one job: get the visitor to book a consultation. Not
to browse services, not to read a menu of prices — to book. That single purpose
is why the page has no navigation, why the CTA repeats down the page, and why
the CTA label never changes across clients.

You are building from a template rather than from scratch. The design decisions
are already made and tested; your job is to learn enough about this specific
client to fill it in convincingly, and to avoid the handful of mistakes that
turn a good funnel into an embarrassing one.

## Before anything else: check the connections

The workflow needs a Lovable account with access to the GBR workspace, and
GitHub access to the `gbrconsultingteam` org. Confirm both before onboarding a
client — discovering a missing permission halfway through is worse than a
30-second check.

1. Lovable connector responding, and the GBR workspace visible.
2. Git configured locally, and push access to `gbrconsultingteam`.

If either is missing, stop and say exactly which one. Teammates on their own
accounts usually need an invite to the Lovable workspace and to the GitHub org.

## Never spend Lovable credits

Every message to Lovable's AI costs the workspace real money, and it is never
necessary here. The template already contains the code.

- **Remix** `beauty-funnel-template` — copying a project costs nothing.
- Then **edit files locally and `git push`**. GitHub syncs into Lovable.
- Do not send build prompts, do not ask Lovable's AI to make changes.

The only legitimate reasons to message Lovable's AI are things git cannot do:
adding a backend, a database, or an integration.

## The shape of the work

1. Onboard the client — see `references/onboarding.md`
2. Remix the template, connect a new repo, clone it
3. Prepare images — see `references/images.md`
4. Fill in the config files
5. Run the pre-launch check — see `references/launch-checklist.md`
6. Publish, and verify the publish actually landed

### 1. Onboarding

Read `references/onboarding.md` and work through it with whoever is briefing
you. It is a conversation, not a form: ask follow-ups when an answer is thin,
because the quality of the four consultation cards depends entirely on how well
you understand what the client actually does.

Two things people routinely forget to ask for, and both block launch:

- **The real booking link.** A scheduler URL, not a contact page.
- **Real reviews.** Copied verbatim, with names, from their Google profile.

Save every answer into `docs/client-brief.md` in the new repo as you go. The
brief lives with the code so the next person — or you in three months — has the
full context without asking the client again.

### 2. Remix, connect, clone

```
remix_project(project_id=<template project>, workspace_id=<GBR workspace>,
              project_name="<client>-funnel")
```

Then connect it to a new GitHub repo. This part is manual and cannot be
scripted — the teammate does it in the Lovable editor:

> Settings (left sidebar) → Project → Git → GitHub → choose the
> `gbrconsultingteam` org → repo name → **Create Repository**

Make sure it says *Create Repository*, not *Connect existing repository*. Then
clone it locally and work there.

### 3. Images

Read `references/images.md`. The hero treatment is what makes these pages look
designed rather than assembled, and it depends on measuring the photograph
rather than eyeballing it. `scripts/measure_image.py` does the measuring and
tells you exactly what to paste into the config.

### 4. Fill in the config

Three files, all heavily commented:

- `src/config/client.ts` — business identity, shared by both funnels
- `src/config/services.ts` — the `/consultation` page
- `src/config/training.ts` — the `/training-consultation` page

Delete the training route and config if the client only sells treatments. A
half-filled second funnel is worse than not having one.

**The four consultation cards are where funnels succeed or fail.** Keep the
shape — four cards, roughly 20-25 words each — because the grid is built for
that rhythm. Change the substance completely. "We discuss your goals and create
a plan" could be any business on earth; "Adriana looks at your skin type, bone
structure and existing brows to work out which technique will actually hold"
could only be a PMU artist. Write from what the client told you, and prefer the
specific over the polished.

### 5. Pre-launch check

Run through `references/launch-checklist.md`. `scripts/preflight.py` automates
the parts a script can check — leftover TODOs, empty CTA links, invented
reviews, oversized images, missing alt text.

### 6. Publish, then verify

Pushing to GitHub does **not** update the live site. Lovable serves the last
published snapshot, so someone must publish — in the editor, or via the
connector's `deploy_project`.

Then verify, because "in sync" on the Git settings page does not mean the live
site was rebuilt:

```bash
curl -s -o /dev/null -w '%{http_code}' https://<project>.lovable.app/images/<a-file-only-in-the-new-commit>
```

If Lovable's ingestion stalls — the commit sits at `pending` in `list_edits`
while the Git panel claims everything is in sync — push an empty commit to
re-fire the webhook. `references/lovable-gotchas.md` has the details.

## Things that are not style preferences

**Never invent reviews or testimonials.** Not as placeholders, not "just to see
the layout", not even when asked directly. Publishing fabricated testimonials on
a commercial page is deceptive and breaches the FTC's rule on fake reviews
(16 CFR Part 465), and a page that ships with them exposes the client to real
liability. The template ships `REVIEWS` empty and the section hides itself —
that is the correct state until real reviews exist. If someone asks for
placeholder reviews to check the layout, explain why not and offer to show the
section with the client's real Google rating badge alone.

**Never invent credentials, experience or outcomes.** No "over a decade of
experience", no student counts, no success rates, unless the client stated it.
It is very easy to write a plausible sentence that turns out to be false about a
real person.

**Never point a CTA somewhere that isn't a real booking flow.** `null` is the
correct value until you have the link — the button then renders visibly
disabled, which is honest. A live-looking button that goes nowhere loses the
booking and the client's trust at once.

**Ask about photo rights.** Before/after images of faces need the client's
consent from the people in them. This is a real question, not a formality.

## Reference files

- `references/onboarding.md` — the client questionnaire, and why each question matters
- `references/images.md` — dimensions, the hero seam technique, optimisation
- `references/launch-checklist.md` — what to verify before publishing
- `references/lovable-gotchas.md` — publish vs push, stalled syncs, credits

## Scripts

- `scripts/measure_image.py` — sample a photo's edges; reports the colours to paste into config and whether the mobile slice is needed
- `scripts/prepare_images.py` — crop, resize and optimise hero and gallery images, and generate the slice
- `scripts/preflight.py` — pre-launch checks across the repo
