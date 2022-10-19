import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.resizable(False, False)
root.title("Scrollbar Widget Example")

# apply the grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# create the text widget
text = tk.Text(root, height=10)
text.grid(row=0, column=0, sticky=tk.EW)

# create a scrollbar widget and set its command to the text widget
scrollbar = ttk.Scrollbar(root, orient='vertical', command=text.yview)
scrollbar.grid(row=0, column=1, sticky=tk.NS)

# communicate back to the scrollbar
text['yscrollcommand'] = scrollbar.set
print(text['yscrollcommand'])
for field in text.keys():
    print(field)

# add sample text to the text widget to show the screen
for i in range(1,50):
    position = f'{i}.0'
    text.insert(position,f'Line {i}\n')



root.mainloop()

