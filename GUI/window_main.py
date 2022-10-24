###############################################################################
# main_window.py
# 
# Created: 8/09/22
# Creator: Ethan de Leon
# Purposes: 
#   - Set the foundational attribues and functions for the Main Window 
#     object
#   - Initializes Pop-up Window parent object to set up pop-up window 
#     attribues, traits, and functions
# Required Installs: pandas, openpyxl
###############################################################################

from GUI.widgets.basics import *
from GUI.widgets.terminal import *
from GUI.widgets.date_entry import *
from GUI.GUI_Mains import FONTBOLD, OECCOLOR

class WindowAttributes(object):
    def __init__(self, master:tk, parent:tk = None, bg:str=OECCOLOR, 
        width:int=500, height:int=500, program_title:str='Untitled', 
        context:str=None, destroy_stop:bool=False, **kw) -> None:
        """Basic Window attributes for all window objects"""

        self.program_title = program_title
        self.master = master
        self.parent = parent 
        self.children = []
        self.data = None
        self.data_dict = {}
        if self.parent != None:
            self.parent.children.append(self)

        # Each window is given the user token at any time
        self.user = self._get_user()
        if self.user != None:
            left_animation_seq = {
                '☆ ★ ★ ★ ★':'★ ★ ★ ★ ★',
                '★ ☆ ★ ★ ★':'☆ ★ ★ ★ ★',
                '★ ★ ☆ ★ ★':'★ ☆ ★ ★ ★',
                '★ ★ ★ ☆ ★':'★ ★ ☆ ★ ★',
                '★ ★ ★ ★ ☆':'★ ★ ★ ☆ ★',
                '★ ★ ★ ★ ★':'★ ★ ★ ★ ☆',
            }
            right_animation_seq = {
                '★ ★ ★ ★ ★':'☆ ★ ★ ★ ★',
                '☆ ★ ★ ★ ★':'★ ☆ ★ ★ ★',
                '★ ☆ ★ ★ ★':'★ ★ ☆ ★ ★',
                '★ ★ ☆ ★ ★':'★ ★ ★ ☆ ★',
                '★ ★ ★ ☆ ★':'★ ★ ★ ★ ☆',
                '★ ★ ★ ★ ☆':'★ ★ ★ ★ ★',
            }
            main = self._find_main()
            self.mainprogram = main
            if program_title.upper() != 'UNTITLED':
                main.load_text.configure(text='LOADING\n'+program_title.upper())
            main.star_txt_right.configure(
                text=right_animation_seq[main.star_txt_right.cget('text')]
            )
            main.star_txt_left.configure(
                text=left_animation_seq[main.star_txt_left.cget('text')]
            )
            master.update()
            #master.after(100)

        self.bg = bg
        self.width = width
        self.height=height

        # Sets up the basic frames containers for each window
        self.shadow_frame = tk.Frame(self.master, bg='black')
        self.frame = tk.Frame(self.master, bg=self.bg)

        # Changes the settings of certain windows under different contexts
        self.context = context

        # Reciever and Sender is are used as channels to communicate between
        # window objects
        self.reciever = None 
        self.sender = None

        # Signal to stop destroying in the window linked list
        self.destroy_stop = destroy_stop

    def _find_main(self):
        try:
            current = self.parent
        except:
            return None
        try:
            while current.parent != None:
                try:
                    current = current.parent
                except:
                    break
            return current
        except:
            return current

    def _get_user(self):
        main = self._find_main()
        if main == None:
            return None
        try:
            return main.user
        except:
            return None

    def delete_children(self):
        WindowAttributes._delete_children(self)
        pass

    def _delete_children(window_object):
        for child in window_object.children:
            WindowAttributes._delete_children(child)
            child.frame.destroy()
            del child

    def send_data(self, data):
        self.sender(data)

    def get_data(self, key, data:tuple or list = None, data_dict:dict = None):
        if data_dict != None:
            index = data_dict.get(key, None)
        else:
            index = self.data_dict.get(key, None)

        if (index != None) and (data != None):
            return data[index]
        elif (index != None):
            return self.data[index]
        else:
            return None
    
