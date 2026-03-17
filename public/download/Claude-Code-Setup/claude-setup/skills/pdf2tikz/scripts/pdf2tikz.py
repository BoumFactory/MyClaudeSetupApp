#!/usr/bin/env python3
"""pdf2tikz — Convert PDF vector graphics to TikZ code via PyMuPDF."""

import argparse
import math
import sys
from pathlib import Path

import fitz  # PyMuPDF


# --- Color mapping ---

NAMED_COLORS = {
    (0, 0, 0): "black",
    (1, 1, 1): "white",
    (1, 0, 0): "red",
    (0, 1, 0): "green",
    (0, 0, 1): "blue",
    (1, 1, 0): "yellow",
    (1, 0, 1): "magenta",
    (0, 1, 1): "cyan",
    (0.5, 0.5, 0.5): "gray",
    (0.75, 0.75, 0.75): "lightgray",
    (0.25, 0.25, 0.25): "darkgray",
    (1, 0.5, 0): "orange",
    (0.5, 0, 0.5): "violet",
    (0.65, 0.16, 0.16): "brown",
}

COLOR_TOLERANCE = 0.08


def match_named_color(rgb):
    """Try to match an RGB tuple to a named TikZ color."""
    if rgb is None:
        return None
    for ref, name in NAMED_COLORS.items():
        if all(abs(a - b) < COLOR_TOLERANCE for a, b in zip(rgb, ref)):
            return name
    return None


def format_color(rgb, use_named=True):
    """Format RGB tuple as TikZ color specification."""
    if rgb is None:
        return None
    if use_named:
        named = match_named_color(rgb)
        if named:
            return named
    r, g, b = [int(c * 255) for c in rgb]
    return f"{{rgb,255:red,{r};green,{g};blue,{b}}}"


# --- Coordinate transforms ---

def pt_to_cm(pt):
    """Convert PDF points to centimeters."""
    return pt / 72.0 * 2.54


def fmt(val, precision=2):
    """Format a float, snapping to clean values and stripping trailing zeros.

    Snaps to nearest 0.25 if within tolerance, so 3.99 → 4, 1.51 → 1.5, etc.
    This produces much cleaner TikZ code that matches typical hand-written coords.
    """
    # Snap to nearest 0.25 increment if very close
    snap = 0.25
    tolerance = 0.04
    snapped = round(val / snap) * snap
    if abs(val - snapped) < tolerance:
        val = snapped

    s = f"{val:.{precision}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


# --- Coordinate transform helper ---

def transform_pt(px, py, page_height, scale, precision, offset_x=0.0, offset_y=0.0):
    """Transform a PDF point to TikZ coordinates, recentered at (0,0).

    PDF origin = top-left, Y down. TikZ origin = bottom-left, Y up.
    offset_x = min X of all content in PDF points (subtracted from X).
    offset_y = max Y of all content in PDF points (the bottom of content).
    After flip: tikz_y = (page_height - py) - (page_height - offset_y)
                       = offset_y - py
    """
    tx = pt_to_cm(px - offset_x) * scale
    ty = pt_to_cm(offset_y - py) * scale
    return fmt(tx, precision), fmt(ty, precision)


# --- Circle detection ---

def is_circle(items):
    """Detect if a sequence of 4 cubic Bezier curves forms a circle.

    Returns (cx, cy, r) in PDF points if detected, else None.
    """
    curves = [it for it in items if it[0] == "c"]
    if len(curves) != 4:
        return None

    # Collect all endpoints
    endpoints = []
    for _, p1, p2, p3, p4 in curves:
        endpoints.append(fitz.Point(p4))

    if len(endpoints) < 4:
        return None

    # Estimate center as average of endpoints
    cx = sum(p.x for p in endpoints) / len(endpoints)
    cy = sum(p.y for p in endpoints) / len(endpoints)

    # Check all endpoints are equidistant from center
    radii = [math.sqrt((p.x - cx) ** 2 + (p.y - cy) ** 2) for p in endpoints]
    if not radii:
        return None

    avg_r = sum(radii) / len(radii)
    if avg_r < 0.5:  # too small
        return None

    # All radii should be within 5% of average
    if any(abs(r - avg_r) / avg_r > 0.05 for r in radii):
        return None

    return (cx, cy, avg_r)


