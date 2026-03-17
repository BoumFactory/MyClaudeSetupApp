"""Parse and apply SVG transform attributes (2D affine matrices)."""

import math
import re


def _parse_transform_func(func_str):
    """Parse a single SVG transform function like 'translate(10, 20)'."""
    match = re.match(r'(\w+)\(([^)]*)\)', func_str.strip())
    if not match:
        return (1, 0, 0, 1, 0, 0)  # identity

    name = match.group(1)
    args = [float(v) for v in re.findall(r'[+-]?[\d.]+(?:e[+-]?\d+)?', match.group(2))]

    if name == 'translate':
        tx = args[0] if len(args) > 0 else 0
        ty = args[1] if len(args) > 1 else 0
        return (1, 0, 0, 1, tx, ty)

    elif name == 'scale':
        sx = args[0] if len(args) > 0 else 1
        sy = args[1] if len(args) > 1 else sx
        return (sx, 0, 0, sy, 0, 0)

    elif name == 'rotate':
        angle = math.radians(args[0]) if len(args) > 0 else 0
        c, s = math.cos(angle), math.sin(angle)
        if len(args) == 3:
            cx, cy = args[1], args[2]
            # rotate around (cx,cy) = translate(cx,cy) * rotate * translate(-cx,-cy)
            return multiply(
                (1, 0, 0, 1, cx, cy),
                multiply((c, s, -s, c, 0, 0), (1, 0, 0, 1, -cx, -cy))
            )
        return (c, s, -s, c, 0, 0)

    elif name == 'matrix':
        if len(args) >= 6:
            return tuple(args[:6])
        return (1, 0, 0, 1, 0, 0)

    elif name == 'skewX':
        angle = math.radians(args[0]) if args else 0
        return (1, 0, math.tan(angle), 1, 0, 0)

    elif name == 'skewY':
        angle = math.radians(args[0]) if args else 0
        return (1, math.tan(angle), 0, 1, 0, 0)

    return (1, 0, 0, 1, 0, 0)


def multiply(m1, m2):
    """Multiply two 2D affine matrices (a,b,c,d,e,f)."""
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (
        a1 * a2 + c1 * b2,
        b1 * a2 + d1 * b2,
        a1 * c2 + c1 * d2,
        b1 * c2 + d1 * d2,
        a1 * e2 + c1 * f2 + e1,
        b1 * e2 + d1 * f2 + f1,
    )


def parse_transform(transform_str):
    """Parse a full SVG transform attribute into a single affine matrix."""
    if not transform_str:
        return (1, 0, 0, 1, 0, 0)

    funcs = re.findall(r'\w+\([^)]*\)', transform_str)
    result = (1, 0, 0, 1, 0, 0)
    for f in funcs:
        result = multiply(result, _parse_transform_func(f))
    return result


def compose_transforms(transform_stack):
    """Compose a list of transform matrices (parent first) into one."""
    result = (1, 0, 0, 1, 0, 0)
    for m in transform_stack:
        result = multiply(result, m)
    return result


def apply_transform(matrix, x, y):
    """Apply affine matrix to a point."""
    a, b, c, d, e, f = matrix
    return (a * x + c * y + e, b * x + d * y + f)
