# ykhan-3410-HW3.1
**Lesson 3.1 – Pixel Manipulation 2 (Preview + Commands + Merge Sort)**

This project highlights pixels in an image based on a target color (in YIQ space), shows a preview,
and lets the user interactively adjust the result with keyboard commands. Selection sort from earlier
lessons is replaced by an **iterative merge sort**.

## Features
- **Preview then loop:** Shows a preview first, then enters a prompt loop.
- **Commands:**
  - `Q` – Save full-size result (`output.jpg`) and quit.
  - `R` – Reverse which side of the boundary index (`subi`) is selected.
  - `T` – Change “tolerance” by moving `subi` without running a new search (enter `+5` or `-10` percent).
  - `C` – Enter a new **R, G, B** color as the target; recompute boundary and update preview.
- **Sorting:** Uses **iterative merge sort** (bottom-up) on the pixel list (sorted by **Y** in YIQ).
- **Clean modules:** Pixel helpers in `PixelFunctions.py`, sort in `SortFunctions.py`, search helpers in `SearchFunctions.py`.  
  `main.py` only defines `main()` and orchestrates the flow.
