#!/usr/bin/env python3
"""Search Wikimedia Commons and Openverse for freely licensed images, download
them, and drop the ones a machine can reject: too small, blurry, duplicate,
mature, or with a license that can't be confirmed.

    /usr/bin/python3 find_image.py --out DIR "query one" ["query two" ...]

Writes DIR/cand-NNN.{jpg,png} and DIR/candidates.json. Saved images are scaled down to at most
MAX_LONG_SIDE px (never up) and have their metadata (camera, GPS) removed; licenses allow this,
including no-derivatives ones, since it's a format change, not an edit. Each entry has the credit
fields (title, creator, license, source_url), `commercial` (true = cv, false = ci),
`no_derivatives`, and `rejected` (null, or why it was dropped). Only entries with
rejected == null are worth looking at.

cv / ci:
  Commons hosts only licenses that allow commercial use, so everything from it is cv.
  Openverse: any NonCommercial license (by-nc, by-nc-sa, by-nc-nd) is ci; the rest is cv.
"""
import argparse
import html
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import numpy as np
from PIL import Image

# Wikimedia requires contact details in the User-Agent and answers 429 without them.
UA = "slides-skill/1.0 (https://github.com/heartnetkung/claude-skills; image search for slide decks)"
MIN_LONG_SIDE = 1000     # px; a half-slide column is ~4.4in, so 1000px is ~225 dpi
MAX_LONG_SIDE = 1920    # px; the most a full-width slide on a 1080p projector can show
MIN_SHARPNESS = 60.0     # Laplacian variance at 1000px wide; below this, visibly soft
MAX_BYTES = 20_000_000
TIMEOUT = 30


def get(url, as_json=False):
    # Wikimedia throttles bursts from one client: space requests out, back off on 429.
    wikimedia = "wikimedia.org" in urllib.parse.urlparse(url).netloc
    for attempt in range(3):
        if wikimedia:
            time.sleep(1 + 4 * attempt)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = r.read(MAX_BYTES + 1)
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 2:
                raise
    if len(data) > MAX_BYTES:
        raise ValueError("file too large")
    return json.loads(data) if as_json else data


def strip_html(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def search_commons(query, n):
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": n,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1920,  # a standard thumbnail width; others get throttled
    }
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params), as_json=True)
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = p["imageinfo"][0]
        meta = ii.get("extmetadata", {})
        lic = strip_html(meta.get("LicenseShortName", {}).get("value"))
        out.append({
            "source": "commons",
            "title": strip_html(meta.get("ObjectName", {}).get("value")) or p["title"].removeprefix("File:"),
            "creator": strip_html(meta.get("Artist", {}).get("value")) or "unknown",
            "license": lic,
            "license_url": meta.get("LicenseUrl", {}).get("value", ""),
            "source_url": ii["descriptionurl"],
            "download_url": ii.get("thumburl") or ii["url"],
            "commercial": True,
            "no_derivatives": False,
            "mature": False,
        })
    return out


def search_openverse(query, n):
    params = {"q": query, "page_size": n, "mature": "false"}
    d = get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params), as_json=True)
    out = []
    for r in d.get("results", []):
        code = r.get("license", "")
        name = code.upper().replace("BY", "CC BY") if code not in ("cc0", "pdm") else code.upper()
        out.append({
            "source": "openverse/" + (r.get("source") or "?"),
            "title": r.get("title") or "untitled",
            "creator": r.get("creator") or "unknown",
            "license": f"{name} {r.get('license_version') or ''}".strip(),
            "license_url": r.get("license_url") or "",
            "source_url": r.get("foreign_landing_url") or "",
            "download_url": r.get("url") or "",
            "commercial": "nc" not in code,
            "no_derivatives": "nd" in code,
            "mature": bool(r.get("mature")),
        })
    return out


def sharpness(img):
    g = img.convert("L")
    if g.width > 1000:
        g = g.resize((1000, round(g.height * 1000 / g.width)))
    a = np.asarray(g, dtype=np.float32)
    lap = -4 * a[1:-1, 1:-1] + a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:]
    return float(lap.var())


