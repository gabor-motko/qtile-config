from libqtile import bar
from libqtile.config import Screen

from widgets import init_widgets, widget_defaults
from theme import theme as tm

bar_height = 24

bar_defaults = dict(
    background = "#000000e0",
    margin = 0,
)

def init_screens():
    return [
        Screen(
            top = bar.Bar(
                init_widgets(0),
                bar_height,
                **bar_defaults
            )
        ),
        Screen(
            top = bar.Bar(
                init_widgets(1),
                bar_height,
                **bar_defaults
            )
        ),
    ]
