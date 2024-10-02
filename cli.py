# cli.py

import sys
from mathscript import MathScript

def main():
    if len(sys.argv) < 2:
        print('Usage: python cli.py <filename.ms>')
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()
    ms = MathScript()
    try:
        ms.execute(code)
        variables = ms.get_variables()
        print('Variables:', variables)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