def encode(img):
    """Encode img for the deck: PNG stays PNG (it may be transparent), everything else becomes JPEG.
    Scales down to MAX_LONG_SIDE, never up, and writes no metadata. Returns (ext, bytes, size)."""
    as_png = img.format == "PNG" or img.mode in ("RGBA", "LA", "P")
    small = img.copy()
    small.thumbnail((MAX_LONG_SIDE, MAX_LONG_SIDE), Image.LANCZOS)
    buf = io.BytesIO()
    if as_png:
        small.save(buf, "PNG", optimize=True)
    else:
        small.convert("RGB").save(buf, "JPEG", quality=85, optimize=True)
    return ("png" if as_png else "jpg"), buf.getvalue(), small.size


def ahash(img):
    g = np.asarray(img.convert("L").resize((8, 8)), dtype=np.float32)
    return "".join("1" if v else "0" for v in (g > g.mean()).flatten())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-source", type=int, default=12, help="results per query per source")
    ap.add_argument("queries", nargs="+")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    found, seen_urls = [], set()
    for q in args.queries:
        hits = 0
        for search in (search_commons, search_openverse):
            try:
                results = search(q, args.per_source)
            except Exception as e:  # one source down shouldn't sink the other
                print(f"warning: {search.__name__}({q!r}) failed: {e}", file=sys.stderr)
                continue
            hits += len(results)
            for r in results:
                if r["download_url"] and r["download_url"] not in seen_urls:
                    seen_urls.add(r["download_url"])
                    r["query"] = q
                    found.append(r)
        if not hits:
            print(f"warning: no results for {q!r}; try fewer or plainer words", file=sys.stderr)

    hashes = {}
    for i, c in enumerate(found, 1):
        c["file"], c["rejected"] = None, None
        if c["mature"]:
            c["rejected"] = "mature"
        elif not c["license"] or not c["source_url"]:
            c["rejected"] = "license or source unconfirmed"
        if c["rejected"]:
            continue
        try:
            data = get(c["download_url"])
            img = Image.open(io.BytesIO(data))
            img.load()
        except Exception as e:
            c["rejected"] = f"download failed: {e}"
            continue
        c["width"], c["height"] = img.size
        c["sharpness"] = round(sharpness(img), 1)
        h = ahash(img)
        dup = next((name for other, name in hashes.items()
                    if sum(a != b for a, b in zip(h, other)) <= 4), None)
        if max(img.size) < MIN_LONG_SIDE:
            c["rejected"] = f"too small ({img.width}x{img.height})"
        elif c["sharpness"] < MIN_SHARPNESS:
            c["rejected"] = f"blurry (sharpness {c['sharpness']})"
        elif dup:
            c["rejected"] = f"duplicate of {dup}"
        if c["rejected"]:
            continue
        ext, encoded, (c["width"], c["height"]) = encode(img)
        c["file"] = os.path.join(os.path.abspath(args.out), f"cand-{i:03d}.{ext}")
        with open(c["file"], "wb") as f:
            f.write(encoded)
        hashes[h] = os.path.basename(c["file"])

    with open(os.path.join(args.out, "candidates.json"), "w") as f:
        json.dump(found, f, indent=1)
    kept = [c for c in found if not c["rejected"]]
    print(f"{len(found)} found, {len(kept)} kept → {args.out}/candidates.json")
    for c in kept:
        tag = "cv" if c["commercial"] else "ci"
        print(f"  {os.path.basename(c['file'])} [{tag}] {c['width']}x{c['height']} "
              f"sharp={c['sharpness']} {c['license']} | {c['title'][:50]}")
    reasons = {}
    for c in found:
        if c["rejected"]:
            key = c["rejected"].split(" (")[0].split(":")[0]
            reasons[key] = reasons.get(key, 0) + 1
    if reasons:
        print("  dropped: " + ", ".join(f"{k} {v}" for k, v in sorted(reasons.items())))


if __name__ == "__main__":
    main()
