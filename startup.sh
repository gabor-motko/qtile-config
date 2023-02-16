#!/bin/sh
# Startup file for Qtile

# Set monitor config on OVERLORD
xrandr --output DP-0 --mode 1280x1024 --pos 0x0 --rotate normal --output DP-1 --off --output DP-2 --off --output DP-3 --off --output HDMI-0 --primary --mode 1920x1080 --pos 1280x0 --rotate normal --output DP-4 --off --output DP-5 --off &

# start compositor
picom -b --vsync & # --experimental-backends

emacs --daemon &
/usr/lib/polkit-kde-authentication-agent-1 &    # Polkit auth pop-up agent
xset r rate 250 50    # set keyboard to repeat after 250ms every 50ms
nitrogen --restore &  # set wallpapers
numlockx on           # set numlock to on
#exec --no-startup-id /usr/lib/pam_kwallet_init & # KDE Wallet