class PopupWindow(WindowAttributes):
    def __init__(self, master:tk, canvas:bool = False, 
        configure=lambda:None, **kw) -> None:
        super().__init__(master, **kw)
        # Initial default attributes
        self.configure_var = configure
        self.back_direction = None

        # Initializes Top Navigation Bar
        self.topbuttonframe = MyFrame(self.frame)

        # Initializes Title Label
        self.titlelabel = MyLabel(self.topbuttonframe, font=FONTBOLD)

        # Initializes Navagation Buttons
        self.cancelbutton = MyButton(self.topbuttonframe, text='  X  ', bg='red', 
            command=self.return_to_main_window)
        self.backbutton = MyButton(self.topbuttonframe,text='  ←  ', 
            bg='grey80',command=self.go_back)

        # Creates a default Canvas Window
        self.canvas_window = CanvasWindow(self.frame, bg=self.bg, parent=self)
        self.canvasframe = self.canvas_window.canvasframe

        # Initializes Loading Screen
        self.l_frame = MyFrame(self.frame)
        
        self.load_text = MyLabel(self.l_frame, fg='white', font=FONTBOLD, 
            text='LOADING\n{}'.format(self.program_title.upper()))
        star_txt_left = MyLabel(self.l_frame, fg='white', font=FONTBOLD, 
            text='★ ☆ ★')
        star_txt_right = MyLabel(self.l_frame, fg='white', font=FONTBOLD, 
            text='★ ☆ ★')

        self.l_frame.place(x=0, y=0, relwidth=1, relheight=1, anchor=NW)
        star_txt_left .pack(side=LEFT, expand=1,anchor=E)
        self.load_text.pack(side=LEFT, expand=1,anchor=CENTER)
        star_txt_right.pack(side=LEFT, expand=1,anchor=W)

        # Canvas Placements
        self.topbuttonframe.pack(side=TOP, fill = 'x', anchor = N)
        self.cancelbutton.pack(side=RIGHT, anchor=NE)
        self.backbutton.pack(side=LEFT, anchor=NW)
        self.titlelabel.place(relx=.5, rely=0, anchor=N)
        self.configure()
        #configure() # Allows for custom Widgets and setups
        self.canvas_window.canvas_show()
        self.l_frame.place_forget()
        if len(self.canvasframe.winfo_children()) == 0:
            self.destroy_canvas()
            self.canvas = False
        else:
            self.canvas = True
        

    def configure(self):
        self.configure_var()
        pass
        
    def cancel_window(self):
        """Hides the pop-up window. Does not destroy window."""
        self.frame.place_forget()
        self.shadow_frame.place_forget()
        self.frame.grab_release()

    def destroy_window(self):
        if self.parent != None:
            self.parent.children.remove(self)
        self.frame.destroy()
        self.shadow_frame.destroy()
        self.delete_children()
        del self

    def return_to_main_window(self):
        self.cancel_window()
        current_window = self
        while not current_window.destroy_stop:
            if current_window.parent == None:
                break 
            next_window = current_window.parent
            if next_window.parent == None:
                break
            current_window.destroy_window()
            current_window = next_window

        current_window.frame.focus_set()
        return

    def cancel_window_sequence(self):
        self.cancel_window()

    # Places pop-up window on screen
    def show_window(self):
        """Places pop-up window in the middle of the master"""
        self.frame.place(relx=.5, rely=.5, 
            width= self.width, 
            height=self.height, 
            anchor=CENTER)

        self.master.update()

        self.frame.grab_set()
        self.frame.focus_set()
        self.l_frame.place_forget()
        if self.canvas:
            self.canvas_window.canvas.xview_moveto(0)
            self.canvas_window.canvas.yview_moveto(0)
        
        self.shadow_frame.place(relx = .505, rely=.51,
            width = self.frame.winfo_width(), 
            height = self.frame.winfo_height(),
            anchor=CENTER)
        

    def show_full_window(self):
        """Places the full window on the master"""
        self.l_frame.tkraise(aboveThis=None)
        self.l_frame.place(relx=.5, rely=.5, 
            width= self.width, 
            height=self.height, 
            anchor=CENTER)
        self.master.update()
        self.frame.place(relx=0, rely=0, 
            relwidth=1, relheight=1, anchor=NW)
        self.frame.grab_set()
        self.frame.focus_set()
        self.l_frame.place_forget()

    def canvas_hide(self):
        """Hides the default canvas"""
        self.canvas_window.canvas_hide()

    def canvas_show(self):
        """Displays the default canvas"""
        self.canvas_window.canvas_show()

    def destroy_canvas(self):
        self.canvas_window.containerframe1.destroy()
        self.children.remove(self.canvas_window)
        del self.canvas_window
        
    def hide_back_button(self):
        self.backbutton.pack_forget()

    def show_back_button(self):
        self.backbutton.pack(side=LEFT, anchor=NW)

    def hide_cancel_button(self):
        self.cancelbutton.pack_forget()

    def show_cancel_button(self):
        self.cancelbutton.pack(side=RIGHT, anchor=NE)

    def change_back_button_direction(self, new_direction):
        self.back_direction = new_direction

    def go_back(self):
        if self.back_direction!=None: self.back_direction()
        self.destroy_window()

    def additional_menu_options(self, menu):
        return

    def clearance_check(self, clearance_lvl, data:int or str or list = None):
        if self.user == None:
            return False
        
        if data == None:
            if self.user.data_clearance >= clearance_lvl:
                return True
            else:
                return False

        if isinstance(data, int):
            if  (self.user.data_clearance >= clearance_lvl) or (
                self.user.user_id == data):
                return True
            else:
                return False

        if isinstance(data, str):
            data = [int(x.strip('\n').strip()) for x in data.split(',')]
        
        if (self.user.data_clearance >= clearance_lvl) or (
            self.user.user_id in data):
            return True
        else:
            return False


