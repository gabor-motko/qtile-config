import subprocess
import numpy as np
from settings import config_path
from libqtile.core.manager import Qtile
from libqtile.utils import send_notification
from rofi import Rofi # type: ignore
from logging import DEBUG

r = Rofi()
def status(text):
    r.status(str(text))

# Execute a shell command and return its results as a tuple of (stdout: array, stderr: array, exitcode).
def exec(cmd: str) -> tuple:
    proc = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return (
        [item.decode() for item in stdout.split(b"\n")],
        [item.decode() for item in stderr.split(b"\n")],
        proc.returncode
    )


# Return 'v' clamped to the ['low', 'high'] range.
def clamp(v, low, high):
    return min(high, max(low, v))


# Converts a color's hex-representation to a tuple of float(0..1)
def color_hex_to_float(s: str) -> tuple:
    s = s.strip().upper()
    if s[0] == "#":
        s = s[1:]
    l = len(s)
    if   l == 8:
        return (
            int(s[0:2], 16) / 255,
            int(s[2:4], 16) / 255,
            int(s[4:6], 16) / 255,
            int(s[6:8], 16) / 255,
        )
    elif l == 6:
        return (
            int(s[0:2], 16) / 255,
            int(s[2:4], 16) / 255,
            int(s[4:6], 16) / 255,
            1
        )
    elif l == 4:
        return (
            int(s[0] * 2, 16) / 255,
            int(s[1] * 2, 16) / 255,
            int(s[2] * 2, 16) / 255,
            int(s[3] * 2, 16) / 255,
        )
    elif l == 3:
        return (
            int(s[0] * 2, 16) / 255,
            int(s[1] * 2, 16) / 255,
            int(s[2] * 2, 16) / 255,
            1
        )
    else:
        raise Exception("Invalid hex representation")


# Converts a color given as a tuple of float(0..1) to its closest hexadecimal representation.
def color_float_to_hex(c, element_count = 6, truncate_opaque_alpha = True, prepend_hash = True):
    ec = element_count

    if ec == 3 or ec == 4:
        r = int(round(clamp(c[0], 0, 1) * 15))
        g = int(round(clamp(c[1], 0, 1) * 15))
        b = int(round(clamp(c[2], 0, 1) * 15))
        a = int(round(clamp(c[3], 0, 1) * 15)) if len(c) > 3 else 15

        if ec == 3 or (a >= 15 and truncate_opaque_alpha):
            return "{}{:x}{:x}{:x}".format(
                "#" if prepend_hash else "",
                r, g, b
            )
        else:
            return "{}{:x}{:x}{:x}{:x}".format(
                "#" if prepend_hash else "",
                r, g, b, a
            )

    elif ec == 6 or ec == 8:
        r = int(round(clamp(c[0], 0, 1) * 255))
        g = int(round(clamp(c[1], 0, 1) * 255))
        b = int(round(clamp(c[2], 0, 1) * 255))
        a = int(round(clamp(c[3], 0, 1) * 255)) if len(c) > 3 else 255

        if ec == 6 or (a >= 255 and truncate_opaque_alpha):
            return "{}{:02x}{:02x}{:02x}".format(
                "#" if prepend_hash else "",
                r, g, b
            )
        else:
            return "{}{:02x}{:02x}{:02x}{:02x}".format(
                "#" if prepend_hash else "",
                r, g, b, a
            )

    else:
        raise Exception("'element_count' must be one of: 3, 4, 6, 8.")


# Performs numpy.interp over a list of equal-size tuples.
def interp_tuple(x, xp, fp, count = 4, left = None, right = None, period = None):
    lerped = []
    for i in range(count):
        lerped.append(np.interp(x, xp, [item[i] for item in fp], left, right, period))

    return tuple(lerped)


# Activate the next group that doesn't have any windows.
def next_empty_group(qtile: Qtile):
    r = Rofi()

    current_index = qtile.groups.index(qtile.current_group)
    start_index = current_index + 1
    if start_index > 8:
        start_index = 0

    # Try to find the next empty group after the active one
    for i in range(start_index, 9):
        group = qtile.groups[i]

        if len(group.windows) <= 0:
            group.toscreen()
            return

    # If no empty groups are found after the active one, try the whole 0..N range
    for i in range(0, 9):
        group = qtile.groups[i]

        if len(group.windows) <= 0:
            group.toscreen()
            return


# Converts a string's unicode representation into unicode characters
def str_unicodify(s):
    return s.encode().decode("unicode-escape")


# Reads the Nerd Fonts data file and returns its content as class-name -> hex
def read_nf_data():
    path = f"{config_path}/assets/nf-data.csv"
    data = dict()
    with open(path, "r") as f:
        for l in f:
            line = l.split(";")
            value = line[1].strip()
            name = line[0].strip()
            data[name] = value

    return data


# Executes the `callback` function on every widget (optionally filtered) in the Qtile instance.
# callback: function(qtile, widget) -> None
# filter_callback: function(qtile, widget) -> bool
# def foreach_widget(qtile: Qtile, callback, *, filter_callback = None):
#     for name in qtile.widgets_map:
#         widget = qtile.widgets_map[name]
#         if

_notif_id = None
def toggle_debug(qtile: Qtile, notify: bool = True, timeout: int = 2500) -> None:
    if qtile.loglevel() == DEBUG:
        qtile.warning()
        state = "disabled"
    else:
        qtile.debug()
        state = "enabled"

    if notify:
        global _notif_id

        _notif_id = send_notification(
            "Logging",
            f"Debugging {state}",
            timeout=timeout,
            id_=_notif_id,
        )
def window_to_front_if_focused(qtile: Qtile):
    w = qtile.current_window
    if w.floating:
        w.bring_to_front()
