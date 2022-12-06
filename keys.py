from libqtile.core.manager import Qtile
from libqtile.config import Key
from libqtile.lazy import lazy
from libqtile.log_utils import logger

from popups import test_popup

mod = "mod4"
global previous_group

# From https://github.com/qtile/qtile-examples/blob/master/emdete/config.py but updated
# Move focused window to adjacent screen (by ``direction``), keep the focus on the current screen
def kick_to_next_screen(qtile, direction=1):
    other_screen_index = (qtile.screens.index(qtile.current_screen) + direction) % len(qtile.screens)
    other_group = None
    for group in qtile.cmd_groups().values():
        if group["screen"] == other_screen_index:
            other_group = group["name"]
            break

    if other_group:
        qtile.move_to_group(other_group)

previous_group = None
def toggle_media_group(qtile: Qtile):
    global previous_group
    logger.error("C: '{}' P: '{}'".format(qtile.current_group.name, previous_group))

    if qtile.current_group.name == "media":
        if previous_group is not None:
            qtile.groups_map[previous_group].cmd_toscreen()

        previous_group = None
    else:
        previous_group = qtile.current_group.name
        qtile.groups_map["media"].cmd_toscreen()

keys = [
    # Show key help
    Key([mod], "s", lazy.function(test_popup), desc="Show key bindings"),

    # Move focus
    Key([mod], "j", lazy.layout.next(), desc="Focus next window"),
    Key(["mod1"], "tab", lazy.layout.next(), desc="Focus next window"), # Alt-tab window switching
    Key([mod], "k", lazy.layout.previous(), desc="Focus previous window"),
    Key([mod], "h", lazy.prev_screen(), desc = "Focus previous screen"),
    Key([mod], "l", lazy.next_screen(), desc = "Focus next screen"),

    # Move focus by direction
    Key([mod], "left", lazy.layout.left(), desc="Focus window to the left"),
    Key([mod], "right", lazy.layout.right(), desc="Focus window to the right"),
    Key([mod], "up", lazy.layout.up(), desc="Focus window above"),
    Key([mod], "down", lazy.layout.down(), desc="Focus window below"),

    # Move focused window
    Key([mod, "control"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "control"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "control"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "control"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "control"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "control"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "control"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Move window to other screen (whichever group is active)
    Key([mod], "o", lazy.function(kick_to_next_screen), desc="Kick to next screen"),

    # Resize focused window
    Key([mod, "shift"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "shift"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    # Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "n", lazy.window.toggle_maximize(), desc="Toggle maximized window"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating window"),
    Key([mod], "m", lazy.window.toggle_fullscreen(), desc="Toggle full-screen window"),
    Key([mod, "shift"], "m", lazy.window.toggle_fullscreen(), desc="Toggle full-screen window"),

    # Toggle between split and unsplit sides of stack. Split = all windows displayed. Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes.
    Key([mod, "control"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Toggle between layouts
    Key([mod], "space", lazy.next_layout(), desc="Next layout"),
    Key([mod, "shift"], "space", lazy.previous_layout(), desc="Previous layout"),

    # Kill window
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    # Reload config
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the QTile config"), # Default keybinding
    Key([mod], "q", lazy.reload_config(), desc="Reload the QTile config"),

    # Exit QTile
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Exit QTile"),

    # Launch programs
    Key([mod, "shift"], "Return", lazy.spawn("kitty"), desc="Launch terminal (the awesome way)"),
    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "r", lazy.spawn("dmenu_run"), desc="Open dmenu"),
    Key([mod], "p", lazy.spawn("rofi -show run"), desc="Rofi"),
    Key([mod, "control"], "p", lazy.spawn("rofi -show drun"), desc="Rofi (apps)"),


    # Media controls
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), lazy.spawn("playsound '/usr/share/sounds/freedesktop/stereo/audio-volume-change.oga'"), desc="Lower volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), lazy.spawn("playsound '/usr/share/sounds/freedesktop/stereo/audio-volume-change.oga'"), desc="Raise volume"),
    Key([mod], "XF86AudioLowerVolume", desc="Lower volume of focused application"),
    Key([mod], "XF86AudioRaiseVolume", desc="Raise volume of focused application"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute audio"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/pause media"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next media"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous media"),
    Key(["control"], "XF86AudioNext", lazy.spawn("playerctl position 10+"), desc="Forward 10s"),
    Key(["control"], "XF86AudioPrev", lazy.spawn("playerctl position 10-"), desc="Back 10s"),
    Key([], "XF86Tools", lazy.function(toggle_media_group), desc="Switch to media player"),
    #Key([], "XF86Explorer"),
    #Key([], "XF86Favorites"),
    #Key([], "XF86Search"),
    #Key([], "XF86Reload"),
    #Key([], "XF86Mail"),
    #Key([], "XF86HomePage"),
    Key([], "XF86Calculator", lazy.spawn("kcalc"), desc="Launch calculator"),

    # Scratchpads
    Key([mod], "F11", lazy.group["scratchpad"].dropdown_toggle("terminal")),
    Key([mod], "backspace", lazy.group["scratchpad"].dropdown_toggle("terminal")),
    Key([mod], "F12", lazy.group["scratchpad"].dropdown_toggle("qtile shell")),
    Key([mod], "F10", lazy.group["scratchpad"].dropdown_toggle("file manager")),
]

