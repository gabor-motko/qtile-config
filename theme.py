# Colors and theme thingies

class _Theme:
    bg                = "#282c3480"
    bg_urgent         = "#fe8000"
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

theme = _Theme()
