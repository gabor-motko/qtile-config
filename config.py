from libqtile import bar, layout, widget, hook
from libqtile.config import Match
from libqtile.lazy import lazy

# Keys and mouse
from keys import init_keys, init_mouse
keys = init_keys()
mouse = init_mouse()

# Groups and group-related keys
from groups import init_groups
groups, group_keys = init_groups()
keys.extend(group_keys)

# Layouts
from layouts import init_layouts
layouts = init_layouts()

# Widget settings, this might be necessary for initializing
# widgets without manually passing **widget_defaults
# to the constructor. Must be defined before init_screens() is called.
# from widgets import widget_defaults as extension_defaults

# Screens, bars, widgets
from screens import init_screens
screens = init_screens()

# Independent hooks
from hooks import init_hooks
init_hooks()

# {{{ The Area of Fuckery
# def test_function(qtile: Qtile):
#     pass

# from libqtile.config import Key
# keys.append(
#     Key(["mod4"], "z", lazy.function(test_function), desc="[Core] Generic test function for whatever")
# )

# }}}

# General WM settings
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# Something to trick Java? dunno
wmname = "LG3D"
