from libqtile import bar
from libqtile.config import Screen

from widgets import init_widgets, widget_defaults
from theme import theme as tm

bar_height = 28

bar_defaults = dict(
    background = "#00000000",
    margin = [4, 4, 0, 4],
)

def init_screens():
    return [
        Screen(
            top = bar.Bar(
                init_widgets(use_systray = True, screen_index = 0),
                bar_height,
                **bar_defaults
            )
        ),
        Screen(
            top = bar.Bar(
                init_widgets(use_systray = True, screen_index = 1),
                bar_height,
                **bar_defaults
            )
        ),
    ]
