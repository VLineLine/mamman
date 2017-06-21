from src.crypto import tools
from src.api import connection
from src.environment import userdir
from src.ui import Icon, Menu
import subprocess
from PIL import Image
from pystray import MenuItem

user_key = None
state=False
crypto_tools = tools(userdir.crypto)
api_tools = connection()
icon = Icon()

def on_click_available(icon):
    print('UI event: click')
    global state
    state = not state
    if state:
        icon.title = 'Mamman henter oppgave\r\nen linje til'
        #icon.icon = Image.open("res\logo_yellow.png")

def on_default(icon):
    print('UI event: Default')

def on_new(icon, item):
    print(icon)
    print(item)
    

def on_exit(icon):
    print('UI event: Exit')
    icon.menu = None
    icon.visible = False
    icon.stop()

def on_click_open_dir(icon, tasting):
    print('UI event: Open working directory')
    subprocess.Popen('explorer "' + userdir.workspace + '"')

menu_1=Menu(
    MenuItem('Åpne arbeidsmappe', on_click_open_dir),
    MenuItem('Hent oppgave', Menu(
        MenuItem('2t, gjennomgang av revisjon', on_new),
        MenuItem('1t, gjennomgang av revisjon', on_new)
    )),
    MenuItem('Ny prosess', Menu(
        MenuItem('Gjennomgang', on_new),
        MenuItem('EPLAN prosjekt', on_new)
    )),
    MenuItem('Jeg er tilgjengelig', on_click_available, checked=lambda item: state),
    MenuItem('Avslutt Mamman', on_exit),
    MenuItem('Default click', on_default ,default=True, visible=False)
    )

def setup(icon):
    icon.visible = True
    user_key = api_tools.post('user', crypto_tools.get_credentials())['resource'][0]['key']
    if user_key != None:
        print("ATOMATIC event: User login OK\n", user_key)
        icon.icon = Image.open("res\logo_blue.png")
        icon.menu = menu_1

    
if __name__=="__main__":
    icon.run(setup)
