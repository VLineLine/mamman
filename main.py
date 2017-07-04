
from src.environment import userdir
from pystray import Icon, Menu, MenuItem
import subprocess
from PIL import Image
from automat import MethodicalMachine

user_key = None
state=False 


def on_click_available(icon):
    print('UI event: click')
    global state
    state = not state
    if state:
        icon.title = 'Mamman henter oppgave\r\nen linje til'

def on_default(icon):
    print('UI event: Default')

def on_new(icon, item):
    print(icon)
    print(item)
    

def on_exit(icon):
    print('UI event: Exit')
    client_machine.close_application()
    print('UI event: Exited')
    


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




#============================ state machine start
class Client_machine(object):
    from src.api import connection
    from src.crypto import tools
    
    _machine = MethodicalMachine()
    _beans = ""
    _connection = None
    _icon = None
    
#============================ inputs
    @_machine.input()
    def initiate_application(self):
        "Initiate connection to server"
        

    @_machine.input()
    def close_application(self):
        "The user put in some beans."

#============================ outputs
    @_machine.output()
    def _heat_the_heating_element(self):
        "Heat up the heating element, which should cause coffee to happen."
        print("heating turned on")

    @_machine.output()
    def test(self):
        return None    

    @_machine.output()
    def _initiate_application(self):
        "We have a new conection; save it."
        self._connection = self.connection()
        credentials = self.tools(userdir.crypto).get_credentials()
        user_key = self._connection.post('user', credentials)['resource'][0]['key']
        print("setup running")
        self._icon = Icon(name='Mamman',
            icon=Image.open("res\logo_red.png"),
            title='LTS AS, Mamman 0.1'
            )
        self._icon.visible = True
        
        if user_key != None:
            print("ATOMATIC event: User login OK\n", user_key)
            self._icon.icon = Image.open("res\logo_blue.png")
            self._icon.menu = menu_1
            
        

    @_machine.output()
    def _describe_coffee(self):
        return "A cup of coffee made with {}.".format(self._beans)
    
    @_machine.output()
    def _close_icon(self):
        self._icon.menu = None
        self._icon.visible = False
        #self._icon.stop()

    @_machine.serializer()
    def get_state(self, state):
        return state

#============================ states

    @_machine.state(initial=True)
    def starting_application(self):
        "In this state, you have not yet connected"

    @_machine.state()
    def connected_reading(self):
        "In this state, you are connected and you read content from the server."

    @_machine.state()
    def connected_idle(self):
        "In this state, you are connected and you wait for tasks."
        
    @_machine.state()
    def connected_writing(self):
        "In this state, you are connected and write data to server."
        
    @_machine.state()
    def ending_application(self):
        "In this state, you are shutting down the application."
#============================ transitions
    # When we don't any connection, upon connecting, we will be connected
    starting_application.upon(
        initiate_application,
        enter=connected_reading,
        outputs=[
            _initiate_application
            ]
        )

    connected_reading.upon(
        close_application,
        enter=ending_application,
        outputs=[
            _close_icon
            ]
        )
    
    connected_idle.upon(
        close_application,
        enter=ending_application,
        outputs=[
            _close_icon
            ]
        )

#============================ state machine end
    
if __name__=="__main__":
    client_machine = Client_machine()
    client_machine.initiate_application()
