# GBR Consulting — agency skills

Claude Code skills for the work we do repeatedly. Each one lives in `skills/`.

| Skill | What it does |
|---|---|
| `beauty-consultation-funnel` | Build a consultation funnel for a beauty client from our Lovable + GitHub template |

New to this? Start with **[docs/getting-started.md](docs/getting-started.md)** —
setup, what to collect from the client, and the two rules that matter.

## Installing

Clone this repo, then symlink or copy the skills you want into your personal
skills directory:

```bash
git clone https://github.com/gbrconsultingteam/gbr-agency-skills.git
cd gbr-agency-skills

# macOS / Linux
ln -s "$PWD/skills/beauty-consultation-funnel" ~/.claude/skills/

# Windows (PowerShell, as admin)
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.claude\skills\beauty-consultation-funnel" `
  -Target "$PWD\skills\beauty-consultation-funnel"
```

A symlink means `git pull` gets you improvements without reinstalling.

Alternatively, drop a skill into a project's `.claude/skills/` if you only want
it available in that repo.

## What you also need

The funnel skill drives Lovable and GitHub, so before using it:

- Access to the **GBR Consulting Lovable workspace** (ask Jon for an invite)
- Membership of the **`gbrconsultingteam`** GitHub org
- Python 3 with Pillow, for the image scripts: `pip install pillow`

## Contributing

These encode what we learned the expensive way — the seam technique, the
publish-vs-push trap, the rule against invented reviews. If you hit something
new on a client build, add it to the relevant reference file rather than keeping
it in your head. The next person building a funnel at 11pm will thank you.
