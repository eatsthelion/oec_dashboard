###############################################################################
# search_window.py
# 
# Created: 8/21/22
# Creator: Ethan de Leon
# Purposes: 
#   - Establishes the Search Window Widget, which is primarily used to display
#     large sets of relational data
#   - Sets up children class objects consisting of
#       - Results Window
#       - Page System
#       - Search System
# Required Installs: None
###############################################################################

import tkinter as tk
from math import ceil
from tkinter import *
from datetime import datetime

from GUI.widgets.terminal import TerminalWindow
from GUI.widgets.highlight import enter_leave_stylechange, rowhighlight, \
    rowhighlightbind
from GUI.GUI_Mains import OECCOLOR, FONT, FONTBOLD
from Backend.search_algorithm import search_algorithm


class SearchWindowAttributes():
    def __init__(self, datasetget = None, dataset=[], 
        searchsystem = True, sorttypes=['SORT BY DATE', 'SORT A➜Z', 'SORT Z➜A'],  
        sortfunction=None, filtertypes = ['NAME','TYPE', 'DATE'], 
        search_alg = search_algorithm,
        pagesystem = True, entrylimit = 20, 
        leftoptions=None, rightoptions=None, rowheight=2, 
        columnwidth=15, columntitles=None, skipfields=[], debug=False, 
        insertGUI = None, modifyGUI = None, additionalPopups = None,
        col_color = 'mediumorchid3', bgcolor = OECCOLOR, **kw):
            
            self.dataset = dataset
            self.datasetget = datasetget
            
            self.sortfunction = sortfunction
            self.filtertypes = filtertypes
            self.sorttypes = ['NO SORT'] + sorttypes
            self.search_algorithm = search_algorithm
            self.debug = debug

            self.insertGUI = insertGUI
            self.modifyGUI = modifyGUI
            self.additionalPopups = additionalPopups

            self.entrylimit = entrylimit

            self.rightoptions = rightoptions
            self.leftoptions = leftoptions

            self.skipfields = skipfields
            self.rowheight = rowheight
            self.columnwidth = columnwidth
            self.columntitles = columntitles    

            self.bgcolor = bgcolor        
            self.col_color = col_color
            if search_alg == None:
                self.search_algorithm = search_algorithm
            else:
                self.search_algorithm = search_alg
    
            
class SearchWindow(SearchWindowAttributes): 
    def __init__(self, master, pagesystem=None, resultwindow=None, searchbar=None, 
        **kw) -> None:
        super().__init__(**kw)
        self.master = master

        self.programframe = tk.Frame(master, bg=self.bgcolor)
        self.loadingframe = tk.Frame(self.programframe, bg=self.bgcolor)

        if (type(pagesystem) != PageSystem) and pagesystem != False:     
            self.pagesystem = PageSystem(self.programframe, parent=self)
        else:   
            self.pagesystem = pagesystem
        if type(resultwindow) != ResultWindow:   
            self.resultwindow = ResultWindow(self.programframe, parent=self,
                bgcolor=self.bgcolor)
        else:   
            self.resultwindow = resultwindow
        if (type(searchbar) != Searchbar) and searchbar != False:
            self.searchbar = Searchbar(self.programframe, parent=self)
        else:   
            self.searchbar = searchbar

        self.terminal_window = TerminalWindow(self.programframe,parent=self, bg='gray60')

        self.refreshbutton = tk.Button(self.programframe, 
            cursor='hand2',bg='white', relief='flat', 
            text="REFRESH ↻", font=(FONT[0],FONT[1]-1), 
            command=self.resultwindow.refresh_results)

        self.optionsframe = tk.Frame(self.programframe, bg=self.bgcolor)

        if self.insertGUI != None: 
            self.insertwindow = self.insertGUI(self.programframe)
            self.insertbutton = tk.Button(self.optionsframe, cursor='hand2',bg='white', relief='flat', text="INSERT NEW ENTRY", font=FONT, command=self.insertwindow.show_window)
            self.insertbutton.pack(side='left', pady=5, anchor=N)
        if self.modifyGUI != None: 
            self.modifywindow = self.modifyGUI(self.programframe)
        if self.additionalPopups!=None: 
            self.additionalPopups(self.optionsframe, self.programframe)

        self.additional_popups()

    def program_start(self):
        if type(self.pagesystem)!=PageSystem: 
            self.resultwindow.display_sequence(self.dataset)
        else:
            self.pagesystem.update_result_text()
            self.pagesystem.initial_settings()
            self.pagesystem.display_page()
        
        self.optionsframe.pack(side='top')
        if self.pagesystem != False:self.pagesystem.frame.pack(side='top',pady=5, anchor=N)
        if self.searchbar != False: self.searchbar.frame.pack(side='top',anchor=NW)
        self.refreshbutton.place(x=5,y=10,anchor=NW)
        self.resultwindow.frame.pack(side='bottom', fill=BOTH,expand=1)

        self.resultframe = self.resultwindow.resultframe

    def additional_popups(self):
        pass

