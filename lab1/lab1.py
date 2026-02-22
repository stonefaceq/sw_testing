import math
import sys

# Константи згідно з варіантом N=16 
MIN_VAL = -116
MAX_VAL = 116
EPS = 1e-8 # Точність для порівняння з нулем 

class Line:
    def __init__(self, A, B, C, name):
        self.A = A
        self.B = B
        self.C = C
        self.name = name

def is_zero(val):
    return abs(val) <= EPS

def read_int(prompt, param_name, allow_zero=True):
    while True:
        try:
            val_str = input(prompt)
            val = int(val_str)
            
            # Перевірка меж [cite: 35, 40]
            if val < MIN_VAL or val > MAX_VAL:
                print(f"\nОпис допущеної помилки: Значення {val} виходить за межі проміжку [{MIN_VAL}; {MAX_VAL}].")
                print(f"Опис дій з виправлення помилки: Введіть ціле число, яке належить дозволеному діапазону.\n")
                continue
                
            # Перевірка на недопустимий нуль 
            if not allow_zero and val == 0:
                print(f"\nОпис допущеної помилки: Параметр {param_name} дорівнює нулю, що є неприпустимим (ділення на нуль).")
                print(f"Опис дій з виправлення помилки: Введіть ненульове ціле число в межах [{MIN_VAL}; {MAX_VAL}].\n")
                continue
                
            return val
        except ValueError:
            print(f"\nОпис допущеної помилки: Введено некоректні дані ('{val_str}'). Очікувалось ціле число.")
            print("Опис дій з виправлення помилки: Будь ласка, введіть коректне ціле число.\n")

def get_intersection(L1, L2):
    D = L1.A * L2.B - L2.A * L1.B
    if is_zero(D):
        return None
    
    x = (-L1.C * L2.B + L2.C * L1.B) / D
    y = (-L1.A * L2.C + L2.A * L1.C) / D
    return (x, y)

def are_coincident(L1, L2):
    return (is_zero(L1.A * L2.B - L2.A * L1.B) and 
            is_zero(L1.A * L2.C - L2.A * L1.C) and 
            is_zero(L1.B * L2.C - L2.B * L1.C))

def main():
    print(f"--- Аналіз взаємного розміщення прямих (Варіант 16) ---")
    print(f"Допустимий проміжок вхідних значень: [{MIN_VAL}; {MAX_VAL}]\n")
    
    # 1-ша пряма (канонічна)
    print("Введення параметрів для першої прямої (канонічне рівняння):")
    x01 = read_int("Введіть x01: ", "x01")
    y01 = read_int("Введіть y01: ", "y01")
    l1 = read_int("Введіть l1 (напрямний вектор, != 0): ", "l1", allow_zero=False)
    m1 = read_int("Введіть m1 (напрямний вектор, != 0): ", "m1", allow_zero=False)
    Line1 = Line(m1, -l1, l1*y01 - m1*x01, "Пряма 1")
    
    # 2-га пряма (канонічна)
    print("\nВведення параметрів для другої прямої (канонічне рівняння):")
    x02 = read_int("Введіть x02: ", "x02")
    y02 = read_int("Введіть y02: ", "y02")
    l2 = read_int("Введіть l2 (напрямний вектор, != 0): ", "l2", allow_zero=False)
    m2 = read_int("Введіть m2 (напрямний вектор, != 0): ", "m2", allow_zero=False)
    Line2 = Line(m2, -l2, l2*y02 - m2*x02, "Пряма 2")
    
    # 3-тя пряма (у відрізках)
    print("\nВведення параметрів для третьої прямої (рівняння у відрізках):")
    a = read_int("Введіть a (!= 0): ", "a", allow_zero=False)
    b = read_int("Введіть b (!= 0): ", "b", allow_zero=False)
    Line3 = Line(b, a, -a*b, "Пряма 3")
    
    lines = [Line1, Line2, Line3]
    
    # Групуємо унікальні прямі (ті, що не співпадають)
    unique_lines = []
    for line in lines:
        matched = False
        for u_line in unique_lines:
            if are_coincident(line, u_line['line']):
                u_line['count'] += 1
                matched = True
                break
        if not matched:
            unique_lines.append({'line': line, 'count': 1})
            
    print("\n--- РЕЗУЛЬТАТ ---")
    num_unique = len(unique_lines)
    
    if num_unique == 1:
        # Усі три прямі співпадають
        print("Прямі співпадають")
        
    elif num_unique == 2:
        # Дві прямі співпадають, одна відрізняється
        L_A = unique_lines[0]['line']
        L_B = unique_lines[1]['line']
        
        pt = get_intersection(L_A, L_B)
        if pt is None:
            print("Прямі не перетинаються")
        else:
            print(f"Єдина точка перетину прямих (x0, y0), x0=<{pt[0]:.5f}>, y0=<{pt[1]:.5f}>")
            
    else:
        # Три унікальні прямі
        L1, L2, L3 = [u['line'] for u in unique_lines]
        
        pt12 = get_intersection(L1, L2)
        pt23 = get_intersection(L2, L3)
        pt31 = get_intersection(L3, L1)
        
        # Рахуємо скільки пар є паралельними
        parallel_count = [pt12, pt23, pt31].count(None)
        
        if parallel_count == 3:
            print("Прямі не перетинаються")
        elif parallel_count == 1:
            # Дві паралельні, одна їх перетинає (дає дві точки)
            pts = [pt for pt in [pt12, pt23, pt31] if pt is not None]
            print(f"Дві точки перетину прямих (x1, y1)=<{pts[0][0]:.5f}, {pts[0][1]:.5f}>, (x2, y2)=<{pts[1][0]:.5f}, {pts[1][1]:.5f}>")
        else:
            # Жодна не паралельна іншій
            # Перевіряємо чи перетинаються вони в одній спільній точці
            dist = math.hypot(pt12[0] - pt23[0], pt12[1] - pt23[1])
            if dist <= EPS:
                print(f"Єдина точка перетину прямих (x0, y0), x0=<{pt12[0]:.5f}>, y0=<{pt12[1]:.5f}>")
            else:
                print(f"Три точки перетину прямих (x1, y1), (x2, y2), (x3, y3), x1=<{pt12[0]:.5f}>, y1=<{pt12[1]:.5f}>, x2=<{pt23[0]:.5f}>, y2=<{pt23[1]:.5f}>, x3=<{pt31[0]:.5f}>, y3=<{pt31[1]:.5f}>, i=1,2,3")

if __name__ == "__main__":
    main()