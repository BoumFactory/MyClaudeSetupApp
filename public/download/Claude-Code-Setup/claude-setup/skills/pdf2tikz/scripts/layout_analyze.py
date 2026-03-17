#!/usr/bin/env python3
"""layout_analyze.py — Analyze PDF page layout and spatial disposition.

Zone-based analysis:
1. Uses TEXT BLOCKS (not lines/decorations) to find horizontal zones
2. Within each zone, detects column layouts from element X-positions
3. Classifies content per column (table, chart, annotation box, text)
4. Detects annotation arrows and colored containers

Usage:
    python layout_analyze.py document.pdf [--pages 1,2,3] [--format json|markdown]
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from collections import defaultdict

import fitz  # PyMuPDF


# ── Helpers ──────────────────────────────────────────────────────────────

def pt_to_cm(pt):
    return round(pt / 72.0 * 2.54, 2)

def rect_to_cm(r):
    return {"x": pt_to_cm(r.x0), "y": pt_to_cm(r.y0),
            "w": pt_to_cm(r.width), "h": pt_to_cm(r.height)}

def rgb_hex(rgb):
    if rgb is None: return None
    return f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"

def is_white(rgb, t=0.93):
    return rgb is None or all(c > t for c in rgb)

def is_black(rgb, t=0.1):
    return rgb is not None and all(c < t for c in rgb)

def rects_overlap(a, b):
    return a.x0 < b.x1 and b.x0 < a.x1 and a.y0 < b.y1 and b.y0 < a.y1

def rect_contains(outer, inner, m=5):
    return (outer.x0 - m <= inner.x0 and outer.y0 - m <= inner.y0
            and outer.x1 + m >= inner.x1 and outer.y1 + m >= inner.y1)


# ── Text Block Extraction ───────────────────────────────────────────────

def extract_text_blocks(page):
    """Extract text blocks with basic classification."""
    blocks = []
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        bbox = fitz.Rect(block["bbox"])
        lines_t = []
        max_size = 0
        is_bold = False
        for line in block["lines"]:
            lt = ""
            for span in line["spans"]:
                lt += span["text"]
                max_size = max(max_size, span["size"])
                if "bold" in span["font"].lower():
                    is_bold = True
            lines_t.append(lt.strip())
        text = " ".join(t for t in lines_t if t)
        if not text:
            continue
        blocks.append({
            "type": "text", "rect": bbox, "text": text[:300],
            "font_size": round(max_size, 1), "bold": is_bold,
            "num_lines": len(lines_t),
        })
    return blocks


# ── Colored Rectangle Extraction ────────────────────────────────────────

def extract_colored_rects(drawings, pw, ph):
    """Extract filled rects: annotation boxes, cell highlights, containers."""
    rects = []
    for d in drawings:
        fill = d.get("fill")
        if not fill or is_white(fill):
            continue
        for item in d["items"]:
            if item[0] != "re":
                continue
            rect = fitz.Rect(item[1])
            if rect.width < 5 or rect.height < 5:
                continue
            # Skip page-spanning decorations
            if rect.width > pw * 0.8 and rect.height > ph * 0.25:
                continue
            role = "cell_highlight"
            area = rect.width * rect.height
            if area > 3000 and not is_black(fill):
                role = "annotation_box"
            elif area < 600:
                role = "legend_swatch"
            rects.append({
                "type": "colored_rect", "rect": rect,
                "fill": rgb_hex(fill), "stroke": rgb_hex(d.get("color")),
                "role": role,
            })
    return rects


# ── Table Detection ─────────────────────────────────────────────────────

def detect_tables(drawings, text_blocks):
    """Detect tables: clusters of h-lines with similar x-extent + v-lines.

    Strategy: Group h-lines by similar x-extent AND y-proximity,
    require at least 2 h-lines and 1 v-line within the area.
    """
    h_lines = []
    v_lines = []
    for d in drawings:
        for item in d["items"]:
            if item[0] != "l":
                continue
            p1, p2 = fitz.Point(item[1]), fitz.Point(item[2])
            length = math.hypot(p2.x - p1.x, p2.y - p1.y)
            if length < 30:  # ignore short lines
                continue
            if abs(p1.y - p2.y) < 2:
                h_lines.append({"y": (p1.y + p2.y) / 2,
                                "x0": min(p1.x, p2.x), "x1": max(p1.x, p2.x),
                                "len": length})
            elif abs(p1.x - p2.x) < 2:
                v_lines.append({"x": (p1.x + p2.x) / 2,
                                "y0": min(p1.y, p2.y), "y1": max(p1.y, p2.y),
                                "len": length})

    if len(h_lines) < 2:
        return []

    # Group h-lines by x-extent similarity (within 20pt)
    # AND they must be within reasonable y-distance of each other
    h_sorted = sorted(h_lines, key=lambda l: l["y"])
    groups = []

    for hl in h_sorted:
        placed = False
        for g in groups:
            # Check x-extent match (tight: 15pt tolerance)
            if (abs(hl["x0"] - g["x0"]) < 15 and abs(hl["x1"] - g["x1"]) < 15):
                # Check y-proximity: within 40pt (~1.4cm) of LAST line
                last_y = max(l["y"] for l in g["lines"])
                if hl["y"] <= last_y + 40:
                    g["lines"].append(hl)
                    g["x0"] = min(g["x0"], hl["x0"])
                    g["x1"] = max(g["x1"], hl["x1"])
                    placed = True
                    break
        if not placed:
            groups.append({"lines": [hl], "x0": hl["x0"], "x1": hl["x1"]})

    tables = []
    for g in groups:
        if len(g["lines"]) < 2:
            continue
        table_w = g["x1"] - g["x0"]
        if table_w < 60:
            continue

        y_min = min(l["y"] for l in g["lines"])
        y_max = max(l["y"] for l in g["lines"])
        table_h = y_max - y_min
        if table_h < 10:
            continue

        # Count v-lines inside — REQUIRE at least 1
        rel_v = [v for v in v_lines
                 if g["x0"] - 5 <= v["x"] <= g["x1"] + 5
                 and y_min - 5 <= v["y0"] and v["y1"] <= y_max + 5]
        n_cols = len(set(round(v["x"]) for v in rel_v))
        if n_cols < 1:
            continue  # Not a table without vertical separators

        # Table rect (add margin above for header text)
        table_rect = fitz.Rect(g["x0"] - 2, y_min - 18, g["x1"] + 2, y_max + 3)

        # Skip if table covers too much of the page (likely box borders)
        if table_rect.height > 400:  # > ~14cm = probably not a table
            continue

        # Text preview
        inside = [b for b in text_blocks if rects_overlap(table_rect, b["rect"])]
        preview = " | ".join(b["text"][:25] for b in inside[:5])

        # Distinct Y positions = rows
        ys = sorted(set(round(l["y"]) for l in g["lines"]))

        tables.append({
            "type": "table", "rect": table_rect,
            "rows": len(ys), "cols": max(n_cols, 1),
            "preview": preview,
        })

    return tables


# ── Chart Detection ──────────────────────────────────────────────────────

def detect_charts(drawings, pw, ph):
    """Detect chart regions: axis pairs, pie charts."""
    charts = []

    # --- Axes detection ---
    h_lines = []
    v_lines = []
    for d in drawings:
        for item in d["items"]:
            if item[0] != "l":
                continue
            p1, p2 = fitz.Point(item[1]), fitz.Point(item[2])
            length = math.hypot(p2.x - p1.x, p2.y - p1.y)
            if length < 40:
                continue
            if abs(p1.y - p2.y) < 2:
                h_lines.append({"y": (p1.y + p2.y) / 2,
                                "x0": min(p1.x, p2.x), "x1": max(p1.x, p2.x),
                                "len": length})
            elif abs(p1.x - p2.x) < 2:
                v_lines.append({"x": (p1.x + p2.x) / 2,
                                "y0": min(p1.y, p2.y), "y1": max(p1.y, p2.y),
                                "len": length})

    for hl in h_lines:
        for vl in v_lines:
            # Check shared origin (L-shape)
            if (abs(hl["x0"] - vl["x"]) < 10 and
                    abs(hl["y"] - vl["y1"]) < 10 and
                    hl["len"] > 80 and vl["len"] > 80):
                chart_rect = fitz.Rect(
                    vl["x"] - 25, vl["y0"] - 20,
                    hl["x1"] + 25, vl["y1"] + 35
                )
                # Limit chart size (max 50% of page)
                if chart_rect.width > pw * 0.55 or chart_rect.height > ph * 0.55:
                    continue
                dup = any(rects_overlap(c["rect"], chart_rect) for c in charts)
                if not dup:
                    charts.append({
                        "type": "chart", "rect": chart_rect,
                        "chart_type": "bar_or_line",
                    })

    # --- Pie chart: multiple colored sectors ---
    sector_centers = defaultdict(list)
    for d in drawings:
        fill = d.get("fill")
        if not fill or is_white(fill) or is_black(fill):
            continue
        items = d["items"]
        has_c = any(i[0] == "c" for i in items)
        has_l = any(i[0] == "l" for i in items)
        if has_c and has_l:
            pts = []
            for item in items:
                if item[0] in ("l", "c"):
                    pts.append(fitz.Point(item[1]))
                    pts.append(fitz.Point(item[-1]))
            if pts:
                cx = sum(p.x for p in pts) / len(pts)
                cy = sum(p.y for p in pts) / len(pts)
                key = (round(cx / 40), round(cy / 40))
                sector_centers[key].append(pts)

    for key, sectors in sector_centers.items():
        if len(sectors) >= 3:
            all_pts = [p for s in sectors for p in s]
            xs = [p.x for p in all_pts]
            ys = [p.y for p in all_pts]
            pie_rect = fitz.Rect(min(xs) - 15, min(ys) - 15,
                                  max(xs) + 15, max(ys) + 15)
            if pie_rect.width > pw * 0.55:
                continue
            dup = any(rects_overlap(c["rect"], pie_rect) for c in charts)
            if not dup:
                charts.append({
                    "type": "chart", "rect": pie_rect,
                    "chart_type": "pie", "sectors": len(sectors),
                })

    return charts


# ── Arrow Detection ──────────────────────────────────────────────────────

def detect_arrows(drawings):
    """Detect annotation arrows: arrowheads (line or curve) + associated paths.

    bfcours arrows typically consist of 3 drawings per arrow:
    1. L-shaped path (2 line segments, colored)
    2. Arrowhead (3 Bezier curves, filled with same color)
    3. Rounded rectangle annotation box (8 items, filled)

    Arrowheads can be made of line segments OR Bezier curves.
    """
    arrowheads = []
    colored_paths = []

    for d in drawings:
        items = d["items"]
        fill = d.get("fill")
        color = d.get("color")
        dashes = d.get("dashes", "")

        # --- Arrowhead detection ---
        # Curve-based arrowheads: 3 Bezier curves, small, filled
        if fill and not is_white(fill) and not is_black(fill):
            curves = [i for i in items if i[0] == "c"]
            lines = [i for i in items if i[0] == "l"]

            if len(curves) >= 2 and len(items) <= 5:
                pts = []
                for item in items:
                    if item[0] == "c":
                        pts.append(fitz.Point(item[1]))
                        pts.append(fitz.Point(item[4]))  # end point
                    elif item[0] == "l":
                        pts.extend([fitz.Point(item[1]), fitz.Point(item[2])])
                if pts:
                    xs = [p.x for p in pts]
                    ys = [p.y for p in pts]
                    bbox = fitz.Rect(min(xs), min(ys), max(xs), max(ys))
                    if bbox.width < 15 and bbox.height < 15:
                        arrowheads.append({
                            "rect": bbox,
                            "color": rgb_hex(fill) or rgb_hex(color),
                        })
                        continue  # don't also treat as path

            # Line-based arrowheads: small filled triangles
            if len(items) <= 5 and lines:
                pts = []
                for item in items:
                    if item[0] == "l":
                        pts.extend([fitz.Point(item[1]), fitz.Point(item[2])])
                if 3 <= len(pts) <= 8:
                    xs = [p.x for p in pts]
                    ys = [p.y for p in pts]
                    bbox = fitz.Rect(min(xs), min(ys), max(xs), max(ys))
                    if 1 < bbox.width < 15 and 1 < bbox.height < 15:
                        arrowheads.append({
                            "rect": bbox,
                            "color": rgb_hex(fill) or rgb_hex(color),
                        })
                        continue

        # --- Colored/dashed path segments (annotation lines) ---
        is_dashed = bool(dashes and str(dashes) != "[] 0")
        is_colored = color and not is_black(color) and not is_white(color)
        if is_dashed or is_colored:
            for item in items:
                if item[0] == "l":
                    p1, p2 = fitz.Point(item[1]), fitz.Point(item[2])
                    length = math.hypot(p2.x - p1.x, p2.y - p1.y)
                    if 10 < length < 300:
                        colored_paths.append({
                            "p1": p1, "p2": p2,
                            "color": rgb_hex(color),
                            "dashed": is_dashed,
                        })

    # Link arrowheads with nearby path segments
    arrows = []
    used_paths = set()
    for ah in arrowheads:
        cx = (ah["rect"].x0 + ah["rect"].x1) / 2
        cy = (ah["rect"].y0 + ah["rect"].y1) / 2
        nearby = []
        for idx, cl in enumerate(colored_paths):
            d1 = math.hypot(cl["p1"].x - cx, cl["p1"].y - cy)
            d2 = math.hypot(cl["p2"].x - cx, cl["p2"].y - cy)
            if min(d1, d2) < 25:
                nearby.append(cl)
                used_paths.add(idx)

        arrow_rect = fitz.Rect(ah["rect"])
        for nl in nearby:
            arrow_rect |= fitz.Rect(
                min(nl["p1"].x, nl["p2"].x), min(nl["p1"].y, nl["p2"].y),
                max(nl["p1"].x, nl["p2"].x), max(nl["p1"].y, nl["p2"].y))

        arrows.append({
            "type": "arrow", "rect": arrow_rect,
            "color": ah["color"],
            "dashed": any(nl["dashed"] for nl in nearby),
            "has_line": len(nearby) > 0,
        })

    # Also detect standalone dashed colored paths as arrows (no arrowhead found)
    for idx, cl in enumerate(colored_paths):
        if idx not in used_paths and cl["dashed"]:
            arrow_rect = fitz.Rect(
                min(cl["p1"].x, cl["p2"].x), min(cl["p1"].y, cl["p2"].y),
                max(cl["p1"].x, cl["p2"].x), max(cl["p1"].y, cl["p2"].y))
            arrows.append({
                "type": "arrow", "rect": arrow_rect,
                "color": cl["color"],
                "dashed": True,
                "has_line": True,
            })

    return arrows


# ── Zone Detection (text-based) ──────────────────────────────────────────

def detect_zones(text_blocks, all_elements, page_height, page_width):
    """Divide page into horizontal zones using TEXT blocks as anchors.

    Text blocks define zone boundaries (no expansion from drawings).
    Each non-text element is assigned to exactly ONE zone (best Y-overlap).
    """
    if not text_blocks:
        return []

    GAP = 12  # pt gap between zones (~4mm)

    # Sort text blocks by y0
    sorted_t = sorted(text_blocks, key=lambda b: b["rect"].y0)

    # Merge text blocks into zones by Y-proximity
    zone_intervals = []
    cur_y0 = sorted_t[0]["rect"].y0
    cur_y1 = sorted_t[0]["rect"].y1

    for tb in sorted_t[1:]:
        if tb["rect"].y0 <= cur_y1 + GAP:
            cur_y1 = max(cur_y1, tb["rect"].y1)
        else:
            zone_intervals.append((cur_y0, cur_y1))
            cur_y0 = tb["rect"].y0
            cur_y1 = tb["rect"].y1
    zone_intervals.append((cur_y0, cur_y1))

    # Build zones with text elements
    zones = []
    for i, (y0, y1) in enumerate(zone_intervals):
        zone_rect = fitz.Rect(0, y0 - 3, page_width, y1 + 3)
        zone_text = [e for e in text_blocks
                     if rects_overlap(zone_rect, e["rect"])]
        zones.append({
            "idx": i, "rect": zone_rect,
            "y_range": (y0, y1),
            "elements": list(zone_text),
        })

    # Assign each non-text element to the zone with best Y-overlap
    non_text = [e for e in all_elements if e["type"] != "text"]
    for elem in non_text:
        best_zone = None
        best_overlap = 0
        for zone in zones:
            ov_y0 = max(elem["rect"].y0, zone["rect"].y0)
            ov_y1 = min(elem["rect"].y1, zone["rect"].y1)
            overlap = max(0, ov_y1 - ov_y0)
            if overlap > best_overlap:
                best_overlap = overlap
                best_zone = zone
        if best_zone is not None and best_overlap > 0:
            best_zone["elements"].append(elem)

    # Remove empty zones
    zones = [z for z in zones if z["elements"]]

    return zones


# ── Column Detection ─────────────────────────────────────────────────────

def detect_columns(elements, page_width):
    """Detect column layout within a zone.

    Uses "significant" elements (text, table, chart, annotation_box)
    sorted by x-center. Finds gaps > threshold in X to split columns.
    """
    # Only use significant elements for column detection
    sig = [e for e in elements
           if e["type"] in ("text", "table", "chart")
           or (e["type"] == "colored_rect" and e.get("role") == "annotation_box")]

    if len(sig) < 2:
        return [elements]  # single column

    # Sort by x-center
    sig_sorted = sorted(sig, key=lambda e: (e["rect"].x0 + e["rect"].x1) / 2)

    # Find the biggest X-gap
    gaps = []
    for i in range(len(sig_sorted) - 1):
        left_x1 = sig_sorted[i]["rect"].x1
        right_x0 = sig_sorted[i + 1]["rect"].x0
        gap = right_x0 - left_x1
        if gap > 0:
            gaps.append((gap, left_x1, right_x0, i))

    if not gaps:
        return [elements]

    # Sort by gap size, take the biggest
    gaps.sort(key=lambda g: -g[0])
    best_gap, split_x_left, split_x_right, split_idx = gaps[0]

    # Need a meaningful gap (> 15pt ~= 0.5cm)
    if best_gap < 15:
        return [elements]

    split_x = (split_x_left + split_x_right) / 2

    # Split ALL elements (not just significant ones) by this X boundary
    left_col = [e for e in elements if (e["rect"].x0 + e["rect"].x1) / 2 < split_x]
    right_col = [e for e in elements if (e["rect"].x0 + e["rect"].x1) / 2 >= split_x]

    if not left_col or not right_col:
        return [elements]

    # Check minimum column width (~2.5cm = 70pt) — avoid axis labels
    MIN_COL_WIDTH = 70
    left_width = max(e["rect"].x1 for e in left_col) - min(e["rect"].x0 for e in left_col)
    right_width = max(e["rect"].x1 for e in right_col) - min(e["rect"].x0 for e in right_col)

    if left_width < MIN_COL_WIDTH:
        return [elements]  # Left too narrow, merge back
    if right_width < MIN_COL_WIDTH:
        return [elements]  # Right too narrow, merge back

    # Recursively check for more columns in each half
    left_cols = detect_columns(left_col, split_x - elements[0]["rect"].x0)
    right_cols = detect_columns(right_col, page_width - split_x)

    return left_cols + right_cols


# ── Column Classification ───────────────────────────────────────────────

def classify_column(elements):
    """Classify content of a column."""
    if not elements:
        return {"primary_type": "empty", "rect_cm": {"x": 0, "y": 0, "w": 0, "h": 0}}

    rects = [e["rect"] for e in elements]
    bbox = fitz.Rect(min(r.x0 for r in rects), min(r.y0 for r in rects),
                      max(r.x1 for r in rects), max(r.y1 for r in rects))

    texts = [e for e in elements if e["type"] == "text"]
    tables = [e for e in elements if e["type"] == "table"]
    charts = [e for e in elements if e["type"] == "chart"]
    colored = [e for e in elements if e["type"] == "colored_rect"]
    arrows = [e for e in elements if e["type"] == "arrow"]

    # Determine primary type
    if charts:
        primary = "chart"
    elif tables:
        primary = "table"
    elif colored and len(texts) <= 3 and any(c.get("role") == "annotation_box" for c in colored):
        primary = "annotation_box"
    else:
        primary = "text"

    # Semantic hints from text
    semantic = None
    if texts:
        first = texts[0]["text"]
        if re.match(r'^\s*•?\s*D[ée]finition', first):
            semantic = "definition"
        elif re.match(r'^\s*Exemple', first):
            semantic = "example"
        elif re.match(r'^\d+\s+\w', first) and texts[0].get("bold"):
            semantic = "section"
        elif texts[0].get("font_size", 0) > 14:
            semantic = "title"

    result = {
        "rect_cm": rect_to_cm(bbox),
        "width_cm": pt_to_cm(bbox.width),
        "primary_type": primary,
        "num_elements": len(elements),
    }

    if charts:
        result["chart_type"] = charts[0].get("chart_type", "unknown")
        if charts[0].get("sectors"):
            result["sectors"] = charts[0]["sectors"]
    if semantic:
        result["semantic"] = semantic
    if texts:
        result["text_preview"] = texts[0]["text"][:120]
    if tables:
        t = tables[0]
        result["table_info"] = {"rows": t["rows"], "cols": t["cols"],
                                 "preview": t.get("preview", "")}
    if colored:
        result["colors"] = list(set(c["fill"] for c in colored))
    if arrows:
        result["arrows"] = [{
            "color": a["color"], "dashed": a.get("dashed", False),
            "rect_cm": rect_to_cm(a["rect"]),
        } for a in arrows]

    return result


# ── Page Analysis ────────────────────────────────────────────────────────

def analyze_page(doc, page_num):
    """Full layout analysis for one page."""
    page = doc[page_num]
    pw, ph = page.rect.width, page.rect.height
    drawings = page.get_drawings()

    # Extract all elements
    text_blocks = extract_text_blocks(page)
    colored_rects = extract_colored_rects(drawings, pw, ph)
    tables = detect_tables(drawings, text_blocks)
    charts = detect_charts(drawings, pw, ph)
    arrows = detect_arrows(drawings)

    all_elements = text_blocks + colored_rects + tables + charts + arrows

    # Detect zones (text-based)
    zones = detect_zones(text_blocks, all_elements, ph, pw)

    # Analyze each zone
    zone_analyses = []
    for zone in zones:
        elems = zone["elements"]
        y0, y1 = zone["y_range"]
        columns = detect_columns(elems, pw)

        col_analyses = [classify_column(col) for col in columns]
        ncols = len(col_analyses)

        # Column ratios
        if ncols > 1:
            widths = [c["width_cm"] for c in col_analyses]
            total = sum(widths)
            ratios = [round(w / total * 100) for w in widths] if total > 0 else []
        else:
            ratios = [100]

        zone_analyses.append({
            "y_range_cm": (pt_to_cm(y0), pt_to_cm(y1)),
            "height_cm": pt_to_cm(y1 - y0),
            "num_columns": ncols,
            "column_ratios": ratios,
            "columns": col_analyses,
        })

    # Summary
    counts = defaultdict(int)
    for e in all_elements:
        counts[e["type"]] += 1

    return {
        "page": page_num + 1,
        "dimensions_cm": {"width": pt_to_cm(pw), "height": pt_to_cm(ph)},
        "element_counts": dict(counts),
        "num_zones": len(zone_analyses),
        "zones": zone_analyses,
    }


# ── Markdown Formatter ───────────────────────────────────────────────────

def format_markdown(analysis):
    lines = []
    lines.append(f"## Page {analysis['page']} Layout")
    dim = analysis["dimensions_cm"]
    ec = analysis["element_counts"]
    parts = [f"{v} {k}" for k, v in sorted(ec.items()) if v > 0]
    lines.append(f"**{dim['width']}x{dim['height']}cm** | "
                 f"{analysis['num_zones']} zones | " + ", ".join(parts))
    lines.append("")

    for i, zone in enumerate(analysis["zones"]):
        y0, y1 = zone["y_range_cm"]
        nc = zone["num_columns"]

        # Zone header
        if nc > 1:
            ratios = ":".join(str(r) for r in zone["column_ratios"])
            lines.append(f"### Zone {i+1} (y={y0}–{y1}cm) — "
                         f"{nc} colonnes ({ratios})")
        else:
            lines.append(f"### Zone {i+1} (y={y0}–{y1}cm) — pleine largeur")

        for j, col in enumerate(zone["columns"]):
            prefix = f"  **Col {j+1}**" if nc > 1 else " "
            r = col["rect_cm"]
            label = col["primary_type"]
            if col.get("chart_type"):
                label += f" ({col['chart_type']})"
            if col.get("semantic"):
                label = f"[{col['semantic']}] {label}"
            lines.append(f"{prefix} {label} — {r['w']}x{r['h']}cm")

            if col.get("text_preview"):
                lines.append(f"    \"{col['text_preview'][:80]}\"")
            if col.get("table_info"):
                ti = col["table_info"]
                lines.append(f"    Tableau {ti['rows']}x{ti['cols']}: {ti['preview'][:60]}")
            if col.get("colors"):
                lines.append(f"    Couleurs: {', '.join(col['colors'])}")
            if col.get("arrows"):
                for a in col["arrows"]:
                    dash = " pointillée" if a["dashed"] else ""
                    lines.append(f"    Flèche {a['color']}{dash}")

        lines.append("")

    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Analyze PDF page layout and disposition"
    )
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("--pages", type=str, default=None,
                        help="Comma-separated pages (default: all)")
    parser.add_argument("--format", choices=["json", "markdown", "both"],
                        default="markdown",
                        help="Output format (default: markdown)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output file (default: stdout)")

    args = parser.parse_args()
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(str(pdf_path))
    if args.pages:
        page_nums = [int(p) - 1 for p in args.pages.split(",")]
    else:
        page_nums = list(range(len(doc)))

    results = []
    for pn in page_nums:
        if 0 <= pn < len(doc):
            results.append(analyze_page(doc, pn))
    doc.close()

    output_parts = []
    if args.format in ("json", "both"):
        output_parts.append(json.dumps(results, indent=2, ensure_ascii=False))
    if args.format in ("markdown", "both"):
        if args.format == "both":
            output_parts.append("\n---\n")
        for r in results:
            output_parts.append(format_markdown(r))

    output = "\n".join(output_parts)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(output)


if __name__ == "__main__":
    main()
