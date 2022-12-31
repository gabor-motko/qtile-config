from os.path import expanduser
from subprocess import Popen
from libqtile import hook
from libqtile import layout

def init_hooks():
    # @hook.subscribe.layout_change
    # def on_layout_change(l, g):
    #     if l is layout.Max:
    #         pass
    
    @hook.subscribe.startup
    def startup():
        Popen(expanduser("~/.config/qtile/startup.sh"))
