from libqtile import layout
from theme import theme as tm

layoutConfig = dict(
    margin = 10,
    border_width = 3,
    border_on_single = True,
    border_normal = tm.border_inactive,
    border_focus = tm.border_active,
    border_normal_stack = tm.border_inactive,
    border_focus_stack = tm.border_active,
)

layouts = [
    layout.MonadTall(**layoutConfig),   # Vertical master-stack
    layout.Columns(**layoutConfig),     # Flexible columns
    # layout.MonadWide(**layoutConfig),   # Horizontal master-stack
    layout.Max(**(layoutConfig | dict(margin = 0, border_width = 0))),         # Focused window only
    #layout.Stack(**layoutConfig, num_stacks = 2), # Fixed number of stacked windows
    #layout.Bsp(**layoutConfig),             # BSPWM-like binary tree
    #layout.Matrix(**layoutConfig, columns = 2),          # Equally sized cells in columns
    #layout.RatioTile(**layoutConfig),   # Tiles based on width/height ratio
    #layout.Tile(**layoutConfig),        # Vertical master-stack with several masters
    #layout.TreeTab(**layoutConfig),     # Maximized with window list
    #layout.VerticalTile(**layoutConfig),    # Vertical-er master-stack
    #layout.Zoomy(**layoutConfig),       # Maximized with window previews
    #layout.Slice(**layoutConfig, fallback = layout.Tile(**layoutConfig)),
    layout.Spiral(**layoutConfig),
    # layout.Floating(**layoutConfig),    # We all float down here
]
