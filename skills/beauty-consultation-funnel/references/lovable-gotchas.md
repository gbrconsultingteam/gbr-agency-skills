# Lovable gotchas

Things that cost real time on the first build. Reading this once saves an hour.

## Pushing to GitHub does not update the live site

This is the big one, and it is genuinely confusing because everything looks
correct while the live site is stale.

Lovable serves the **last published snapshot**. Git sync updates the project and
the editor preview; it does not rebuild the public URL. Someone must publish:

- In the editor: **Publish changes** in the Published panel (top right), or
- Via the connector: `deploy_project(project_id=...)`

Then verify, rather than trusting the UI:

```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  https://<project>.lovable.app/images/<file-only-in-the-new-commit>
```

A 404 on a file you know you committed means the publish shipped an older build.

## "In sync with GitHub" does not mean what it looks like

The Git settings panel reports whether Lovable *received* the commit. It can say
"in sync" while the ingestion job that turns a commit into a buildable state is
still queued — or stuck.

`list_files` is not a reliable check either: it can read the new tree from
GitHub while the project's own build state is behind.

**Diagnose with `list_edits`.** Each commit appears with a `status`. Healthy
commits reach `completed`. One sitting at `pending` for a long time is stalled,
and every build and publish will keep shipping the previous commit.

Note that `list_edits` paginates **oldest-first**, so a small `limit` returns the
oldest edits, not the newest. That is easy to misread as "the commit never
arrived".

## Fixing a stalled ingestion

Push an empty commit to re-fire the webhook:

```bash
git commit --allow-empty -m "Nudge Lovable to ingest <sha>"
git push origin main
```

It usually clears within a few minutes. If it does not, that is worth a support
ticket quoting the project ID and the stuck commit.

## Credits

Messaging Lovable's AI spends workspace credits. Remixing a project and pushing
git commits do not.

There is never a reason to send a build prompt for this template — the code
already exists. The only legitimate uses are things git cannot do: adding a
backend, a database, or an integration.

## Preview vs live

Two different URLs:

- `id-preview--<uuid>.lovable.app` — the editor preview, requires auth
- `<project-slug>.lovable.app` — the public published site

The editor's commit list can also be **pinned** to an older commit — if an entry
reads "Previewing", that is what the pane is showing. Click Preview on the newest
entry, or the refresh icon, to return to HEAD.

## Connecting a repo

In the editor: **Settings → Project → Git → GitHub**, pick the org, name the
repo, **Create Repository**.

Choose *Create*, not *Connect existing*. A Lovable-created repo is standalone,
never a fork of the template — which is what you want, since each client's funnel
should have its own independent history.
