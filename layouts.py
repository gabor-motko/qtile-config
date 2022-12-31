from libqtile import layout
from theme import theme as tm

layout_defaults = dict(
    margin = 4,
    border_width = 2,
    border_on_single = True,
    border_normal = tm.border_inactive,
    border_focus = tm.border_active,
    border_normal_stack = tm.border_inactive,
    border_focus_stack = tm.border_active,
)


def init_layouts():
    return [
        # layout.MonadTall(**layout_defaults),   # Vertical master-stack
        layout.Columns(**layout_defaults),     # Flexible columns
        # layout.MonadWide(**layout_defaults),   # Horizontal master-stack
        layout.Max(**(layout_defaults | dict(margin = [4, 0, 0, 0], border_width = 0))),         # Focused window only
        layout.Stack(**layout_defaults, num_stacks = 2), # Fixed number of stacked windows
        #layout.Bsp(**layout_defaults),             # BSPWM-like binary tree
        #layout.Matrix(**layout_defaults, columns = 2),          # Equally sized cells in columns
        #layout.RatioTile(**layout_defaults),   # Tiles based on width/height ratio
        #layout.Tile(**layout_defaults),        # Vertical master-stack with several masters
        #layout.TreeTab(**layout_defaults),     # Maximized with window list
        #layout.VerticalTile(**layout_defaults),    # Vertical-er master-stack
        #layout.Zoomy(**layout_defaults),       # Maximized with window previews
        #layout.Slice(**layout_defaults, fallback = layout.Tile(**layoutConfig)),
        layout.Spiral(**layout_defaults),
        # layout.Floating(**layout_defaults),    # We all float down here
    ]
