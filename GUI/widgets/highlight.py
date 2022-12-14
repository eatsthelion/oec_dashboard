import re
from GUI.widgets.basics import *

def enter_leave_stylechange(widget, enter=None, leave=None):
    widget.bind("<Enter>", lambda m: widget_stylechange(widget, style=enter))
    widget.bind("<Leave>", lambda m: widget_stylechange(widget, style=leave))

def widget_stylechange(widget, style=None):
    fontstyle = widget.cget('font')
  
    font = re.findall(r'\{.*?\}',fontstyle)
    font = font[0].strip('{').strip('}')

    size = ""
    for ch in fontstyle:
        if ch.isdigit(): size+=ch
    if style == None: widget.configure(font=(font, int(size)))
    else: widget.configure(font=(font, int(size), style))

def rowhighlightbind(widget,selectcolor = 'gold2', 
    highlightcolor='lightgoldenrod1',normalcolor='white'):
    widget.bind('<Enter>',lambda name=None,index=None, mode=None,ev=widget, 
        color = highlightcolor: rowhighlight(True,ev,color,selectcolor))
    widget.bind('<Leave>',lambda name=None,index=None,mode=None,ev=widget,
        color = normalcolor:rowhighlight(True,ev,color,color))

def rowhighlight(event,widget,color,selectcolor,labelstyle=None,column=True):
    widgetarray = []
    selectrow = widget.grid_info()['row']
    selectcolumn = widget.grid_info()['column']
    for child in widget.master.winfo_children():
        if not (isinstance(child, Label) or isinstance(child,Text)): 
            continue

        childinfo = child.grid_info()
        try:
            if childinfo['row']==selectrow: widgetarray.append(child)
            if (childinfo['column']==selectcolumn) and column: 
                widgetarray.append(child)
        except: pass

    for selectwidget in widgetarray:
        if isinstance(selectwidget, Entry):  
            selectwidget.configure(readonlybackground=color,
                disabledbackground=color)
        elif isinstance(selectwidget, Text): 
            selectwidget.configure(background=color)
        elif isinstance(selectwidget, Label): 
            selectwidget.configure(fg=color)
            if labelstyle!=None: selectwidget.configure(font=labelstyle)

    if isinstance(widget, Label) or isinstance(widget, Text): 
        widget.configure(background=selectcolor)
