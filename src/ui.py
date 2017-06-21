import pystray
from PIL import Image

class Icon(pystray.Icon):
    def __init__(self):
        super(Icon, self).__init__(
            name='Mamman',
            icon=Image.open("res\logo_red.png"),
            title='LTS AS, Mamman 0.1'
            )
        
def on_new(icon, item):
            print('on_new')

class Menu(pystray.Menu):
#        def __init__(self):
    pass
        
    
