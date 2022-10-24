import sys
sys.dont_write_bytecode = True

import json

def main():
    with open(r".\Assets\data_format.json") as j:
        format_dict = json.load(j)['project_catalog']
    new_dict =  dict(
        [(format_dict[key]['name'], int(key)) 
        for key in format_dict])
    print(new_dict)
    

if __name__ == '__main__':
    main()