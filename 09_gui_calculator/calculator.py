import tkinter as tk
from tkinter import ttk
import math

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Set style
        self.style = ttk.Style()
        self.style.configure('Calculator.TButton', font=('Arial', 12))
        self.style.configure('Display.TEntry', font=('Arial', 20))
        
        # Variables
        self.current_number = tk.StringVar(value="0")
        self.operation = None
        self.first_number = None
        self.new_number = True
        self.history = []
        
        self.create_widgets()
        
    def create_widgets(self):
        """Membuat semua widget calculator"""
        # Frame untuk display
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.pack(fill=tk.X)
        
        # Display
        self.display = ttk.Entry(
            display_frame, 
            textvariable=self.current_number,
            justify="right",
            style='Display.TEntry',
            state='readonly'
        )
        self.display.pack(fill=tk.X, pady=10)
        
        # Frame untuk history
        history_frame = ttk.Frame(self.root, padding="10")
        history_frame.pack(fill=tk.X)
        
        # History display
        self.history_display = tk.Text(
            history_frame,
            height=4,
            width=30,
            font=('Arial', 10),
            state='disabled'
        )
        self.history_display.pack(fill=tk.X)
        
        # Frame untuk buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Konfigurasi grid
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Scientific buttons
        self.create_scientific_buttons(button_frame)
        
        # Number buttons
        self.create_number_buttons(button_frame)
        
        # Operation buttons
        self.create_operation_buttons(button_frame)
        
    def create_scientific_buttons(self, frame):
        """Membuat tombol untuk fungsi scientific"""
        scientific_buttons = [
            ('√', lambda: self.calculate_scientific('sqrt')),
            ('x²', lambda: self.calculate_scientific('square')),
            ('sin', lambda: self.calculate_scientific('sin')),
            ('cos', lambda: self.calculate_scientific('cos')),
            ('tan', lambda: self.calculate_scientific('tan')),
            ('log', lambda: self.calculate_scientific('log')),
            ('π', lambda: self.input_constant('pi')),
            ('e', lambda: self.input_constant('e')),
        ]
        
        row = 0
        col = 0
        for (text, command) in scientific_buttons:
            ttk.Button(
                frame, 
                text=text,
                style='Calculator.TButton',
                command=command
            ).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
                
    def create_number_buttons(self, frame):
        """Membuat tombol angka"""
        numbers = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2),
            ('0', 5, 0), ('.', 5, 1)
        ]
        
        for (text, row, col) in numbers:
            ttk.Button(
                frame,
                text=text,
                style='Calculator.TButton',
                command=lambda x=text: self.input_number(x)
            ).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
    def create_operation_buttons(self, frame):
        """Membuat tombol operasi"""
        operations = [
            ('÷', 2, 3), ('×', 3, 3), ('-', 4, 3), ('+', 5, 3),
            ('C', 5, 2), ('=', 5, 3)
        ]
        
        for (text, row, col) in operations:
            if text == 'C':
                cmd = self.clear
            elif text == '=':
                cmd = self.calculate
            else:
                cmd = lambda x=text: self.input_operation(x)
                
            ttk.Button(
                frame,
                text=text,
                style='Calculator.TButton',
                command=cmd
            ).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
    def input_number(self, number):
        """Handle input angka"""
        if self.new_number:
            self.current_number.set(number)
            self.new_number = False
        else:
            current = self.current_number.get()
            if current == "0" and number != ".":
                self.current_number.set(number)
            else:
                self.current_number.set(current + number)
                
    def input_operation(self, op):
        """Handle input operasi"""
        if not self.new_number:
            self.calculate()
        self.operation = op
        self.first_number = float(self.current_number.get())
        self.new_number = True
        
    def calculate(self):
        """Melakukan perhitungan"""
        if self.operation and not self.new_number:
            second_number = float(self.current_number.get())
            result = 0
            
            if self.operation == '+':
                result = self.first_number + second_number
            elif self.operation == '-':
                result = self.first_number - second_number
            elif self.operation == '×':
                result = self.first_number * second_number
            elif self.operation == '÷':
                if second_number != 0:
                    result = self.first_number / second_number
                else:
                    self.current_number.set("Error")
                    self.add_to_history(f"{self.first_number} {self.operation} {second_number} = Error")
                    return
                
            # Format result
            if result.is_integer():
                result = int(result)
                
            # Update display
            self.current_number.set(str(result))
            
            # Add to history
            self.add_to_history(
                f"{self.first_number} {self.operation} {second_number} = {result}"
            )
            
            self.operation = None
            self.new_number = True
            
    def calculate_scientific(self, func):
        """Handle fungsi scientific"""
        try:
            number = float(self.current_number.get())
            result = 0
            
            if func == 'sqrt':
                if number >= 0:
                    result = math.sqrt(number)
                    operation = '√'
                else:
                    raise ValueError("Cannot calculate square root of negative number")
            elif func == 'square':
                result = number ** 2
                operation = '^2'
            elif func == 'sin':
                result = math.sin(math.radians(number))
                operation = 'sin'
            elif func == 'cos':
                result = math.cos(math.radians(number))
                operation = 'cos'
            elif func == 'tan':
                result = math.tan(math.radians(number))
                operation = 'tan'
            elif func == 'log':
                if number > 0:
                    result = math.log10(number)
                    operation = 'log'
                else:
                    raise ValueError("Cannot calculate log of non-positive number")
                    
            # Format result for display
            if isinstance(result, float):
                result = round(result, 8)
                if result.is_integer():
                    result = int(result)
                    
            self.current_number.set(str(result))
            self.add_to_history(f"{operation}({number}) = {result}")
            self.new_number = True
            
        except Exception as e:
            self.current_number.set("Error")
            self.add_to_history(f"Error: {str(e)}")
            
    def input_constant(self, const):
        """Handle input konstanta matematika"""
        if const == 'pi':
            value = math.pi
            symbol = 'π'
        elif const == 'e':
            value = math.e
            symbol = 'e'
            
        self.current_number.set(str(round(value, 8)))
        self.add_to_history(f"{symbol} = {value}")
        self.new_number = True
        
    def clear(self):
        """Reset calculator"""
        self.current_number.set("0")
        self.operation = None
        self.first_number = None
        self.new_number = True
        
    def add_to_history(self, text):
        """Menambahkan operasi ke history"""
        self.history.append(text)
        if len(self.history) > 4:  # Keep only last 4 operations
            self.history.pop(0)
            
        # Update history display
        self.history_display.config(state='normal')
        self.history_display.delete(1.0, tk.END)
        for item in self.history:
            self.history_display.insert(tk.END, item + '\n')
        self.history_display.config(state='disabled')

def main():
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()