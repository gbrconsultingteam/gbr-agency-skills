# Images

## What to ask the client for

| Asset | Ask for | Ends up as |
|---|---|---|
| Logo | SVG, transparent, single dark colour | `logo.svg` |
| Hero | One good photo of the owner at work | two crops, below |
| Gallery | 4–6 real results or class photos | 1000×1000 each |

## Dimensions

| File | Size | Where it appears |
|---|---|---|
| `{svc,trn}-hero-desktop.jpg` | **1400 × 1400** | right 56% of the desktop hero |
| `{svc,trn}-hero-mobile.jpg` | **1200 wide**, roughly square to 1:1.2 tall | stacked under the copy on mobile |
| `{svc,trn}-gallery-1..4.jpg` | **1000 × 1000** | 2-column grid |

Keep every file **under ~250 KB**. These pages are mostly opened on phones over
mobile data, and unoptimised camera JPEGs or PNG exports routinely arrive at
5–8 MB each. `scripts/prepare_images.py` handles the resize and re-encode.

## What makes a good hero photo

- The owner **at work**, ideally with a client or student, rather than a posed
  portrait. It shows the service rather than the person.
- Shot against a **plain backdrop** — a seamless, a clean wall. Busy rooms make
  the copy unreadable and the seam impossible.
- **Clear space above their head.** The copy panel sits directly above the photo
  on mobile, so a subject cropped at the top edge leaves nowhere for the join.
- The subject **left of centre**, so on desktop they sit next to the copy rather
  than at the far edge.

## The seam — why this matters

On mobile the layout is: copy panel, then photo, stacked with nothing between
them. They read as one continuous section only if the panel's background matches
the photo's top edge exactly. A few levels off and you get a visible band across
the page.

Two cases, and `scripts/measure_image.py` tells you which one you are in:

**The backdrop is flat** (a painted wall usually is). A single colour matches it.
Set `PANEL_GROUND` to the measured value and `HERO_IMAGE_MOBILE_TOP` to `null`.
Simplest case — one less asset to keep in sync.

**The backdrop drifts** across the frame (studio seamlesses usually do — lighting
falls off toward the edges). No flat colour can match at both ends: match the
left and the right shows a seam. Instead use a **1-pixel-tall slice of the
photo's own top row**, stretched vertically behind the panel. It carries the
drift across and matches at every horizontal position. The script generates this
as `{svc,trn}-hero-mobile-top.png`; point `HERO_IMAGE_MOBILE_TOP` at it.

On desktop the photo sits in the right column with a soft gradient on its left
edge. `HERO_GROUND` should match the photo's **left edge**, so the gradient has
almost nothing to bridge.

**Re-run the measurement whenever a hero photo changes**, and update the config.
A swapped photo with stale ground colours is the most common way the seam comes
back.

## Cropping the mobile hero

The mobile photo wants a small amount of clear backdrop above the subject —
around 45–90 px at 1200 wide. Not more.

The reason: the copy panel above supplies the vertical space, and it is a roughly
fixed height at any screen width while the photo scales with the viewport. Baked
headroom that looks right on one phone is dead air on another. Let CSS carry the
spacing and keep the photo tight.

`scripts/prepare_images.py` finds the subject's top edge and crops to leave the
right margin automatically.

## Generated photos

If a client has no usable photos, generated imagery is an option, but be careful:

- Whiteboard or signage **text comes out as garbled pseudo-writing**. Ask for
  diagrams and shapes instead, or plan to paint text out afterwards.
- Hands holding objects, and anything reflective like a mirror, fail often.
  Reflections in particular are worth designing around rather than fixing.
- Very glossy skin is a strong "AI" tell. Ask for natural, matte, documentary
  lighting instead.

Always tell the client which images are generated. Passing off a generated
classroom as a photo of their real studio is a misrepresentation they will have
to defend, not you.
