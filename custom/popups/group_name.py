from qtile_extras.popup.toolkit import PopupAbsoluteLayout, PopupRelativeLayout, PopupText, PopupImage, PopupWidget
from custom.color.current import *

active_popup = None


def group_name_popup(qtile, title: str = "Group"):
    global active_popup, popup_defaults

    if active_popup:
        active_popup.hide()
        active_popup = None


    control_defaults = dict(
        background = "#00000000",
        font = "mononoki Nerd Font Mono",
    )

    controls = [
        PopupText(
            text = title,
            pos_x = 0, pos_y = 0,
            width = 1, height = 0.25,
            fontsize = 18,
            h_align = "center", v_align = "center",
            foreground = color05,
            **(control_defaults | dict(
                font = "mononoki Nerd Font Mono Bold"
            )),
        ),
        PopupText(
            text = qtile.current_group.label,
            pos_x = 0, pos_y = 0.25,
            width = 1, height = 0.75,
            fontsize = 60,
            h_align = "center", v_align = "center",
            foreground = color06,
            **(control_defaults | dict(
                font = "mononoki Nerd Font Mono Bold"
            )),
        ),
    ]

    layout = PopupRelativeLayout(
        qtile, controls = controls,
        width = 300, height = 100,
        close_on_click = True,
        hide_on_timeout = 0.5,
        background = "#000000c0",
    )

    active_popup = layout

    layout.show(centered = True)
