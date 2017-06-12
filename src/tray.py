from pystray import Icon, Menu, MenuItem
from PIL import Image

app_info='LTS AS, Mamman 0.1'
state=False

def on_clicked(icon):
    print('UI event: click')
    global state
    state = not state

def on_default(icon):
    print('UI event: Default')
    
def on_exit(icon):
    print('UI event: Exit')
    icon.stop()

menu=Menu(
    MenuItem('Checkable', on_clicked, checked=lambda item: state),
    MenuItem('Exit', on_exit),
    MenuItem('Default click', on_default ,default=True, visible=False)
    )

icon = Icon(app_info, icon=Image.open("logo_red.ico"), title=app_info, menu=menu)

def setup(icon):
    icon.visible = True


if __name__=="__main__":
    import pprint
    icon.run(setup)
