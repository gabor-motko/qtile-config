# Colors and theme thingies

from utils import interp_tuple

class _Theme:
    bg                = "#00000000"
    bg_translucent    = "#282c34a0"
    bg_urgent         = "#fe8000"
    fg_neutral        = "#ffffff"
    fg_inactive       = "#51afef"
    fg_inactive_dim   = "#347098"
    fg_active         = "#ecbe7b"
    fg_active_dim     = "#765f3d"
    border_inactive   = "#282c34"
    border_active     = "#51afef"
    # Use this to grab colors from a gradient:
    # $ for i in {0..8}; do c=`xcolor`; echo "\"$c\","; done
    widget_border = [
        "#f9e110",
        "#fdb419",
        "#f0780f",
        "#dd5803",
        "#d34803",
        "#e92620",
        "#b11a07",
        "#7c0618",
    ]

    gradient = [
        "#dc4b02",
        "#dd5a00",
        "#e67201",
        "#f08c01",
        "#f69c04",
        "#fcab00",
    ]


    gradient_dim = [
        "#180b1a",
        "#2b0c17",
        "#510f13",
        "#ad1911",
        "#d32f0f",
        "#e94a0e",
    ]

    gradient_light = [
        "#aa80b0",
        "#cb84a8",
        "#ea909c",
        "#fead97",
        "#ffcf90",
        "#ffe68b",
    ]

    font_mono        = "DejaVuSansMono Nerd Font"
    font_mono_bold   = "DejaVuSansMono Nerd Font Bold"
    font             = "DejaVuSans Nerd Font"
    font_bold        = "DejaVuSans Nerd Font Bold"

theme = _Theme()