# --- Path conversion ---

def convert_path(path, scale, precision, use_named_colors, page_height,
                 offset_x=0.0, offset_y=0.0):
    """Convert a single PyMuPDF drawing path to TikZ commands."""
    items = path["items"]
    if not items:
        return []

    stroke_color = path.get("color")
    fill_color = path.get("fill")
    width = path.get("width", 0)
    dashes = path.get("dashes", "")
    path_type = path.get("type", "s")  # s=stroke, f=fill, fs=both
    closepath = path.get("closePath", False)

    # Build TikZ options
    options = []

    # Color
    if "s" in path_type and stroke_color:
        color_str = format_color(stroke_color, use_named_colors)
        if color_str and color_str != "black":
            options.append(f"draw={color_str}")
        elif "f" in path_type:
            options.append("draw")

    if "f" in path_type and fill_color:
        color_str = format_color(fill_color, use_named_colors)
        if color_str:
            options.append(f"fill={color_str}")

    # Line width (default is ~1pt in PDF)
    if width and abs(width - 1.0) > 0.1:
        options.append(f"line width={fmt(width, 1)}pt")

    # Dashes — '[] 0' means solid line, only real patterns like '[ 2.98 2.98 ] 0'
    if dashes and isinstance(dashes, str):
        # Extract the array part between [ and ]
        import re
        dash_match = re.search(r'\[([^\]]*)\]', dashes)
        if dash_match and dash_match.group(1).strip():
            options.append("dashed")

    opts_str = f"[{', '.join(options)}]" if options else ""

    # Helper to transform a point using the shared function
    def tp(px, py):
        return transform_pt(px, py, page_height, scale, precision,
                            offset_x, offset_y)

    # Check for circle
    circle = is_circle(items)
    if circle:
        cx, cy, r = circle
        x, y = tp(cx, cy)
        radius = fmt(pt_to_cm(r) * scale, precision)

        cmd = "\\filldraw" if "f" in path_type and "s" in path_type else (
            "\\fill" if path_type == "f" else "\\draw"
        )
        return [f"{cmd}{opts_str} ({x},{y}) circle ({radius});"]

    # General path conversion
    tikz_parts = []
    current_pos = None
    first_pos = None

    for item in items:
        item_type = item[0]

        if item_type == "l":  # line
            p1, p2 = fitz.Point(item[1]), fitz.Point(item[2])
            x1, y1 = tp(p1.x, p1.y)
            x2, y2 = tp(p2.x, p2.y)

            if current_pos and current_pos == (x1, y1):
                tikz_parts.append(f"-- ({x2},{y2})")
            else:
                if tikz_parts:
                    tikz_parts.append(";")
                tikz_parts.append(f"({x1},{y1}) -- ({x2},{y2})")

            current_pos = (x2, y2)
            if first_pos is None:
                first_pos = (x1, y1)

        elif item_type == "c":  # cubic Bezier
            p1 = fitz.Point(item[1])
            cp1 = fitz.Point(item[2])
            cp2 = fitz.Point(item[3])
            p2 = fitz.Point(item[4])

            x1, y1 = tp(p1.x, p1.y)
            cx1, cy1 = tp(cp1.x, cp1.y)
            cx2, cy2 = tp(cp2.x, cp2.y)
            x2, y2 = tp(p2.x, p2.y)

            if current_pos and current_pos == (x1, y1):
                tikz_parts.append(
                    f".. controls ({cx1},{cy1}) and ({cx2},{cy2}) .. ({x2},{y2})"
                )
            else:
                if tikz_parts:
                    tikz_parts.append(";")
                tikz_parts.append(
                    f"({x1},{y1}) .. controls ({cx1},{cy1}) and ({cx2},{cy2}) .. ({x2},{y2})"
                )

            current_pos = (x2, y2)
            if first_pos is None:
                first_pos = (x1, y1)

        elif item_type == "re":  # rectangle
            rect = fitz.Rect(item[1])
            x, y = tp(rect.x0, rect.y1)
            x2, y2 = tp(rect.x1, rect.y0)

            if tikz_parts:
                tikz_parts.append(";")
            tikz_parts.append(f"({x},{y}) rectangle ({x2},{y2})")
            current_pos = None
            first_pos = None

        elif item_type == "qu":  # quad (4 points)
            quad = item[1]
            points = [fitz.Point(quad.ul), fitz.Point(quad.ur),
                      fitz.Point(quad.lr), fitz.Point(quad.ll)]

            if tikz_parts:
                tikz_parts.append(";")

            coords = []
            for p in points:
                px, py = tp(p.x, p.y)
                coords.append(f"({px},{py})")

            tikz_parts.append(" -- ".join(coords) + " -- cycle")
            current_pos = None
            first_pos = None

    if not tikz_parts:
        return []

    # Close path if needed
    if closepath and first_pos and current_pos and current_pos != first_pos:
        tikz_parts.append("-- cycle")

    # Build final command
    cmd = "\\filldraw" if "f" in path_type and "s" in path_type else (
        "\\fill" if path_type == "f" else "\\draw"
    )

    line = f"{cmd}{opts_str} " + " ".join(tikz_parts) + ";"
    # Clean up double semicolons
    line = line.replace(";;", ";")

    return [line]


