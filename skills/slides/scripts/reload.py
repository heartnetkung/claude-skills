#!/usr/bin/env python3
"""Open a deck in LibreOffice Impress, or reload it if it is already open.

    /usr/bin/python3 reload.py path/to/deck.pptx

LibreOffice is started with a local pipe so this script can control it later.
One LibreOffice serves every deck; other open documents are left alone.
"""
import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException

PIPE = "claude_slide"
CONNECT = f"uno:pipe,name={PIPE};urp;StarOffice.ComponentContext"


def connect():
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local)
    ctx = resolver.resolve(CONNECT)
    return ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)


def main(deck):
    deck_url = uno.systemPathToFileUrl(deck)
    try:
        desktop = connect()
    except NoConnectException:
        subprocess.Popen(
            ["soffice", f"--accept=pipe,name={PIPE};urp;", "--impress", deck],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        print("Started LibreOffice with the deck.")
        return

    for doc in desktop.getComponents():
        if getattr(doc, "URL", None) == deck_url:
            doc.close(True)
            time.sleep(0.5)
            break

    hidden = PropertyValue()
    hidden.Name = "Hidden"
    hidden.Value = False
    desktop.loadComponentFromURL(deck_url, "_blank", 0, (hidden,))
    print("Reloaded the deck.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: reload.py DECK.pptx")
    main(os.path.abspath(sys.argv[1]))
