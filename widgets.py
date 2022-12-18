from libqtile import widget as widget_base
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration, PowerLineDecoration
from theme import theme as tm

from widgets_custom import NvidiaSensors2

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

# The system monitor widgets use border colors in sequence - this variable
# stores the index of the color to be used when instantiating the widget.
global current_color_index
current_color_index = 0

# Add decorations to system monitor widgets
def decorate_border(color_index = None, *, progress = True):
    global current_color_index
    border_color = "#000000"
    if color_index is not None:
        border_color = tm.widget_border[color_index]
    elif progress:
        current_color_index += 1
    border_color = tm.widget_border[current_color_index]

    return [
        BorderDecoration(
            border_width = (0, 0, 3, 0),
            colour = border_color,
        ),
    ]

def decorate_rect(color_index = None, *, progress = True):
    global current_color_index
    border_color = "#000000"
    if color_index is not None:
        border_color = tm.widget_border[color_index]
    elif progress:
        current_color_index += 1
    border_color = tm.widget_border[current_color_index]

    return [
        RectDecoration(
            colour = border_color,
            # use_widget_background = True,
            radius = 8,
            line_width = 2,
            padding_x = 0,
            padding_y = 3,
            filled = True,
            group = True,
            clip = True,
        ),
        RectDecoration(
            colour = "#000000",
            # use_widget_background = True,
            radius = 8,
            line_width = 2,
            padding_x = 0,
            padding_y = 3,
            group = True,
            clip = True,
        ),
    ]

def decorate(color_index = None, *, progress = True):
    return decorate_border(color_index, progress = progress)

# Return a separator or spacer widget
def sep(width = 8):
    # return widget.Sep(linewidth = 2)
    return widget.Spacer(length = width)

# Default settings for all widgets
widget_defaults = dict(
    font = "DejaVuSansMono Nerd Font",
    fontsize = 12,
    padding = 3,
    inactive = tm.fg_inactive,
    active = tm.fg_active,
)

# Default settings for system monitor widgets
monitor_defaults = widget_defaults | dict(
    fontsize = 14,
    padding = 10,
)

# Default for group box widgets
groupbox_defaults = widget_defaults | dict(
    fontsize = 16,
    highlight_method = "line",
    highlight_color = tm.bg,
    other_current_screen_border = tm.fg_inactive_dim,    # screen unfocused, group unfocused
    this_screen_border = tm.fg_active_dim,             # screen unfocused, group focused
    this_current_screen_border = tm.fg_active,  # screen focused, group focused
    other_screen_border = tm.fg_inactive,       # screen focused, group unfocused
    urgent_alert_method = "block",
    urgent_border = tm.bg_urgent,
)

# }}}



# Initialize the system monitor widgets
def init_monitors():
    s = sep()

    cpu_widget =  widget.CPU(
        format = "<span font_size='12pt'></span> {load_percent: >3.0f}%",
        decorations = decorate(0),
        mouse_callbacks = {
            "Button1": lazy.spawn("kitty -e htop"),
            "Button3": lazy.spawn("kitty -e bpytop"),
        },
        **monitor_defaults,
    )

    memory_widget_outside = widget.Memory(
        format = " {MemPercent: 2.0f}%",
        decorations = decorate(0),
        mouse_callbacks = {
            # "Button1": lazy.widget["widgetbox_memory"].toggle(),
        },
        **monitor_defaults
    )

    # memory_widgetbox = widget.WidgetBox(
    #     widgets = [
    #         widget.Memory(
    #             format = "﬙ {MemUsed:.2f}{mm}/{MemTotal:.0f}{mm}   {SwapUsed:.2f}{ms}/{SwapTotal:.0f}{ms}",
    #             measure_mem = "G",
    #             measure_swap = "G",
    #             decorations = decorate(progress = False),
    #             **monitor_defaults,
    #         ),
    #     ],
    #     text_open = " ❱ ",
    #     text_closed = " ❰ ",
    #     close_button_location = "left",
    #     decorations = decorate(progress = True),
    #     name = "widgetbox_memory",
    #     **(monitor_defaults),
    # )

    gpu_widget = widget.modify(
        NvidiaSensors2,
        format = " {utilization_gpu: >2}% {temperature_gpu: >2}°C",
        format_alert = "<span color='#ffe000'> {utilization_gpu: >2}% {temperature_gpu: >2}°C</span>",
        sensors = ["utilization.gpu", "temperature.gpu", "fan.speed"],
        threshold = 70,
        decorations = decorate(0),
        **monitor_defaults,
        initialise=True
    )

    volume_widget = widget.Volume(
        decorations = decorate(),
        mouse_callbacks = {
            "Button1": lazy.spawn("kitty -e pulsemixer"),
        },
        **monitor_defaults,
    )

    weather_widget = widget.OpenWeather(
        format = "{icon}  {main_temp:.0f}°{units_temperature}",
        app_key = "0521d207c853c983abea0b3358f1dfeb",
        cityid = "721472",
        decorations = decorate(progress = False),
        weather_symbols = openweather_symbols,
        mouse_callbacks = {
            "Button1": lazy.spawn("xdg-open 'https://koponyeg.hu/elorejelzes/Debrecen'"),
            # "Button3": lazy.spawn("xdg-open 'https://openweathermap.org/city/721472'"),
        },
        **monitor_defaults
    )

    return [
        cpu_widget,
        s,
        memory_widget_outside,
        s,
        gpu_widget,
        s,
        volume_widget,
        s,
        weather_widget
    ]

# Initialize left side widgets (common to both screens)
def init_left_widgets():
    return [
        widget.CurrentLayoutIcon(scale = 0.6),
        # widget.CurrentScreen(inactive_text = f"{screen_index}", active_text = f"{screen_index}"),
        widget.GroupBox(
            visible_groups = [str(i) for i in range(1, 7)],
            disable_drag = True,
            **groupbox_defaults,
        ),
        sep(),
        widget.GroupBox(
            visible_groups = ["media", "web", "vm"],
            **(groupbox_defaults),
        ),
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
            border = tm.fg_inactive_dim,
            max_title_width = 240,
            decorations = [],

        ),

        # Right
        *(init_monitors()),
    ]

    if use_systray:
        widgets.extend([
            sep(),
            widget.StatusNotifier(
                decorations = decorate(),
            ),
        ])

    widgets.extend([
        # Date and time
        sep(),
        widget.Clock(format="%b %d\r<span size='6pt'>%A</span>", fontsize = 12, font = "sans bold"),
        sep(),
        widget.Clock(format="%H:%M", fontsize = 24, font = "sans bold"),
    ])

    return widgets
