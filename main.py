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

user_key = None
state = False
client_machine = None

traces = []

def tracer(old_state, input, new_state):
    "Tracer function for debugging"
    traces.append((old_state, input, new_state))
    print("input:", input, "new state:", new_state)
    return None # "I only care about inputs, not outputs"


def on_click_available(icon):
    "UI event: User is enabeling the available flag"
    print('UI event: click')
    global state
    state = not state
    if state:
        icon.title = 'Mamman henter oppgave\r\nen linje til'

def on_default():
    "UI event: Single click event. Not used yet."
    print('UI event: Default')

def on_new_process(icon, item):
    "UI event: Establish new process"
    print(icon)
    print(item)

def on_open_task(icon, item):
    "UI event: Open task folder"
    print(icon)
    print(item)

def on_exit():
    "UI event: Exit"
    client_machine.close_application()

def on_click_open_dir(icon, tasting):
    "UI event: Open working directory"
    print('UI event: Open working directory')
    subprocess.Popen('explorer "' + userdir.workspace + '"')

menu_1 = Menu(
    MenuItem('Åpne arbeidsmappe', on_click_open_dir),
    MenuItem('Hent oppgave', Menu(
        MenuItem('2t, gjennomgang av revisjon', on_open_task),
        MenuItem('1t, gjennomgang av revisjon', on_open_task)
    )),
    MenuItem('Ny prosess', Menu(
        MenuItem('Gjennomgang', on_new_process),
        MenuItem('EPLAN prosjekt', on_new_process)
    )),
    MenuItem('Jeg er tilgjengelig', on_click_available, checked=lambda item: state),
    MenuItem('Avslutt Mamman', on_exit),
    MenuItem('Default click', on_default, default=True, visible=False))

#============================ state machine start
class clientMachine(object):
    "Finite state-machine for the Mamman client"
    from src.api import connection
    from src.crypto import tools

    _machine = MethodicalMachine()
    _connection = None
    _icon = None

    setTrace = _machine._setTrace # making trace-function available. Usefull debugging feature

#============================ inputs
    @_machine.input()
    def initiate_application(self):
        "Initiate connection to server"

    @_machine.input()
    def toggle_available(self):
        "Toggle availability flag"

    @_machine.input()
    def close_application(self):
        "The user put in some beans."

#============================ outputs
    @_machine.output()
    def _initiate_application(self):
        "Establish the icon"
        self._icon = Icon(name='Mamman',
                          icon=Image.open("res\logo_yellow.png"),
                          title='LTS AS, Mamman 0.1')
        self._icon.visible = True
        #self._icon.icon = Image.open("res\logo_blue.png")
        self._icon.menu = Menu(MenuItem('Avslutt Mamman', on_exit))
        self._icon.run()
        ##TODO: flag finished

    @_machine.output()
    def _verify_user(self):
        "Connect to API and verify user"
        self._connection = self.connection()
        credentials = self.tools(userdir.crypto).get_credentials()
        user_key = self._connection.post('user', credentials)['resource'][0]['key']
        if user_key != None:
            print("ATOMATIC event: User login OK\n", user_key)


    @_machine.output()
    def _close_application(self):
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
        "In this state, you are connected and you read content from the server."

    @_machine.state()
    def idle(self):
        "In this state, you are connected and you wait for tasks."

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

    idle.upon(
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
