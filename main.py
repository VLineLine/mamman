from pystray import Icon, Menu, MenuItem
from PIL import Image
from src.crypto import tools
from src.api import connection
from src.environment import userdir
import subprocess


user_key = None
app_info='LTS AS, Mamman 0.1'
state=False
crypto_tools = tools(userdir.crypto)
api_tools = connection()

def on_click_available(icon):
    print('UI event: click')
    global state
    state = not state

def on_default(icon):
    print('UI event: Default')
    
def on_exit(icon):
    print('UI event: Exit')
    icon.menu = menu_disconnected
    icon.visible = False
    icon.stop()

def on_click_open_dir(icon):
    print('UI event: Open working directory')
    subprocess.Popen('explorer "' + userdir.workspace + '"')
    
menu_disconnected=Menu(
    )
menu_1=Menu(
    MenuItem('Åpne arbeidsmappe', on_click_open_dir),
    MenuItem('Jeg er tilgjengelig', on_click_available, checked=lambda item: state),
    MenuItem('Avslutt Mamman', on_exit),
    MenuItem('Default click', on_default ,default=True, visible=False)
    )
icon = Icon(app_info, icon=Image.open("res\logo_red.png"), title=app_info, menu=menu_disconnected)


def setup(icon):
    icon.visible = True
    user_key = api_tools.post('user', crypto_tools.get_credentials())['resource'][0]['key']
    if user_key != None:
        print("ATOMATIC event: User login OK\n", user_key)
        icon.icon = Image.open("res\logo.png")
        icon.menu = menu_1

    
if __name__=="__main__":
    icon.run(setup)
