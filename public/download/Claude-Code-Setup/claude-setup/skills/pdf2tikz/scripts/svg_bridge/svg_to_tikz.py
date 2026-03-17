"""Convert parsed SVG elements to TikZ commands."""

import sys
import os

# Add parent dir to path so we can import from pdf2tikz
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf2tikz import format_color, pt_to_cm, fmt

from .svg_path_parser import parse_svg_path
from .svg_transforms import compose_transforms, apply_transform


def _build_options(style, use_named_colors):
    """Build TikZ options string from SVGStyle."""
    opts = []
    has_stroke = style.stroke is not None
    has_fill = style.fill is not None

    if has_stroke:
        c = format_color(style.stroke, use_named_colors)
        if c and c != 'black':
            opts.append(f'draw={c}')
        elif has_fill:
            opts.append('draw')
    if has_fill:
        c = format_color(style.fill, use_named_colors)
        if c:
            opts.append(f'fill={c}')

    if has_stroke and abs(style.stroke_width - 1.0) > 0.1:
        opts.append(f'line width={fmt(style.stroke_width, 1)}pt')

    if style.dashes:
        opts.append('dashed')

    return f'[{", ".join(opts)}]' if opts else ''


def _tp(x, y, matrix, scale, precision, page_height, offset_x, offset_y):
    """Transform SVG point → TikZ coordinates."""
    # Apply SVG transform stack
    px, py = apply_transform(matrix, x, y)
    # SVG coords are in PDF points (top-left origin, Y down)
    # Convert to TikZ (bottom-left, Y up, cm)
    tx = pt_to_cm(px - offset_x) * scale
    ty = pt_to_cm(offset_y - py) * scale
    return fmt(tx, precision), fmt(ty, precision)


def _convert_path_element(elem, scale, precision, use_named_colors,
                          page_height, offset_x, offset_y):
    """Convert a single SVG <path> to TikZ commands."""
    commands = parse_svg_path(elem.d)
    if not commands:
        return []

    matrix = compose_transforms(elem.transform_stack)
    opts = _build_options(elem.style, use_named_colors)

    def tp(x, y):
        return _tp(x, y, matrix, scale, precision, page_height,
                   offset_x, offset_y)

    # Determine command type
    has_stroke = elem.style.stroke is not None
    has_fill = elem.style.fill is not None
    if has_fill and has_stroke:
        cmd = '\\filldraw'
    elif has_fill:
        cmd = '\\fill'
    else:
        cmd = '\\draw'

    # Build path segments (may have multiple subpaths via M)
    lines = []
    parts = []
    first_pos = None

    for c in commands:
        if c[0] == 'M':
            # New subpath — emit previous if any
            if parts:
                lines.append(f'{cmd}{opts} ' + ' '.join(parts) + ';')
                parts = []
            x, y = tp(c[1], c[2])
            parts.append(f'({x},{y})')
            first_pos = (x, y)

        elif c[0] == 'L':
            x, y = tp(c[1], c[2])
            parts.append(f'-- ({x},{y})')

        elif c[0] == 'C':
            cx1, cy1 = tp(c[1], c[2])
            cx2, cy2 = tp(c[3], c[4])
            x, y = tp(c[5], c[6])
            parts.append(
                f'.. controls ({cx1},{cy1}) and ({cx2},{cy2}) .. ({x},{y})')

        elif c[0] == 'Q':
            # Convert quadratic to cubic: Q(p0,p1,p2) → C(p0, p0+2/3*(p1-p0), p2+2/3*(p1-p2), p2)
            # Approximate: just emit as cubic with repeated control
            qx, qy = tp(c[1], c[2])
            x, y = tp(c[3], c[4])
            parts.append(
                f'.. controls ({qx},{qy}) and ({qx},{qy}) .. ({x},{y})')

        elif c[0] == 'A':
            # Simplify: straight line to endpoint (arc approximation TODO)
            x, y = tp(c[6], c[7])
            parts.append(f'-- ({x},{y})')

        elif c[0] == 'Z':
            parts.append('-- cycle')

    if parts:
        lines.append(f'{cmd}{opts} ' + ' '.join(parts) + ';')

    return lines


def _convert_line_element(elem, scale, precision, use_named_colors,
                          page_height, offset_x, offset_y):
    """Convert SVG <line> to TikZ."""
    matrix = compose_transforms(elem.transform_stack)
    opts = _build_options(elem.style, use_named_colors)
    a = elem.attrs

    def tp(x, y):
        return _tp(x, y, matrix, scale, precision, page_height,
                   offset_x, offset_y)

    x1, y1 = tp(a['x1'], a['y1'])
    x2, y2 = tp(a['x2'], a['y2'])
    return [f'\\draw{opts} ({x1},{y1}) -- ({x2},{y2});']


def _convert_rect_element(elem, scale, precision, use_named_colors,
                          page_height, offset_x, offset_y):
    """Convert SVG <rect> to TikZ."""
    matrix = compose_transforms(elem.transform_stack)
    opts = _build_options(elem.style, use_named_colors)
    a = elem.attrs

    def tp(x, y):
        return _tp(x, y, matrix, scale, precision, page_height,
                   offset_x, offset_y)

    x1, y1 = tp(a['x'], a['y'])
    x2, y2 = tp(a['x'] + a['width'], a['y'] + a['height'])

    has_fill = elem.style.fill is not None
    has_stroke = elem.style.stroke is not None
    cmd = '\\filldraw' if has_fill and has_stroke else (
        '\\fill' if has_fill else '\\draw')
    return [f'{cmd}{opts} ({x1},{y1}) rectangle ({x2},{y2});']


def _convert_circle_element(elem, scale, precision, use_named_colors,
                            page_height, offset_x, offset_y):
    """Convert SVG <circle> to TikZ."""
    matrix = compose_transforms(elem.transform_stack)
    opts = _build_options(elem.style, use_named_colors)
    a = elem.attrs

    cx, cy = _tp(a['cx'], a['cy'], matrix, scale, precision,
                 page_height, offset_x, offset_y)
    r = fmt(pt_to_cm(a['r']) * scale, precision)

    has_fill = elem.style.fill is not None
    has_stroke = elem.style.stroke is not None
    cmd = '\\filldraw' if has_fill and has_stroke else (
        '\\fill' if has_fill else '\\draw')
    return [f'{cmd}{opts} ({cx},{cy}) circle ({r});']


# Dispatch table
_CONVERTERS = {
    'path': _convert_path_element,
    'line': _convert_line_element,
    'rect': _convert_rect_element,
    'circle': _convert_circle_element,
}


def convert_svg_element(elem, scale, precision, use_named_colors,
                        page_height, offset_x, offset_y):
    """Convert any SVGElement to TikZ commands."""
    converter = _CONVERTERS.get(elem.tag)
    if converter:
        return converter(elem, scale, precision, use_named_colors,
                         page_height, offset_x, offset_y)
    return []
