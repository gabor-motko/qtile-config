from libqtile.config import Group, Key, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.hook import subscribe
from settings import mod, terminal, group_count
from custom.popups.group_name import group_name_popup # NOTE: workaround, should use changegroup hook instead, but it is fucked.


def show_group_name_popup(qtile, *args):
    group_name_popup(qtile, *args)

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
# fancy shit    

group_defaults = dict(
    init = True,
    persist = True,
)


# Group definition tuples of name: str -> key: str, kwargs: dict)
group_defs = dict()
for i in range(group_count):
    n = str(i + 1)
    group_defs[n] = (n, {"label": n})

group_defs.update({
    "media": ("odiaeresis", dict(label = "media")),
    "web": ("udiaeresis", dict(label = "web", layout = "max")),
    "vm": ("oacute", dict(label = "game", layout = "max")),
})

dropdown_defaults = dict(
    y = 0.05,
    height = 0.7,
    width = 0.7,
)

dropdown_defs = {
    "terminal":         (terminal, ["F12", "backspace"]),
    "qtile shell":      (terminal + " -e qtile shell", "F11"),
    "pcmanfm":          ("pcmanfm", "F10", dict(on_focus_lost_hide = False)),
    "pavucontrol":      ("pavucontrol", "XF86AudioRaiseVolume"),

}


scratch = ScratchPad("scratchpad", [
    DropDown(
        "terminal",
        terminal,
        y=0.05,
    ),
    DropDown(
        "qtile shell",
        terminal + " -e qtile shell",
        y=0.05,
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

# Create groups and keybindings. Returns (groups: list[Group], keys: list[Key])
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
                lazy.function(show_group_name_popup),
                desc = "[Group] Switch to group {}".format(name)
            )
        )
        # Mod + ctrl + N to move window to group
        group_keys.append(
            Key(
                [mod, "control"],
                g[0],
                lazy.window.togroup(name, switch_group = False),
                lazy.function(show_group_name_popup, "Yeet to group"),
                desc = "[Group] Move window to group {}".format(name)
            )
        )
        # Mod + shift + N to move window and activate group
        group_keys.append(
            Key(
                [mod, "shift"],
                g[0],
                lazy.window.togroup(name, switch_group = True),
                lazy.function(show_group_name_popup, "Yoink to group"),
                desc = "[Group] Move window and switch to group {}".format(name)
            )
        )

        # Add scratchpads
        groups.append(scratch)

    return groups, group_keys
