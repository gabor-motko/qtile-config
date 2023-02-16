from libqtile import widget as widget_base
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration, PowerLineDecoration

from theme import theme as tm
from custom.color.SolarizedDark import *

from settings import groupbox_start_hide_unused, config_path, group_count
from custom.widgets import NvidiaSensors2, OpenWeather2, GroupBoxFn, BoxStyle, WindowIndex, WindowState
from custom.popups import weather_popup
from utils import interp_tuple, color_float_to_hex, next_empty_group, window_to_front_if_focused

font_mono = "mononoki Nerd Font Mono"
font_mono_bold = "mononoki Nerd Font Mono Bold"
colorGray = "#cecece"

def colortest():
    return [
        widget.TextBox(text = "01", foreground = colorFore, background = color01),
        widget.TextBox(text = "02", foreground = colorFore, background = color02),
        widget.TextBox(text = "03", foreground = colorFore, background = color03),
        widget.TextBox(text = "04", foreground = colorFore, background = color04),
        widget.TextBox(text = "05", foreground = colorFore, background = color05),
        widget.TextBox(text = "06", foreground = colorFore, background = color06),
        widget.TextBox(text = "07", foreground = colorFore, background = color07),
        widget.TextBox(text = "08", foreground = colorFore, background = color08),
        widget.TextBox(text = "09", foreground = colorFore, background = color09),
        widget.TextBox(text = "10", foreground = colorFore, background = color10),
        widget.TextBox(text = "11", foreground = colorFore, background = color11),
        widget.TextBox(text = "12", foreground = colorFore, background = color12),
        widget.TextBox(text = "13", foreground = colorFore, background = color13),
        widget.TextBox(text = "14", foreground = colorFore, background = color14),
        widget.TextBox(text = "15", foreground = colorFore, background = color15),
        widget.TextBox(text = "16", foreground = colorFore, background = color16),
    ]

# {{{ Helper functions
from rofi import Rofi
def status(s):
    r = Rofi()
    r.status(str(s))


def groupbox_toggle_hide_unused(qtile: Qtile):
    # Enumerate all widgets
    for name in qtile.widgets_map:
        w: widget_base.groupbox.GroupBox = qtile.widgets_map[name]
        # If the widget is a GroupBox and toggling is enabled (custom attribute)...
        if isinstance(w, widget.GroupBox) and w.toggle_hide_unused_enable:
            w.hide_unused = not w.hide_unused
            # Redrawing the widget updates only the widget itself
            w.draw()

            # Redraw all bars to update their layout
            for screen in qtile.screens:
                if screen.top: screen.top.draw()
                if screen.bottom: screen.bottom.draw()
                if screen.left: screen.left.draw()
                if screen.right: screen.right.draw()


def group_label_transform(group, has_windows, active, current):
    label = group.label
    if active:
        return f"[{label}]"
    else:
        return f" {label} "


def volume_widgets_update(qtile: Qtile, delta):
    volume_changed = False
    for name in qtile.widgets_map:
        w = qtile.widgets_map[name]
        if isinstance(w, widget.Volume):
            if not volume_changed:
                if delta < 0:
                    w.decrease_vol()
                elif delta > 0:
                    w.increase_vol()
            w.update()

# }}}


# {{{ Style

# Symbol icons used by the OpenWeatherMap widget
# Requires some Nerd Font flavour.
openweather_symbols = {
    "Unknown": "",
    # Day
    "01d": "", # Clear
    "02d": "", # Few clouds
    "03d": "", # Scattered clouds
    "04d": "", # Broken clouds
    "09d": "", # Shower
    "10d": "", # Rain
    "11d": "", # Thunder
    "13d": "", # Snow
    "50d": "", # Mist
    # Night
    "01n": "",
    "02n": "",
    "03n": "",
    "04n": "",
    "09n": "",
    "10n": "",
    "11n": "",
    "13n": "",
    "50n": "",
}

def decorate_rect(**config):
    return [
        RectDecoration(
            **(dict(
                colour = tm.bg_translucent,
                radius = 8,
                line_width = 1,
                line_colour = tm.fg_inactive,
                filled = True,
                group = True,
                clip = True,
            ) | config)
        )
    ]


def decorate(**config):
    return [
        BorderDecoration(
            **(dict(
                border_width = [0, 0, 2, 0],
                extrawidth = 0,
                group = True,
                padding = 0,
            ) | config)
        )
    ]

decorate_default = decorate(colour = "#ffffff")


# Return a separator or spacer widget
def sep(width = 4):
    # return widget.Sep(linewidth = 2)
    return widget.Spacer(length = width)


