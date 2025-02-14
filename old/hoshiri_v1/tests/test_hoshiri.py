import unittest
from script_manager import generate_script


class TestHoshiri(unittest.TestCase):
    def test_script_generation(self):
        script_name = generate_script("test_script", "print('Hello')")
        self.assertEqual(script_name, "test_script")


if __name__ == "__main__":
    unittest.main()
