import unittest
import ast

class TestStaticAnalysis(unittest.TestCase):
    def test_static_analysis(self):
        with open('src/config.py', 'r') as file:
            tree = ast.parse(file.read())
        self.assertIsNotNone(tree)

if __name__ == '__main__':
    unittest.main()
