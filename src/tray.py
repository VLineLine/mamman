import pystray
from PIL import Image

app_info='LTS AS, Mamman 0.1'
state=False

def on_clicked(icon):
    global state
    state = not state

def on_exit(icon):
    icon.stop()


menu=pystray.Menu(
    pystray.MenuItem('Checkable', on_clicked, checked=lambda item: state),
    pystray.MenuItem('Exit', on_exit)
    )

icon = pystray.Icon(app_info, icon=Image.open("logo_red.ico"), title=app_info, menu=menu)

def setup(icon):
    icon.visible = True


if __name__=="__main__":
    import pprint
    icon.run()
