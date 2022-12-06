from qtile_extras.popup.toolkit import PopupGridLayout, PopupRelativeLayout, PopupText, PopupWidget
from libqtile.popup import Popup


def test_popup(qtile, *args):
    controls = [
        PopupText(
            text="Lock",
            pos_x=0.1,
            pos_y=0.7,
            width=0.2,
            height=0.2,
            h_align="center"
        ),
        PopupText(
            text="Sleep",
            pos_x=0.4,
            pos_y=0.7,
            width=0.2,
            height=0.2,
            h_align="center"
        ),
        PopupText(
            text="Shutdown",
            pos_x=0.7,
            pos_y=0.7,
            width=0.2,
            height=0.2,
            h_align="center"
        ),

    ]
    layout = PopupRelativeLayout(
        qtile,
        width=400,
        height=200,
        controls=controls,
        background="282c34f0",
        margin=8,
        border_size=2,
        initial_focus=None,
    )

    layout.show(centered=True)
    qtile.call_later(1, layout.kill)
