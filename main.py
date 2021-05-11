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
    Status_panel_list = ['NC', 'C', 'D', 'A', 'E', 'P', 'BUSY', 'PAUSE', 'DITHER', 'DARV', 'SYNC']
    Status_list = ['NCC', 'IDL', 'BUS', 'CAP', 'E01', 'E02']
    file_exts = ['.fit','.CR2']

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
            # r = self.check_socket()
            # if r:
            self.sock.StrSend('S')
            connect_state = True
            self.connect_label.text = '*** CONNECTED ***'
            self.connect_label.color = [0,1,0,1] #green
            Thread(target=self.get_status2).start()
        except:
            self.connect_label.text = 'No CONNECTION '
            self.connect_label.color = [1, 0, 0, 1] #red

            connect_state = False
        # if connect_state == True:
        #
        #     #Thread(target=self.get_status2).start()




    def get_status(self):
        self.filename= None
        while True:
            # time.sleep(0.5)
            # buffer_S = self.sock.StrSend('S')
            # if buffer_S != None:
            #     self.status_label.text = buffer_S
            time.sleep(0.5)
            buffer_GI = self.sock.StrSend('GI')

            if buffer_GI != None:
                if 'DON' in buffer_GI:
                    self.sock.StrSend('GI')
                    time.sleep(0.5)
                    self.sock.StrSend('GI')
                    time.sleep(0.5)
                    continue
                self.statuspanel_label.text = buffer_GI
                time.sleep(0.5)
                # don = ['DON']
                # if any(x in don for x in buffer_GI):
                #     continue
            time.sleep(0.1)
            self.plan = self.sock.StrSend('GE')

            if self.plan != None:
                if 'DON' in self.plan:
                    self.sock.StrSend('GE')
                    time.sleep(0.5)
                    self.sock.StrSend('GE')
                    time.sleep(0.5)
                    continue
                try:
                    print('selfplan',self.plan)
                    self.plan = int(self.plan)
                    # print("type = ",type(self.plan))
                except:
                    print("conversion error")
                    self.plan = self.sock.StrSend('GE')
                    time.sleep(0.5)
                    self.plan = int(self.plan)
                if type(self.plan) == int:
                    if int(self.plan) > 0:
                        print("Plan running.....display thumbnails")
                        time.sleep(0.5)
                        if int(self.plan)>1:
                            busy_matches = ['BUSY', 'BUSY.']
                            p_match = ['P']
                            d1 = self.sock.StrSend('GI')
                            if d1 != None:
                                l1 = d1.split(' ')
                                print(l1)
                                if any(x in l1 for x in busy_matches):
                                    print('it\'s there!')
                                else:
                                    if any(x in l1 for x in p_match):  #print('not there my friend')
                                        print('Found P, let\'s get file')# d2 = sock.StrSend('S')
                                        self.filename = self.sock.StrSend('G')
                                        print('FILENAME:',self.filename)

                                        # print(d1, '  ', d2, '  ', d3)
                            time.sleep(2.2)

                            if self.filename != None:
                                self.filename = self.filename.replace('\\', '/')
                                drive, path_and_file = os.path.splitdrive(self.filename)
                                path, file = os.path.split(path_and_file)
                                new_loc = path + '/apt_thumbs/'
                                new_loc = drive + new_loc + file
                                self.new_loc = new_loc.replace('fit', 'png')
                                self.new_loc = new_loc.replace('CR2', 'png')
                                print("new path..",self.new_loc)
                                shutil.copy(self.new_loc,"C:/Users/dtoot/Documents/live_image.png")
                                time.sleep(1)



    def get_status2(self):
        while True:
            buffer_S = self.sock.StrSend('S')
            self.check_response(buffer_S)
            time.sleep(0.5)
            buffer_GI = self.sock.StrSend('GI')
            self.check_response(buffer_GI)
            time.sleep(0.5)

    def get_file(self):
        self.filename = self.sock.StrSend('G')
        print('FILENAME:', self.filename)

        if self.filename != None:
            self.filename = self.filename.replace('\\', '/')
            drive, path_and_file = os.path.splitdrive(self.filename)
            path, file = os.path.split(path_and_file)
            new_loc = path + '/apt_thumbs/'
            new_loc = drive + new_loc + file
            self.new_loc = new_loc.replace('fit', 'png')
            self.new_loc = new_loc.replace('CR2', 'png')
            print("new path..", self.new_loc)
            shutil.copy(self.new_loc, "C:/Users/dtoot/Documents/live_image.png")



    def check_response(self,resp):
        while resp != None:
            if 'DON' in resp:
                print('DONE! Photo ready...go grab file!...',resp)
                self.sock.clear_buffer()
                self.get_file()
                return
            if any(x in resp for x in self.Status_list):
                self.statuspanel_label.text = resp
                print('CR1:',resp)
                return
            if any(x in resp for x in self.Status_panel_list):
                self.status_label.text = resp
                print('CR2:',resp)
                return
            if any(x in resp for x in self.file_exts):
                return#self.status_label.text = resp
            else:
                print('else:',resp)



class ImageButton(ButtonBehavior,Image):
    pass

#
class MyImage(Image):

    def __init__(self,**kwargs):
        super(MyImage, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_image, 2)

    def update_image(self,*args):
        self.source = 'C:/Users/dtoot/Documents/live_image.png'
        self.reload()


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