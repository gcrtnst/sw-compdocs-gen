import pathlib
import sw_compdocs._types
import typing
import unittest


class TestIsPathLike(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_v", object),
                ("want_ok", bool),
            ],
        )

        for tc in [
            tt(input_v="", want_ok=True),
            tt(input_v=b"", want_ok=True),
            tt(input_v=pathlib.PurePath(), want_ok=True),
            tt(input_v=None, want_ok=False),
        ]:
            with self.subTest(tc=tc):
                got_ok = sw_compdocs._types.is_pathlike(tc.input_v)
                self.assertEqual(got_ok, tc.want_ok)
