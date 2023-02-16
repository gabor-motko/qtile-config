from libqtile.widget.groupbox import GroupBox

from rofi import Rofi
r = Rofi()
def status(o):
    r.status(str(o))

class BoxStyle:
    """Represents a highlight style for the GroupBoxFn widget's elements."""


    style: dict = {
        "text_color": None,
        "border_active": None,
        "border_color": None,
        "border_size": None,
        "line_active": None,
        "line_color": None,
        "line_size": None,
        "line_length": None,
        "block_active": None,
        "block_color": None,
        "block_rounded": None,
    }


    def __init__(self, **kwargs):
        if "style" in kwargs and kwargs["style"] is dict:
            self.style = self.style | kwargs["style"]

        for key in kwargs:
            if key in self.style:
                self.style[key] = kwargs[key]


    def __getattr__(self, name):
        if name in self.style:
            return self.style[name]
        else:
            raise AttributeError


    def __setattr__(self, name, value):
        if name in self.style:
            self.style[name] = value
        else:
            raise AttributeError


    def combine(self, other):
        """Returns a copy of this instance updated with non-None values from the other instance."""
        result = BoxStyle()
        style = self.style.copy()

        for key in result.style:
            s = self.style[key]
            o = other.style[key] if key in other.style else None
            result.style[key] = s if o is None else o

        return result


    def get_default():
        """Returns a new instance with all attributes set."""
        return BoxStyle(
            text_color = "#000000",
            border_active = False,
            border_color = "#000000",
            border_size = 1,
            line_active = False,
            line_color = "#ff0000",
            line_size = 3,
            line_length = 1,
            block_active = False,
            block_color = "#ffffff",
            block_rounded = False
        )