# --- Text extraction ---

def extract_text_nodes(page, scale, precision, page_height,
                       offset_x=0.0, offset_y=0.0, text_blocks=None):
    """Extract text blocks as TikZ node commands."""
    nodes = []
    blocks = text_blocks if text_blocks is not None else page.get_text("dict")["blocks"]

    for block in blocks:
        if block["type"] != 0:  # text block
            continue
        for line in block["lines"]:
            text = ""
            font_size = 10
            for span in line["spans"]:
                text += span["text"]
                font_size = span["size"]

            text = text.strip()
            if not text:
                continue

            # Position (use line origin), recentered with offsets
            origin = line["spans"][0]["origin"]
            x, y = transform_pt(origin[0], origin[1], page_height,
                                scale, precision, offset_x, offset_y)

            # Escape LaTeX special chars
            text = text.replace("\\", "\\textbackslash ")
            text = text.replace("&", "\\&")
            text = text.replace("%", "\\%")
            text = text.replace("$", "\\$")
            text = text.replace("#", "\\#")
            text = text.replace("_", "\\_")
            text = text.replace("{", "\\{")
            text = text.replace("}", "\\}")

            # Check if it looks like math
            if text.startswith("\\$") and text.endswith("\\$"):
                text = "$" + text[2:-2] + "$"

            nodes.append(f"\\node at ({x},{y}) {{{text}}};")

    return nodes


# --- Bounding box calculation ---

def compute_origin(drawings, text_blocks, page_height):
    """Compute the bounding box origin from DRAWINGS ONLY (not text).

    Text labels often overshoot the figure bounds, so using only geometric
    paths gives a cleaner (0,0) origin that matches the original TikZ intent.

    Returns (offset_x, offset_y) in PDF points.
    """
    all_x, all_y = [], []

    for d in drawings:
        for item in d["items"]:
            if item[0] == "l":
                all_x.extend([item[1].x, item[2].x])
                all_y.extend([item[1].y, item[2].y])
            elif item[0] == "c":
                all_x.extend([item[1].x, item[2].x, item[3].x, item[4].x])
                all_y.extend([item[1].y, item[2].y, item[3].y, item[4].y])
            elif item[0] == "re":
                r = fitz.Rect(item[1])
                all_x.extend([r.x0, r.x1])
                all_y.extend([r.y0, r.y1])
            elif item[0] == "qu":
                q = item[1]
                for p in [q.ul, q.ur, q.lr, q.ll]:
                    all_x.append(p.x)
                    all_y.append(p.y)

    if not all_x:
        # Fallback to text if no drawings
        for block in text_blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    ox, oy = span["origin"]
                    all_x.append(ox)
                    all_y.append(oy)

    if not all_x:
        return 0.0, 0.0

    # offset_x = leftmost X in PDF pts
    # offset_y = max Y in PDF pts (bottom of content in PDF space,
    #            which becomes Y=0 after flip)
    return min(all_x), max(all_y)


# --- Main conversion ---

