import os
import string

HOME    = r'G:\My Drive\Databases'
WORK    = r'.\Databases'

for letter in list(string.ascii_uppercase):
    home = '{}:\My Drive\Databases'.format(letter)
    if not os.path.exists(home): 
        continue
    HOME = home
    break

if os.path.exists(WORK):  LOCATION = WORK
else: LOCATION = HOME