class ResultWindow(SearchWindow):
    def __init__(self, master, parent=None, **kwargs) -> None:
        self.master = master
        self.parent = parent
        if self.parent == None: 
            self.parent = SearchWindow(master, **kwargs, resultwindow=self)

        self.frame = tk.Frame(master, bg=self.parent.bgcolor)
        self.containerframe1 = tk.Frame(self.frame, bg=self.parent.bgcolor)
        self.containerframe2 = tk.Frame(self.containerframe1, bg=self.parent.bgcolor)

        self.resultcanvas = tk.Canvas(self.containerframe2, bg=self.parent.bgcolor,highlightthickness=0)
        self.resultframe = tk.Frame(self.resultcanvas, bg=self.parent.bgcolor)

        self.h_scrollbar = tk.Scrollbar(self.containerframe2, orient='horizontal',command=self.h_scroll)
        self.v_scrollbar = tk.Scrollbar(self.containerframe1, orient='vertical',command=self.v_scroll)
        
        self.columncanvas = tk.Canvas(self.containerframe2, bg=self.parent.bgcolor,highlightthickness=0)
        self.columnframe = tk.Frame(self.columncanvas, bg=self.parent.bgcolor)
        
        self.noresultsframe = tk.Frame(self.frame,bg=self.parent.bgcolor)
        self.noresultslabel = tk.Label(self.noresultsframe, bg=self.parent.bgcolor, text='☆  NO RESULTS  ☆', font=FONTBOLD, fg='white')
        self.noresultslabel.place(relx=.5, rely=.5, anchor=S)

        self.loadingframe = tk.Frame(self.frame,bg=self.parent.bgcolor)
        self.loadinglabel = tk.Label(self.loadingframe, bg=self.parent.bgcolor, text='★ ☆ ★ LOADING ★ ☆ ★', font=FONTBOLD, fg='white')
        self.loadinglabel.place(relx=.5, rely=.5, anchor=S)

        self.columncanvas.pack(fill=BOTH)
        self.resultcanvas.pack(fill=BOTH, expand=1)

        self.containerframe1.pack(fill=BOTH, expand=1)
        self.containerframe2.pack(side='left',fill=BOTH, expand=1)
        
        self.v_scrollbar.pack(side= 'right',fill='y')
        self.h_scrollbar.pack(side='bottom',fill='x')

        self.resultcanvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.resultcanvas.bind('<Configure>', lambda e:self.resultcanvas.configure(scrollregion=self.resultcanvas.bbox('all')))
        self.resultcanvas.create_window((0,0),window=self.resultframe, anchor=NW)

        self.columncanvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.columncanvas.bind('<Configure>', lambda e:self.columncanvas.configure(scrollregion=self.columncanvas.bbox('all')))
        self.columncanvas.create_window((0,0),window=self.columnframe, anchor=NW)

        self.frame.bind('<Enter>', self.mousewheel_bind)
        self.frame.bind('<Leave>', self.mousewheel_unbind)

        self.currentdataset = self.parent.dataset
    
    def refresh_results(self):
        self.parent.dataset = self.parent.datasetget()
        self.currentdataset = self.parent.dataset
        if self.parent.searchbar!=False:
            self.parent.searchbar.viewallbutton.grid_remove()
            self.parent.searchbar.entrybar.delete(0,END)
        if self.parent.pagesystem !=False: 
            self.parent.pagesystem.first_page()
        else:
            self.parent.resultwindow.display_sequence(self.parent.dataset)

    def display_results(self, dataset, index=0):
        if not dataset: 
            self.noresultsframe.place(relx=0,rely=0,relwidth=1, relheight=1)
            return False
        l_frame_max = 0
        r_frame_max = 0
        for row in range(len(dataset)):
            # displays number
            num_label = tk.Label(self.resultframe,
                bg=self.master.cget('background'), 
                font=(FONTBOLD[0],12,'bold'), text=str(index+1+row)+'.', 
                fg='white')
            num_label.grid(row=row, column=0,sticky=E, ipadx=(2,5))

            # displays left options
            l_frame = tk.Frame(self.resultframe, 
                bg=self.master.cget('background'))
            if self.parent.leftoptions!=None: 
                self.parent.leftoptions(l_frame,dataset[row],row)
            l_frame.grid(row=row, column=1, sticky=NS)

            # displays result info
            for column in range(len(dataset[row])):
                if column in self.parent.skipfields: continue
                textbox = tk.Text(self.resultframe,bg='white', 
                    height=self.parent.rowheight, relief="solid", wrap='word', 
                    font=FONT)
                
                if type(self.parent.columnwidth) is list: 
                    textbox.configure(width = self.parent.columnwidth[column])
                else: textbox.configure(width = self.parent.columnwidth)

                data = dataset[row][column]
                data = self.clean_data(data)

                textbox.insert('1.0',data)
                textbox.configure(state=DISABLED)
                textbox.grid(row=row, column=column+2)

                rowhighlightbind(textbox)
                textbox.bind("<Button-2>", self.display_to_terminal)
                textbox.bind("<Button-3>", self.display_to_terminal)

            # displays right options
            r_frame = tk.Frame(self.resultframe, 
                bg=self.master.cget('background'))
            if self.parent.rightoptions!=None: 
                self.parent.rightoptions(r_frame,dataset[row],row)
            r_frame.grid(row=row,column=column+3, sticky=NS)

            self.master.update()

            l_frame_max = max(l_frame_max,l_frame.winfo_width())
            r_frame_max = max(r_frame_max,r_frame.winfo_width())

            rowhighlightbind(r_frame)
            rowhighlightbind(l_frame)
        
        # displays column titles
        self.master.update()

        if self.parent.columntitles==None:
            self.parent.columntitles = []
            for num in range(len(max(dataset))):
                self.parent.columntitles.append(str(num))
        
        for col in range(len(self.parent.columntitles)):
            if col in self.parent.skipfields: continue
            titlebox = tk.Text(self.columnframe,bg=self.parent.col_color, 
                height=2, relief="solid", wrap='word', font=FONT)
            titlebox.grid(row=0, column=col+1)

            if type(self.parent.columnwidth) is list: titlebox.configure(
                width = self.parent.columnwidth[col])
            else: titlebox.configure(width = self.parent.columnwidth,height=1)
            titlebox.insert(INSERT,self.parent.columntitles[col])
        
        self.master.update()

        # Finds the length of the number label
        maxlabelwidth = 0
        for child in self.resultframe.winfo_children(): 
            if type(child)!= tk.Label: continue
            maxlabelwidth = max(maxlabelwidth, child.winfo_width())

        bufferbox1 = tk.Frame(self.columnframe, bg=self.parent.bgcolor, 
            width=l_frame_max+maxlabelwidth,height=titlebox.winfo_height())
        bufferbox1.grid(row=0,column=0)

        bufferbox2 = tk.Frame(self.columnframe, bg=self.parent.bgcolor, 
            width=r_frame_max,height=titlebox.winfo_height())
        bufferbox2.grid(row=0,column=column+2)

        self.resultcanvas.xview_moveto(0)
        self.resultcanvas.yview_moveto(0)
        self.columncanvas.xview_moveto(0)
        self.columncanvas.yview_moveto(0)
        self.resultcanvas.configure(scrollregion=self.resultcanvas.bbox('all'))
        self.columncanvas.configure(scrollregion=self.resultcanvas.bbox('all'))

        self.master.update()
        
        self.mousewheel_bind()
        self.columncanvas.configure(height=self.columnframe.winfo_height())
        return True

    def display_to_terminal(self, event):
        data = event.widget.get("1.0",END)
        self.parent.terminal_window.terminal.print_terminal(data)
        
        headertext = \
            self.get_column_from_widget(event.widget).strip('\n').upper() + \
            ' OF ' + \
            str(self.get_data_from_widget(event.widget)[1]).strip('\n').upper()

        if len(headertext)>40:
            headertext = headertext[:40]+'...'
    
        self.parent.terminal_window.titlelabel.configure(
            text=headertext, font=FONT)
        row_select = event.widget.grid_info()['row']
        col_select = event.widget.grid_info()['column']
        #for child in event.widget.master.winfo_children():
        #    if type(child) == tk.Text:
        #        if child.grid_info()['row'] == row_select:
        #            continue
        #        if child.grid_info()['column'] == col_select:
        #            continue
        #        child.configure(bg='grey80')
        self.parent.terminal_window.origin_widget = event.widget
        self.parent.terminal_window.show_window()
        rowhighlight(None, event.widget, 'gold3', 'gold1')

    def get_data_from_widget(self, widget):
        row_select = widget.grid_info()['row']
        return self.currentdataset[row_select]

    def get_column_from_widget(self,widget):
        col_select = widget.grid_info()['column'] - 1
        for child in self.columnframe.winfo_children():
            try: 
                if child.grid_info()['column']==col_select:
                    return child.get('1.0', END)
            except AttributeError:
                continue
        return ''

    def clear_display(self):
        for child in self.resultframe.winfo_children(): 
            ResultWindow.destroy_children(child)
            child.destroy()
        for child in self.columnframe.winfo_children(): 
            ResultWindow.destroy_children(child)
            child.destroy()

    def destroy_children(widget):
        widget_children = widget.winfo_children()
        if not widget_children: return
        for child in widget_children:
            ResultWindow.destroy_children(child)
            child.destroy()

    def display_sequence(self, dataset, index=0):
        #self.loading_enter_animation()
        if self.loadinglabel.cget('text')=='★ ☆ ★ LOADING ★ ☆ ★':
            self.loadinglabel.configure(text='☆ ★ ☆ LOADING ☆ ★ ☆')
        else:
            self.loadinglabel.configure(text='★ ☆ ★ LOADING ★ ☆ ★')
        self.loadingframe.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.master.update()

        self.noresultsframe.place_forget()
        self.clear_display()
        try: self.display_results(dataset, index)
        except tk.TclError: pass
        #self.loading_exit_animation()
        self.loadingframe.place_forget()
   
    def loading_enter_animation(self):
        placement = 0
        while placement<1:
            self.loadingframe.place(relx=0, rely=placement, 
                relwidth=1, relheight=1)
            placement += .001
            self.master.update()
            self.master.after(10)
    
    def loading_exit_animation(self):
        placement = 1
        while placement<0:
            self.loadingframe.place(relx=0, rely=placement, 
                relwidth=1, relheight=1)
            placement -= .001
            self.master.update()
            self.master.after(10)

    def clean_data(self,data):
        # for empty datafield
        if (data=="")or(data==None): 
            data="N/A"
        # reformats dates if needed
        try:
            data = datetime.strptime(data,'%Y-%m-%d %H:%M:%S')
            data = data.strftime('%m/%d/%y %I:%M:%S %p')
        except: pass
        try:
            data = datetime.strptime(data,'%Y-%m-%d')
            data = data.strftime('%m/%d/%y')
        except: pass
        return str(data)

    def h_scroll(self, *args):
        self.resultcanvas.xview(*args)
        self.columncanvas.xview(*args)

    def v_scroll(self, *args):
        self.resultcanvas.yview(*args)

    def _on_mousewheely(self, event):
        self.resultcanvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.master.update()        

    def _on_mousewheelx(self, event):
        self.resultcanvas.xview_scroll(int(-1*(event.delta/120)), "units")
        self.columncanvas.xview_scroll(int(-1*(event.delta/120)), "units")
        self.master.update()

    def mousewheel_bind(self, event=False):
        if self.resultcanvas.winfo_height()>self.resultframe.winfo_height(): 
            self.resultcanvas.unbind_all('<MouseWheel>')
        else: self.resultcanvas.bind_all("<MouseWheel>", self._on_mousewheely)
        self.resultcanvas.bind_all("<Shift-MouseWheel>",self._on_mousewheelx)

    def mousewheel_unbind(self, event=False):
        self.resultcanvas.unbind_all('<MouseWheel>')
        self.resultcanvas.unbind_all('<Shift-MouseWheel>')