# Default settings for all widgets
widget_defaults = dict(
    font = "DejaVu Sans Mono Nerd Font",
    fontsize = 12,
    padding = 3,
    foreground = "#268bd2",
    inactive = tm.fg_inactive,
    active = tm.fg_active,
    rounded = False,
)


# Default settings for system monitor widgets
monitor_defaults = widget_defaults | dict(
    fontsize = 14,
    padding = 4,
    foreground = colorGray,
    colour = color15,
)


# Default for group box widgets
groupbox_defaults = dict(
    highlight_method = "text",
    font = "DejaVu Sans Mono Nerd Font",
    fontsize = 14,
    urgent_alert_method = "block",
    urgent_border = tm.bg_urgent,
    center_aligned = False,
    margin = 0,
    padding_x = -4,
    disable_drag = True,
    inactive = "#268bd2",
    active =   "#d33682",
    markup = True,
    this_current_screen_border = "#d33682",
)

# }}}


# {{{ Weather widget data


weather_data = None
weather_callback_configured = False

def weather_set_data(data):
    global weather_data
    weather_data = data

def weather_popup_show(qtile):
    global weather_data
    weather_popup(qtile, weather_data)

# }}}

# {{{ Initialize widgets
# Initialize right side resource monitor and datetime widgets.
def init_monitors(si = 0):
    # Initialize each widget individually
    s = widget.Sep(foreground = colorGray, padding = 12, size_percent = 60, linewidth = 1)

    cpu_icon = widget.Image(
        filename = "~/.config/qtile/assets/cpu.svg",
        mask = True,
        margin_y = 6,
        decorations = decorate(colour = color02),
        name = f"cpu_icon_{si}",
        **(monitor_defaults),
    )

    cpu_widget =  widget.CPU(
        format = "{load_percent:.0f}%",
        decorations = decorate(colour = color02),
        mouse_callbacks = {
            "Button1": lazy.spawn("kitty -e htop"),
            "Button3": lazy.spawn("kitty -e bpytop"),
        },
        name = f"cpu_{si}",
        **(monitor_defaults),
    )

    memory_icon = widget.Image(
        filename = "~/.config/qtile/assets/memory.svg",
        mask = True,
        margin_y = 6,
        decorations = decorate(colour = color03),
        name = f"memory_icon_{si}",
        **(monitor_defaults),
    )

    memory_widget_outside = widget.Memory(
        format = "{MemPercent:.0f}%",
        decorations = decorate(colour = color03),
        mouse_callbacks = {
            # "Button1": lazy.widget["widgetbox_memory"].toggle(),
        },
        name = f"memory_{si}",
        **(monitor_defaults),
    )

    gpu_icon = widget.Image(
        filename = "~/.config/qtile/assets/gpu.svg",
        mask = True,
        margin_y = 6,
        decorations = decorate(colour = color05),
        name = f"gpu_icon_{si}",
        **(monitor_defaults),
    )

    gpu_widget = widget.modify(
        NvidiaSensors2,
        format = "{utilization_gpu}% {temperature_gpu}°C",
        format_alert = "<span color='#ffe000'>{utilization_gpu: >2}% {temperature_gpu: >2}°C</span>",
        sensors = ["utilization.gpu", "temperature.gpu", "fan.speed"],
        threshold = 70,
        decorations = decorate(colour = color05),
        name = f"gpu_{si}",
        **monitor_defaults,
        initialise=True
    )

    # mpris_widget = widget.Mpris2(
    #     format = "{xesam:title} - {xesam:artist})",
    #     playing_text = " 契 {track}",
    #     paused_text  = "  {track}",
    #     width = 200,
    #     foreground = gradient[3],
    #     decorations = decorate_default,
    #     scroll_delay = 5,
    #     scroll_interval = 0.25,
    #     scroll_step = 15,
    #     name = f"mpris_{si}",
    #     **(monitor_defaults),
    # )

    volume_widget = widget.Volume(
        fmt = "<big>墳</big> {}",
        decorations = decorate(colour = color07),
        update_interval = 0.5,
        mouse_callbacks = {
            "Button1": lazy.spawn("pavucontrol"),
            # "Button4": lazy.function(volume_widgets_update, 1),
            # "Button5": lazy.function(volume_widgets_update, -1),
        },
        name = f"volume_{si}",
        **monitor_defaults,
    )

    weather_widget = OpenWeather2(
        format = "{main_temp:.0f}°{units_temperature} {icon} ",
        app_key = "0521d207c853c983abea0b3358f1dfeb",
        cityid = "721472",
        weather_symbols = openweather_symbols,
        mouse_callbacks = {
            "Button1": lazy.spawn("xdg-open 'https://koponyeg.hu/elorejelzes/Debrecen'"),
            "Button3": lazy.function(weather_popup_show),
        },
        callback = None if weather_callback_configured else lambda o, d: weather_set_data(d),
        name = f"weather_{si}",
        **monitor_defaults
    )

    clock_date = widget.Clock(
        format="%b %d %a",
        fmt = "<span rise='0pt'>{}</span>",
        name = f"clock_date_{si}",
        **(monitor_defaults | dict(
            font = font_mono,
            fontsize = 12
        ))
    )

    clock_time = widget.Clock(
        format="%H:%M",
        fmt = "<span rise='6pt'>{}</span>",
        name = f"clock_time_{si}",
        **(monitor_defaults | dict(
            font = font_mono,
            fontsize = 18,
            foreground = color03,
        ))
    )

    # Assemble widgets in the correct order and as needed
    all_widgets = [
        cpu_icon,
        cpu_widget,
        s,
        memory_icon,
        memory_widget_outside,
        s,
        gpu_icon,
        gpu_widget,
        s,
        # mpris_widget,
        volume_widget,
        s,
        weather_widget,
        clock_date,
        clock_time
    ]

    return all_widgets


