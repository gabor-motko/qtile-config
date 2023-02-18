# Copyright (c) 2008, Aldo Cortesi. All rights reserved.
# Copyright (c) 2017, Dirk Hartmann.
# Copyright (c) 2023, Gábor Motkó
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.command.base import expose_command
from libqtile.layout.base import _SimpleLayoutBase


class CenterFocus(_SimpleLayoutBase):
    """CenterFocus layout
    """

    defaults = [
        ("margin", 0, "Margin of the layout (int or list of ints [N E S W])"),
        ("border_focus", "#0000ff", "Border colour(s) for the window when focused"),
        ("border_normal", "#000000", "Border colour(s) for the window when not focused"),
        ("border_width", 0, "Border width."),
        ("sizing_mode", "absolute", "Method to determine the size of the window rect: absolute or relative."),
        ("width", 1280, "The window rect's width."),
        ("height", 720, "The window rect's height."),
        ("grow_amount", 100, "Amount by which to grow/shrink the window."),
    ]

    def __init__(self, **config):
        _SimpleLayoutBase.__init__(self, **config)
        self.add_defaults(CenterFocus.defaults)

    def add_client(self, client):
        return super().add_client(client, 1)

    def configure(self, client, screen_rect):
        if self.clients and client is self.clients.current_client:
            w = (screen_rect.width * self.width if self.sizing_mode == "relative" else self.width) - self.border_width * 2
            h = (screen_rect.height * self.height if self.sizing_mode == "relative" else self.height) - self.border_width * 2

            client.place(
                screen_rect.x + int((screen_rect.width - w) / 2),
                screen_rect.y + int((screen_rect.height - h) / 2),
                w,
                h,
                self.border_width,
                self.border_focus if client.has_focus else self.border_normal,
                margin=self.margin,
            )
            client.unhide()
        else:
            client.hide()

    @expose_command("previous")
    def up(self):
        _SimpleLayoutBase.previous(self)

    @expose_command("next")
    def down(self):
        _SimpleLayoutBase.next(self)

    @expose_command
    def resize(self, resize_by = (0, 0)):
        self.width = self.width + resize_by[0]
        self.height = self.height + resize_by[1]
        self.group.layout_all()

    @expose_command(["grow_left", "grow_right"])
    def grow_h(self):
        self.resize((self.grow_amount, 0))

    @expose_command(["grow_up", "grow_down"])
    def grow_v(self):
        self.resize((0, self.grow_amount))

    @expose_command(["shrink_left", "shrink_right"])
    def shrink_h(self):
        self.resize((-self.grow_amount, 0))

    @expose_command(["shrink_up", "shrink_down"])
    def shrink_v(self):
        self.resize((0, -self.grow_amount))
