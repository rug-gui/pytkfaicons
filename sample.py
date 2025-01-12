import tkinter as tk
from PIL import Image, ImageTk, ImageDraw


if False:
    # set to True to build all icons

    from pytkfaicons.conv import build, get_repo, convert_all, copy_meta, copy_fonts

    # build(opts="-c", callb=print) # use custom credit file
    # build(callb=print)  # use global .pygg_credits file

    # convert_all()
    # copy_meta()
    # copy_fonts()


from pytkfaicons.conv import get_meta, get_scaled_tk_icon, get_colored_scaled_tk_icon
from pytkfaicons.icons import get_icon, get_icon_image, tk_image_loader, get_tk_icon

from pytkfaicons.fonts import get_font, get_font_icon


root = tk.Tk()

frame_t = tk.Frame(root)

tk.Label(frame_t, text="svg based - different size and color support").pack(
    side="left", pady=20
)

frame_t.pack()


frame1 = tk.Frame(root)
tk.Label(frame1, text="on the fly resized (slow)").pack(side="left")

# resize on the fly (slow)
img0 = get_colored_scaled_tk_icon("arrow-left", "solid", 64, "green")
tk.Button(frame1, justify=tk.LEFT, padx=10, image=img0).pack(side="left")

img1 = get_colored_scaled_tk_icon("arrow-right", "solid", 48, "green", invert=True)
tk.Button(frame1, justify=tk.LEFT, padx=10, image=img1).pack(side="left")

img2 = get_colored_scaled_tk_icon("asterisk", "solid", 32, "blue", invert=True)
tk.Button(frame1, justify=tk.LEFT, padx=10, image=img2).pack(side="left")

img3 = get_colored_scaled_tk_icon("barcode", "solid", 24, "blue")
tk.Button(frame1, justify=tk.LEFT, padx=10, image=img3).pack(side="left")

img4 = get_scaled_tk_icon("baby", "solid", 12)
tk.Button(frame1, justify=tk.LEFT, padx=10, image=img4).pack(side="left")

img5 = get_scaled_tk_icon("bahai", "solid", 8)
tk.Button(frame1, justify=tk.LEFT, padx=10, image=img5).pack(side="left")

img6 = get_scaled_tk_icon("bars", "solid", 6)
tk.Button(frame1, justify=tk.LEFT, padx=10, image=img6).pack(side="left")

frame1.pack()

# this is the same implementation as get_tk_icon()
# using get_icon_image(), and tk_image_loader() as loader
# what returns tk.PhotoImage


def icon(name, style):
    # pre-calculated 32px height icons (fast)
    return get_icon_image(name, style, loader=tk_image_loader)


frame2 = tk.Frame(root)

left = icon("arrow-left", "solid")
right = icon("arrow-right", "solid")
asterisk = icon("asterisk", "solid")
barcode = icon("barcode", "solid")
baby = icon("baby", "solid")
bahai = icon("bahai", "solid")
bars = icon("bars", "solid")

tk.Label(frame2, text="pre-caclulated (fast)").pack(side="left")

tk.Button(frame2, justify=tk.LEFT, padx=10, image=left).pack(side="left")
tk.Button(frame2, justify=tk.LEFT, padx=10, image=right).pack(side="left")
tk.Button(frame2, justify=tk.LEFT, padx=10, image=asterisk).pack(side="left")
tk.Button(frame2, justify=tk.LEFT, padx=10, image=barcode).pack(side="left")
tk.Button(frame2, justify=tk.LEFT, padx=10, image=baby).pack(side="left")
tk.Button(frame2, justify=tk.LEFT, padx=10, image=bahai).pack(side="left")
tk.Button(frame2, justify=tk.LEFT, padx=10, image=bars).pack(side="left")

frame2.pack()

# info text

frame_m = tk.Frame(root)

tk.Label(frame_m, text="font based - different size and color support").pack(
    side="left", pady=20
)

frame_m.pack()

#

# use fonts

