from libqtile import hook
from libqtile import layout

# @hook.subscribe.layout_change
# def on_layout_change(l, g):
#     if l is layout.Max:
#         pass
    
@hook.subscribe.startup
def startup():
    subprocess.Popen(os.path.expanduser("~/.config/qtile/startup.sh"))
