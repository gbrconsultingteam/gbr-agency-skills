# Getting started — your first funnel

For anyone on the team building their first client funnel. Roughly 20 minutes of
setup, once.

## 0. Access you need first

Ask Jon for these before you start. Each takes him a minute and blocks
everything otherwise.

- **Lovable** — an invite to the *GBR Consulting Lovable* workspace
- **GitHub** — membership of the `gbrconsultingteam` org

Confirm both work:

- Open Lovable. You should see the GBR workspace and a project called
  `beauty-funnel-template`.
- Run `git ls-remote https://github.com/gbrconsultingteam/beauty-funnel-template.git`
  in a terminal. If it prints a commit hash, you're in.

## 1. Install the skill

```bash
git clone https://github.com/gbrconsultingteam/gbr-agency-skills.git
cd gbr-agency-skills
```

Then link the skill into your personal skills directory.

**macOS / Linux**

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/beauty-consultation-funnel" ~/.claude/skills/
```

**Windows** (PowerShell as Administrator)

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.claude\skills\beauty-consultation-funnel" `
  -Target "$PWD\skills\beauty-consultation-funnel"
```

A symlink means `git pull` in this repo gets you fixes and improvements without
reinstalling anything.

## 2. Install Pillow

The image scripts need it:

```bash
pip install pillow
```

Check it: `python -c "import PIL; print('ok')"`

## 3. Start a build

Open Claude Code in whatever folder you keep client work in, and describe the
job in your own words. Something like:

> New funnel for a lash studio in Austin, services only. Walk me through the
> onboarding questions.

You don't need to name the skill — it should pick it up. If it doesn't, say
"use the beauty-consultation-funnel skill".

## 4. What to collect from the client

The build stalls without these, so gather them early. The skill will ask, but
you'll move faster if you already have them.

**Non-negotiable before the page can go live:**

- **Their website URL.** Not screenshots — the live site is where the exact
  brand colours and fonts come from.
- **The real booking link.** Open it yourself and confirm it lets someone pick
  a time. A contact form is not a scheduler.
- **Real reviews**, copied word for word, with names. If they have none, the
  reviews section stays hidden — that's fine and correct.

**Also needed:**

- Logo, ideally SVG on transparent background
- One good hero photo — the owner at work, plain backdrop, space above their head
- Four to six gallery photos
- Whether they own those photos and have consent from anyone recognisable in them
- Business name, legal name, city, phone, email, address, socials
- How a consultation actually runs, start to finish — this feeds the four cards
  and is the question people rush

## 5. Two rules with real consequences

**Never invent reviews.** Not even as temporary placeholders to see the layout.
Publishing fabricated testimonials breaches the FTC's rule on fake reviews
(16 CFR Part 465) and the exposure lands on the client. Leave the array empty;
the section hides itself.

**Never invent facts about the client.** No years of experience, class sizes or
success rates unless they said it. It's easy to write a plausible sentence that
turns out to be false about a real person.

If either feels like it's blocking you, that's the signal to go back to the
client, not to fill the gap.

## 6. Before you publish

Run the pre-launch check:

```bash
python ~/.claude/skills/beauty-consultation-funnel/scripts/preflight.py /path/to/client-repo
```

It blocks on leftover placeholders, a CTA link that goes nowhere, and invented
reviews. Then walk `references/launch-checklist.md` for the things a script
can't judge — the hero seam, mobile fit, whether the copy sounds like this
client or like a template.

## 7. Publishing

**Pushing to GitHub does not update the live site.** Lovable serves the last
*published* snapshot. You must publish in the Lovable editor, then verify by
loading a file that only exists in your new commit.

This trips up everyone once. It's normal, not something you did wrong.

## When something doesn't match these instructions

Tell Jon. This skill is new and parts of it were written from expectation
rather than experience — the first version told you to create the GitHub repo
yourself, which turned out to be wrong. Corrections make it better for the next
person; working around it silently doesn't.
