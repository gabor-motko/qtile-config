from libqtile import widget as widget_base
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration, PowerLineDecoration

from theme import theme as tm
from settings import groupbox_start_hide_unused
from custom.widgets import NvidiaSensors2, OpenWeather2
from custom.popups import weather_popup
from utils import interp_tuple, color_float_to_hex, next_empty_group


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

# Add decorations to system monitor widgets
def decorate_border(**config):
    return [
        BorderDecoration(
            **(dict(border_width = (0, 0, 3, 0)) | config)
        ),
    ]


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


def decorate(**kwargs):
    return decorate_rect(**kwargs)


decorate_default = [
    RectDecoration(
        colour = tm.bg_translucent,
        radius = 8,
        line_width = 1,
        line_colour = tm.fg_inactive,
        filled = True,
        group = True,
        clip = True,
    )
]


# Return a separator or spacer widget
def sep(width = 4):
    # return widget.Sep(linewidth = 2)
    return widget.Spacer(length = width)


# Default settings for all widgets
widget_defaults = dict(
    font = tm.font_mono,
    fontsize = 12,
    padding = 3,
    inactive = tm.fg_inactive,
    active = tm.fg_active,
    rounded = False,
)


# Default settings for system monitor widgets
monitor_defaults = widget_defaults | dict(
    fontsize = 14,
    padding = 4,
)


