from libqtile import hook, pangocffi
from libqtile.group import _Group
from libqtile.core.manager import Qtile
from libqtile.widget import base
from libqtile.log_utils import logger

from rofi import Rofi
r = Rofi()

class WindowState(base._TextBox):
    defaults = [
        (
            "callback",
            None,
            "Function that returns a string based on the window's state. It receives the focused window as argument."
        )
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, **config)
        self.add_defaults(WindowState.defaults)

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        hook.subscribe.focus_change(self.on_focus_change)
        hook.subscribe.float_change(self.on_focus_change)
        hook.subscribe.current_screen_change(self.on_focus_change)

    def remove_hooks(self):
        hook.unsubscribe.focus_change(self.on_focus_change)
        hook.unsubscribe.float_change(self.on_focus_change)
        hook.unsubscribe.current_screen_change(self.on_focus_change)

    def on_focus_change(self, *args):
        w = self.bar.screen.group.current_window
        state = self.txt_normal
        if w:
            if callable(self.callback):
                try:
                    self.callback(w)
                except:
                    logger.exception("WindowState callback function failed.")
            elif w.maximized:
                state = self.txt_maximized
            elif w.minimized:
                state = self.txt_minimized
            elif w.floating:
                state = self.txt_floating
        self.update(pangocffi.markup_escape_text(state))

    def finalize(self):
        self.remove_hooks()
        base._TextBox.finalize(self)


class WindowIndex(base._TextBox):
    defaults = [
        (
            "format",
            "{index1}/{count}",
            "Format string. Available vars are count (N), index0 (0 to N-1), index1 (1 to N)."
        ),
        (
            "placeholder_index",
            "-",
            "Used in place of an index if there is no focused window."
        ),
        (
            "placeholder_count",
            "-",
            "Used in place of an index if there is no focused window."
        ),
    ]

    _window_count = None
    _window_index = None

    def __init__(self, **config):
        base._TextBox.__init__(self, **config)
        self.add_defaults(WindowIndex.defaults)

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        hook.subscribe.focus_change(self.on_focus_change)
        hook.subscribe.float_change(self.on_focus_change)
        hook.subscribe.current_screen_change(self.on_focus_change)
        hook.subscribe.client_managed(self.on_client_managed)
        hook.subscribe.client_killed(self.on_client_managed)

    def remove_hooks(self):
        hook.unsubscribe.focus_change(self.on_focus_change)
        hook.unsubscribe.float_change(self.on_focus_change)
        hook.unsubscribe.current_screen_change(self.on_focus_change)
        hook.unsubscribe.client_managed(self.on_client_managed)
        hook.unsubscribe.client_killed(self.on_client_managed)

    def _get_window_count(self):
        try:
            return len(self.bar.screen.group.windows)
        except:
            return None

    def _get_window_index(self):
        # Windows can be either "managed" by the layout or "unmanaged" and not participating
        # in the layout algorithm (such as floating). Unmanaged windows are present
        # in group.windows, but not in layout.clients.

        group = self.bar.screen.group
        cw = group.current_window
        # Return None if there is no focused window in the current group.
        if not cw:
            return None
        layout = group.layout


        # If the focused window is managed, use layout.current_index.
        if cw in layout.clients:
            return layout.clients.current_index
        else:
            unmanaged_windows = [w for w in group.windows if w not in layout.clients.clients]
            return len(layout.clients) + unmanaged_windows.index(cw)


    def on_focus_change(self):
        count = self._get_window_count()
        self._window_count = count

        index = self._get_window_index()
        self._window_index = index

        self.update(
            self.format.format(
                index0 = self._window_index     if self._window_index is not None else self.placeholder_index,
                index1 = self._window_index + 1 if self._window_index is not None else self.placeholder_index,
                count   = self._window_count or self.placeholder_count,
            )
        )

    def on_client_managed(self, client):
        self.on_focus_change()


    def finalize(self):
        self.remove_hooks()
        base._TextBox.finalize(self)