class CanvasWindow(WindowAttributes):
    def __init__(self,master,**kw) -> None:
        super().__init__(master, **kw)

        self.containerframe1 = tk.Frame(master, bg=self.bg)
        self.containerframe2 = tk.Frame(self.containerframe1, bg=self.bg)
        self.canvas = tk.Canvas(self.containerframe2, bg=self.bg, 
            highlightthickness=0)
        self.canvasframe = tk.Frame(self.containerframe2, bg=self.bg)

        self.h_scrollbar = tk.Scrollbar(self.containerframe2, 
            orient='horizontal',command=self.canvas.xview)
        self.v_scrollbar = tk.Scrollbar(self.containerframe1, 
            orient='vertical',  command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, 
            xscrollcommand=self.h_scrollbar.set)
        self.canvas.bind('<Configure>', 
            lambda e:self.canvas.configure( 
                scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0),
            window=self.canvasframe, anchor=NW)

        self.canvas.place(relx=.5,rely=.5,relheight=1,
            relwidth=1,anchor=CENTER)
        self.containerframe2.pack(side='left',fill=BOTH, expand=1)

        self.containerframe1.bind('<Enter>', self.mousewheel_bind)
        self.containerframe1.bind('<Leave>', self.mousewheel_unbind)
    
    def h_scroll_hide(self):
        self.h_scrollbar.pack_forget()
    def h_scroll_pack(self):
        self.h_scrollbar.pack(side='bottom', fill='x')
    def v_scroll_hide(self):
        self.v_scrollbar.pack_forget()
    def v_scroll_pack(self):
        self.v_scrollbar.pack(side='right', fill='y')

    # Canvas Placements
    def canvas_hide(self):
        self.containerframe1.pack_forget()
    def canvas_show(self):
        self.containerframe1.pack(fill=BOTH, expand=1)

    def mousewheel_bind(self, event=False):
        if self.canvas.winfo_height()>self.canvasframe.winfo_height(): 
            self.canvas.unbind_all('<MouseWheel>')
        else: self.canvas.bind_all("<MouseWheel>", self._on_mousewheely)
        self.canvas.bind_all("<Shift-MouseWheel>",self._on_mousewheelx)

    def mousewheel_unbind(self, event=False):
        self.canvas.unbind_all('<MouseWheel>')
        self.canvas.unbind_all('<Shift-MouseWheel>')

    def _on_mousewheely(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.master.update()        

    def _on_mousewheelx(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        self.master.update()
    
