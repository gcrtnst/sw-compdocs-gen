import collections
import pathlib
import sw_compdocs.validator
import unittest


class TestIsPathLike(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_v", "want_ret"))

        for tc in [
            tt(input_v="pathlike", want_ret=True),
            tt(input_v=b"pathlike", want_ret=True),
            tt(input_v=pathlib.PurePath("pathlike"), want_ret=True),
            tt(input_v=None, want_ret=False),
        ]:
            with self.subTest(tc=tc):
                got_ret = sw_compdocs.validator.is_pathlike(tc.input_v)
                self.assertEqual(got_ret, tc.want_ret)
