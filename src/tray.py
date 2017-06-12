import pystray
from PIL import Image
from time import sleep

tray = pystray.Icon('test name')

tray.icon = im = Image.open("logo.ico")

tray.run()

sleep(10) # Time in seconds.

#tray.stop() not working
