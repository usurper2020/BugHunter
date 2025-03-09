import subprocess
import unittest


class TestDynamicAnalysis(unittest.TestCase):
    def test_dynamic_analysis(self):
        result = subprocess.run(
            ["pytest", "--maxfail=1", "--disable-warnings"],
            capture_output=True,
            text=True,
        )
        self.assert_equal(result.returncode, 0)

        if __name__ == "__main__":
            unittest.main()
