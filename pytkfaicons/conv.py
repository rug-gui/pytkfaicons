import os
import shutil
import json
import tempfile
import glob
from multiprocessing import Pool

import tkinter as tk

from wand.image import Image
from wand.color import Color

from . import (
    _thisdir,
    get_meta,
    get_icons,
    ICONS,
    FONTS,
    S_BRANDS,
    S_REGULAR,
    S_SOLID,
    FORMAT,
    HEIGHT,
)


height = HEIGHT

download_temp = os.path.abspath("downloads")
os.makedirs(download_temp, exist_ok=True)

curd = os.path.abspath(os.getcwd())

repo_url = "https://github.com/FortAwesome/Font-Awesome"


def mk_temp_pygg(reftag):

    pygg = """
        [fontawesome_github]
        url="%s"

        tag = %s

        #brands= "svgs/brands/*.svg", "brands"
        #regular= "svgs/regular/*.svg", "regular"
        #solid= "svgs/solid/*.svg", "solid"

        meta = "metadata/icons.json", "meta/icons.json"
        #otf_fonts = "otfs/*.otf", "fonts/"
        ttf_fonts = "webfonts/*.ttf", "fonts/"
    """ % (
        repo_url,
        reftag,
    )
    fpygg = os.path.join(download_temp, "fa.pygg")
    with open(fpygg, "w") as f:
        f.write(pygg)
    return fpygg


def get_repo(reftag=None, opts=None, callb=None):
    if reftag is None:
        reftag = "master"
    if opts is None:
        opts = ""
    lines = []

    fpygg = mk_temp_pygg(reftag)

    try:
        os.chdir(download_temp)
        f = os.popen(f"pygitgrab {opts} -f {fpygg} ")
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            line = line.strip()
            lines.append(line)
            if callb:
                callb(line)
        f.close()
        return lines
    finally:
        os.chdir(curd)


def img_i():

    icons_src = os.path.join(download_temp, "meta", "icons.json")
    with open(icons_src) as f:
        icons = json.loads(f.read())

    for key, val in icons.items():
        for style in val["styles"]:
            yield style, key, val["svg"][style]["raw"]


def convert(svg, dest=None, output=None):
    if output is None:
        output = FORMAT

    svgimg = get_svg_image(svg)

    img = get_svg_trans_resize(svgimg, height)
    img.convert(output)

    if dest:
        img.save(filename=dest)

    return img


def convert_task(args):
    fld, f, svg = args
    fsvg = os.path.join(download_temp, fld, f)
    fpng = os.path.join(_thisdir, ICONS, fld, f + "." + FORMAT)
    os.makedirs(os.path.dirname(fpng), exist_ok=True)
    convert(svg, fpng)
    print(fpng)
    return fpng


def convert_all():
    cnt = 0
    with Pool() as p:
        files = p.map(convert_task, img_i())
        cnt += len(files)
        print("---", cnt)


def copy_meta():
    icons_src = os.path.join(download_temp, "meta", "icons.json")
    with open(icons_src) as f:
        icons = json.loads(f.read())
    for key, val in icons.items():

        for st in val["styles"]:
            val["svg_" + st] = val["svg"][st]["raw"]

        for tag in [
            "svg",
            "label",
            "voted",
            "changes",
            "ligatures",
        ]:
            try:
                del val[tag]
            except:
                pass
    icons_dest = os.path.join(_thisdir, ICONS, os.path.basename(icons_src))
    with open(icons_dest, "w") as f:
        f.write(json.dumps(icons, indent=4))


def copy_fonts():
    fonts_src = os.path.join(download_temp, FONTS, "*")
    fonts_dest = os.path.join(_thisdir, FONTS)
    os.makedirs(fonts_dest, exist_ok=True)
    for f in glob.iglob(fonts_src):
        destf = os.path.join(fonts_dest, os.path.basename(f))
        print("copy from", f, "to", destf)
        shutil.copy2(f, destf)


def build(reftag=None, opts=None, callb=None):
    get_repo(reftag, opts=opts, callb=callb)
    convert_all()
    copy_meta()
    copy_fonts()


# svg direct support


def get_svg(name, style):
    icons = get_icons()
    if not name in icons:
        raise Exception("not found", name)
    if not "svg_" + style in icons[name]:
        raise Exception("not found", name, style)
    svg = icons[name]["svg_" + style]
    return svg


def get_svg_image(svg):
    img = Image(blob=svg.encode())
    return img


# wand image modifiers


def mod_invert_img(img):
    img.negate()


def mod_transparent_img(img):
    img.transparent_color(Color("white"), 0.0)


def mod_resized_img(img, height):
    if height:
        img.transform(resize=f"x{height}")


def mod_color(img, color):
    """changes black to new color"""
    if color:
        if type(color) == str:
            color = Color(color)
        img.opaque_paint(target=Color("black"), fill=color)


# pre-defined helper


