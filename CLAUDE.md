# CLAUDE.md

GitHub profile README for `Queena1021` — the special `<username>/<username>` repo
that renders on the profile page. Built with the `building-profile-readmes` skill.

## Docs

- [Regenerating the artwork](docs/regenerating.md) — `profile.toml` → SVG, image
  prep, verification and preview commands
- [Why the profile looks the way it does](docs/decisions.md) — what is deliberately
  omitted, why nothing is pinned, why two stats cards were dropped

## Rules for this repo

- **Never hand-edit `assets/hero.svg` or `assets/about.svg`.** They are generated
  from `profile.toml` and edits are overwritten. Change the TOML and rerun.
- **Never add a card URL without fetching it first.** These services return HTTP
  200 with an error card when they fail.
- **The repo must be public for the README to appear on the profile.** It is
  currently private.
