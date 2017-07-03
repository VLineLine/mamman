from src.crypto import tools
from src.api import connection
from src.environment import userdir
from src.ui import Icon, Menu
import subprocess
from PIL import Image
from pystray import MenuItem
from automat import MethodicalMachine

user_key = None
state=False
crypto_tools = tools(userdir.crypto)
api_tools = connection()
icon = Icon()


#============================ state machine start
class State_machine(object):
    _machine = MethodicalMachine()
    _beans = ""
    
#============================ inputs
    @_machine.input()
    def initiate_connection(self):
        "Initiate connection to server"

    @_machine.input()
    def put_in_beans(self, beans):
        "The user put in some beans."

#============================ outputs
    @_machine.output()
    def _heat_the_heating_element(self):
        "Heat up the heating element, which should cause coffee to happen."
        print("heating turned on")

    @_machine.output()
    def _save_beans(self, beans):
        "The beans are now in the machine; save them."
        self._beans = beans

    @_machine.output()
    def _describe_coffee(self):
        return "A cup of coffee made with {}.".format(self._beans)

#============================ states
    @_machine.state()
    def have_beans(self):
        "In this state, you have some beans."
        
    @_machine.state(initial=True)
    def dont_have_beans(self):
        "In this state, you don't have any beans."
        

#============================ transitions
    # When we don't have beans, upon putting in beans, we will then have beans
    dont_have_beans.upon(
        put_in_beans,
        enter=have_beans,
        outputs=[
            _save_beans
            ]
        )

    # When we have beans, upon pressing the brew button, we will then not have
    # beans any more (as they have been entered into the brewing chamber) and
    have_beans.upon(
        brew_button, enter=dont_have_beans,
        outputs=[
            _heat_the_heating_element,
            _describe_coffee
            ],
        collector=lambda iterable: list(iterable)[-1]
        )
#============================ state machine end
    
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
    #icon.run(setup)
    coffee_machine = State_machine()
    coffee_machine.put_in_beans("real good beans")
    print(coffee_machine.brew_button())
