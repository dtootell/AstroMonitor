import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from threading import Thread
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import random

class Image(Image):
    #bum: StringProperty()

    def __init__(self,**kwargs):
        super(Image, self).__init__(**kwargs)
        #Thread(target=self.update_image).start()
        Clock.schedule_interval(self.update_image,2)


    def update_image(self,*args):
        #print(*args)
        t=random.randint(1,2)
        time.sleep(0.9)
        if t%2 ==0:
            self.source ='kv/pix/picture.png'
                #self.reload()
        else:
            self.source = 'kv/pix/download.png'
                #self.reload()

        print(t)

class MyApp(App):

    def build(self):
        tip = Image(source = 'kv/pix/dtoot.jpg')
        return tip#Image(source = 'kv/pix/dtoot.jpg')

if __name__ == "__main__":
    MyApp().run()

