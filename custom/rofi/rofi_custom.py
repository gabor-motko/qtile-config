# Custom menus based on python-rofi
import subprocess
import json
from rofi import Rofi
from libqtile.config import Key
from libqtile.lazy import lazy
from libqtile.core.manager import Qtile
from logging import DEBUG

from utils import str_unicodify, read_nf_data, toggle_debug
from groups import group_defs

rofi_default_args = ["-i"]

nf_names = None
nf_codes = None


# Set group's label to a Nerd Font entity or custom text
def rename_group_menu(qtile: Qtile, *, rofi = None):
    global nf_names, nf_codes

    if nf_names is None or nf_codes is None:
        nf_data = read_nf_data()
        nf_names = [key for key in nf_data]
        nf_codes = [nf_data[key] for key in nf_data]

    r = rofi or Rofi(rofi_args = rofi_default_args)
    group = qtile.current_group

    i, k = r.select(f"Set label for group {group.name}", nf_names, key1 = ("F1", "Reset"), key2 = ("F2", "Custom text"))

    # Reset to default
    if k == 1:
        group_def = group_defs[group.name][1]
        group.set_label(group_def["label"] if "label" in group_def else group.name)
    # Set custom text
    elif k == 2:
        text = r.text_entry("Custom label", f"Setting custom label for group {group.name}")
        if text:
            group.set_label(text)
    elif i >= 0:
        group.set_label(str_unicodify(r"\u" + nf_codes[i]))


# Set default pulse sink to user choice
def set_audio_sink_menu(qtile, *, rofi = None):
    r = rofi or Rofi(rofi_args = rofi_default_args)
    proc = subprocess.Popen("pactl -f json list sinks".split(" "), stdout=subprocess.PIPE)
    stdout = proc.communicate()[0]
    data = json.loads(stdout)
    i, k = r.select("Select audio output", [item["description"] for item in data])

    if i >= 0:
        sel = data[i]
        try:
            cmd = "pactl set-default-sink {}".format(sel["name"])
            subprocess.Popen(cmd.split(" "))
            # r.status("Audio output set to {}.".format(sel["description"]))
        except Exception as ex:
            r.error(str(ex))


# Kill or restart Picom
def restart_picom_menu(qtile: Qtile, *, rofi = None):
    r = rofi or Rofi(rofi_args = rofi_default_args)
    i, k = r.select(
        "Picom options",
        [
            "Kill",
            "Restart with vsync",
            "Restart without vsync",
            "Restart with custom options..."
        ]
    )

    if i == 0:
        qtile.spawn("pkill picom", shell = True)
    elif i == 1:
        qtile.spawn("pkill picom; sleep 2; picom -b --vsync", shell=True)
    elif i == 2:
        qtile.spawn("pkill picom; sleep 2; picom -b", shell=True)
    elif i == 3:
        new_args = r.text_entry("Options")
        qtile.spawn(f"pkill picom; sleep 2; picom {new_args}", shell=True)


# Menu where I lump everything together
def main_menu(qtile, *, rofi = None):
    r = rofi or Rofi(rofi_args = rofi_default_args)
    i, k = r.select(
        "Main menu",
        [
            "Open bluetoothctl",
            "Keybindings",
            "Manage Picom...",
            "{} debug mode".format("Disable" if qtile.loglevel() == DEBUG else "Enable"),
        ],
        key1=("1", "Select audio output"),
        key2=("2", "Bluetooth")
    )

    if k == 1:
        set_audio_sink_menu(qtile, rofi = r)
    elif k == 2:
        qtile.spawn("rofi-bluetooth")
    else:
        if i == 0:
            qtile.spawn("kitty -e bluetoothctl")
        if i == 1:
            r.status("nothing is worth the risk\n" * 20) # NOTE: maybe do the keybinding popup like this?
        elif i == 2:
            restart_picom_menu(qtile, rofi = r)
        elif i == 3:
            toggle_debug(qtile)
        else:
            pass
