import os
import string

HOME    = r'G:\My Drive\Databases'
WORK    = r'O:\pythonprograms\Databases'

for letter in list(string.ascii_uppercase):
    home = '{}:\My Drive\Databases'.format(letter)
    if not os.path.exists(home): continue
    HOME = home
    break

if os.path.exists(HOME):  LOCATION = HOME
else: LOCATION = WORK