def get_svg_trans_resize(svgimg, height):
    img = svgimg.clone()
    mod_transparent_img(img)
    mod_resized_img(img, height)
    return img


def get_tk_image(svgimg, format="png"):
    """convert image"""
    img = tk.PhotoImage(data=svgimg.make_blob(format))
    return img


def get_scaled_icon(name, style, height=32):
    svg = get_svg(name, style)
    svgimg = get_svg_image(svg)
    tr_svg = get_svg_trans_resize(svgimg, height)
    return tr_svg


def get_scaled_tk_icon(name, style, height=32, format="png"):
    tr_svg = get_scaled_icon(name, style, height)
    tk_img = get_tk_image(tr_svg, format=format)
    return tk_img


def get_colored_scaled_tk_icon(
    name, style, height=32, color=None, invert=False, format="png"
):
    svg = get_svg(name, style)
    img = get_svg_image(svg)
    if invert:
        mod_invert_img(img)
    mod_color(img, color)
    mod_transparent_img(img)
    mod_resized_img(img, height)
    img_tk = get_tk_image(img, format=format)
    return img_tk

class faicon:
    from PIL import ImageOps, ImageTk
    from PIL.Image import Image
    from icons import get_icon_image, tk_image_loader, get_tk_icon

    global NAMED_COLORS
    NAMED_COLORS = {
    "white":   (0xFF, 0xFF, 0xFF),
    "silver":  (0xC0, 0xC0, 0xC0),
    "gray":    (0x80, 0x80, 0x80),
    "black":   (0x00, 0x00, 0x00),
    "red":     (0xFF, 0x00, 0x00),
    "maroon":  (0x80, 0x00, 0x00),
    "yellow":  (0xFF, 0xFF, 0x00),
    "olive":   (0x80, 0x80, 0x00),
    "lime":    (0x00, 0xFF, 0x00),
    "green":   (0x00, 0x80, 0x00),
    "aqua":    (0x00, 0xFF, 0xFF),
    "teal":    (0x00, 0x80, 0x80),
    "blue":    (0x00, 0x00, 0xFF),
    "navy":    (0x00, 0x00, 0x80),
    "fuchsia": (0xFF, 0x00, 0xFF),
    "purple":  (0x80, 0x00, 0x80)
}

    def icon(name, style):
        # pre-calculated 32px height icons (fast)
        return get_icon_image(name, style, loader=tk_image_loader)
    def inverticon(name, style):
        from PIL import Image,ImageTk,ImageOps
        image = get_icon_image(name, style, loader=Image.open)
        if image.mode == 'RGBA':
            r,g,b,a = image.split()
            rgb_image = Image.merge('RGB', (r,g,b))

            inverted_image = ImageOps.invert(rgb_image)

            r2,g2,b2 = inverted_image.split()

            final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            return ImageTk.PhotoImage(final_transparent_image)
        else:
            inverted_image = ImageOps.invert(image)
            return ImageTk.PhotoImage(inverted_image)

    def coloricon(name, style,color_name):
        from PIL import Image,ImageTk
        import numpy as np
        rgb=color_string_to_rgb(color_name)
        image = get_icon_image(name, style, loader=Image.open)
        im =image
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        # Replace black with rgb... (leaves alpha values alone...)
        white_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][white_areas.T] = rgb
        im2 = Image.fromarray(data)
        return ImageTk.PhotoImage(im2)
    global color_string_to_rgb
    def color_string_to_rgb(color_string):
        # Named color
        if color_string in NAMED_COLORS:
            return NAMED_COLORS[color_string]
        # #f00 or #ff0000 -> f00 or ff0000
        if color_string.startswith("#"):
            color_string = color_string[1:]
        # f00 -> ff0000
        if len(color_string) == 3:
            color_string = color_string[0] * 2 + color_string[1] * 2 + color_string[2] * 2  # noqa
        # ff0000 -> (255, 0, 0)
        return (
            int(color_string[0:2], 16),
            int(color_string[2:4], 16),
            int(color_string[4:], 16)
            ) 

    def colorico(name, style,cname):
        from PIL import Image,ImageTk
        img = get_icon_image(name, style, loader=Image.open)
        pixdata = img.load()
        # Clean the background noise, if color != white, then set to cname.
        rgb=color_string_to_rgb(cname)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y] == (0, 0, 0, 255):
                    pixdata[x, y] = rgb  #rgb to rgba
        im = img
        return ImageTk.PhotoImage(im)

    def color(icon,color):
        from PIL import Image,ImageTk
        k=ImageTk.PhotoImage(icon)
        img=ImageTk.getimage(k)
        pixdata = img.load()
        # Clean the background noise, if color != white, then set to cname.
        rgb=color_string_to_rgb(color)
        print(rgb)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y] == (0, 0, 0, 255):
                    r,g,b = rgb
                    pixdata[x, y] = (r,g,b,255)#rgb to rgba
        im=img
        return ImageTk.PhotoImage(img)
