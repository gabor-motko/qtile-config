# Custom menus based on python-rofi
import subprocess
import json
from rofi import Rofi
from libqtile.config import Key
from libqtile.lazy import lazy
from keys import keys

def set_audio_sink(qtile, *, rofi = None):
    r = rofi or Rofi(rofi_args = ["-i"])
    proc = subprocess.Popen("pactl -f json list sinks".split(" "), stdout=subprocess.PIPE)
    stdout = proc.communicate()[0]
    data = json.loads(stdout)
    i, k = r.select("Select audio output", [item["description"] for item in data])

    if i >= 0:
        sel = data[i]
        try:
            cmd = "pactl set-default-sink {}".format(sel["name"])
            subprocess.Popen(cmd.split(" "))
            r.status("Audio output set to {}.".format(sel["description"]))
        except Exception as ex:
            r.error(str(ex))

def main_menu(qtile, *, rofi = None):
    r = rofi or Rofi(rofi_args = ["-i"])
    i, k = r.select("Main menu", ["Open bluetoothctl"], key1=("1", "Select audio output"), key2=("2", "Bluetooth"))

    if k == 1:
        set_audio_sink(qtile, r = r)
    elif k == 2:
        qtile.cmd_spawn("rofi-bluetooth")
    else:
        if i == 0:
            qtile.cmd_spawn("kitty -e bluetoothctl")
        else:
            pass
