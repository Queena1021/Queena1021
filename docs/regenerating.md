# Regenerating the artwork

`assets/hero.svg` and `assets/about.svg` are generated from `profile.toml` by the
`building-profile-readmes` skill (`~/.claude/skills/building-profile-readmes`).
Hand edits to the SVGs are overwritten on the next run — change the TOML instead.

```bash
python3 ~/.claude/skills/building-profile-readmes/scripts/gen_banner.py --config profile.toml --out assets/hero.svg
python3 ~/.claude/skills/building-profile-readmes/scripts/gen_panel.py  --config profile.toml --out assets/about.svg
```

## Palette

`cinnamoroll` — a daytime palette added to both generators for this profile. Pale
sky blue crossfading to pastel pink, white cloud banks, a warm sun, dark blue ink.

It sets `light = True`, which flips the scene builders: the dark palettes draw
stars, mountain ridges and a *darkening* scrim, none of which read on a pale sky.
In light mode those become sparkles, cloud banks and a *whitening* scrim, the moon
becomes a sun with its own warm edge colour, and the title switches from a glowing
neon gradient to solid dark type over a white bloom.

Every colour that ends up as small text has to clear 4.5:1 on its background. In
the panel that includes `accent`, which appears as 12px stack-tag text — which is
why the panel's accent is a deep rose (`#a83d6e`) and not a pastel pink. The soft
pink (`#ff9ec6`) lives on the banner, where only the frame and horizon rule use it.

The card URLs in `README.md` hardcode matching values: background `#f6fcff`,
headings `#a83d6e`, body text `#14435f`, icons `#1f5878`. Changing `[palette]`
means updating those query strings too, then re-running `audit_contrast.py`.

## Images

Both mascot images are base64-embedded into the SVGs, so nothing is hotlinked and
nothing can 404 later.

- `assets/cinnamoroll.png` — banner motif, positioned by `banner.image_x/_y/_size`
- `assets/avatar.png` — the circle in the panel

Source files came from `~/CinnamorollPic/`. Two things were done to them first:

1. **Resized** to ~360px (`sips -Z 360`). Base64 inflates by a third and every
   visitor downloads the whole SVG.
2. **Metadata stripped** — only `IHDR/PLTE/IDAT/IEND/tRNS` chunks kept. Both
   source files carried an `eXIf` chunk that `sips` alone does not remove.

The banner source also shipped with a transparency checkerboard **baked into the
pixels** and a fully opaque alpha channel, which drew a grey grid in the banner.
It was keyed out by clearing border-connected pixels matching the two checker
greys (`#ffffff`, `#f0f0f0`) — the character survives because its body is
`#feff fe`, a shade off pure white, and is enclosed by the brown outline.

## Before publishing

```bash
python3 ~/.claude/skills/building-profile-readmes/scripts/verify_services.py --user Queena1021 --repo simptradkeyboard
python3 ~/.claude/skills/building-profile-readmes/scripts/audit_contrast.py --readme README.md
python3 ~/.claude/skills/building-profile-readmes/scripts/audit_privacy.py  --path . --repo Queena1021/Queena1021
```

The stats services are volunteer-run and a dead one returns HTTP 200 with an SVG
reading "Something went wrong", so re-probe rather than trusting a status code.

To preview locally the way GitHub will render it:

```bash
python3 -c "import base64,pathlib,subprocess; md=pathlib.Path('README.md').read_text(); b=subprocess.run(['gh','api','markdown','-f','text='+md,'-f','mode=markdown'],capture_output=True,text=True).stdout; [b:=b.replace(f'./assets/{n}.svg','data:image/svg+xml;base64,'+base64.b64encode(pathlib.Path(f'assets/{n}.svg').read_bytes()).decode()) for n in ('hero','about')]; pathlib.Path('preview.html').write_text('<style>body{background:#0d1117;color:#e6edf3;font:16px/1.6 sans-serif;max-width:1012px;margin:0 auto;padding:32px 48px}img{max-width:100%}</style>'+b)"
```
