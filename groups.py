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

# Group definition dicts
group_defs = [
    dict(name = "1", key = "1", label = "1"),
    dict(name = "2", key = "2", label = "2"),
    dict(name = "3", key = "3", label = "3"),
    dict(name = "4", key = "4", label = "4"),
    dict(name = "5", key = "5", label = "5"),
    dict(name = "6", key = "6", label = "6"),
    dict(name = "media", key = "odiaeresis", label = ""),
    dict(name = "web", key = "udiaeresis", label = "爵"),
    dict(name = "vm", key = "oacute", label = "調"),
]

scratch = ScratchPad("scratchpad", [
    DropDown("terminal", "kitty", y=0.05),
    DropDown("qtile shell", "kitty --hold -e qtile shell"),
    DropDown("file manager", "dolphin", height=0.7, width=0.7),
])

# Create groups and keybindings
groups = []

for g in group_defs:
    groups.append(
        Group(
            g["name"],
            label = g["label"],
            init = True,
            persist = True
        )
    )

    # Mod + N to activate group
    keys.append(
        Key(
            [mod],
            g["key"],
            lazy.group[g["name"]].toscreen(),
            desc = "Switch to group {}".format(g["label"])
        )
    )
    # Mod + shift + N to move window and activate group
    keys.append(
        Key(
            [mod, "shift"],
            g["key"],
            lazy.window.togroup(g["name"], switch_group = True),
            desc = "Switch to group {}".format(g["label"])
        )
    )

# Add scratchpads
groups.append(scratch)
