#!/usr/bin/env python3
"""Find overflowing slides in a built deck, and optionally export every slide as PNG.

    /usr/bin/python3 check.py path/to/deck.pptx [--png OUT_DIR]

Runs its own headless LibreOffice with a throwaway profile, so the user's
LibreOffice (and the reload pipe) is never touched.

error:   text, a table or an image runs past the bottom of the slide (exit 1)
warning: text runs past the bottom of its own text box but stays on the slide

PNGs land in OUT_DIR as slide-01.png, slide-02.png, ... (numbered like the
report).
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import time

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException

TOLERANCE = 50  # 1/100 mm; rounding noise when a box grows to fit its text
PNG_DPI = 80    # 800x450 per 10in slide: enough to judge layout, cheap to read


def prop(name, value):
    p = PropertyValue()
    p.Name, p.Value = name, value
    return p


def start_office(profile, pipe):
    proc = subprocess.Popen(
        ["soffice", f"-env:UserInstallation={uno.systemPathToFileUrl(profile)}",
         "--headless", "--invisible", "--norestore", f"--accept=pipe,name={pipe};urp;"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local)
    for _ in range(120):
        try:
            ctx = resolver.resolve(f"uno:pipe,name={pipe};urp;StarOffice.ComponentContext")
            return proc, ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        except NoConnectException:
            time.sleep(0.5)
    proc.kill()
    sys.exit("error: headless LibreOffice did not start")


def slide_title(page):
    for j in range(page.Count):
        s = page.getByIndex(j)
        if s.ShapeType.endswith(("TitleTextShape", "SubtitleShape")) and s.String.strip():
            return s.String.strip().replace("\n", " ")
    return "(untitled)"


def check(doc):
    errors, warnings = [], []
    pages = doc.DrawPages
    for i in range(pages.Count):
        page = pages.getByIndex(i)
        bottom_edge = page.Height
        where = f"slide {i + 1} \"{slide_title(page)}\""
        for j in range(page.Count):
            s = page.getByIndex(j)
            kind = s.ShapeType.split(".")[-1]
            if kind in ("TableShape", "GraphicObjectShape"):
                if s.Position.Y + s.Size.Height > bottom_edge + TOLERANCE:
                    what = "table" if kind == "TableShape" else "image"
                    errors.append(f"{where}: {what} runs off the bottom of the slide")
                continue
            if not hasattr(s, "String") or not s.String.strip():
                continue
            box = s.Size.Height
            s.TextMinimumFrameHeight = 0
            s.TextAutoGrowHeight = True
            needed = s.Size.Height
            if s.Position.Y + needed > bottom_edge + TOLERANCE:
                errors.append(f"{where}: text runs off the bottom of the slide "
                              f"(\"{s.String.strip()[:40]}...\")")
            elif needed > box + TOLERANCE:
                warnings.append(f"{where}: text is taller than its box by {(needed - box) / 100:.0f} mm")
    return errors, warnings


def export_pngs(desktop, deck, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for old in glob.glob(os.path.join(out_dir, "slide-*.png")):
        os.remove(old)
    pdf = os.path.join(out_dir, "deck.pdf")
    doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(deck), "_blank", 0, (prop("Hidden", True),))
    doc.storeToURL(uno.systemPathToFileUrl(pdf), (prop("FilterName", "impress_pdf_Export"),))
    doc.close(True)
    # pdftocairo, not pdftoppm: pdftoppm draws faint bands across images that look like layout bugs.
    subprocess.run(["pdftocairo", "-png", "-r", str(PNG_DPI), pdf, os.path.join(out_dir, "slide")], check=True)
    os.remove(pdf)
    # pdftocairo pads to the page count's width (slide-1 or slide-01); always use two digits.
    for png in glob.glob(os.path.join(out_dir, "slide-*.png")):
        n = int(os.path.basename(png)[len("slide-"):-len(".png")])
        os.rename(png, os.path.join(out_dir, f"slide-{n:02d}.png"))
    print(f"PNGs: {out_dir}/slide-*.png")


def main(argv):
    if len(argv) not in (1, 3) or (len(argv) == 3 and argv[1] != "--png"):
        sys.exit("usage: check.py DECK.pptx [--png OUT_DIR]")
    deck = os.path.abspath(argv[0])
    profile = tempfile.mkdtemp(prefix="slides-check-")
    proc, desktop = start_office(profile, f"slides_check_{os.getpid()}")
    try:
        if len(argv) == 3:
            export_pngs(desktop, deck, os.path.abspath(argv[2]))
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(deck), "_blank", 0, (prop("Hidden", True),))
        errors, warnings = check(doc)
        doc.close(True)
    finally:
        try:
            desktop.terminate()
        except Exception:
            pass
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(profile, ignore_errors=True)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    if not errors and not warnings:
        print("no overflow")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
