import unittest

import pylint.lint


class TestCodeQuality(unittest.TestCase):
    def test_code_quality(self):
        pylint_opts = ["src/"]
        pylint.lint.Run(pylint_opts)

        if __name__ == "__main__":
            unittest.main()
