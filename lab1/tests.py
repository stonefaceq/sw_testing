import unittest
from unittest.mock import patch
import io
import lab1  # Імпортуємо твій основний файл (він має називатися lab1.py)

class TestLineIntersections(unittest.TestCase):
    
    def run_app(self, mock_stdout, mock_input, inputs):
        """Допоміжний метод для запуску програми з імітацією вводу"""
        mock_input.side_effect = inputs
        try:
            lab1.main()
        except StopIteration:
            # Виникає, якщо програма просить більше вводів, ніж ми передали
            # (наприклад, зациклилась через помилку)
            pass
        return mock_stdout.getvalue()


    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc1_coincident_lines(self, mock_stdout, mock_input):
        """Тест 1: Усі три прямі співпадають"""
        # Входи: L1(0,2, 1,-1), L2(2,0, -1,1), L3(a=2, b=2)
        inputs = ['0', '2', '1', '-1',  '2', '0', '-1', '1',  '2', '2']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("Прямі співпадають", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc2_boundary_coincident(self, mock_stdout, mock_input):
        """Тест 2: Усі три прямі співпадають (Ліва границя -116)"""
        inputs = ['-116', '0', '1', '-1',  '0', '-116', '-1', '1',  '-116', '-116']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("Прямі співпадають", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc3_parallel_lines(self, mock_stdout, mock_input):
        """Тест 3: Три паралельні прямі, що не співпадають"""
        inputs = ['0', '2', '1', '-1',  '0', '4', '1', '-1',  '6', '6']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("Прямі не перетинаються", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc4_one_intersection(self, mock_stdout, mock_input):
        """Тест 4: Усі три прямі перетинаються в одній точці"""
        inputs = ['0', '0', '1', '1',  '0', '6', '1', '-2',  '4', '4']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("Єдина точка перетину прямих", output)
        self.assertIn("x0=<2.00000>", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc5_two_intersections(self, mock_stdout, mock_input):
        """Тест 5: Дві паралельні, одна їх перетинає (дві точки)"""
        inputs = ['0', '0', '1', '1',  '0', '4', '1', '-1',  '2', '2']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("Дві точки перетину прямих", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc6_three_intersections(self, mock_stdout, mock_input):
        """Тест 6: Утворюють трикутник (три точки)"""
        inputs = ['0', '0', '1', '1',  '0', '2', '1', '2',  '4', '4']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("Три точки перетину прямих", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc7_out_of_bounds_left(self, mock_stdout, mock_input):
        """Тест 7: Вихід за ліву границю (< -116)"""
        # Передаємо -117 (викличе помилку), потім 0 (коректне), щоб продовжити виконання
        inputs = ['-117', '0', '0', '1', '-1',  '0', '4', '1', '-1',  '6', '6']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("виходить за межі проміжку", output)
        self.assertIn("Опис дій з виправлення помилки", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc8_out_of_bounds_right(self, mock_stdout, mock_input):
        """Тест 8: Вихід за праву границю (> 116)"""
        inputs = ['0', '2', '1', '-1',  '0', '4', '1', '-1',  '117', '6', '6']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("виходить за межі проміжку", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc9_invalid_zero_vector(self, mock_stdout, mock_input):
        """Тест 9: Недопустимий нуль для напрямного вектора l1"""
        # Передаємо 0 для l1, ловимо помилку, потім передаємо 1
        inputs = ['0', '0', '0', '1', '1',  '0', '4', '1', '-1',  '2', '2']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("дорівнює нулю, що є неприпустимим (ділення на нуль)", output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tc11_invalid_type_string(self, mock_stdout, mock_input):
        """Тест 11: Введення літер замість чисел"""
        inputs = ['A', '0', '0', '1', '1',  '0', '4', '1', '-1',  '2', '2']
        output = self.run_app(mock_stdout, mock_input, inputs)
        self.assertIn("Введено некоректні дані", output)
        self.assertIn("Очікувалось ціле число", output)

if __name__ == '__main__':
    unittest.main(verbosity=2)