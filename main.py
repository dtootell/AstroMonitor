import time
import kivy
from client import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from threading import Thread
from kivy.clock import Clock
from kivy.properties import ObjectProperty

#
# class Label(Label):
#     pass


class ConnectButton(ButtonBehavior, Image):

    status_label: ObjectProperty()
    connect_label: ObjectProperty()
    ip_label: ObjectProperty()
    statuspanel_label: ObjectProperty()

    def __init__(self, **kwargs):
        super(ConnectButton, self).__init__(**kwargs)

    def on_press(self):
        self.source = "kv/icons/link.png"
        self.iptext = self.ip_label.text

    def on_release(self):
        self.source = "kv/icons/link_white.png"
        self.sock = MySocket(self.iptext)
        try:
            self.sock.StrSend('0')
            connect_state = True
            self.connect_label.text = '*** CONNECTED ***'
            self.connect_label.color = [0,1,0,1] #green
        except:
            self.connect_label.text = 'No CONNECTION '
            self.connect_label.color = [1, 0, 0, 1] #red

            connect_state = False
        if connect_state == True:

            Thread(target=self.get_status).start()

    def get_status(self):
        while True:
            time.sleep(0.2)
            self.status_label.text = self.sock.StrSend('S')
            time.sleep(0.2)
            self.statuspanel_label.text = self.sock.StrSend('GI')


class ImageButton(ButtonBehavior,Image):
    pass
#
#     statuspanel_label: ObjectProperty()
#     # connect_label: ObjectProperty()
#     # ip_label: ObjectProperty()
#
#     def __init__(self, **kwargs):
#         super(ImageButton, self).__init__(**kwargs)
#
#     def on_press(self):
#         self.source = "kv/icons/shortlist.png"
#
#
#     def on_release(self):
#         self.source = "kv/icons/shortlist_white.png"
#         Thread(target=self.get_status1).start()
#
#     def get_status1(self):
#         while True:
#             time.sleep(2)
#             self.statuspanel_label.text = ConnectButton.on_release.MySocket.StrSend('GI')
#             time.sleep(0.2)
#


class AstroMonitorApp(App):
    def build(self):
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    AstroMonitorApp().run()