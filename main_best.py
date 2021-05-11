import time,shutil,random
import kivy
from client import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from threading import Thread
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.cache import Cache
import os,re
#
# class Label(Label):
#     pass


class ConnectButton(ButtonBehavior, Image):

    #status_label: ObjectProperty()
    #connect_label: ObjectProperty()
    #ip_label: ObjectProperty()
    #statuspanel_label: ObjectProperty()
   # latest_image: ObjectProperty()

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
        t=1
        while True:
            time.sleep(0.2)
            self.status_label.text = self.sock.StrSend('S')
            time.sleep(0.2)
            self.statuspanel_label.text = self.sock.StrSend('GI')
            time.sleep(0.2)
            #self.filename = self.sock.StrSend('G')
            #print(self.filename)
            # if t%2 == 0:
            #
            #     #self.filename = "C:/Users/dtoot/Documents/download.png"
            #     shutil.copy("C:/Users/dtoot/Documents/download.png","C:/Users/dtoot/Documents/live_image.png")
            #
            # else:
            #     #self.filename = "C:/Users/dtoot/Documents/picture.png"
            #     shutil.copy("C:/Users/dtoot/Documents/picture.png", "C:/Users/dtoot/Documents/live_image.png")
            # # self.filename = self.filename.replace("fit","png")
            # # self.filename = self.filename.replace("\\", "/")
            # # print(self.filename)
            # # self.source = self.filename
            # self.latest_image.source = "C:/Users/dtoot/Documents/live_image.png"
            # self.latest_image.reload()
            #
            # print(self.latest_image.source)
            # t+=1


class ImageButton(ButtonBehavior,Image):
    pass

#
class MyImage(Image):
    #location = "C:/Users/dtoot/Documents/picture.png"
    # latest_image: StringProperty('C:\/Users\/dtoot/Documents/picture.png')
    # latest_image: StringProperty(raw('C:\\Users\\dtoot\\Documents\\picture.png'))
    #latest_image:ObjectProperty()
    # latest_image:StringProperty()#'C:/Users/dtoot/Documents/picture.png')

    def __init__(self,**kwargs):
        super(MyImage, self).__init__(**kwargs)
        #Thread(target=self.update_image).start()
        Clock.schedule_interval(self.update_image, 2)

    def update_image(self,*args):
        print(*args)
        t = random.randint(1, 2)
        time.sleep(0.9)
        if t % 2 == 0:
            self.source = 'kv/pix/picture.png'
            # self.reload()
        else:
            self.source = 'kv/pix/download.png'
            # self.reload()

        print(t)



class AstroMonitorApp(App):

    def build(self):
        return Builder.load_file("main.kv")



if __name__ == "__main__":
    AstroMonitorApp().run()





    #
    # def update_image(self,*args):
    #     t = 1
    #     while True:
    #
    #         time.sleep(0.9)
    #         # self.filename = self.sock.StrSend('G')
    #         # print(self.filename)
    #         if t % 2 == 0:
    #             self.source = "kv/pix/picture.png"
    #             #self.filename = "kv/pix/picture.png"
    #             #shutil.copy("C:/Users/dtoot/Documents/download.png", "C:/Users/dtoot/Documents/live_image.png")
    #             print('even')
    #
    #         else:
    #             self.source = "kv/pix/download.png"
    #
    #             #self.filename = "kv/pix/download.png"
    #             #shutil.copy("C:/Users/dtoot/Documents/picture.png", "C:/Users/dtoot/Documents/live_image.png")
    #             print('odd')
    #         # self.filename = self.filename.replace("fit","png")
    #         # self.filename = self.filename.replace("\\", "/")
    #
    #         #self.latest_image.source = self.filename
    #         #print('Before',self.children)
    #         #self.source = "C:/Users/dtoot/Documents/live_image.png"
    #         #self.latest_image.source = "kv/pix/dtoot.jpg"
    #         #self.reload()
    #
    #         #print('aftere',self.ids)
    #         print(t)
    #         t += 1