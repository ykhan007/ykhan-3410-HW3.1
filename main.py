# main.py — Lesson 3.1 solution
# - Sort/search in YIQ (Y only)
# - Iterative MERGE SORT replaces selection sort
# - Preview, then while-loop:
#   Q: save full-size and quit
#   R: reverse slice side (toggle)
#   T: tweak tolerance by moving 'subi' without re-search
#   C: new RGB target → re-search
#
# Python 3 only

from PixelFunctions import (
    store_pixels_yiq_and_rgb, to_grayscale, yiq_subset_to_overlay, show_preview
)
from SortFunctions import merge_sort_iterative
from SearchFunctions import lower_bound
from PIL import Image
import colorsys

IMG_PATH = "input.jpg"    # put a small JPEG here

def choose_slice(yiq_sorted, subi, take_upper: bool):
    """Return the slice of pixels to highlight based on toggle."""
    if take_upper:
        return yiq_sorted[subi:]          # take subi..end
    else:
        return yiq_sorted[:subi]          # take start..subi-1

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def main():
    # 1) load & precompute
    original = Image.open(IMG_PATH).convert("RGB")
    yiq_pixels, rgb_pixels = store_pixels_yiq_and_rgb(original)

    # 2) sort by Y (tuples compare by first element, which starts with Y)
    merge_sort_iterative(yiq_pixels)

    # 3) base = grayscale original
    base = to_grayscale(original)

    # 4) pick a starting target color (a warm yellow works well as a demo)
    start_rgb = (240, 210, 30)
    y_start = colorsys.rgb_to_yiq(*(c/255.0 for c in start_rgb))[0]

    # lower_bound to get 'subi' (first index with Y >= target)
    y_values = [p[0][0] for p in yiq_pixels]
    subi = lower_bound(y_values, y_start)

    # default slice side: for many “yellow-ish” cases, upper slice shows it
    take_upper = True

    # build first overlay + preview
    selected = choose_slice(yiq_pixels, subi, take_upper)
    preview = yiq_subset_to_overlay(base, selected)
    show_preview(preview)

    # 5) command loop
    n = len(yiq_pixels)
    print("Commands: [Q] Save & Quit  [R] Reverse slice  [T] Tolerance  [C] Change target color")
    while True:
        cmd = input("> ").strip().upper() or ""
        if cmd == "Q":
            # save at original size
            out = yiq_subset_to_overlay(base, choose_slice(yiq_pixels, subi, take_upper))
            out.save("output.jpg")
            print("Saved output.jpg — bye!")
            break

        elif cmd == "R":
            take_upper = not take_upper
            print(f"Slice reversed. take_upper={take_upper}")
            out = yiq_subset_to_overlay(base, choose_slice(yiq_pixels, subi, take_upper))
            show_preview(out)

        elif cmd == "T":
            # move subi by a percent of the whole list (no new search)
            step_str = input("Tolerance step percent (e.g., +5 or -5): ").strip()
            try:
                pct = int(step_str)
            except ValueError:
                pct = 5
            delta = max(1, (abs(pct) * n) // 100)
            if pct < 0:
                subi = clamp(subi - delta, 0, n)
            else:
                subi = clamp(subi + delta, 0, n)
            print(f"Tolerance moved. subi={subi}")
            out = yiq_subset_to_overlay(base, choose_slice(yiq_pixels, subi, take_upper))
            show_preview(out)

        elif cmd == "C":
            # new target color → recalc subi (but keep same sorted list)
            try:
                r = int(input("R (0-255): ").strip())
                g = int(input("G (0-255): ").strip())
                b = int(input("B (0-255): ").strip())
                r = clamp(r, 0, 255); g = clamp(g, 0, 255); b = clamp(b, 0, 255)
            except ValueError:
                print("Invalid color; keeping previous.")
                r, g, b = start_rgb
            start_rgb = (r, g, b)
            y_target = colorsys.rgb_to_yiq(r/255.0, g/255.0, b/255.0)[0]
            subi = lower_bound(y_values, y_target)
            print(f"New target set. subi={subi}")
            out = yiq_subset_to_overlay(base, choose_slice(yiq_pixels, subi, take_upper))
            show_preview(out)

        else:
            print("Use Q, R, T, or C.")
            
if __name__ == "__main__":
    main()
