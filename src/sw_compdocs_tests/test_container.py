import collections
import sw_compdocs.container
import unittest
import unittest.mock


class TestSequenceInit(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.Sequence((1, 2, 3))
        self.assertEqual(seq._l, [1, 2, 3])

    def test_default(self):
        seq = sw_compdocs.container.Sequence()
        self.assertEqual(seq._l, [])


class TestSequenceGetItem(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.Sequence((1, 2, 3))
        self.assertEqual(seq[0], 1)
        self.assertEqual(seq[1], 2)
        self.assertEqual(seq[2], 3)
        self.assertEqual(seq[0:1], [1])
        self.assertEqual(seq[1:2], [2])
        self.assertEqual(seq[2:3], [3])
        self.assertEqual(seq[0:2], [1, 2])
        self.assertEqual(seq[1:3], [2, 3])
        self.assertEqual(seq[0:3], [1, 2, 3])
        self.assertEqual(seq[:2], [1, 2])
        self.assertEqual(seq[1:], [2, 3])


class TestSequenceLen(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.Sequence((1, 2, 3))
        self.assertEqual(len(seq), 3)


class TestSequenceRepr(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.Sequence((1, 2, 3))
        self.assertEqual(repr(seq), "Sequence([1, 2, 3])")


class TestSequenceEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        for tc in [
            tt(
                input_self=sw_compdocs.container.Sequence([1, 2, 3]),
                input_other=sw_compdocs.container.Sequence([1, 2, 3]),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.container.Sequence([1, 2, 3]),
                input_other=sw_compdocs.container.Sequence([1, 2, 4]),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.container.Sequence([1, 2, 3]),
                input_other=sw_compdocs.container.MutableSequence([1, 2, 3]),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.container.Sequence([1, 2, 3]),
                input_other=[1, 2, 3],
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestMutableSequenceInit(unittest.TestCase):
    def test(self):
        with unittest.mock.patch.object(
            sw_compdocs.container.MutableSequence, "_check_value"
        ) as mock:
            mock.return_value = None
            seq = sw_compdocs.container.MutableSequence((1, 2, 3))
            self.assertEqual(
                mock.call_args_list,
                [unittest.mock.call(1), unittest.mock.call(2), unittest.mock.call(3)],
            )
        self.assertEqual(seq._l, [1, 2, 3])

    def test_default(self):
        with unittest.mock.patch.object(
            sw_compdocs.container.MutableSequence, "_check_value"
        ) as mock:
            mock.return_value = None
            seq = sw_compdocs.container.MutableSequence()
        self.assertEqual(seq._l, [])
        self.assertEqual(mock.call_args_list, [])


class TestMutableSequenceGetItem(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.MutableSequence((1, 2, 3))
        self.assertEqual(seq[0], 1)
        self.assertEqual(seq[1], 2)
        self.assertEqual(seq[2], 3)
        self.assertEqual(seq[0:1], [1])
        self.assertEqual(seq[1:2], [2])
        self.assertEqual(seq[2:3], [3])
        self.assertEqual(seq[0:2], [1, 2])
        self.assertEqual(seq[1:3], [2, 3])
        self.assertEqual(seq[0:3], [1, 2, 3])
        self.assertEqual(seq[:2], [1, 2])
        self.assertEqual(seq[1:], [2, 3])


class TestMutableSequenceSetItem(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple(
            "tt",
            (
                "input_list",
                "input_key",
                "input_value",
                "want_list",
                "want_mock_call_args_list",
            ),
        )

        for tc in [
            tt(
                input_list=[1, 2, 3],
                input_key=0,
                input_value=4,
                want_list=[4, 2, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=1,
                input_value=4,
                want_list=[1, 4, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=2,
                input_value=4,
                want_list=[1, 2, 4],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=-1,
                input_value=4,
                want_list=[1, 2, 4],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=-2,
                input_value=4,
                want_list=[1, 4, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=-3,
                input_value=4,
                want_list=[4, 2, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(0, 1),
                input_value=[4],
                want_list=[4, 2, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(1, 2),
                input_value=[4],
                want_list=[1, 4, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(2, 3),
                input_value=[4],
                want_list=[1, 2, 4],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(0, 2),
                input_value=[4, 5],
                want_list=[4, 5, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                    unittest.mock.call(5),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(1, 3),
                input_value=[4, 5],
                want_list=[1, 4, 5],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                    unittest.mock.call(5),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(0, 3),
                input_value=[4, 5, 6],
                want_list=[4, 5, 6],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                    unittest.mock.call(5),
                    unittest.mock.call(6),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(None, 2),
                input_value=[4, 5],
                want_list=[4, 5, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                    unittest.mock.call(5),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(1, None),
                input_value=[4, 5],
                want_list=[1, 4, 5],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                    unittest.mock.call(5),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(1, 2),
                input_value=[4],
                want_list=[1, 4, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                ],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(1, 2),
                input_value=[],
                want_list=[1, 3],
                want_mock_call_args_list=[],
            ),
            tt(
                input_list=[1, 2, 3],
                input_key=slice(1, 2),
                input_value=[4, 5],
                want_list=[1, 4, 5, 3],
                want_mock_call_args_list=[
                    unittest.mock.call(4),
                    unittest.mock.call(5),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                seq = sw_compdocs.container.MutableSequence(tc.input_list)

                with unittest.mock.patch.object(
                    sw_compdocs.container.MutableSequence, "_check_value"
                ) as mock:
                    mock.return_value = None
                    seq[tc.input_key] = tc.input_value
                self.assertEqual(seq._l, tc.want_list)
                self.assertEqual(mock.call_args_list, tc.want_mock_call_args_list)

    def test_exc(self):
        def _check_type(self, value):
            if type(value) is not int:
                raise TypeError

        seq = sw_compdocs.container.MutableSequence((1, 2, 3))

        with unittest.mock.patch.object(
            sw_compdocs.container.MutableSequence, "_check_value", new=_check_type
        ):
            with self.assertRaises(TypeError):
                seq[:] = [4, 5, "6"]
        self.assertEqual(seq._l, [1, 2, 3])


class TestMutableSequenceDelItem(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_list", "input_key", "want_list"))

        for tc in [
            tt(input_list=[1, 2, 3], input_key=1, want_list=[1, 3]),
            tt(input_list=[1, 2, 3], input_key=slice(0, 2), want_list=[3]),
        ]:
            with self.subTest(tc=tc):
                seq = sw_compdocs.container.MutableSequence(tc.input_list)
                del seq[tc.input_key]
                self.assertEqual(seq._l, tc.want_list)


class TestMutableSequenceLen(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.MutableSequence((1, 2, 3))
        self.assertEqual(len(seq), 3)


class TestMutableSequenceRepr(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.MutableSequence((1, 2, 3))
        self.assertEqual(repr(seq), "MutableSequence([1, 2, 3])")


class TestMutableSequenceEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        for tc in [
            tt(
                input_self=sw_compdocs.container.MutableSequence((1, 2, 3)),
                input_other=sw_compdocs.container.MutableSequence((1, 2, 3)),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.container.MutableSequence((1, 2, 3)),
                input_other=sw_compdocs.container.MutableSequence((1, 2, 4)),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.container.MutableSequence((1, 2, 3)),
                input_other=sw_compdocs.container.Sequence((1, 2, 3)),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.container.MutableSequence((1, 2, 3)),
                input_other=[1, 2, 3],
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestMutableSequenceInsert(unittest.TestCase):
    def test(self):
        seq = sw_compdocs.container.MutableSequence((1, 2, 3))
        with unittest.mock.patch.object(
            sw_compdocs.container.MutableSequence, "_check_value"
        ) as mock:
            mock.return_value = None
            seq.insert(1, 4)
        self.assertEqual(seq._l, [1, 4, 2, 3])
        self.assertEqual(mock.call_args_list, [unittest.mock.call(4)])
