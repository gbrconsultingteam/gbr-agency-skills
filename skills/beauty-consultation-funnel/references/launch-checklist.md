# Pre-launch checklist

Run `scripts/preflight.py <repo>` first — it catches the mechanical failures.
Then walk the rest by hand, because some of these need judgement.

## Blocking — do not publish until these are true

- [ ] **Booking link is real and works.** Open it. Confirm it loads and lets
      someone actually pick a time. `BOOKING_URL` / `ENROLL_URL` is not `null`.
- [ ] **No invented reviews.** Every entry in `REVIEWS` is a real review from a
      real person, copied verbatim. If there are none, the array is empty and
      the section is hidden — that is a valid state to launch in.
- [ ] **No invented claims.** No years of experience, student counts, success
      rates or credentials that the client did not state.
- [ ] **No TODO placeholders left** in any config, meta title, or alt text.
- [ ] **Contact details verified** with the client, not transcribed from an old
      footer screenshot. A wrong phone number costs bookings silently.
- [ ] **Photo rights confirmed**, including consent for any recognisable faces.

## Content

- [ ] The four consultation cards describe *this* client's craft, not generic
      reassurance. If a card would read fine on a competitor's site, rewrite it.
- [ ] Services and training copy are not mixed. A page addressed to both clients
      and students persuades neither.
- [ ] The Google rating, if shown, is labelled as the business's overall rating.
      On a training page it is not a training-specific score and must not imply
      students left it.
- [ ] Meta title and description name the service and the city.
- [ ] Every gallery image has real alt text describing what is happening.

## Visual

- [ ] **The hero seam is invisible** on mobile — the copy panel and the photo
      meet with no visible band. Re-measure if you changed the photo.
- [ ] The desktop hero copy never runs under the photo, at 1024, 1280 and 1440.
- [ ] The headline holds **two lines on a phone**. Three lines pushes the CTA
      down and looks cramped. Shortening the headline usually beats shrinking
      the type — check at 320, 360 and 390 px wide.
- [ ] The CTA button is visible without scrolling on a typical phone.
- [ ] No horizontal scrolling at any width.
- [ ] Small accent-coloured text — rating stars, reviewer names, footer icons —
      is actually readable. Pale brand accents often fail here; that is what the
      darker accent token is for.
- [ ] Logo reads correctly on the black header. If the client's logo is
      multicolour, the invert trick will not work and you need a white version.

## Technical

- [ ] `npx tsc --noEmit` clean.
- [ ] `npm run build` clean.
- [ ] Every image under ~250 KB.
- [ ] `/` redirects to `/consultation`.
- [ ] The training route is deleted if the client does not sell courses.

## After publishing

- [ ] **Verify the publish actually landed.** Request a file that only exists in
      the new commit and confirm it returns 200. Lovable's "in sync" indicator
      refers to git, not to the live site.
- [ ] Load the live URL on a real phone. Emulators miss things.
- [ ] Click the CTA on the live site and confirm it reaches the booking flow.
