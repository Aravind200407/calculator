import tkinter as tk
from tkinter import messagebox
import math
import numpy as np
import matplotlib.pyplot as plt

# --- STYLING ---
BG_COLOR = "#0f172a"
DISPLAY_BG = "#1e293b"
TEXT_COLOR = "#f8fafc"
OP_COLOR = "#38bdf8"    # Sky Blue
SCI_COLOR = "#818cf8"   # Indigo
GRAPH_COLOR = "#f43f5e" # Rose for Graphing

class GraphingCalculator:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Python Graphing Pro")
        self.root.geometry("450x650")
        self.root.configure(bg=BG_COLOR)

        self.equation = ""

        # Display screen
        self.display = tk.Entry(
            root, font=("Consolas", 28), bg=DISPLAY_BG, fg=TEXT_COLOR,
            borderwidth=0, justify='right', insertbackground=TEXT_COLOR
        )
        self.display.pack(expand=True, fill="both", padx=20, pady=30)

        self.button_frame = tk.Frame(root, bg=BG_COLOR)
        self.button_frame.pack(expand=True, fill="both")

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ['sin', 'cos', 'tan', 'π'],
            ['√', 'x²', '^', 'log'],
            ['(', ')', 'x', 'GRAPH'], # Added 'x' variable and 'GRAPH' button
            ['C', '⌫', '/', '*'],
            ['7', '8', '9', '-'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '='],
            ['0', '.', '', '']
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                if not char: continue
                
                # Dynamic Styling
                if char == 'GRAPH': bg = GRAPH_COLOR
                elif char in ['sin', 'cos', 'tan', 'π', '√', 'x²', '^', 'log', 'x']: bg = SCI_COLOR
                elif char in ['/', '*', '-', '+', '=']: bg = OP_COLOR
                elif char in ['C', '⌫']: bg = "#ef4444"
                else: bg = "#334155"
                
                btn = tk.Button(
                    self.button_frame, text=char, font=("Arial", 11, "bold"),
                    bg=bg, fg=TEXT_COLOR, borderwidth=0, cursor="hand2",
                    command=lambda x=char: self.on_button_click(x)
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        for i in range(8): self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): self.button_frame.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == '=':
            self.calculate()
        elif char == 'GRAPH':
            self.plot_graph()
        elif char == 'C':
            self.equation = ""
        elif char == '⌫':
            self.equation = self.equation[:-1]
        elif char == 'π':
            self.equation += "math.pi"
        elif char == 'x':
            self.equation += "x" # Used as a variable for plotting
        elif char == '√':
            self.equation += "np.sqrt("
        elif char in ['sin', 'cos', 'tan', 'log']:
            self.equation += f"np.{char}("
        elif char == '^':
            self.equation += "**"
        else:
            self.equation += str(char)
        
        self.update_display()

    def plot_graph(self):
        try:
            # Prepare data range for X (from -10 to 10)
            x = np.linspace(-10, 10, 400)
            
            # Replace user-friendly terms with numpy terms for calculation
            eq = self.equation.replace('math.pi', 'np.pi')
            
            # Evaluate the equation across the entire X array
            y = eval(eq)
            
            plt.figure(figsize=(6, 4))
            plt.plot(x, y, label=f"f(x) = {self.equation}", color="#38bdf8")
            plt.axhline(0, color='white', linewidth=0.5)
            plt.axvline(0, color='white', linewidth=0.5)
            plt.title("Function Visualization")
            plt.grid(True, linestyle='--', alpha=0.3)
            plt.legend()
            plt.style.use('dark_background')
            plt.show()
        except Exception as e:
            messagebox.showerror("Graph Error", "Ensure your equation uses 'x' correctly.\nExample: sin(x)")

    def calculate(self):
        try:
            # Use math context for single value calculation
            calc_eq = self.equation.replace('np.', 'math.')
            result = eval(calc_eq)
            self.equation = str(round(result, 6))
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.equation = ""
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.equation)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphingCalculator(root)
    root.mainloop()