def convert_page(doc, page_num, scale, precision, use_named_colors,
                 include_text, cluster, svg_bridge=False):
    """Convert a single page to TikZ code."""
    page = doc[page_num]
    page_height = page.rect.height

    drawings = page.get_drawings()
    text_blocks = page.get_text("dict")["blocks"] if include_text else []

    if not drawings and not text_blocks and not svg_bridge:
        return None

    # Compute origin offset to recenter at (0,0)
    offset_x, offset_y = compute_origin(drawings, text_blocks, page_height)

    lines = []

    if svg_bridge:
        # SVG bridge mode: extract via SVG (captures overlays)
        from svg_bridge import svg_extract_paths
        svg_lines = svg_extract_paths(
            page, scale, precision, use_named_colors,
            page_height, offset_x, offset_y
        )
        lines.extend(svg_lines)
    elif cluster and hasattr(page, 'cluster_drawings'):
        clusters = page.cluster_drawings()
        for i, cluster_paths in enumerate(clusters):
            if len(clusters) > 1:
                lines.append(f"% --- Cluster {i + 1} ---")
            for path in cluster_paths:
                tikz = convert_path(path, scale, precision,
                                    use_named_colors, page_height,
                                    offset_x, offset_y)
                lines.extend(tikz)
            if len(clusters) > 1:
                lines.append("")
    else:
        for path in drawings:
            tikz = convert_path(path, scale, precision,
                                use_named_colors, page_height,
                                offset_x, offset_y)
            lines.extend(tikz)

    if include_text:
        text_nodes = extract_text_nodes(page, scale, precision, page_height,
                                        offset_x, offset_y, text_blocks)
        if text_nodes:
            lines.append("% --- Text labels ---")
            lines.extend(text_nodes)

    return lines


def wrap_tikzpicture(lines, standalone=False):
    """Wrap TikZ commands in a tikzpicture environment."""
    result = []

    if standalone:
        result.append("\\documentclass[tikz,border=5pt]{standalone}")
        result.append("\\begin{document}")

    result.append("\\begin{tikzpicture}")
    for line in lines:
        if line:
            result.append(f"  {line}")
        else:
            result.append("")
    result.append("\\end{tikzpicture}")

    if standalone:
        result.append("\\end{document}")

    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF vector graphics to TikZ code"
    )
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("--page", type=int, default=1,
                        help="Page number to extract (default: 1)")
    parser.add_argument("--pages", type=str, default=None,
                        help="Comma-separated page numbers (e.g., 1,3,5)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output file (default: stdout)")
    parser.add_argument("--scale", type=float, default=1.0,
                        help="Scale factor (default: 1.0)")
    parser.add_argument("--precision", type=int, default=2,
                        help="Decimal precision for coordinates (default: 2)")
    parser.add_argument("--colors", choices=["named", "rgb"], default="named",
                        help="Color format (default: named)")
    parser.add_argument("--standalone", action="store_true",
                        help="Generate a complete standalone LaTeX document")
    parser.add_argument("--cluster", action="store_true",
                        help="Group nearby drawings into clusters")
    parser.add_argument("--no-text", action="store_true",
                        help="Skip text extraction")
    parser.add_argument("--svg-bridge", action="store_true",
                        help="Use SVG-based extraction (captures overlay elements)")

    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(str(pdf_path))

    # Determine pages
    if args.pages:
        page_nums = [int(p) - 1 for p in args.pages.split(",")]
    else:
        page_nums = [args.page - 1]

    # Validate pages
    for pn in page_nums:
        if pn < 0 or pn >= len(doc):
            print(f"Error: page {pn + 1} out of range (1-{len(doc)})",
                  file=sys.stderr)
            sys.exit(1)

    all_lines = []
    for pn in page_nums:
        lines = convert_page(
            doc, pn, args.scale, args.precision,
            use_named_colors=(args.colors == "named"),
            include_text=not args.no_text,
            cluster=args.cluster,
            svg_bridge=args.svg_bridge,
        )
        if lines:
            if len(page_nums) > 1:
                all_lines.append(f"% === Page {pn + 1} ===")
            all_lines.extend(lines)
            all_lines.append("")

    if not all_lines:
        print("No vector graphics found on the specified page(s).",
              file=sys.stderr)
        sys.exit(0)

    output = wrap_tikzpicture(all_lines, standalone=args.standalone)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(output)

    doc.close()


if __name__ == "__main__":
    main()
