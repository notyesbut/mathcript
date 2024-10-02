# gui/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.font import Font
import threading
import sys
import io

from mathscript import Lexer, Parser, Interpreter

class MathScriptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MathScript IDE")
        self.filename = None

        # Create GUI elements
        self.create_widgets()
        self.create_menu()
        self.bind_shortcuts()

    def create_widgets(self):
        # Create font for the text editor
        self.font = Font(family="Consolas", size=12)

        # Text editor
        self.editor = scrolledtext.ScrolledText(self.root, font=self.font, wrap=tk.NONE)
        self.editor.pack(fill=tk.BOTH, expand=1)

        # Line numbers
        self.line_numbers = tk.Text(self.root, width=4, font=self.font, state='disabled', bg='#F0F0F0')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.update_line_numbers()

        # Output console
        self.console = scrolledtext.ScrolledText(self.root, height=10, font=self.font, bg='#F5F5F5', fg='black', state='disabled')
        self.console.pack(fill=tk.X)

        # Button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)

        # Run button
        self.run_button = tk.Button(self.button_frame, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_menu(self):
        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New File", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open File...", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="MathScript Documentation", command=self.show_documentation)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def bind_shortcuts(self):
        self.root.bind('<Control-n>', lambda event: self.new_file())
        self.root.bind('<Control-o>', lambda event: self.open_file())
        self.root.bind('<Control-s>', lambda event: self.save_file())
        self.root.bind('<Control-S>', lambda event: self.save_file_as())
        self.editor.bind('<KeyRelease>', lambda event: self.on_key_release())

    def update_line_numbers(self):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        line_count = int(self.editor.index('end-1c').split('.')[0])
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f'{i}\n')
        self.line_numbers.config(state='disabled')

    def on_key_release(self):
        self.update_line_numbers()

    def new_file(self):
        self.filename = None
        self.editor.delete(1.0, tk.END)
        self.root.title("MathScript IDE - New File")

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".ms",
                                                   filetypes=[("MathScript Files", "*.ms"), ("All Files", "*.*")])
        if self.filename:
            try:
                with open(self.filename, 'r') as file:
                    code = file.read()
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(1.0, code)
                self.root.title(f"MathScript IDE - {self.filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        if self.filename:
            try:
                code = self.editor.get(1.0, tk.END)
                with open(self.filename, 'w') as file:
                    file.write(code)
                messagebox.showinfo("Saved", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".ms",
                                                     filetypes=[("MathScript Files", "*.ms"), ("All Files", "*.*")])
        if self.filename:
            self.save_file()
            self.root.title(f"MathScript IDE - {self.filename}")

    def show_documentation(self):
        messagebox.showinfo("Documentation", "Visit the MathScript documentation at:\nhttps://mathscript.org/docs")

    def show_about(self):
        messagebox.showinfo("About", "MathScript IDE\nVersion 1.0")

    def run_code(self):
        code = self.editor.get(1.0, tk.END)
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.config(state='disabled')

        # Run the code in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.execute_code, args=(code,), daemon=True).start()

    def execute_code(self, code):
        try:
            # Redirect print statements to the console
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()

            # Lexing
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()

            # Interpreting
            interpreter = Interpreter()
            interpreter.interpret(ast)

            # Restore stdout
            sys.stdout = old_stdout

            output = redirected_output.getvalue()

            self.console.config(state='normal')
            self.console.insert(tk.END, output)
            self.console.config(state='disabled')

        except Exception as e:
            sys.stdout = old_stdout
            self.console.config(state='normal')
            self.console.insert(tk.END, f'Error: {e}')
            self.console.config(state='disabled')

def main():
    root = tk.Tk()
    gui = MathScriptGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
