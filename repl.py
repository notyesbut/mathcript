# repl.py

from mathscript import MathScript

def main():
    print("Welcome to MathScript REPL")
    ms = MathScript()
    while True:
        try:
            text = input('>>> ')
            if text.strip() == '':
                continue
            result = ms.execute(text)
            if result is not None:
                print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    main()
