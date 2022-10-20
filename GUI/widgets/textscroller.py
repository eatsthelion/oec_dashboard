import time
import random
import threading
from datetime import datetime

from GUI.widgets.basics import *
    
class TextScroller(MyFrame):
    def __init__(self, master,bg='blue', fg='white', 
        font = (FONT[0], 16, 'bold'), width = 50,
        text_file =r"./Assets/tips.txt",
        user=None, speed = 1, timer = True, updates=True,
        **kw) -> None:
        super().__init__(master, bg=bg, width=width, **kw)
        
        self.user = user
        self.scroll_start = False
        self.timer = timer
        self.speed = self.init_speed = speed
        self.updates = updates
        self.font = font 
        self.fg = fg
        self.text_file = text_file

        self.mask = MyFrame(self)

    def start(self):
        self.master.update()
        self.on = True
        self.scroll_start = True
        self.create_message(self.user)
        self.message_maker()
        time.sleep(1)
        self.message_label = MyLabel(self, font=self.font, fg=self.fg)
        self.scroll_thread = threading.Thread(daemon=True, 
            target=self.scroll)
        self.scroll_thread.start()
        self.mask.place_forget()

    def stop(self):
        self.on = False
        self.scroll_start = False
        self.message_label.destroy()

    def pause(self, event):
        self.scroll_start = not self.scroll_start

    def fastforward(self, event):
        self.speed = 4 * self.init_speed
    
    def normal_speed(self, event):
        self.speed = self.init_speed

    def message_maker(self):
        self.message_text = ''
        for message in self.message_list:
            if message == '':
                continue
            self.message_text += message + '\t\t'
        self.now = ''
        if self.timer:
            self.now = time.ctime()
            self.message_text = self.now + '\t\t' + self.message_text

    def scroll(self):
        self.message_label.place_forget()
        try:
            while self.on:
                if not self.scroll_start:
                    time.sleep(1)
                    continue
                self.pos = self.winfo_width()
                while self.on and (self.pos >=(0-self.message_label.winfo_width())):
                    if not self.scroll_start:
                        time.sleep(1)
                        continue
                    if self.timer:
                        newtime = time.ctime()
                        self.message_text = self.message_text.replace(self.now, newtime)
                        self.now = newtime
                        self.message_label.configure(text=self.message_text)
                    elif self.now != "":
                        self.message_text=self.message_text.replace(self.now,"")
                        self.now= ""
                        self.message_label.configure(text=self.message_text)

                    # always keeps the message label at the edge of the window if the user
                    # resizes the window
                    if self.pos>self.winfo_width():
                        self.pos = self.winfo_width()

                    self.message_label.place(x=self.pos, rely=.5, anchor=W)

                    self.pos-=self.speed

                    self.master.update()
                    time.sleep(.0005)

                if self.updates:
                    self.create_message(self.user)
                    self.message_maker()
                    self.message_label.configure(text=self.message_text)
        except:
            pass

    def create_message(self, user:str=None):

        with open(self.text_file, 'r') as f:
            self.textlines = f.readlines()
        if user == None:
            user = 'Valued Employee'
        morning_msg = [f'Good Morning, {user}!', f'Magandang umaga, {user}!']
        afternoon_msg=[f'Good afternoon, {user}!', f'Magandang hapon, {user}!']
        evening_msg=[f'Good evening, {user}!',f'Magandang gabi, {user}']
        lunch_msg=[f'It\'s time for lunch, {user}! What will you eat today?', 
            f'Oras na para kumain, {user}!']

        greeting_msg = ''
        now = datetime.now()
        if now.hour < 12:
            greeting_msg = morning_msg[random.randint(0,1)]
        elif now.hour == 12:
            greeting_msg = lunch_msg[random.randint(0,1)]
        elif now.hour > 16:
            greeting_msg = evening_msg[random.randint(0,1)]
        elif now.hour > 12:
            greeting_msg = afternoon_msg[random.randint(0,1)]

        self.message_list = [
            greeting_msg, 
            self.textlines[random.randint(0,len(self.textlines)-1)].strip('\n'),
            ]

        return self.message_list



                


        
