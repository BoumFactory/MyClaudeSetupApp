"""Parse SVG path `d` attribute into a list of absolute command tuples."""

import re

# Regex: split on command letters, keeping the letter
_CMD_RE = re.compile(r'([MmLlHhVvCcSsQqTtAaZz])')
_NUM_RE = re.compile(r'[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?')


def tokenize_d(d_string):
    """Split a d-attribute into (command_letter, [numbers]) pairs."""
    parts = _CMD_RE.split(d_string.strip())
    # parts[0] is empty or whitespace before first command
    commands = []
    i = 1
    while i < len(parts):
        cmd = parts[i]
        nums_str = parts[i + 1] if i + 1 < len(parts) else ""
        nums = [float(n) for n in _NUM_RE.findall(nums_str)]
        commands.append((cmd, nums))
        i += 2
    return commands


def _reflect(cx, cy, px, py):
    """Reflect point (px,py) through (cx,cy)."""
    return 2 * cx - px, 2 * cy - py


def parse_svg_path(d_string):
    """Parse SVG d-attribute into absolute command tuples.

    Returns list of tuples:
      ('M', x, y), ('L', x, y), ('C', x1,y1, x2,y2, x,y),
      ('Q', x1,y1, x,y), ('A', rx,ry, rot, large, sweep, x,y), ('Z',)
    """
    tokens = tokenize_d(d_string)
    result = []
    cx, cy = 0.0, 0.0  # current position
    sx, sy = 0.0, 0.0  # subpath start
    last_ctrl = None    # last control point (for S/T)
    last_cmd = None

    for cmd, nums in tokens:
        is_rel = cmd.islower()
        CMD = cmd.upper()

        if CMD == 'M':
            # Consume pairs; first is moveto, rest are implicit lineto
            for j in range(0, len(nums), 2):
                x, y = nums[j], nums[j + 1]
                if is_rel:
                    x, y = cx + x, cy + y
                if j == 0:
                    result.append(('M', x, y))
                    sx, sy = x, y
                else:
                    result.append(('L', x, y))
                cx, cy = x, y
            last_ctrl = None

        elif CMD == 'L':
            for j in range(0, len(nums), 2):
                x, y = nums[j], nums[j + 1]
                if is_rel:
                    x, y = cx + x, cy + y
                result.append(('L', x, y))
                cx, cy = x, y
            last_ctrl = None

        elif CMD == 'H':
            for x in nums:
                if is_rel:
                    x = cx + x
                result.append(('L', x, cy))
                cx = x
            last_ctrl = None

        elif CMD == 'V':
            for y in nums:
                if is_rel:
                    y = cy + y
                result.append(('L', cx, y))
                cy = y
            last_ctrl = None

        elif CMD == 'C':
            for j in range(0, len(nums), 6):
                x1, y1, x2, y2, x, y = nums[j:j + 6]
                if is_rel:
                    x1, y1 = cx + x1, cy + y1
                    x2, y2 = cx + x2, cy + y2
                    x, y = cx + x, cy + y
                result.append(('C', x1, y1, x2, y2, x, y))
                last_ctrl = (x2, y2)
                cx, cy = x, y

        elif CMD == 'S':
            for j in range(0, len(nums), 4):
                x2, y2, x, y = nums[j:j + 4]
                if is_rel:
                    x2, y2 = cx + x2, cy + y2
                    x, y = cx + x, cy + y
                # Reflect previous control point
                if last_cmd in ('C', 'S') and last_ctrl:
                    x1, y1 = _reflect(cx, cy, *last_ctrl)
                else:
                    x1, y1 = cx, cy
                result.append(('C', x1, y1, x2, y2, x, y))
                last_ctrl = (x2, y2)
                cx, cy = x, y

        elif CMD == 'Q':
            for j in range(0, len(nums), 4):
                x1, y1, x, y = nums[j:j + 4]
                if is_rel:
                    x1, y1 = cx + x1, cy + y1
                    x, y = cx + x, cy + y
                result.append(('Q', x1, y1, x, y))
                last_ctrl = (x1, y1)
                cx, cy = x, y

        elif CMD == 'T':
            for j in range(0, len(nums), 2):
                x, y = nums[j], nums[j + 1]
                if is_rel:
                    x, y = cx + x, cy + y
                if last_cmd in ('Q', 'T') and last_ctrl:
                    x1, y1 = _reflect(cx, cy, *last_ctrl)
                else:
                    x1, y1 = cx, cy
                result.append(('Q', x1, y1, x, y))
                last_ctrl = (x1, y1)
                cx, cy = x, y

        elif CMD == 'A':
            for j in range(0, len(nums), 7):
                rx, ry, rot, large, sweep, x, y = nums[j:j + 7]
                if is_rel:
                    x, y = cx + x, cy + y
                result.append(('A', rx, ry, rot, int(large), int(sweep), x, y))
                cx, cy = x, y
            last_ctrl = None

        elif CMD == 'Z':
            result.append(('Z',))
            cx, cy = sx, sy
            last_ctrl = None

        last_cmd = CMD

    return result