class PageSystem(SearchWindow):
    def __init__(self,master, parent, **kwargs):
        self.page = 1
        self.master = master
        self.parent = parent
        if self.parent == None: self.parent = SearchWindow(master, **kwargs, pagesystem = self)

        self.frame = tk.Frame(master, bg=master.cget('background')) 
        self.leftpagebutton  = tk.Button(self.frame,cursor='hand2',relief='flat', text = '  <  ', font=FONT,bg='gray90', command=self.previous_page)
        self.rightpagebutton = tk.Button(self.frame,cursor='hand2',relief='flat', text = '  >  ', font=FONT,bg='gold1' , command=self.next_page)
        self.firstpagebutton = tk.Button(self.frame,cursor='hand2',relief='flat', text = ' << ', font=FONT,bg='gold1' , command=lambda: self.first_page(safety=True))
        self.lastpagebutton  = tk.Button(self.frame,cursor='hand2',relief='flat', text = ' >> ', font=FONT,bg='gold1' , command=self.last_page)
        self.resulttext = tk.Label(self.frame, bg=master.cget('background'), text = 'Showing Results', font=FONT, fg='white')

        enter_leave_stylechange(self.leftpagebutton , enter='underline')
        enter_leave_stylechange(self.rightpagebutton, enter='underline')
        enter_leave_stylechange(self.firstpagebutton, enter='underline')
        enter_leave_stylechange(self.lastpagebutton , enter='underline')

        self.firstpagebutton .grid(row=0,column=0,padx=10)
        self.leftpagebutton .grid(row=0,column=1,)
        self.resulttext.grid(row=0,column=2, padx=10)
        self.rightpagebutton.grid(row=0,column=3,)
        self.lastpagebutton.grid(row=0,column=4,padx=10)

        pass

    def initial_settings(self):
        if len(self.parent.resultwindow.currentdataset)>=self.parent.entrylimit: 
            self.firstpagebutton .grid(row=0,column=0,padx=10)
            self.leftpagebutton .grid(row=0,column=1,)
            self.resulttext.grid(row=0,column=2, padx=10)
            self.rightpagebutton.grid(row=0,column=3,)
            self.lastpagebutton.grid(row=0,column=4,padx=10)
            return
        self.leftpagebutton .grid_forget()
        self.rightpagebutton.grid_forget()
        self.resulttext     .grid_forget()
        self.lastpagebutton .grid_forget()
        self.firstpagebutton.grid_forget()
    
    def first_page(self, safety=False):
        if (self.page == 1) and safety: return 
        self.page = 1
        self.display_page()

    def last_page(self):
        if ((self.page)*self.parent.entrylimit)>=len(self.parent.resultwindow.currentdataset): return
        self.page = ceil(len(self.parent.resultwindow.currentdataset)/self.parent.entrylimit)
        self.display_page()
        
    def next_page(self):
        if ((self.page)*self.parent.entrylimit)>=len(self.parent.resultwindow.currentdataset): return
        self.page +=1
        self.display_page()

    def previous_page(self):        
        if self.page == 1: return       
        self.page-=1
        self.display_page()
    
    def display_page(self):
        self.disable_page_buttons()
        page_results = self.datapage_select()
        self.update_result_text()

        #recolors the buttons to signify enable status
        if self.page <= 1: 
            self.page = 1
            self.leftpagebutton.configure(bg='gray90')
            self.firstpagebutton.configure(bg='gray90')
        else: 
            self.leftpagebutton.configure(bg='gold1')
            self.firstpagebutton.configure(bg='gold1')

        if ((self.page)*self.parent.entrylimit)>=len(
            self.parent.resultwindow.currentdataset): 
            self.rightpagebutton.configure(bg='gray90')
            self.lastpagebutton.configure(bg='gray90')
        else: 
            self.rightpagebutton.configure(bg='gold1')
            self.lastpagebutton.configure(bg='gold1')
        
        self.parent.resultwindow.display_sequence(
            page_results, index=(self.page-1)*self.parent.entrylimit)
        self.enable_page_buttons()

    def datapage_select(self): 
        if len(self.parent.resultwindow.currentdataset) <= \
            (self.page)*self.parent.entrylimit:
            upperlimit = len(self.parent.resultwindow.currentdataset)
        else: 
            upperlimit = (self.page)*self.parent.entrylimit
        return self.parent.resultwindow.currentdataset[
            ((self.page-1)*self.parent.entrylimit):upperlimit]

    def disable_page_buttons(self):
        self.leftpagebutton.configure(command=None)
        self.rightpagebutton.configure(command=None)

    def enable_page_buttons(self):
        self.leftpagebutton.configure(command=self.previous_page)
        self.rightpagebutton.configure(command=self.next_page)

    def update_result_text(self):
        if len(self.parent.resultwindow.currentdataset) == 0:
            self.resulttext.configure(
                text = 'No Results'
            )
            return
        if (self.page-1)*self.parent.entrylimit+self.parent.entrylimit > \
            len( self.parent.resultwindow.currentdataset):
            upperlimit = len(self.parent.resultwindow.currentdataset)
        else:
            upperlimit = (self.page-1) * self.parent.entrylimit + \
                self.parent.entrylimit
        self.resulttext.configure(
            text='Page {} of {}\nShowing Results {}-{} of {}'.format(
                self.page,
                ceil(len(self.parent.resultwindow.currentdataset) / \
                    float(self.parent.entrylimit)),
                (self.page-1)*self.parent.entrylimit+1,
                upperlimit,
                len(self.parent.resultwindow.currentdataset)
                ))

