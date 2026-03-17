"""SVG Bridge — Extract overlay TikZ elements via SVG intermediary.

Uses page.get_svg_image() which captures ALL rendered content including
tikzmark overlays that page.get_drawings() misses.
"""

from .svg_extract import extract_svg_elements
from .svg_to_tikz import convert_svg_element


def svg_extract_paths(page, scale, precision, use_named_colors,
                      page_height, offset_x, offset_y):
    """Extract all SVG graphic elements and convert to TikZ commands.

    This is the single entry point for the SVG bridge. It:
    1. Gets the page's full SVG representation (includes overlays)
    2. Parses all graphic elements with their transforms and styles
    3. Converts each to TikZ syntax

    Returns a list of TikZ command strings.
    """
    elements, vb_w, vb_h = extract_svg_elements(page)

    lines = []
    lines.append('% --- SVG bridge extraction (includes overlays) ---')

    for elem in elements:
        tikz = convert_svg_element(
            elem, scale, precision, use_named_colors,
            page_height, offset_x, offset_y
        )
        lines.extend(tikz)

    return lines
