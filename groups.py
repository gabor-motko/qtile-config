from libqtile.config import Group, Key, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.hook import subscribe
from keys import keys, mod

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

# Group definition tuples of (name: str, key: str, kwargs: dict)
group_defs = [
    ("1", "1", dict(label = "1")),
    ("2", "2", dict(label = "2")),
    ("3", "3", dict(label = "3")),
    ("4", "4", dict(label = "4")),
    ("5", "5", dict(label = "5")),
    ("6", "6", dict(label = "6")),
    ("media", "odiaeresis", dict(label = "", layout = "max")),
    ("web", "udiaeresis", dict(label = "爵", layout = "max")),
    ("vm", "oacute", dict(label = "調", layout = "max")),
]

scratch = ScratchPad("scratchpad", [
    DropDown("terminal", "kitty", y=0.05),
    DropDown("qtile shell", "kitty --hold -e qtile shell"),
    DropDown("file manager", "pcmanfm", height=0.7, width=0.7, on_focus_lost_hide=False),
    DropDown("calculator", "kcalc", height=0.5, width=0.4, on_focus_lost_hide=False),
    DropDown("volume", "kitty -e pulsemixer", height=0.5, width=0.4, on_focus_lost_hide=False),
])

# Create groups and keybindings
groups = []

for g in group_defs:
    groups.append(
        Group(
            g[0],
            **(group_defaults | g[2]),
        )
    )

    # Mod + N to activate group
    keys.append(
        Key(
            [mod],
            g[1],
            lazy.group[g[0]].toscreen(),
            desc = "Switch to group {}".format(g[0])
        )
    )
    # Mod + ctrl + N to move window to group
    keys.append(
        Key(
            [mod, "control"],
            g[1],
            lazy.window.togroup(g[0], switch_group = False),
            desc = "Move window to group {}".format(g[0])
        )
    )
    # Mod + shift + N to move window and activate group
    keys.append(
        Key(
            [mod, "shift"],
            g[1],
            lazy.window.togroup(g[0], switch_group = True),
            desc = "Move and switch to group {}".format(g[0])
        )
    )

# Add scratchpads
groups.append(scratch)