# Initialize widgets on the left side that deal with layouts and groups.
def init_workspace_widgets(sp = 0):

    current_screen_icon = widget.CurrentScreen(
        active_text = "",
        inactive_text = "",
        active_color = color06,
        inactive_color = color05,
        mouse_callbacks = {
            "Button1": lazy.spawn("rofi -show drun"),
        },
        name = f"current_screen_icon_{sp}",
        **(widget_defaults | dict(
            padding = 7,
            fontsize = 16
            )
        )
    )

    chord = widget.Chord(
        chords_colors = {
            "file explorer": (color02, color04),
        },
        name_transform = lambda name: name.upper(),
        name = f"chord_{sp}",
        **(widget_defaults),
    )

    layout_icon = widget.CurrentLayoutIcon(
        scale = 0.6,
        use_mask = True,
        custom_icon_paths = [config_path + "/assets/layouticons"],
        name = f"layout_icon_{sp}",
        **(widget_defaults)
    )

    groupbox_number = GroupBoxFn(
        visible_groups = [str(i + 1) for i in range(group_count)],
        hide_unused = groupbox_start_hide_unused,
        toggle_hide_unused_enable = True, # Custom attribute used by `groupbox_toggle_hide_unused`
        transform_label = group_label_transform,
        #normal_style = BoxStyle(text_color = "#ffff00"),
        #active_any_screen_style = BoxStyle(line_active = True, line_color = "#00ff00"),
        name = f"group_box_a_{sp}",
        **groupbox_defaults,
    )

    groupbox_special = GroupBoxFn(
        visible_groups = ["media", "web", "vm"],
        hide_unused = False,
        toggle_hide_unused_enable = False, # Custom attribute used by `groupbox_toggle_hide_unused`
        transform_label = group_label_transform,
        #normal_style = BoxStyle(text_color = "#ffff00"),
        #active_any_screen_style = BoxStyle(block_active = True, block_color = "#00ff00"),
        name = f"group_box_b_{sp}",
        **groupbox_defaults
    )


    return [
        chord,
        current_screen_icon,
        layout_icon,
        groupbox_number,
        groupbox_special,
    ]



# Initialize central/flex widgets that display window details.
def init_window_widgets(sp = 0):
    window_state = WindowState(
        txt_normal    = "[ﱖ]",
        txt_floating  = "[缾]",
        txt_maximized = "[类]",
        txt_minimized = "[絛]",
        name = f"window_state_{sp}",
        **(widget_defaults | dict(
            font_size = 12,
            font = font_mono,
            foreground = colorGray
            )
        )
    )

    window_index = WindowIndex(
        font = font_mono_bold,
        name = f"window_index_{sp}",
    )

    window_name = widget.WindowName(
        format = "[ {name} ]",
        mouse_callbacks = {
            "Button1": lazy.window.toggle_minimize(),
            "Button2": lazy.function(window_to_front_if_focused),
            "Button4": lazy.group.prev_window(),
            "Button5": lazy.group.next_window(),
        },
        name = f"window_name_{sp}",
        **(widget_defaults | dict(
            foreground = colorGray
            )
        )
    )

    return [
        window_state,
        window_index,
        window_name,
    ]


# Initialize the bar widgets
def init_widgets(screen_index = -1):
    widgets = []
    widgets.extend(init_workspace_widgets())
    widgets.extend(init_window_widgets())
    widgets.extend(init_monitors(screen_index))
    return widgets

# }}}