class Searchbar(SearchWindow):
    def __init__(self,master, parent=None, **kwargs) -> None:
        self.parent = parent
        if self.parent == None: 
            self.parent = SearchWindow(master, **kwargs, searchbar=self)
        if self.parent.sortfunction == None: 
            self.parent.sortfunction = self.default_sort

        self.frame = tk.Frame(master, bg = master.cget('background'))
        self.entrybar = tk.Entry(self.frame, font=FONT)
        self.entrybar.bind('<Return>',self.search_command)
        self.enterbutton   = tk.Button(self.frame,cursor='hand2', relief='flat', text="SEARCH",   font=(FONT[0],FONT[1]+2), command=self.search_command)
        self.viewallbutton = tk.Button(self.frame,cursor='hand2', relief='flat', text='VIEW ALL', font=(FONT[0],FONT[1]+2), command=self.view_all)

        self.sortvar = tk.StringVar(value=self.parent.sorttypes[0])
        self.sortOptions = tk.OptionMenu(self.frame, self.sortvar, *self.parent.sorttypes, command=self.sort_command)
        self.sortOptions.config(font=(FONT[0],FONT[1]+2), relief = 'flat',indicatoron=0, cursor='hand2')
        self.sortmenu = self.frame.nametowidget(self.sortOptions.menuname)
        self.sortmenu.config(font=(FONT[0],FONT[1]))

        self.sortvar.trace('w',lambda n, m, o: self.sort_command)

        self.filtervar = tk.StringVar(value=self.parent.filtertypes[0])
        self.filterOptions = tk.OptionMenu(self.frame, self.filtervar, *self.parent.filtertypes)
        self.filterOptions.config(font=(FONT[0],FONT[1]+2), relief = 'flat',indicatoron=0, cursor='hand2')
        self.filtermenu = self.frame.nametowidget(self.filterOptions.menuname)
        self.filtermenu.config(font=(FONT[0],FONT[1]))
        
        enter_leave_stylechange(self.enterbutton,  enter="underline")
        enter_leave_stylechange(self.viewallbutton,enter="underline")
        enter_leave_stylechange(self.sortOptions,  enter="underline")
        enter_leave_stylechange(self.filterOptions,  enter="underline")

        self.entrybar.grid(row=0,column=0,sticky=NS, padx=(5,0), pady=5, ipadx=5)
        self.enterbutton.grid(row=0,column=1, padx=5, pady=5)
        self.sortOptions.grid(row=0,column=3, padx=(0,5), pady=5, sticky=NS)
        #self.filterOptions.grid(row=0,column=4,padx=(0,5), pady=5, sticky=NS)

    def view_all(self):
        self.parent.resultwindow.currentdataset = self.parent.dataset
        self.nosortdataset = self.parent.dataset
        if self.sortvar.get()!='NO SORT':  self.parent.resultwindow.currentdataset = self.parent.sortfunction(self.sortvar.get(),self.parent.resultwindow.currentdataset)
        if self.parent.pagesystem != False: self.parent.pagesystem.first_page()
        else:
            self.parent.resultwindow.display_sequence(self.parent.resultwindow.currentdataset)
        self.entrybar.delete(0,END)
        self.hide_viewall()

    def hide_viewall(self): self.viewallbutton.grid_remove()
    def show_viewall(self): self.viewallbutton.grid(row=0,column=2, padx=(0,5))

    def search_command(self,event=None):
        searched_dataset = self.parent.search_algorithm(
            self.parent.dataset, self.entrybar.get(), self.parent.skipfields)
        if searched_dataset == False: return False
        self.nosortdataset = searched_dataset
        if self.sortvar.get()!='NO SORT':  
            searched_dataset = self.parent.sortfunction(
                self.sortvar.get(),searched_dataset)
        
        # updates the window's current dataset
        self.parent.resultwindow.currentdataset = searched_dataset

        if self.parent.pagesystem == False: 
            self.parent.resultwindow.display_sequence(searched_dataset)
        else: 
            self.parent.pagesystem.first_page()
        self.show_viewall()
        pass

    def default_sort(self,sortby,dataset):
        if sortby == 'SORT BY DATE':pass #dataset.sort(key=lambda i: datetime.strptime(i[6], "%m%d%y"), reverse=True)
        elif sortby == 'SORT BY A➜Z': dataset.sort(key=lambda i:i[0])
        elif sortby == 'SORT BY Z➜A':  dataset.sort(key=lambda i:i[0],reverse=True)
        return dataset

    def sort_command(self,event=None):
        if self.sortvar.get()=='NO SORT': self.parent.resultwindow.currentdataset = self.nosortdataset
        else: self.parent.resultwindow.currentdataset = self.parent.sortfunction(self.sortvar.get(),self.parent.resultwindow.currentdataset)
        
        if self.parent.pagesystem!=False: self.parent.pagesystem.first_page()
        else: 
            self.parent.resultwindow.display_sequence(self.parent.resultwindow.currentdataset)

if __name__ == '__main__':
    root = tk.Tk()
    program = SearchWindow(root, debug=True)
    program.programframe.pack(fill=BOTH,expand=1)
    program.program_start()
    tk.mainloop()

