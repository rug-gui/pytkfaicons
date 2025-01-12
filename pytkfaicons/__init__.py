import os
import json

ICONS = "icons"
FONTS = "fonts"

S_BRANDS = "brands"
S_REGULAR = "regular"
S_SOLID = "solid"

FORMAT = "png"
HEIGHT = 32

VERSION = "v0.0.4-a"

_icons = None

_thisdir = os.path.dirname(os.path.abspath(__file__))


def get_icons():
    global icons
    if _icons is None:
        read_icons()
        assert _icons
    return _icons


def read_icons():
    icons_src = os.path.join(_thisdir, ICONS, "icons.json")
    with open(icons_src) as f:
        global _icons
        _icons = json.loads(f.read())


def get_meta(name):
    icons = get_icons()
    ic = icons.get(name, None)
    if ic is None:
        raise Exception("not found", name)
    return ic
