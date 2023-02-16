from libqtile.core.manager import Qtile
from libqtile.config import Key, KeyChord, Click, Drag
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from settings import mod, terminal
from custom.rofi import main_menu, rename_group_menu, set_audio_sink_menu

# Move focused window to the adjacent screen
def kick_to_next_screen(qtile, direction = 1):
    other_index = (qtile.screens.index(qtile.current_screen) + direction) % len(qtile.screens)
    qtile.current_window.toscreen(other_index)

def launch_media_app(qtile):
    pass

def show_keys_popup(qtile):
    qtile.spawn("kitty --hold -e ~/.config/qtile/tools/qtile-keys", shell=True)


def init_keys():
    keys = [
        # Show key help
        Key([mod], "s", lazy.function(show_keys_popup), desc="[Core] Show key bindings"),

        # Move focus
        Key([mod], "j", lazy.group.next_window(), desc="[Layout] Focus next window"),
        Key(["mod1"], "tab", lazy.layout.next(), desc="[Layout] Focus next window"), # Alt-tab window switching
        Key([mod], "tab", lazy.spawn("rofi -show window"), desc="[Layout] Switch windows"),
        Key([mod], "k", lazy.group.prev_window(), desc="[Layout] Focus previous window"),
        Key([mod], "h", lazy.prev_screen(), desc = "[Screen] Focus previous screen"),
        Key([mod], "l", lazy.next_screen(), desc = "[Screen] Focus next screen"),

        # Move focus by direction
        Key([mod], "left", lazy.layout.left(), desc="[Layout] Focus window to the left"),
        Key([mod], "right", lazy.layout.right(), desc="[Layout] Focus window to the right"),
        Key([mod], "up", lazy.layout.up(), desc="[Layout] Focus window above"),
        Key([mod], "down", lazy.layout.down(), desc="[Layout] Focus window below"),

        # Move focused window
        Key([mod, "control"], "j", lazy.layout.shuffle_down(), desc="[Layout] Move window down"),
        Key([mod, "control"], "k", lazy.layout.shuffle_up(), desc="[Layout] Move window up"),
        Key([mod, "control"], "h", lazy.layout.decrease_nmaster()),
        Key([mod, "control"], "l", lazy.layout.increase_nmaster()),

        # Move window to other screen (whichever group is active)
        Key([mod], "o", lazy.function(kick_to_next_screen), desc="[Screen] Kick to next screen"),
        Key([mod], "i", lazy.layout.promote_or_demote()),
        Key([mod, "mod1"], "i", lazy.layout.reposition_master(target = "rotate")),

        # Resize focused window
        Key([mod, "shift"], "h", lazy.layout.decrease_ratio(), desc="[Layout] Grow window to the left"),
        Key([mod, "shift"], "l", lazy.layout.increase_ratio(), desc="[Layout] Grow window to the right"),

        Key([mod], "n", lazy.window.toggle_maximize(), desc="[Window] Toggle maximized window"),
        Key([mod], "b", lazy.window.toggle_floating(), desc="[Window] Toggle floating window"),
        Key([mod], "m", lazy.window.toggle_fullscreen(), desc="[Window] Toggle full-screen window"),

        Key([mod], "prior", lazy.window.toggle_maximize(), desc="[Window] Toggle maximized window"),
        Key([mod], "next", lazy.window.toggle_minimize(), desc="[Window] Toggle full-screen window"),

        # Toggle between layouts
        Key([mod], "space", lazy.next_layout(), desc="[Core] Next layout"),
        Key([mod, "shift"], "space", lazy.previous_layout(), desc="[Core] Previous layout"),

        # Kill window
        Key([mod], "w", lazy.window.kill(), desc="[Window] Kill focused window"),
        Key([mod, "shift"], "c", lazy.window.kill(), desc="[Window] Kill focused window"),

        # Reload config
        Key([mod, "control"], "r", lazy.reload_config(), desc="[Core] Reload the QTile config"), # Default keybinding
        Key([mod], "q", lazy.reload_config(), desc="[Core] Reload the QTile config"),

        # Exit QTile
        Key([mod, "shift"], "q", lazy.shutdown(), desc="[Core] Exit QTile"),

        # Lock session
        Key([mod], "escape", lazy.spawn("physlock"), desc="[Core] Lock session"),

        # Launch programs
        Key([mod], "Return", lazy.spawn(terminal), desc="[App] Launch terminal"),
        Key([mod], "r", lazy.spawn("dmenu_run"), desc="[App] Open dmenu"),
        Key([mod], "p", lazy.spawn("rofi -show drun"), desc="[App] Rofi drun"),
        Key([mod, "control"], "p", lazy.spawn("rofi -show run"), desc="[App] Rofi run"),

        # Media controls
        Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), lazy.spawn("play '/usr/share/sounds/freedesktop/stereo/audio-volume-change.oga'"), desc="[Media] Lower volume"),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), lazy.spawn("play '/usr/share/sounds/freedesktop/stereo/audio-volume-change.oga'"), desc="[Media] Raise volume"),
        Key([mod], "XF86AudioLowerVolume", desc="[Media] Lower volume of focused application"), # TODO
        Key([mod], "XF86AudioRaiseVolume", desc="[Media] Raise volume of focused application"), # TODO
        Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="[Media] Mute audio"),
        Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="[Media] Play/pause media"),
        Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="[Media] Next media"),
        Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="[Media] Previous media"),
        Key(["control"], "XF86AudioNext", lazy.spawn("playerctl position 10+"), desc="[Media] Forward 10s"),
        Key(["control"], "XF86AudioPrev", lazy.spawn("playerctl position 10-"), desc="[Media] Back 10s"),
        Key([], "XF86Tools", lazy.group["media"].toscreen(toggle=True), desc="[Media] Switch to media group"),
        Key([mod], "XF86Tools", lazy.group["media"].toscreen(toggle=True), desc="[Media] Launch media player"),
        #Key([], "XF86Explorer"),
        #Key([], "XF86Favorites"),
        #Key([], "XF86Search"),
        #Key([], "XF86Reload"),
        #Key([], "XF86Mail"),
        #Key([], "XF86HomePage"),
        Key([], "XF86Calculator", lazy.spawn("kcalc"), desc="[App] Launch calculator"),

        # Scratchpads
        Key([mod], "F11", lazy.group["scratchpad"].dropdown_toggle("terminal"), desc="[Scratchpad] Terminal"),
        Key([mod], "backspace", lazy.group["scratchpad"].dropdown_toggle("terminal"), desc="[Scratchpad] Terminal"),
        Key([mod], "F12", lazy.group["scratchpad"].dropdown_toggle("qtile shell"), desc="[Scratchpad] Qtile Shell"),
        Key([mod], "F10", lazy.group["scratchpad"].dropdown_toggle("file manager"), desc="[Scratchpad] File manager"),
        Key([mod], "F9", lazy.group["scratchpad"].dropdown_toggle("calculator"), desc="[Scratchpad] Calculator"),
        Key([mod, "control"], "XF86AudioMute", lazy.group["scratchpad"].dropdown_toggle("volume"), desc="[Scratchpad] Volume"),
    ]

    keys.extend([
        KeyChord(
            [mod], "f",
            [
                Key([], "d", lazy.spawn("dolphin")),
                Key([], "p", lazy.spawn("pcmanfm")),
            ],
            name = "file explorer",
            desc = "[App] File explorer...",
        )
    ])

    keys.extend([
        Key([mod], "t", lazy.function(main_menu), desc="[App] Main menu"),
        # Key([mod], "g", lazy.function(show_keys_popup), desc="[App] Main menu"),
        Key([mod], "z", lazy.function(rename_group_menu), desc="[Group] Rename group"),
        Key([mod], "XF86AudioMute", lazy.function(set_audio_sink_menu), desc="[Scratchpad] Volume"),
    ])


    return keys


def init_mouse():
    mouse = [
        Drag([mod], "Button1",
             lazy.window.set_position_floating(),
             start=lazy.window.get_position()
             ),

        Drag([mod], "Button3",
             lazy.window.set_size_floating(),
             start=lazy.window.get_size()
             ),

        Click([mod], "Button2",
              lazy.window.bring_to_front()
              ),
    ]

    return mouse
