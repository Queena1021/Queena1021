#!/usr/bin/env python3
"""Render README.md the way GitHub will, into preview.html.

Uses GitHub's own markdown API rather than a local markdown library, so the
HTML matches what the profile page produces.

Two substitutions are needed because the preview pane serves the page from a
data: URL, where neither relative paths nor the private repo's raw URLs
resolve:

- ./assets/*.svg          -> inlined, since ./ cannot resolve from a data: URL
- the snake's raw URLs    -> inlined from the output branch, since
                             raw.githubusercontent.com 404s while the repo is
                             private

Both <picture> sources are inlined, not just the fallback. Substituting only
the light one makes the preview show a white grid to anyone in dark mode and
sends you chasing a colour bug that is not in the artwork.

    python3 scripts/preview.py            # snake from the output branch
    python3 scripts/preview.py --no-snake # skip it if gh is unavailable
"""
import argparse
import base64
import pathlib
import re
import subprocess
import sys

REPO = "Queena1021/Queena1021"
PAGE_CSS = (
    'body{background:#0d1117;color:#e6edf3;'
    'font:16px/1.6 -apple-system,"Segoe UI",sans-serif;'
    'max-width:1012px;margin:0 auto;padding:32px 48px}'
    'img{max-width:100%}'
    'h2{border-bottom:1px solid #30363d;padding-bottom:.3em}'
    'sub{color:#8d97a8}a{color:#4493f8}'
    '@media(prefers-color-scheme:light){body{background:#fff;color:#1f2328}'
    'h2{border-color:#d1d9e0}}'
)


def data_uri(raw: bytes) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()


def gh(*args: str) -> str:
    out = subprocess.run(["gh", *args], capture_output=True, text=True)
    if out.returncode:
        sys.exit(out.stderr.strip() or "gh failed")
    return out.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-snake", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    md = (root / "README.md").read_text()
    body = gh("api", "markdown", "-f", f"text={md}", "-f", "mode=markdown")

    # The markdown API wraps every rendered image in an <a>. That makes the
    # <img> a grandchild of <picture>, and <picture> only applies its <source>
    # elements to a direct child <img> — so every theme-aware image silently
    # falls back to its light variant in the preview and looks like a palette
    # bug. GitHub's own README rendering keeps the img directly inside.
    body = re.sub(r"<a\b[^>]*>\s*(<img\b[^>]*>)\s*</a>", r"\1", body)

    for asset in sorted((root / "assets").glob("*.svg")):
        body = body.replace(f"./assets/{asset.name}", data_uri(asset.read_bytes()))

    if not args.no_snake:
        light, dark = (data_uri(base64.b64decode(gh(
            "api", f"repos/{REPO}/contents/{n}?ref=output", "--jq", ".content")))
            for n in ("github-snake.svg", "github-snake-dark.svg"))
        # The <picture> block is rebuilt whole rather than having its URLs
        # substituted: the markdown API rewrites every image URL to its camo
        # proxy, so matching on raw.githubusercontent.com finds nothing, fails
        # silently, and leaves the preview showing something else entirely.
        # Only the snake's block: the footer is a second <picture>, and its
        # capsule-render URLs are public, so camo serves those fine.
        blocks = [m for m in re.finditer(r"<picture>.*?</picture>", body, re.S)
                  if "Snake eating" in m.group(0)]
        if len(blocks) != 1:
            sys.exit(f"expected 1 snake <picture> block, found {len(blocks)}")
        m = blocks[0]
        body = (body[:m.start()]
                + '<picture><source media="(prefers-color-scheme: dark)" '
                  f'srcset="{dark}"/><img alt="Snake eating my contribution graph" '
                  f'src="{light}"/></picture>'
                + body[m.end():])

    out = root / "preview.html"
    out.write_text('<!doctype html><meta charset="utf-8">'
                   '<title>README preview</title>\n'
                   f"<style>{PAGE_CSS}</style>\n{body}")
    print(f"{out}  {len(out.read_text())} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