f_brands = get_font("brands", 44)
print(f_brands.getname())
f_solid = get_font("solid", 44)
print(f_solid.getname())
f_regular = get_font("regular", 44)
print(f_regular.getname())

# custom image - thats how get_font_icon() is implemented

meta_ic = get_meta("asterisk")

unicode_ic = meta_ic["unicode"]  # this is a hex string
style_ic = meta_ic["styles"]  # list of supported fonts

print("icon-data", unicode_ic, style_ic)
print("icon-meta", meta_ic)

# convert hex string to unicode
unicode_text = chr(int(unicode_ic, 16))

# load the first supported font
font_ic = get_font(style_ic[0], 44)

# background color == green
imag = Image.new(mode="RGB", size=(66, 66), color="black")
draw = ImageDraw.Draw(im=imag)

# draw text with color == white
draw.text(xy=(33, 33), text=unicode_text, font=font_ic, fill="white", anchor="mm")

im = ImageTk.PhotoImage(imag)

# end-of custom image


frame3 = tk.Frame(root)

tk.Label(frame3, text="font based").pack(side="left")

# use the custom image
tk.Button(frame3, justify=tk.LEFT, padx=10, image=im).pack(side="left")

im_python = get_font_icon("python", height=100, bg="green", fg="white")
tk.Button(frame3, justify=tk.LEFT, padx=10, image=im_python).pack(side="left")

im_baby = get_font_icon("baby", height=44, bg="blue", fg="white")
tk.Button(frame3, justify=tk.LEFT, padx=10, image=im_baby).pack(side="left")

im_bahai = get_font_icon("bahai", height=44, image_size=(100, 70), bg="red", fg="white")
tk.Button(frame3, justify=tk.LEFT, padx=10, image=im_bahai).pack(side="left")

frame3.pack()


frame4 = tk.Frame(root)

tk.Label(frame4, text="font styles").pack(side="left")

im_quest = get_font_icon(
    "question-circle",
    style="regular",
    height=22,
    image_size=(50, 50),
    bg="black",
    fg="white",
)
tk.Button(frame4, justify=tk.LEFT, padx=10, image=im_quest).pack(side="left")

im_quest2 = get_font_icon(
    "question-circle",
    style="solid",
    height=22,
    image_size=(50, 50),
    bg="black",
    fg="white",
)
tk.Button(frame4, justify=tk.LEFT, padx=10, image=im_quest2).pack(side="left")

im_quest3 = get_font_icon(
    "question-circle",
    style="regular",
    height=22,
    image_size=(50, 50),
)
tk.Button(frame4, justify=tk.LEFT, padx=10, image=im_quest3).pack(side="left")

im_quest4 = get_font_icon(
    "question-circle",
    style="solid",
    height=22,
    image_size=(50, 50),
)
tk.Button(frame4, justify=tk.LEFT, padx=10, image=im_quest4).pack(side="left")

frame4.pack()

frame5 = tk.Frame(root)

tk.Label(frame5, text="coding icons").pack(side="left", pady=20)

frame5.pack()

frame6 = tk.Frame(root)

im_code = get_font_icon(
    "code",
    height=22,
    image_size=(33, 33),
)
tk.Button(frame6, justify=tk.LEFT, padx=10, image=im_code).pack(side="left")

im_code2 = get_font_icon(
    "bug",
    height=22,
    image_size=(33, 33),
)
tk.Button(frame6, justify=tk.LEFT, padx=10, image=im_code2).pack(side="left")

im_code_branch = get_font_icon(
    "code-branch",
    height=22,
    image_size=(33, 33),
)
tk.Button(frame6, justify=tk.LEFT, padx=10, image=im_code_branch).pack(side="left")

im_code_cmp = get_font_icon(
    "cube",
    height=22,
    image_size=(33, 33),
)
tk.Button(frame6, justify=tk.LEFT, padx=10, image=im_code_cmp).pack(side="left")

frame6.pack()


# run tkinter mainloop
root.mainloop()
