from pystray import Icon, Menu, MenuItem
from PIL import Image
from src.crypto import tools
from src.api import connection
import base64

user_key = None
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
    
icon = Icon(app_info, icon=Image.open("res\logo_red.png"), title=app_info, menu=menu)

def setup(icon):
    icon.visible = True

if __name__=="__main__":
    crypto_tools = tools()
    api_tools = connection()

    credentials = crypto_tools.get_credentials()

    #icon.run(setup)
    #credentials['time_created'] =   ""
    user_key = api_tools.post('user', credentials)['resource'][0]['key']
    print(user_key)
    icon.run(setup)
    print(menu.__dict__)
    #print(api_tools.get('process'))
    #print(api_tools.get('task'))
