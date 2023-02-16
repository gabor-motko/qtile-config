from os.path import expanduser
from subprocess import Popen
from libqtile import hook
from libqtile import layout
from libqtile import qtile
from custom.popups import group_name_popup
#from libqtile.core.manager import Qtile
from rofi import Rofi

r = Rofi()



def init_hooks():
    # @hook.subscribe.layout_change
    # def on_layout_change(l, g):
    #     if l is layout.Max:
    #         pass
    
    @hook.subscribe.startup
    def startup():
        # Run the startup script
        Popen(expanduser("~/.config/qtile/startup.sh"))

        # Set window properties to exclude bars from Picom

    # NOTE: this hook seems to be broken, only fires on reload, not on group change.
    # Workaround is to call group_name_popup on keybind defined in groups.py.
    #@hook.subscribe.changegroup
    #def changegroup():
        #r.status("asd")
        #group_name_popup(qtile.current_group)
