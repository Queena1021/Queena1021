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
- **Streak card** is genuinely flaky. Sampled six times against each of its two
  hosts (`streak-stats.demolab.com` and the legacy `herokuapp` deployment): both
  scored 3/6 — two timeouts past 25s and one HTTP 200 carrying a "Failed to
  retrieve contributions" error card. About half of visitors would see something
  broken. A single probe passes and tells you nothing, which is the whole reason
  to sample.

The first two become worth adding the moment more repos go public. The streak card
only becomes worth adding if its hosting improves; re-sample before trusting it.

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

## Stats host

`github-readme-stats.vercel.app` (the canonical one) returns `DEPLOYMENT_PAUSED`.
Of the working forks, `gh-readme-stats.vercel.app` was chosen because it renders
the real account name and its colour parameters apply correctly.
`github-readme-stats-git-master-rickstaa.vercel.app` serves a valid card to curl
but is blocked by common content blockers, so some visitors would see nothing.

`hide_rank=true` drops the letter grade — the forks disagree with each other
(A+ vs C for the same account), so it measures the fork, not the work.
