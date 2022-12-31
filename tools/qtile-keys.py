#!/usr/bin/env python3

from os.path import expanduser
import sys
from colorama import Fore, Back, Style

sys.path.insert(0, expanduser("~/.config/qtile/"))
from config import keys as key_defs
from libqtile.config import Key

fctrl = Fore.LIGHTRED_EX
falt = Fore.BLUE
fshift = Fore.GREEN
fsuper = Fore.LIGHTMAGENTA_EX
fdash = Fore.LIGHTBLACK_EX
freset = Style.RESET_ALL

key_transform_colorize_long = {
    "shift": f"{Fore.GREEN}shift{Style.RESET_ALL}-",
    "control": f"{Fore.LIGHTRED_EX}control{Style.RESET_ALL}-",
    "mod4": f"{Fore.LIGHTMAGENTA_EX}super{Style.RESET_ALL}-",
    "mod1": f"{Fore.BLUE}alt{Style.RESET_ALL}-",
}

key_transform_colorize_short = {
    "shift": f"{Fore.GREEN}S{Style.RESET_ALL}-",
    "control": f"{Fore.LIGHTRED_EX}C{Style.RESET_ALL}-",
    "mod4": f"{Fore.LIGHTMAGENTA_EX}{Style.RESET_ALL}-",
    "mod1": f"{Fore.BLUE}M{Style.RESET_ALL}-",
}

def special_keysym_transform(s):
    t = {
        "odiaeresis": "ö",
        "udiaeresis": "ü",
        "oacute": "ó",
        "left": ""
    }

    return t[s] if s in t else s

def format_modkeys_long(mods, key, use_colors = False, capitalize = True):
    s = ""
    for mod in mods:
        mod = mod.lower()
        if mod == "mod1":
            s += "alt-"
        elif mod == "mod4":
            s += "super-"
        elif mod == "control":
            s += "control-"
        elif mod == "shift":
            s += "shift-"

    key = special_keysym_transform(key)
    if capitalize:
        key = key.upper()

    length = len(s) + len(key or "")

    s = s.replace("alt", f"{falt}alt{freset}")
    s = s.replace("super", f"{fsuper}super{freset}")
    s = s.replace("control", f"{fctrl}control{freset}")
    s = s.replace("shift", f"{fshift}shift{freset}")
    s = s.replace("-", f"{fdash}-{freset}")

    s += key or ""
    return s, length


def format_modkeys_short(mods, key, use_colors = False, capitalize = True):
    s = ""
    for mod in mods:
        mod = mod.lower()
        if mod == "mod1":
            s += "M-"
        elif mod == "mod4":
            s += "-"
        elif mod == "control":
            s += "C-"
        elif mod == "shift":
            s += "S-"

    key = special_keysym_transform(key)
    if capitalize:
        key = key.upper()

    length = len(s) + len(key or "")

    s = s.replace("M-", f"{falt}M{freset}-")
    s = s.replace("-", f"{fsuper}{freset}-")
    s = s.replace("C-", f"{fctrl}C{freset}-")
    s = s.replace("S-", f"{fshift}S{freset}-")
    s = s.replace("-", f"{fdash}-{freset}")

    s += key or ""
    return s, length


def format_modkeys_emacs(mods, key, use_colors = False):
    s = ""
    for mod in mods:
        mod = mod.lower()
        if mod == "mod1":
            s += "M-"
        elif mod == "mod4":
            s += "-"
        elif mod == "control":
            s += "C-"
        elif mod == "shift":
            s += "S-"


def main():

    keys = dict()   # group -> list of (key, desc, orig_length)
    longest_keybinding = 0

    key: Key
    for key in key_defs:
        group = None
        desc = "(MISSING)"

        group_delim = key.desc.find("]") + 1
        if group_delim > 0:
            group = key.desc[:group_delim].strip("[]")
            desc = key.desc[group_delim:].strip()
        else:
            group = "N/A"
            desc = key.desc.strip()

        if group not in keys:
            keys[group] = []

        keybinding, length = format_modkeys_short(key.modifiers, key.key, True)
        longest_keybinding = max(longest_keybinding, length)
        keys[group].append((keybinding, desc, length))


    for group in keys:
        print(f"{Back.WHITE}{Fore.BLACK}{group}{Style.RESET_ALL}")

        for key in keys[group]:
            k, d, l = key
            print("{} : {}".format(k.ljust(longest_keybinding + (len(k) - l)), d))

if __name__ == "__main__":
    main()
