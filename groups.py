from libqtile.config import Group, Key, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.hook import subscribe
from settings import mod, terminal

# from libqtile import qtile
# from os.path import expanduser
# @subscribe.setgroup
# def group_change(*args, **kwargs):
#     filepath = expanduser("~/.local/share/qtile/qtile.log")
#     with open(filepath, "a") as f:
#         print("GROUP CHANGED {}".format(qtile.current_group.name), file=f)

# Icons:
# vlc 嗢
# movie 
# web 爵
# film strip 
# Xbox controller 調
# Music library 

group_defaults = dict(
    init = True,
    persist = True,
)

# Group definition tuples of name: str -> key: str, kwargs: dict)
group_defs = {
    "1": ("1", dict(label = "1")),
    "2": ("2", dict(label = "2")),
    "3": ("3", dict(label = "3")),
    "4": ("4", dict(label = "4")),
    "5": ("5", dict(label = "5")),
    "6": ("6", dict(label = "6")),
    "7": ("7", dict(label = "7")),
    "8": ("8", dict(label = "8")),
    "9": ("9", dict(label = "9")),
    "media": ("odiaeresis", dict(label = "")),
    "web": ("udiaeresis", dict(label = "", layout = "max")),
    "vm": ("oacute", dict(label = "", layout = "max")),
}


scratch = ScratchPad("scratchpad", [
    DropDown(
        "terminal",
        terminal,
        y=0.05,
    ),
    DropDown(
        "qtile shell",
        terminal + " -e qtile shell"
    ),
    DropDown(
        "file manager",
        "pcmanfm",
        height=0.7, width=0.7,
        y=0.05,
        on_focus_lost_hide=False
    ),
    DropDown(
        "calculator",
        "kcalc",
        height=0.5, width=0.4,
        y=0.05,
        on_focus_lost_hide=False
    ),
    DropDown(
        "volume",
        # terminal + " -e pulsemixer",
        "pavucontrol",
        height=0.5, width=0.4,
        y=0.05,
        on_focus_lost_hide=False
    ),
])

# Create groups and keybindings
def init_groups():
    groups = []
    group_keys = []
    for name in group_defs:
        g = group_defs[name]
        groups.append(
            Group(
                name,
                **(group_defaults | g[1]),
            )
        )

        # Mod + N to activate group
        group_keys.append(
            Key(
                [mod],
                g[0],
                lazy.group[name].toscreen(),
                desc = "[Group] Switch to group {}".format(name)
            )
        )
        # Mod + ctrl + N to move window to group
        group_keys.append(
            Key(
                [mod, "control"],
                g[0],
                lazy.window.togroup(name, switch_group = False),
                desc = "[Group] Move window to group {}".format(name)
            )
        )
        # Mod + shift + N to move window and activate group
        group_keys.append(
            Key(
                [mod, "shift"],
                g[0],
                lazy.window.togroup(name, switch_group = True),
                desc = "[Group] Move window and switch to group {}".format(name)
            )
        )

        # Add scratchpads
        groups.append(scratch)

    return groups, group_keys
