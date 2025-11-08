import pytest
from tkinter import Tk
from calculator import CalculatorGUI

@pytest.fixture
def calculator():
    root = Tk()
    calc = CalculatorGUI(root)
    yield calc
    root.destroy()

def test_input_number(calculator):
    """Test input angka"""
    calculator.input_number('5')
    assert calculator.current_number.get() == '5'
    
    calculator.input_number('3')
    assert calculator.current_number.get() == '53'

def test_decimal_input(calculator):
    """Test input desimal"""
    calculator.input_number('5')
    calculator.input_number('.')
    calculator.input_number('3')
    assert calculator.current_number.get() == '5.3'

def test_basic_operations(calculator):
    """Test operasi dasar"""
    # Test addition
    calculator.input_number('5')
    calculator.input_operation('+')
    calculator.input_number('3')
    calculator.calculate()
    assert calculator.current_number.get() == '8'
    
    # Test subtraction
    calculator.input_operation('-')
    calculator.input_number('2')
    calculator.calculate()
    assert calculator.current_number.get() == '6'
    
    # Test multiplication
    calculator.input_operation('×')
    calculator.input_number('3')
    calculator.calculate()
    assert calculator.current_number.get() == '18'
    
    # Test division
    calculator.input_operation('÷')
    calculator.input_number('2')
    calculator.calculate()
    assert calculator.current_number.get() == '9'

def test_division_by_zero(calculator):
    """Test pembagian dengan nol"""
    calculator.input_number('5')
    calculator.input_operation('÷')
    calculator.input_number('0')
    calculator.calculate()
    assert calculator.current_number.get() == 'Error'

def test_scientific_functions(calculator):
    """Test fungsi scientific"""
    # Test square root
    calculator.input_number('16')
    calculator.calculate_scientific('sqrt')
    assert float(calculator.current_number.get()) == 4
    
    # Test square
    calculator.input_number('4')
    calculator.calculate_scientific('square')
    assert calculator.current_number.get() == '16'
    
    # Test trigonometric
    calculator.input_number('0')
    calculator.calculate_scientific('sin')
    assert float(calculator.current_number.get()) == 0
    
    calculator.input_number('90')
    calculator.calculate_scientific('cos')
    assert abs(float(calculator.current_number.get())) < 0.000001

def test_constants(calculator):
    """Test konstanta matematika"""
    calculator.input_constant('pi')
    assert abs(float(calculator.current_number.get()) - 3.14159265) < 0.00001
    
    calculator.input_constant('e')
    assert abs(float(calculator.current_number.get()) - 2.71828183) < 0.00001

def test_clear(calculator):
    """Test fungsi clear"""
    calculator.input_number('5')
    calculator.input_operation('+')
    calculator.input_number('3')
    calculator.clear()
    assert calculator.current_number.get() == '0'
    assert calculator.operation is None
    assert calculator.first_number is None
    assert calculator.new_number is True

def test_history(calculator):
    """Test history operasi"""
    calculator.input_number('5')
    calculator.input_operation('+')
    calculator.input_number('3')
    calculator.calculate()
    
    assert len(calculator.history) == 1
    assert '5 + 3 = 8' in calculator.history[0]
    
    # Test history limit
    for i in range(5):
        calculator.add_to_history(f"Test {i}")
    assert len(calculator.history) == 4  # Should keep only last 4 entries

def test_invalid_scientific_operations(calculator):
    """Test operasi scientific yang tidak valid"""
    # Test negative square root
    calculator.input_number('-4')
    calculator.calculate_scientific('sqrt')
    assert calculator.current_number.get() == 'Error'
    
    # Test negative logarithm
    calculator.input_number('-1')
    calculator.calculate_scientific('log')
    assert calculator.current_number.get() == 'Error'