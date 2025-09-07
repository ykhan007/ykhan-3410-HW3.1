from typing import List, Tuple
from PIL import Image
import colorsys

# types
RGB = Tuple[int, int, int]
XY  = Tuple[int, int]
YIQ = Tuple[float, float, float]        # (y, i, q) floats in [0,1] / [-, +] range from colorsys
YIQPix = Tuple[YIQ, XY]                 # ((y,i,q), (x,y))
RGBPix = Tuple[RGB, XY]                 # ((r,g,b), (x,y))

def store_pixels_yiq_and_rgb(img: Image.Image) -> Tuple[List[YIQPix], List[RGBPix]]:
    """Walk image once; build parallel lists of YIQ-pixels and RGB-pixels."""
    img = img.convert("RGB")
    w, h = img.size
    src = img.load()

    yiq_list: List[YIQPix] = []
    rgb_list: List[RGBPix] = []

    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
            yv, iv, qv = colorsys.rgb_to_yiq(rf, gf, bf)
            yiq_list.append(((yv, iv, qv), (x, y)))
            rgb_list.append(((r, g, b), (x, y)))

    return yiq_list, rgb_list

def to_grayscale(img: Image.Image) -> Image.Image:
    """Average grayscale (integer) as used in class."""
    w, h = img.size
    gray = Image.new("RGB", (w, h))
    src, dst = img.load(), gray.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            m = (r + g + b) // 3
            dst[x, y] = (m, m, m)
    return gray

def yiq_subset_to_overlay(base_img: Image.Image, yiq_subset: List[YIQPix]) -> Image.Image:
    """Overlay only the given YIQ pixels (converted to RGB) onto base image."""
    out = base_img.copy()
    put = out.load()
    for (yval, ival, qval), (x, y) in yiq_subset:
        r, g, b = colorsys.yiq_to_rgb(yval, ival, qval)
        # convert floats back to 0..255 ints
        rgb = tuple(max(0, min(255, int(round(v * 255.0)))) for v in (r, g, b))
        put[x, y] = rgb
    return out

def show_preview(img: Image.Image) -> None:
    """Open a preview window (blocking depends on OS)."""
    img.show()
