# -*- coding: utf-8 -*
"""Main part of the Mamman application

This module encapsulates the UI and the state-machine for application control

Example:
 python main.py

Todo:
    * Populate menu-array
    * Finish PDF process

More info:
   https://lts.no
   https://github.com/lts-as

"""

import subprocess
from src.environment import userdir
from pystray import Icon, Menu, MenuItem
from PIL import Image
from automat import MethodicalMachine
from yapsy.PluginManager import PluginManager
from os import getcwd, path, sys


user_key = None
state = False
client_machine = None

#============================ tools start
def tracer(old_state, input, new_state):
    "Tracer function for debugging"
    print("old_state:", old_state, "input:", input, "new state:", new_state)
#============================ tools end
#============================ event handelers start
def event_click_available():
    "UI event: User is enabeling the available flag"
    print('UI event: click')
    global state
    state = not state

def event_default():
    "UI event: Single click on icon"
    
    #For windows
    if "WIN" in sys.platform.upper():
      os.startfile('https://lts.no/produkter/mamman')
    else:	#Linux or mac
      subprocess.call(['xdg-open','https://lts.no/produkter/mamman'])
    

def event_ready():
    "Event: Mamman is ready for use"
    client_machine.reading_finished()

def event_new_process(icon, item):
    "UI event: Establish new process"
    print(icon)
    print(item)

def event_open_task(icon, item):
    "UI event: Open task folder"
    print(icon)
    print(item)

def event_exit():
    "UI event: Exit"
    client_machine.close_application()

def event_click_open_dir(icon, tasting):
    "UI event: Open working directory"
    print('UI event: Open working directory')
    subprocess.Popen('explorer "' + userdir.workspace + '"')
#============================ event handelers end
#============================ state machine start
class clientMachine(object):
    "Finite state-machine for the Mamman client"
    from src.api import connection
    from src.crypto import tools

    _machine = MethodicalMachine()
    _connection = None
    _icon = None
    _plugin_manager = PluginManager()

    setTrace = _machine._setTrace # making trace-function available. Usefull debugging feature

#============================ inputs
    @_machine.input()
    def initiate_application(self):
        "Initiate connection to server"

    @_machine.input()
    def reading_finished(self):
        "Add tasks to menu"

    @_machine.input()
    def toggle_available(self):
        "Toggle availability flag"

    @_machine.input()
    def close_application(self):
        "The user put in some beans."

#============================ outputs
    @_machine.output()
    def _initiate_application(self):
        "Establish all parts of the application"
        self._icon = Icon(name='Mamman',
                          icon=Image.open(path.join('res','logo_yellow.png')),
                          title='LTS AS, Mamman 0.1')
        self._icon.visible = True
        self._icon.menu = Menu(MenuItem('Avslutt Mamman', event_exit))

        self._plugin_manager.setPluginPlaces([path.join(getcwd(), "src", "plugins")]) # Find plugins
        self._plugin_manager.collectPlugins() # Load plugins
        for _pluginInfo in self._plugin_manager.getAllPlugins(): # Activate plugins
            self._plugin_manager.activatePluginByName(_pluginInfo.name)
        event_ready() # Mark that the process is finished by trigging an event
        self._icon.run() #_icon.run is last because it is not ending before _icon.stop

    @_machine.output()
    def _verify_user(self):
        "Connect to API and verify user"
        self._connection = self.connection()
        credentials = self.tools(userdir.crypto).get_credentials()
        user_key = self._connection.post('user', credentials)['resource'][0]['key']
        if user_key != None:
            print("ATOMATIC event: User login OK\n", user_key)

    @_machine.output()
    def _list_tasks(self):
        "Populate tasks in the the icon menu"
        self._icon.icon = Image.open(path.join('res','logo_blue.png'))
        self._icon.menu = Menu(
            MenuItem('Hent oppgave', Menu(
                MenuItem('2t, gjennomgang av revisjon', event_open_task),
                MenuItem('1t, gjennomgang av revisjon', event_open_task)
            )),
            MenuItem('Ny prosess', Menu(
                MenuItem('Gjennomgang', event_new_process),
                MenuItem('EPLAN prosjekt', event_new_process)
            )),
            MenuItem('Jeg er tilgjengelig', event_click_available, checked=lambda self: state, enabled=lambda self: state),
            MenuItem('Jeg er tilgjengelig', event_click_available, checked=lambda item: state),
            MenuItem('Avslutt Mamman', event_exit),
            MenuItem('Default click', event_default, default=True, visible=False))

    @_machine.output()
    def _close_application(self):
        "Close the application"
        self._icon.menu = None
        #self._icon.visible = False
        self._icon.stop()

    @_machine.serializer()
    def get_state(self, state):
        "Returning the internal machine state"
        return state

#============================ states

    @_machine.state(initial=True)
    def starting(self):
        "In this state, you have not yet connected"

    @_machine.state()
    def reading(self):
        "In this state, you are loading tasks"

    @_machine.state()
    def listing(self):
        "In this state, the UI lists available tasks"

    @_machine.state()
    def working(self):
        "In this state, you are working on a task"

    @_machine.state()
    def ending(self):
        "In this state, you are shutting down the application."
#============================ transitions
    # When we don't any connection, upon connecting, we will be connected
    starting.upon(
        initiate_application,
        enter=reading,
        outputs=[
            _initiate_application
            ]
        )

    starting.upon(
        close_application,
        enter=ending,
        outputs=[
            _close_application
            ]
        )

    reading.upon(
        close_application,
        enter=ending,
        outputs=[
            _close_application
            ]
        )

    reading.upon(
        reading_finished,
        enter=listing,
        outputs=[
            _list_tasks
            ]
        )

    listing.upon(
        close_application,
        enter=ending,
        outputs=[
            _close_application
            ]
        )

#============================ state machine end

if __name__ == "__main__":
    client_machine = clientMachine()
    client_machine.setTrace(tracer)
    client_machine.initiate_application()
