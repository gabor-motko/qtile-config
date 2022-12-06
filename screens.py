from libqtile import bar
from libqtile.config import Screen

from widgets import init_widgets, widget_defaults
from theme import theme as tm

bar_height = 32

screens = [
    Screen(
        top = bar.Bar(
            init_widgets(use_systray = True, screen_index = 0),
            bar_height,
            background = tm.bg,
        )
    ),
]
