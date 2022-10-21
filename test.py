import sys
sys.dont_write_bytecode = True

def main():
    with open(r'.\Assets\tips.txt', 'r') as f:
        textlines = f.read()
        print(textlines)

if __name__ == '__main__':
    main()