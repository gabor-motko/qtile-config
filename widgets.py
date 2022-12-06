from libqtile.widget import base
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration, PowerLineDecoration
from theme import theme as tm

from nvidia_sensors_2 import NvidiaSensors2

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
def decorate(*, color_index = None):
    global current_color_index
    border_color = tm.widget_border[current_color_index]
    current_color_index += 1
    return [
        BorderDecoration(
            border_width = (0, 0, 3, 0),
            colour = border_color,
        ),
    ]

# Add decorations to the widget immediately before the first
# decorated widget to cap the PowerLineDecoration
def decorate_nothing():
    return []

# Return a separator or spacer widget
def sep(width = 8):
    return widget.Sep(linewidth = 2)
    # return widget.Spacer(length = width)

# Default settings for all widgets
widget_defaults = dict(
    font = "sans",
    fontsize = 12,
    padding = 3,
    inactive = tm.fg_inactive,
    active = tm.fg_active,
)

# Default settings for system monitor widgets
monitor_defaults = widget_defaults | dict(
    font = "DejaVuSansMono Nerd Font",
    fontsize = 14,
    padding = 10,
)

# Default for group box widgets
groupbox_defaults = widget_defaults | dict(
    font = "DejaVuSansMono Nerd Font",
    fontsize = 16,
    highlight_method = "line",
    highlight_color = tm.bg,
    this_current_screen_border = tm.fg_active,
    other_screen_border = tm.fg_inactive,
    urgent_alert_method = "block",
    urgent_border = tm.bg_urgent,
)

# }}}

# {{{ Custom widgets

from qtile_extras.widget.mixins import TooltipMixin
import psutil

class MyMemory(widget.Memory, TooltipMixin):
    def __init__(self, *args, **kwargs):
        widget.Memory.__init__(self, *args, **kwargs)
        TooltipMixin.__init__(self)
        self.add_defaults(TooltipMixin.defaults)
        self.tooltip_text = "hello world"

    def _show_tooltip(self, x, y):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        self.tooltip_text = "Memory: {}\nSwap: {}".format(mem.used / self.calc_mem, swap.used / self.calc_swap)
        TooltipMixin._show_tooltip(self, x, y)


# }}}

memory_widget = None
memory_format_percent = "<span font_size='12pt'></span> {MemPercent: >3.0f}%{SwapPercent: >3.0f}%"
memory_format_value = "<span font_size='12pt'></span> {MemUsed:.0f}M {SwapUsed:.0f}M"
memory_is_percent = True
def toggle_memory_display():
    global memory_is_percent
    memory_is_percent = not memory_is_percent
    memory_widget.format = memory_format_percent if memory_is_percent else memory_format_value

# Initialize the system monitor widgets
def init_monitors():
    return [
        widget.CPU(
            format = "<span font_size='12pt'></span> {load_percent: >3.0f}%",
            decorations = decorate(),
            mouse_callbacks = {
                "Button1": lazy.spawn("kitty -e htop"),
                "Button3": lazy.spawn("kitty -e bpytop"),
            },
            **monitor_defaults,
        ),
        sep(),
        MyMemory(
            format = memory_format_percent,
            decorations = decorate(),
            # mouse_callbacks = {
            #     "Button1": toggle_memory_display
            # },
            **monitor_defaults
        ),
        sep(),
        widget.modify(
            NvidiaSensors2,
            format = " {utilization_gpu: >2}% {temperature_gpu: >2}°C",
            format_alert = "<span color='#ffe000'> {utilization_gpu: >2}% {temperature_gpu: >2}°C</span>",
            sensors = ["utilization.gpu", "temperature.gpu", "fan.speed"],
            threshold = 70,
            decorations = decorate(),
            **monitor_defaults,
            initialise=True
        ),
        sep(),
        widget.PulseVolume(
            step = 5,
            decorations = decorate(),
            **monitor_defaults,
        ),
        sep(),
        widget.OpenWeather(
            format = "{icon}  {main_temp:.0f}°{units_temperature}",
            app_key = "0521d207c853c983abea0b3358f1dfeb",
            cityid = "721472",
            decorations = decorate(),
            weather_symbols = openweather_symbols,
            mouse_callbacks = {
                "Button1": lazy.spawn("xdg-open 'https://koponyeg.hu/elorejelzes/Debrecen'"),
                "Button3": lazy.spawn("xdg-open 'https://openweathermap.org/city/721472'"),
            },
            **monitor_defaults
        ),
    ]

# Initialize left side widgets (common to both screens)
def init_left_widgets():
    return [
        widget.CurrentLayoutIcon(scale = 0.6),
        # widget.CurrentScreen(inactive_text = f"{screen_index}", active_text = f"{screen_index}"),
        widget.GroupBox(
            visible_groups = [str(i) for i in range(1, 7)],
            **groupbox_defaults,
        ),
        sep(),
        widget.GroupBox(
            visible_groups = ["media", "web", "vm"],
            **(groupbox_defaults | dict(font = "DejaVuSansMono Nerd Font Mono", fontsize = 24)),
        ),
    ]

# Initialize the bar widgets
def init_widgets(*, use_systray = False, screen_index = -1):
    global current_color_index
    current_color_index = 0

    memory_as_percent = True

    widgets = [
        # Left
        *(init_left_widgets()),
        sep(),

        # Flex
        widget.TaskList(
            border = tm.fg_inactive_dim,
            max_title_width = 240,
            decorations = decorate_nothing(),
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