# Default for group box widgets
groupbox_defaults = widget_defaults | dict(
    highlight_method = "line",
    fontsize = 16,
    borderwidth = 3,
    highlight_color = tm.bg,
    other_current_screen_border = tm.fg_inactive_dim,    # screen unfocused, group unfocused
    this_screen_border = tm.fg_active_dim,             # screen unfocused, group focused
    this_current_screen_border = tm.fg_active,  # screen focused, group focused
    other_screen_border = tm.fg_inactive,       # screen focused, group unfocused
    urgent_alert_method = "block",
    urgent_border = tm.bg_urgent,
    center_aligned = False,
    margin_y = 2,
    disable_drag = True,
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
# Initialize the system monitor widgets
def init_monitors(systray = True):
    # Initialize each widget
    s = sep()

    # gradient = tm.gradient
    # gradient = [color_float_to_hex(interp_tuple(x / 6, [0, 1], [(1, 0.4, 0.1, 1), (1, 1, 0.3, 1)])) for x in range(8)]
    gradient = [tm.fg_neutral] * 8


    cpu_icon = widget.Image(
        filename = "~/.config/qtile/assets/cpu.svg",
        colour = gradient[0],
        mask = True,
        margin_y = 6,
        decorations = decorate_default,
        **(monitor_defaults),
    )

    cpu_widget =  widget.CPU(
        format = "{load_percent:.0f}%",
        decorations = decorate_default,
        foreground = gradient[0],
        mouse_callbacks = {
            "Button1": lazy.spawn("kitty -e htop"),
            "Button3": lazy.spawn("kitty -e bpytop"),
        },
        **(monitor_defaults),
    )

    memory_icon = widget.Image(
        filename = "~/.config/qtile/assets/memory.svg",
        colour = gradient[1],
        mask = True,
        margin_y = 6,
        decorations = decorate_default,
        **(monitor_defaults),
    )

    memory_widget_outside = widget.Memory(
        format = "{MemPercent:.0f}%",
        decorations = decorate_default,
        mouse_callbacks = {
            # "Button1": lazy.widget["widgetbox_memory"].toggle(),
        },
        foreground = gradient[1],
        **(monitor_defaults),
    )

    gpu_icon = widget.Image(
        filename = "~/.config/qtile/assets/gpu.svg",
        colour = gradient[2],
        mask = True,
        margin_y = 6,
        decorations = decorate_default,
        **(monitor_defaults),
    )

    gpu_widget = widget.modify(
        NvidiaSensors2,
        format = "{utilization_gpu}% {temperature_gpu}°C",
        format_alert = "<span color='#ffe000'>{utilization_gpu: >2}% {temperature_gpu: >2}°C</span>",
        sensors = ["utilization.gpu", "temperature.gpu", "fan.speed"],
        threshold = 70,
        decorations = decorate_default,
        foreground = gradient[2],
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
    #     **(monitor_defaults),
    # )

    volume_widget = widget.Volume(
        fmt = "<big>墳</big> {}",
        decorations = decorate_default,
        mouse_callbacks = {
            "Button1": lazy.spawn("pavucontrol"),
        },
        foreground = gradient[3],
        **monitor_defaults,
    )

    weather_widget = OpenWeather2(
        format = "{main_temp:.0f}°{units_temperature} {icon} ",
        app_key = "0521d207c853c983abea0b3358f1dfeb",
        cityid = "721472",
        decorations = decorate_default,
        weather_symbols = openweather_symbols,
        mouse_callbacks = {
            "Button1": lazy.spawn("xdg-open 'https://koponyeg.hu/elorejelzes/Debrecen'"),
            "Button3": lazy.function(weather_popup_show),
        },
        foreground = gradient[4],
        callback = None if weather_callback_configured else lambda o, d: weather_set_data(d),
        **monitor_defaults
    )

    clock_date = widget.Clock(
        format="%b %d %a",
        fmt = "<span rise='0pt'>{}</span>",
        decorations = decorate_default,
        foreground = gradient[5],
        **(monitor_defaults | dict(
            font = tm.font_mono,
            fontsize = 12
        ))
    )

    clock_time = widget.Clock(
        format="%H:%M",
        fmt = "<span rise='6pt'>{}</span>",
        decorations = decorate_default,
        **(monitor_defaults | dict(
            font = tm.font_mono_bold,
            fontsize = 20
        ))
    )

    # Assemble widgets in the correct order
    all_widgets = [
        cpu_icon,
        cpu_widget,
        memory_icon,
        memory_widget_outside,
        gpu_icon,
        gpu_widget,
        s,
        # mpris_widget,
        volume_widget,
    ]

    if systray:
        all_widgets.extend(
            [
                widget.StatusNotifier(
                    decorations = decorate_default,
                ),
            ]
        )

    all_widgets.extend([
        s,
        weather_widget,
        clock_date,
        clock_time
    ])

    return all_widgets


# Initialize left side widgets (common to both screens)
def init_left_widgets():
    return [
        widget.CurrentScreen(
            active_text = "",
            inactive_text = "",
            active_color = tm.fg_active,
            inactive_color = tm.fg_inactive_dim,
            decorations = decorate_default,
            mouse_callbacks = {
                "Button1": lazy.spawn("rofi -show drun"),
            },
            **(widget_defaults | dict(
                padding = 7,
                fontsize = 16
            ))
        ),
        widget.Chord(
            chords_colors = {
                "file explorer": (tm.bg_urgent, tm.fg_active),
            },
            decorations = decorate_default,
            name_transform = lambda name: name.upper(),
            **(widget_defaults),
        ),
        widget.CurrentLayoutIcon(
            scale = 0.6,
            use_mask = True,
            foreground = tm.fg_active,
            decorations = decorate_default,
            **(widget_defaults)
        ),
        widget.GroupBox(
            visible_groups = [str(i + 1) for i in range(9)],
            hide_unused = groupbox_start_hide_unused,
            decorations = decorate_default,
            toggle_hide_unused_enable = True, # Custom attribute used by `groupbox_toggle_hide_unused`
            **groupbox_defaults,
        ),
        widget.CurrentScreen(
            active_text = "+",
            inactive_text = "+",
            active_color = tm.fg_active,
            inactive_color = tm.fg_inactive,
            mouse_callbacks = {
                "Button1": lazy.function(groupbox_toggle_hide_unused),
                "Button3": lazy.function(next_empty_group),
            },
            decorations = decorate_default,
            **(widget_defaults | dict(
                fontsize = 16
            ))
        ),
        sep(),
        widget.Spacer(length = 8,decorations = decorate_default),
        widget.GroupBox(
            visible_groups = ["media", "web", "vm"],
            decorations = decorate_default,
            hide_unused = False,
            toggle_hide_unused_enable = False, # Custom attribute used by `groupbox_toggle_hide_unused`
            **(groupbox_defaults | dict(
                font = "Symbols Nerd Font",
                fontsize = 18
            )),
        ),
        widget.Spacer(length = 8,decorations = decorate_default),
    ]


# Initialize the bar widgets
def init_widgets(*, use_systray = False, screen_index = -1):
    global current_color_index
    current_color_index = 0

    widgets = [
        # Left
        *(init_left_widgets()),
        sep(),

        # Flex
        widget.TaskList(
            # TODO: test 'pyxdg' themed icons
            max_title_width = 200,
            highlight_method = "block",
            unfocused_border = tm.bg_translucent,
            border = tm.fg_inactive_dim,
            txt_floating  = "缾 ",
            txt_maximized = "类 ",
            txt_minimized = "絛 ",
            **(widget_defaults | dict(
                rounded = True,
                font = tm.font
            )),
        ),
        sep(),

        # Right
        *(init_monitors(systray = True))
    ]

    return widgets


# }}}
