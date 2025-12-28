# data/bad_code.py

def calculate(a,b):
    # Нет docstring, плохие отступы и пробелы
    res=a+b
    return res

def very_long_function():
    # Пример функции с дубликатами для проверки вашего метода _check_duplicates
    print("Starting process...")
    print("Loading data...")
    x = 10
    y = 20
    z = x + y
    print(f"Result is {z}")
    
    # Повторяющийся блок (дубликат)
    print("Starting process...")
    print("Loading data...")
    x = 10
    y = 20
    z = x + y
    print(f"Result is {z}")

def SimpleFunction(): # Нарушение snake_case
    pass