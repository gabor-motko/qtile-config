#!/usr/bin/bash

logfile="$HOME/.local/share/qtile/qtile.log"

case $1 in
	"clear")
		truncate --size=0 "$logfile"
		echo "Qtile log cleared."
		;;
	"restart")
		qtile cmd-obj -o cmd -f restart
		echo "Qtile restarted."
		;;
	"git")
		echo "Opening Qtile github..."
		xdg-open "https://github.com/qtile/qtile"
		;;
	"git-ex")
		echo "Opening Qtile-Extras github..."
		xdg-open "https://github.com/elparaguayo/qtile-extras"
		;;
	"doc")
		echo "Opening documentation..."
		xdg-open "http://docs.qtile.org/en/latest/"
		;;
	"doc-ex")
		echo "Opening Qtile-Extras doc..."
		xdg-open "https://qtile-extras.readthedocs.io/en/latest/"
		;;
	"nf")
		echo "Opening Nerd Fonts cheat sheet..."
		xdg-open "https://www.nerdfonts.com/cheat-sheet"
		;;
	*)
		echo "Begin Qtile log"
		cat "$logfile"
		echo "End Qtile log"
		;;
esac
