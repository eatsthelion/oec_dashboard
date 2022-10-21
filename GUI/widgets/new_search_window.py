
from math import ceil
from Backend.database import format_data
from GUI.GUI_Mains import FONTBOLD
from GUI.widgets.basics import *
from Backend.search_algorithm import search_algorithm
from GUI.widgets.highlight import rowhighlight, rowhighlightbind
from GUI.window_terminal import TerminalWindow

class SearchWindow(MyFrame):
    def __init__(self, master, dataset_get=None, bg=None, searchsystem = True, 
        pagesystem = True,
        search_alg = search_algorithm, sortfunction = None, 
        filtertypes = ['NAME','TYPE', 'DATE'],
        sorttypes=['SORT BY DATE', 'SORT A➜Z', 'SORT Z➜A'],
        entrylimit = 20, rowheight = 2, columntitles = [], columnwidth = 15,
        skipfields = [], col_color = 'mediumorchid3', 
        leftoptions=None, rightoptions=None, additional_windows = None, 
        format_dict = {}, 
        debug = False,
        **kw) -> None:
        super().__init__(master, bg=bg, **kw)

        # region Initialize Object Attributes 
        self.dataset = []
        self.dataset_get = dataset_get
        self.searchsystem = searchsystem
        self.pagesystem = pagesystem 
        
        self.sortfunction = sortfunction
        self.filtertypes = filtertypes
        self.sorttypes = ['NO SORT'] + sorttypes
        
        if search_alg == None:
            self.search_algorithm = search_algorithm
        else:
            self.search_algorithm = search_alg
        
        # Result Window attributes
        # Action widgets
        self.rightoptions = rightoptions
        self.leftoptions = leftoptions
        self.additional_windows = additional_windows

        # Display attributes
        self.entrylimit = entrylimit
        self.skipfields = skipfields
        self.rowheight = rowheight
        self.columnwidth = columnwidth
        self.format_dict = format_dict

        # Page System attributes
        self.page = 1
        self.index = 0

        # Searching attributes
        self.search_text = ''

        # Sets up the color for background
        self.col_color = col_color

        # Allows for debugging
        self.debug = debug

        # endregion 

        # region Initialize Widgets        
        # region Page System Widgets
        self.pageframe = MyFrame(self)
        self.left_page_button = MyButton(self.pageframe, text = '  <  ',
            bg ='gray90', command = self.previous_page)
        self.right_page_button = MyButton(self.pageframe, text = '  >  ', 
            bg = 'gold1', command = self.next_page)
        self.first_page_button = MyButton(self.pageframe, text = ' << ',
            bg = 'gold1', command = self.first_page)
        self.last_page_button = MyButton(self.pageframe, text=' >> ',
            bg = 'gold1', command = self.last_page)
        self.page_results = MyLabel(self.pageframe, fg='white', 
            text = 'Showing Results')

        self.first_page_button.grid(row=0, column=0, padx=10)
        self.left_page_button.grid(row=0, column=1)
        self.page_results.grid(row=0, column=2, padx = 10)
        self.right_page_button.grid(row=0, column=3)
        self.last_page_button.grid(row=0, column=4, padx=10)
        # endregion 
        # region Result Window Widgets
        self.result_window_frame = MyFrame(self)
        self.containerframe1 = MyFrame(self.result_window_frame)
        self.containerframe2 = MyFrame(self.containerframe1)
        self.result_canvas = MyCanvas(self.containerframe2)
        self.result_frame  = MyFrame(self.result_canvas)

        self.h_scrollbar = MyScrollbar(self.containerframe2, 
            orient='horizontal', command = self._h_scroll)
        self.v_scrollbar = MyScrollbar(self.containerframe1,
            orient='vertical', command = self._v_scroll)

        self.column_canvas = MyCanvas(self.containerframe2)
        self.column_frame = MyFrame(self.column_canvas)
        
        # Result Frame that appears when no results are found
        self.no_results_frame = MyFrame(self)
        self.no_results_label = MyLabel(self.no_results_frame, 
            text='☆  NO RESULTS  ☆', font=FONTBOLD, fg='white')
        self.no_results_label.place(relx=.5, rely=.5, anchor=S)
        
        self.loading_frame = MyFrame(self)
        self.loading_label = MyLabel(self.loading_frame, 
            text='★ ☆ ★ LOADING ★ ☆ ★', font=FONTBOLD, fg='white')
        self.loading_label.place(relx=.5, rely=.5, anchor=CENTER)

        self.column_canvas.pack(fill=BOTH)
        self.result_canvas.pack(fill=BOTH, expand=1)
        self.containerframe1.pack(fill=BOTH, expand=1)
        self.containerframe2.pack(side='left',fill=BOTH, expand=1)
        self.v_scrollbar.pack(side= 'right',fill='y')
        self.h_scrollbar.pack(side='bottom',fill='x')

        # Configures Canvases to Align with the scrollbars
        self.result_canvas.configure(yscrollcommand=self.v_scrollbar.set, 
            xscrollcommand=self.h_scrollbar.set)
        self.result_canvas.bind('<Configure>', 
            lambda e:self.result_canvas.configure(
                scrollregion=self.result_canvas.bbox('all')))
        self.result_canvas.create_window((0,0),window=self.result_frame, 
            anchor=NW)

        self.column_canvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.column_canvas.bind('<Configure>', 
            lambda e:self.column_canvas.configure(
                scrollregion=self.column_canvas.bbox('all')))
        self.column_canvas.create_window((0,0),window=self.column_frame, 
            anchor=NW)
        # endregion
        # region Searchbar Widgets
        self.search_frame = MyFrame(self)
        self.search_bar = MyEntry(self.search_frame)
        self.search_bar.bind("<Return>", self.search_command)
        self.enter_button = MyButton(self.search_frame, text='SEARCH', 
            command=self.search_command)
        self.view_all_button = MyButton(self.search_frame, text='VIEW ALL', 
            command=self.view_all)

        self.bind('<Enter>', self.mousewheel_bind)
        self.bind('<Leave>', self.mousewheel_unbind)

        self.sort_optionmenu = MyOptionMenu(self.search_frame, self.sorttypes)
        self.filter_optionmenu = MyOptionMenu(self.search_frame, self.filtertypes)

        self.search_bar.grid(row=0,column=0,sticky=NS,padx=(5,0))
        self.enter_button.grid(row=0,column=1,padx=5, sticky=NS)

        #self.filter_optionmenu.grid(row=0,column=2, padx=(0,5), sticky=NS)
        self.sort_optionmenu.grid(row=0, column=3, padx=(0,5), sticky=NS)
        
        # endregion
        # region Additional Widgets
        self.optionsframe = MyFrame(self)
        self.refresh_button = MyButton(self, text="REFRESH ↻", 
            command=self.refresh_results)

        if self.additional_windows!=None:
            self.additional_windows(self.optionsframe, self)

        # endregion 
        # endregion 
        
        # region Main Sections Packing

        self.optionsframe.pack(side='top', pady=5, anchor=N)
        if self.pagesystem:
            self.pageframe.pack(side='top', pady=(0,5), anchor=N)
        if self.searchsystem:
            self.search_frame.pack(side='top', anchor=NW, pady=(0,5))
        self.result_window_frame.pack(side='bottom', fill=BOTH, expand=1)
        self.refresh_button.place(x=5, y=10, anchor=NW)
        # endregion

        if dataset_get == None:
            return
        self.dataset = dataset_get()
        if self.pagesystem:
            self.first_page()
        else:
            self.display_sequence(self.dataset)

    # region Display Functions
    def display_sequence(self, dataset, index=0):
        """General sequence of how the result display is created"""

        # Loading screen is raised
        if self.loading_label.cget('text')=='★ ☆ ★ LOADING ★ ☆ ★':
            self.loading_label.configure(text='☆ ★ ☆ LOADING ☆ ★ ☆')
        else:
            self.loading_label.configure(text='★ ☆ ★ LOADING ★ ☆ ★')
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.master.update()
        
        # No Results Screen's place is forgotten
        self.no_results_frame.place_forget()
        self.clear_display()
        try: self.display_results(dataset, index)
        except tk.TclError: pass
        self.loading_frame.place_forget()

    def display_results(self, dataset, index=0):
        # If there is no data, then the No Results Frame will show
        if not dataset:
            self.no_results_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            return False
        
        l_frame_max = 0
        r_frame_max = 0
        num_label_max = 0
        for row, datarow in enumerate(dataset):
            # Displays Result No
            num_label = MyLabel(self.result_frame, text=str(index+1+row)+'.', 
                fg='white')
            num_label.grid(row=row, column=0, sticky=E)

            # Displays Left Widgets
            l_frame = MyFrame(self.result_frame)
            if self.leftoptions!=None:
                self.leftoptions(l_frame,datarow,row)
            l_frame.grid(row=row, column=1, sticky=E)

            for column, data in enumerate(datarow):
                columnstr = str(column)
                if column in self.skipfields: continue
                if columnstr not in self.format_dict:
                    continue
                if "title" not in self.format_dict[columnstr]:
                    continue
                # Initializes the textbox that displays the data
                textbox = MyText(self.result_frame, height=self.rowheight, 
                    relief='solid')

                # Configures the textbox's width
                if "width" in self.format_dict[columnstr]:
                        textbox.configure(width=self.format_dict[columnstr]['width'])
                else:
                    if type(self.columnwidth) is list: 
                        textbox.configure(width = self.columnwidth[column])
                    else: textbox.configure(width = self.columnwidth)

                if 'format' in self.format_dict[columnstr]:
                    data = format_data(data, self.format_dict[columnstr]['format'])

                textbox.insert(data)
                textbox.configure(state=DISABLED)
                textbox.grid(row=row,column=column+2)

                # Highlights the row and column of the  
                rowhighlightbind(textbox)
                textbox.bind("<Button-2>", self.display_to_terminal)
                textbox.bind("<Button-3>", self.display_to_terminal)

            r_frame = MyFrame(self.result_frame)
            if self.rightoptions!=None:
                self.rightoptions(r_frame,dataset)
            r_frame.grid(row=row,column=column+3, sticky=E)

            rowhighlightbind(r_frame)
            rowhighlightbind(l_frame)

            self.master.update()
            
            num_label_max=max(num_label_max, num_label.winfo_width())
            l_frame_max = max(l_frame_max,l_frame.winfo_width())
            r_frame_max = max(r_frame_max,r_frame.winfo_width())
        
        self.master.update()

        for column in range(len(datarow)):
            columnstr = str(column)
            if column in self.skipfields: 
                continue
            if columnstr not in self.format_dict:
                continue
            if 'title' not in self.format_dict[columnstr]:
                continue
            titlebox = MyText(self.column_frame, bg=self.col_color, height=2,
                relief='solid')
            titlebox.grid(row=0, column = column+1)
            
            titlebox.insert(self.format_dict[columnstr]['title'])
            if "width" in self.format_dict[columnstr]:
                titlebox.configure(width=self.format_dict[columnstr]['width'])
            else:
                if type(self.columnwidth) is list: 
                    titlebox.configure(width = self.columnwidth[column])
                else: textbox.configure(width = self.columnwidth)
            titlebox.configure(state=DISABLED)

        self.master.update()

        # Adds bufferboxes to help align the titles and columns
        l_bufferbox = MyFrame(self.column_frame, 
            width=l_frame_max + num_label_max, height=1)
        r_bufferbox = MyFrame(self.column_frame, width=r_frame_max, height=1)
        l_bufferbox.grid(row=0,column=0)
        r_bufferbox.grid(row=0,column=column + 2)

        self.result_canvas.xview_moveto(0)
        self.result_canvas.yview_moveto(0)
        self.column_canvas.xview_moveto(0)
        self.column_canvas.yview_moveto(0)
        self.result_canvas.configure(scrollregion=self.result_canvas.bbox('all'))
        self.column_canvas.configure(scrollregion=self.result_canvas.bbox('all'))

        self.mousewheel_bind()

        self.master.update()
        self.column_canvas.configure(height=self.column_frame.winfo_height())
        return True
    
    def refresh_results(self):
        if self.searchsystem:
            self.view_all_button.grid_remove()
            self.search_bar.delete()

        self.dataset = self.dataset_get()
        if self.pagesystem:
            self.first_page()
        else:
            self.display_sequence(self.dataset)

    def clear_display(self):
        for child in self.result_frame.winfo_children(): 
            self.destroy_children(child)
            child.destroy()
        for child in self.column_frame.winfo_children(): 
            self.destroy_children(child)
            child.destroy()

    def destroy_children(self, widget):
        widget_children = widget.winfo_children()
        if not widget_children: return
        for child in widget_children:
            self.destroy_children(child)
            child.destroy()
    # endregion 
    # region Pagesystem Functions
    def display_page(self):
        self.disable_page_buttons()
        page_results = self.dataset[((self.page-1)*self.entrylimit):
            min(len(self.dataset), (self.page)*self.entrylimit)]
        self.update_result_text()

        #recolors the buttons to signify enable status
        if self.page <= 1: 
            self.page = 1
            self.left_page_button.configure(bg='gray90')
            self.first_page_button.configure(bg='gray90')
        else: 
            self.left_page_button.configure(bg='gold1')
            self.first_page_button.configure(bg='gold1')

        if ((self.page)*self.entrylimit)>=len(self.dataset): 
            self.right_page_button.configure(bg='gray90')
            self.last_page_button.configure(bg='gray90')
        else: 
            self.right_page_button.configure(bg='gold1')
            self.last_page_button.configure(bg='gold1')

        self.display_sequence(page_results, index=(self.page-1)*self.entrylimit)
        self.enable_page_buttons()
    
    def first_page(self, safety=False) -> None:
        """Displays the first page of the results"""
        if (self.page == 1) and safety: 
            return 
        self.page = 1
        self.display_page()

    def last_page(self) -> None:
        """Displays the last page of the results"""
        if ((self.page)*self.entrylimit)>=len(self.dataset): 
            return
        self.page = ceil(len(self.dataset)/self.entrylimit)
        self.display_page()
        
    def next_page(self) -> None:
        """Displays the next page of the results"""
        if ((self.page)*self.entrylimit)>=len(self.dataset): 
            return
        self.page +=1
        self.display_page()

    def previous_page(self) -> None:   
        """Displays the previous page of the results"""     
        if self.page == 1: 
            return       
        self.page -= 1
        self.display_page()

    def update_result_text(self) -> None:
        if len(self.dataset) == 0:
            self.page_results.configure(text = 'No Results')
            return
        if (self.page-1)*self.entrylimit+self.entrylimit > len( self.dataset):
            upperlimit = len(self.dataset)
        else:
            upperlimit = (self.page-1) * self.entrylimit + self.entrylimit
        self.page_results.configure(
            text='Page {} of {}\nShowing Results {}-{} of {}'.format(
                self.page, ceil(len(self.dataset) / float(self.entrylimit)),
                (self.page-1)*self.entrylimit+1, upperlimit, len(self.dataset)))

    def disable_page_buttons(self) -> None:
        """Disables the page button to prevent user for turning pages while 
        the page is still loading"""
        self.left_page_button.configure(command=None)
        self.right_page_button.configure(command=None)

    def enable_page_buttons(self) -> None:
        """Re-enables the page buttons once the page is done loading"""
        self.left_page_button.configure(command=self.previous_page)
        self.right_page_button.configure(command=self.next_page)

    def refresh_page(self) -> None:
        self.dataset = self.dataset_get()
        
        if not self.pagesystem:
            self.display_sequence(self.dataset)
            return
        if ((self.page)*self.entrylimit)>=len(self.dataset)+self.entrylimit:
            self.page -= 1
        self.display_page()
    # endregion


    # region Searching, Sorting, and Filtering Functions
    def view_all(self) -> None:
        self.dataset = self.dataset_get()
        self.search_bar.delete()
        self.search_text = ''
        self.view_all_button.grid_remove()
        if self.pagesystem:
            self.first_page()
        else:
            self.display_sequence(self.dataset)

    def search_command(self, event=None) -> None:
        search_text = self.search_bar.get()
        if search_text == '':
            return False
        if self.search_algorithm == search_algorithm:
            search_results = search_algorithm(self.dataset_get(),
                search_text, skipfields = self.skipfields)
        else:
            search_results = self.search_algorithm(search_text)
        if search_results == False:
            return False

        self.search_text = search_text

        if (self.sort_optionmenu.get()!='NO SORT') and (self.sortfunction!=None):
            search_results = self.sortfunction(self.sort_optionmenu.get(),
                search_results)
        self.dataset.clear()
        self.dataset = search_results
        if self.pagesystem:
            self.first_page()
        else:
            self.display_sequence(search_results)
        self.view_all_button.grid(row=0,column=2, padx=(0,5))
        return

    def sort_command(self, event) -> None:
        if self.sortfunction == None:
            return False
        if self.search_text != '':
            self.search_command(event)
            return
        
        # creates new sorted data
        if self.sort_optionmenu.get() == 'NO SORT':
            self.dataset.clear()
            self.dataset = self.dataset_get()            
        else:
            self.dataset.clear()
            self.dataset = self.sortfunction(self.sort_optionmenu.get(), 
                self.dataset)

        # displays the new sorted data
        if self.pagesystem:
            self.first_page()
        else:
            self.display_sequence(self.dataset)
        return




    # endregion 
    # region Scrolling Functions
    def _h_scroll(self, *args):
        self.result_canvas.xview(*args)
        self.column_canvas.xview(*args)

    def _v_scroll(self, *args):
        self.result_canvas.yview(*args)

    def _on_mousewheely(self, event):
        self.result_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.master.update()        

    def _on_mousewheelx(self, event):
        self.result_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        self.column_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        self.master.update()

    def mousewheel_bind(self, event=False):
        if self.result_canvas.winfo_height()>self.result_frame.winfo_height(): 
            self.result_canvas.unbind_all('<MouseWheel>')
        else: self.result_canvas.bind_all("<MouseWheel>", self._on_mousewheely)
        self.result_canvas.bind_all("<Shift-MouseWheel>",self._on_mousewheelx)

    def mousewheel_unbind(self, event=False):
        self.result_canvas.unbind_all('<MouseWheel>')
        self.result_canvas.unbind_all('<Shift-MouseWheel>')
    # endregion
    # region Zoom Terminal Functions
    def display_to_terminal(self,event):
        data = event.widget.get()
        zoom_window = TerminalWindow(self)
        zoom_window.terminal.print_terminal(data)
        headertext = \
            self.get_column_from_widget(event.widget).strip('\n').upper() + \
            ' OF ' + \
            str(self.get_data_from_widget(event.widget)[1]).strip('\n').upper()

        if len(headertext)>40:
            headertext = headertext[:40]+'...'

        zoom_window.titlelabel.configure(
            text=headertext, font=FONT)
        zoom_window.origin_widget = event.widget
        zoom_window.show_window()
        rowhighlight(None, event.widget, 'gold3', 'gold1')

    def get_data_from_widget(self, widget):
        row_select = widget.grid_info()['row']
        return self.dataset[row_select]

    def get_column_from_widget(self,widget):
        col_select = widget.grid_info()['column'] - 1
        for child in self.column_frame.winfo_children():
            try: 
                if child.grid_info()['column']==col_select:
                    return child.get()
            except AttributeError:
                continue
        return ''

    # endregion 

