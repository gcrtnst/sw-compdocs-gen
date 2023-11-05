import sw_compdocs.convert
import unittest


class TestAsStr(unittest.TestCase):
    def test_validate_pass(self):
        s = sw_compdocs.convert.as_str("foo")
        self.assertEqual(s, "foo")

    def test_validate_error(self):
        with self.assertRaises(TypeError):
            sw_compdocs.convert.as_str(0)