class GroupBoxFn(GroupBox):
    defaults = [
        (
            "transform_label",
            None,
            "If this function is set, its result is used in place of the group's label;"
            "if None (default), the group's label is used directly. The function"
            "returns a str, and takes the following positional arguments:"
            "- group: the group object for which the box is drawn."
            "- has_windows: whether the group contains any windows."
            "- active: whether the group is active on any screen."
            "- current: whether the group is active on the screen that has focus."
        ),
        (
            "normal_style",
            None,
            "The BoxStyle applied to all groups regardless of highlighting."
        ),
        (
            "has_windows_style",
            None,
            "The BoxStyle applied to groups that contain windows."
        ),
        (
            "active_any_screen_style",
            None,
            "The BoxStyle applied to groups that are active on any screens."
        ),
        (
            "active_own_screen_style",
            None,
            "The BoxStyle applied to groups that are active on the screens where the widgets are located."
        ),
        (
            "active_current_screen_style",
            None,
            "The BoxStyle applied to the single group that is active on the screen that has the focus."
        ),
        (
            "urgent_style",
            None,
            "The BoxStyle applied to groups that have urgent windows."
        ),
    ]

    def __init__(self, **config):
        GroupBox.__init__(self, **config)
        self.add_defaults(GroupBoxFn.defaults)


    def combine_styles(self):
        text_color = None
        border_active = False
        border_color = None
        border_size = None


    def box_width(self, groups):
        if self.transform_label is None:
            return GroupBox.box_width(self, groups)

        width, _ = self.drawer.max_layout_size(
            [self.fmt.format(self._execute_transform_label(i)) for i in groups], self.font, self.fontsize
        )
        return width + self.padding_x * 2 + self.borderwidth * 2

    def _execute_transform_label(self, group):
        return group.label if self.transform_label is None else self.transform_label(
            group,
            bool(group.windows),
            bool(group.screen),
            self.qtile.current_screen == self.bar.screen
        )

    def draw(self):
        return self.draw_old()

    def draw_old(self):
        self.drawer.clear(self.background or self.bar.background)

        offset = self.margin_x
        for i, g in enumerate(self.groups):
            to_highlight = False
            is_block = self.highlight_method == "block"
            is_line = self.highlight_method == "line"

            bw = self.box_width([g])

            if self.group_has_urgent(g) and self.urgent_alert_method == "text":
                text_color = self.urgent_text
            elif g.windows:
                text_color = self.active
            else:
                text_color = self.inactive

            if g.screen:
                if self.highlight_method == "text":
                    border = None
                    text_color = self.this_current_screen_border
                else:
                    if self.block_highlight_text_color:
                        text_color = self.block_highlight_text_color
                    if self.bar.screen.group.name == g.name:
                        if self.qtile.current_screen == self.bar.screen:
                            border = self.this_current_screen_border
                            to_highlight = True
                        else:
                            border = self.this_screen_border
                    else:
                        if self.qtile.current_screen == g.screen:
                            border = self.other_current_screen_border
                        else:
                            border = self.other_screen_border
            elif self.group_has_urgent(g) and self.urgent_alert_method in ("border", "block", "line"):
                border = self.urgent_border
                if self.urgent_alert_method == "block":
                    is_block = True
                elif self.urgent_alert_method == "line":
                    is_line = True
            else:
                border = None

            self.drawbox(
                offset,
                g.label if self.transform_label is None else self._execute_transform_label(g),
                border,
                text_color,
                highlight_color=self.highlight_color,
                width=bw,
                rounded=self.rounded,
                block=is_block,
                line=is_line,
                highlighted=to_highlight,
            )
            offset += bw + self.spacing
        self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.width)

    def drawbox_new(
            self,
            offset,
            text,
            style,
            box_width = None,
            ):

        self.layout.text = self.fmt.format(text)
        self.layout.font_family = self.font
        self.layout.font_size = self.fontsize
        self.layout.colour = style.text_color

        if box_width is not None:
            self.layout.width = box_width

        if style.line_active:
            pad_y = [
                (self.bar.height - self.layout.height - self.borderwidth) / 2,
                (self.bar.height - self.layout.height + self.borderwidth) / 2,
            ]
        else:
            pad_y = self.padding_y

        if style.border_active:
            border_width = self.borderwidth
            framecolor = style.border_color
        else:
            border_width = 0
            framecolor = self.background or self.bar.background

        framed = self.layout.framed(border_width, framecolor, 0, pad_y, None)
        y = self.margin_y
        if self.center_aligned:
            for t in base.MarginMixin.defaults:
                if t[0] == "margin":
                    y += (self.bar.height - framed.height) / 2 - t[1]
                    break
        if style.block_active:
            framed.draw_fill(offset, y, style.block_rounded)

        framed.draw(offset, y, style.block_rounded)

        if style.line_active:
            framed.draw_line(offset, y, True)


    def draw_new(self):
        self.drawer.clear(self.background or self.bar.background)

        offset = self.margin_x

        for i, g in enumerate(self.groups):
            active_style: BoxStyle = self.normal_style or BoxStyle.get_default()

            has_windows = bool(g.windows)
            active_any = bool(g.screen)
            active_own = self.bar.screen.group.name == g.name
            active_current = self.qtile.current_screen == self.bar.screen
            urgent = self.group_has_urgent(g)

            bw = self.box_width([g])

            if urgent:
                active_style = active_style.combine(self.urgent_style) if self.urgent_style else active_style
            else:
                if has_windows and self.has_windows_style:
                    active_style = active_style.combine(self.has_windows_style)

                if active_any and self.active_any_screen_style:
                    active_style = active_style.combine(self.active_any_screen_style)

                if active_own and self.active_own_screen_style:
                    active_style = active_style.combine(self.active_own_style)

                if active_current and self.active_current_screen_style:
                    active_style = active_style.combine(self.active_current_screen_style)



            self.drawbox_new(
                offset,
                g.label if self.transform_label is None else self._execute_transform_label(g),
                active_style,
                bw
            )

            offset += bw + self.spacing
        self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.width)
