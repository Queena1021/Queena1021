# Why the profile looks the way it does

## What is deliberately not here

Email, phone, employer and university are all omitted. The résumé they came from
has them; a profile README is not a CV, and a personal email on a public profile
is scraped within days.

`git config user.email` is set **per-repo** to the GitHub noreply address
(`<numeric-id>+Queena1021@users.noreply.github.com`, id from
`https://api.github.com/users/Queena1021`) so commit metadata on a public repo does
not publish a personal address. This only affects commits made after it was set,
which is why it was set before the first commit. Check it with `git config
user.email`.

## Pinned repos: none

13 of 15 repos are private. A pin card for a private repo renders broken for every
visitor *and* puts the repo name and its description in the README source as plain
text — the second part is the one that matters for unreleased work.

The two public repos are `simptradkeyboard` and `forage-midas`. Add pins once more
repos are public:

```
<img src="https://github-readme-stats-git-master-rickstaa.vercel.app/api/pin/?username=Queena1021&repo=NAME"/>
```

## One stats card, not four

Three other cards were built, verified, and then removed:

- **Top languages** read **Swift 100%**. The service only sees public repos, and
  the one substantial public repo is the Swift keyboard. The card was not broken —
  it was accurate about public code and badly wrong about the person.
- **Activity graph** rendered an empty flat line. Private-repo contributions do
  not reach that service, so it looked like a dead account.
The two become worth adding the moment more repos go public.

## The streak card ships flaky, knowingly

Sampled six times against each of its two hosts (`streak-stats.demolab.com` and
the legacy `herokuapp` deployment). Both scored **3/6**: two timeouts past 25s and
one HTTP 200 carrying a "Failed to retrieve contributions" error card. Roughly half
of visitors see something broken.

It is in the README by explicit request with that tradeoff understood. A single
probe passes and tells you nothing here, which is the whole reason to sample — if
you ever wonder whether it has improved, sample it again rather than loading the
profile once.

## Contribution snake

`.github/workflows/snake.yml` runs `Platane/snk` on every push to `main` and every
12 hours, rendering to the `output` branch, which the README references by raw URL.

Two things about it:

- **The raw URL 404s while the repo is private.** `raw.githubusercontent.com` does
  not serve private repos. The workflow still runs and the `output` branch still
  updates — the image simply cannot load until the repo is public. Expected, not a
  bug to chase.
- **The ramp has to step, and it has to clear the page.** The empty cell is most of
  the grid, so two separate mistakes both make it look broken: levels 0-2 bunched
  at the pale end (the grid reads as empty), and an empty cell close to the GitHub
  background (`#e8f4fd` vanished on white, `#16202b` on `#0d1117`). Current ramps:

  | | empty | 1 | 2 | 3 | 4 | snake |
  |---|---|---|---|---|---|---|
  | light | `#d3e8f7` | `#8ecdf0` | `#4a9fd4` | `#2a6f96` | `#14435f` | `#a83d6e` |
  | dark | `#243447` | `#2f6c92` | `#4a9fd4` | `#8fd0ee` | `#d6f0fd` | `#ff9ec6` |

The grid is sparse because the public calendar has 12 active days in the last year
(121 contributions, concentrated in bursts). That is accurate, not a rendering
fault, and it fills in on its own.

`count_private=true` is on the stats card by explicit choice. It folds private-repo
contribution counts into the totals — no repo names are exposed, but the aggregate
is derived from private activity. `audit_privacy.py` flags it as MED every run;
that finding is expected, not an oversight.

## The stack is drawn once

As a `skillicons.dev` strip in `README.md`, not also as a tag row in the panel —
`panel.stack` is deliberately empty in `profile.toml`. A tag row, an icon strip and
a prose list are three renderings of one fact.

Unknown slugs are dropped **silently**, so a short row means a typo rather than an
error. Verify by counting the nested `<svg>` elements in the response:

```bash
curl -s 'https://skillicons.dev/icons?i=java,ts,py' | grep -c '<svg'
```

`n8n` is not a slug — it, Spring AI and Qwen are named in the caption underneath
instead. `theme=light` matches the pale palette; `theme=dark` puts the icons on
near-black tiles that float on the light cards.

## Theme-aware images: two traps

The snake and the footer wave each ship as a `<picture>` with a light and a dark
variant. Both broke in ways that looked like colour bugs in the artwork.

**A comma in `srcset` truncates the URL.** `srcset` parses commas as separators
between candidates, so capsule-render's gradient
`color=0:9bdcf7,50:4a9fd4,100:a83d6e` was cut down to `color=0:9bdcf7` — a
near-black wave with no text. Percent-encode them (`%2C`, and `%3A` for the
colons) inside any `srcset`. The `src` of a plain `<img>` has no such parsing,
which is why only the dark variant was affected. The snake URLs contain no
commas, which is why they never showed this.

**`<picture>` only drives a direct child `<img>`.** The markdown API wraps every
rendered image in an `<a>`, which makes the `<img>` a grandchild and causes every
theme-aware image to fall back silently to its light variant. That is a preview
artifact — `scripts/preview.py` unwraps them — but it hid the real result for
several rounds. If a variant looks wrong, check `img.currentSrc` before changing
any colours.

## The divider

`assets/divider.svg` is **hand-written**, not generated from `profile.toml` — the
skill's generators produce the banner and the panel only. Editing it directly is
correct; it will not be overwritten.

The rule is a `<rect>`, not a `<line>`: a line has zero height, so its bounding box
has no area and an `objectBoundingBox` gradient resolves to nothing and vanishes.
Both ends fade to transparent so it carries no background of its own and reads on
a white page and a dark one alike.

## Stats host

`github-readme-stats.vercel.app` (the canonical one) returns `DEPLOYMENT_PAUSED`.
Of the working forks, `gh-readme-stats.vercel.app` was chosen because it renders
the real account name and its colour parameters apply correctly.
`github-readme-stats-git-master-rickstaa.vercel.app` serves a valid card to curl
but is blocked by common content blockers, so some visitors would see nothing.

`hide_rank=true` drops the letter grade — the forks disagree with each other
(A+ vs C for the same account), so it measures the fork, not the work.
