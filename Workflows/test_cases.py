# Python script to generate the test_cases.py file with the provided unit tests

def generate_test_file(filename):
    test_code = '''import unittest
from your_module import add_numbers  # Assuming the function is in a file named your_module.py

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(10, 20), 30)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(10.5, 20.3), 30.8)

    def test_add_mixed_types(self):
        self.assertAlmostEqual(add_numbers(10, 20.5), 30.5)

    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(10, 0), 10)
        self.assertEqual(add_numbers(0, 10), 10)

    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-10, -20), -30)
        self.assertEqual(add_numbers(-10, 20), 10)
        self.assertEqual(add_numbers(10, -20), -10)

    def test_add_large_numbers(self):
        self.assertEqual(add_numbers(1000000, 2000000), 3000000)

    def test_type_error_with_string(self):
        with self.assertRaises(TypeError):
            add_numbers("10", 20)

    def test_type_error_with_list(self):
        with self.assertRaises(TypeError):
            add_numbers([10], 20)

if __name__ == '__main__':
    unittest.main()
'''
    with open(filename, 'w') as file:
        file.write(test_code)

if __name__ == '__main__':
    generate_test_file('test_cases.py')

