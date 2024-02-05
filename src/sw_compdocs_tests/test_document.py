import sw_compdocs.document
import typing
import unittest


class TestDocumentInit(unittest.TestCase):
    def test_pass(self) -> None:
        input_iterable_list: list[list[sw_compdocs.document.Block]] = [
            [],
            [
                sw_compdocs.document.Heading("head"),
                sw_compdocs.document.Paragraph("para"),
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
                sw_compdocs.document.Callout("callout"),
            ],
        ]
        for input_iterable in input_iterable_list:
            with self.subTest(input_iterable=input_iterable):
                doc = sw_compdocs.document.Document(input_iterable)
                got_list = list(doc)
                self.assertEqual(got_list, input_iterable)


class TestDocumentGetItem(unittest.TestCase):
    def test(self) -> None:
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Heading("head"),
                sw_compdocs.document.Paragraph("para"),
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
                sw_compdocs.document.Callout("callout"),
            ]
        )
        self.assertEqual(doc[0], sw_compdocs.document.Heading("head"))
        self.assertEqual(doc[1], sw_compdocs.document.Paragraph("para"))
        self.assertEqual(
            doc[2],
            sw_compdocs.document.Table(
                sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(["tbl"])
                )
            ),
        )
        self.assertEqual(doc[3], sw_compdocs.document.Callout("callout"))


class TestDocumentSetItem(unittest.TestCase):
    def test_pass_int(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_list", list[sw_compdocs.document.Block]),
                ("input_key", int),
                ("input_value", sw_compdocs.document.Block),
                ("want_list", list[sw_compdocs.document.Block]),
            ],
        )

        for tc in [
            tt(
                input_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
                input_key=0,
                input_value=sw_compdocs.document.Paragraph("qux"),
                want_list=[
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
            ),
            tt(
                input_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
                input_key=1,
                input_value=sw_compdocs.document.Paragraph("qux"),
                want_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
            ),
            tt(
                input_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
                input_key=2,
                input_value=sw_compdocs.document.Paragraph("qux"),
                want_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("qux"),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                doc = sw_compdocs.document.Document(tc.input_list)
                doc[tc.input_key] = tc.input_value
                got_list = list(doc)
                self.assertEqual(got_list, tc.want_list)

    def test_pass_slice(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_list", list[sw_compdocs.document.Block]),
                ("input_key", slice),
                ("input_value", list[sw_compdocs.document.Block]),
                ("want_list", list[sw_compdocs.document.Block]),
            ],
        )

        for tc in [
            tt(
                input_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
                input_key=slice(0, 2),
                input_value=[
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("quux"),
                ],
                want_list=[
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("quux"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
            ),
            tt(
                input_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
                input_key=slice(1, 3),
                input_value=[
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("quux"),
                ],
                want_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("quux"),
                ],
            ),
            tt(
                input_list=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
                input_key=slice(None, None),
                input_value=[
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("quux"),
                    sw_compdocs.document.Paragraph("corge"),
                ],
                want_list=[
                    sw_compdocs.document.Paragraph("qux"),
                    sw_compdocs.document.Paragraph("quux"),
                    sw_compdocs.document.Paragraph("corge"),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                doc = sw_compdocs.document.Document(tc.input_list)
                doc[tc.input_key] = tc.input_value
                got_list = list(doc)
                self.assertEqual(got_list, tc.want_list)


class TestDocumentDelItem(unittest.TestCase):
    def test(self) -> None:
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("bar"),
                sw_compdocs.document.Paragraph("baz"),
            ]
        )
        del doc[1]
        self.assertEqual(
            list[sw_compdocs.document.Block](doc),
            list[sw_compdocs.document.Block](
                [
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("baz"),
                ]
            ),
        )


class TestDocumentLen(unittest.TestCase):
    def test(self) -> None:
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("bar"),
                sw_compdocs.document.Paragraph("baz"),
            ]
        )
        self.assertEqual(len(doc), 3)


class TestDocumentRepr(unittest.TestCase):
    def test(self) -> None:
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Heading("head"),
                sw_compdocs.document.Paragraph("para"),
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
                sw_compdocs.document.Callout(
                    "callout", kind=sw_compdocs.document.CalloutKind.WARNING
                ),
            ]
        )

        want_s = (
            "Document(["
            + "Heading(text='head', level=1), "
            + "Paragraph(text='para'), "
            + "Table(data=TableData(TableDataRow(['tbl']), [])), "
            + "Callout(text='callout', kind=<CalloutKind.WARNING: 2>)"
            + "])"
        )
        got_s = repr(doc)
        self.assertEqual(got_s, want_s)


class TestDocumentEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.document.Document),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Paragraph("foo"),
                        sw_compdocs.document.Paragraph("bar"),
                        sw_compdocs.document.Paragraph("baz"),
                    ]
                ),
                input_other=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Paragraph("foo"),
                        sw_compdocs.document.Paragraph("bar"),
                        sw_compdocs.document.Paragraph("baz"),
                    ]
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Paragraph("foo"),
                        sw_compdocs.document.Paragraph("bar"),
                        sw_compdocs.document.Paragraph("baz"),
                    ]
                ),
                input_other=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Paragraph("foo"),
                        sw_compdocs.document.Paragraph("qux"),
                        sw_compdocs.document.Paragraph("baz"),
                    ]
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Paragraph("foo"),
                        sw_compdocs.document.Paragraph("bar"),
                        sw_compdocs.document.Paragraph("baz"),
                    ]
                ),
                input_other=[
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ],
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestDocumentInsert(unittest.TestCase):
    def test_pass(self) -> None:
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("baz"),
            ]
        )
        doc.insert(1, sw_compdocs.document.Paragraph("bar"))
        self.assertEqual(
            list[sw_compdocs.document.Block](doc),
            list[sw_compdocs.document.Block](
                [
                    sw_compdocs.document.Paragraph("foo"),
                    sw_compdocs.document.Paragraph("bar"),
                    sw_compdocs.document.Paragraph("baz"),
                ]
            ),
        )


class TestDocumentShift(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_doc", sw_compdocs.document.Document),
                ("input_level", int),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            tt(
                input_doc=sw_compdocs.document.Document(),
                input_level=1,
                want_doc=sw_compdocs.document.Document(),
            ),
            tt(
                input_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("head_a", level=1),
                        sw_compdocs.document.Paragraph("para_a"),
                        sw_compdocs.document.Heading("head_b", level=2),
                        sw_compdocs.document.Paragraph("para_b"),
                    ]
                ),
                input_level=1,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("head_a", level=2),
                        sw_compdocs.document.Paragraph("para_a"),
                        sw_compdocs.document.Heading("head_b", level=3),
                        sw_compdocs.document.Paragraph("para_b"),
                    ]
                ),
            ),
            tt(
                input_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("head_a", level=2),
                        sw_compdocs.document.Paragraph("para_a"),
                        sw_compdocs.document.Heading("head_b", level=3),
                        sw_compdocs.document.Paragraph("para_b"),
                    ]
                ),
                input_level=-1,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("head_a", level=1),
                        sw_compdocs.document.Paragraph("para_a"),
                        sw_compdocs.document.Heading("head_b", level=2),
                        sw_compdocs.document.Paragraph("para_b"),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                doc = sw_compdocs.document.Document(tc.input_doc)  # copy
                doc.shift(tc.input_level)
                self.assertEqual(doc, tc.want_doc)


class TestBlockInit(unittest.TestCase):
    def test(self) -> None:
        with self.assertRaises(NotImplementedError):
            sw_compdocs.document.Block()


class TestTableDataInit(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_head", sw_compdocs.document.TableDataRow),
                ("input_list", list[sw_compdocs.document.TableDataRow]),
            ],
        )

        for tc in [
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_data = sw_compdocs.document.TableData(tc.input_head, tc.input_list)
                got_list = list(got_data)
                self.assertEqual(got_data.head, tc.input_head)
                self.assertEqual(got_list, tc.input_list)

    def test_exc_value(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_head", sw_compdocs.document.TableDataRow),
                ("input_list", list[sw_compdocs.document.TableDataRow]),
            ],
        )

        for tc in [
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3", "B4")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3", "C4")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3", "D4")),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(ValueError):
                    sw_compdocs.document.TableData(tc.input_head, tc.input_list)


class TestTableDataGetItem(unittest.TestCase):
    def test(self) -> None:
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        self.assertEqual(data[0], sw_compdocs.document.TableDataRow(("B1", "B2", "B3")))
        self.assertEqual(data[1], sw_compdocs.document.TableDataRow(("C1", "C2", "C3")))
        self.assertEqual(data[2], sw_compdocs.document.TableDataRow(("D1", "D2", "D3")))


class TestTableDataSetItem(unittest.TestCase):
    def test_pass_int(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_head", sw_compdocs.document.TableDataRow),
                ("input_list", list[sw_compdocs.document.TableDataRow]),
                ("input_key", int),
                ("input_value", sw_compdocs.document.TableDataRow),
                ("want_list", list[sw_compdocs.document.TableDataRow]),
            ],
        )

        for tc in [
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=0,
                input_value=sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                want_list=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=1,
                input_value=sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                want_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=2,
                input_value=sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                want_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                data = sw_compdocs.document.TableData(tc.input_head, tc.input_list)
                data[tc.input_key] = tc.input_value
                got_list = list(data)
                self.assertEqual(got_list, tc.want_list)

    def test_pass_slice(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_head", sw_compdocs.document.TableDataRow),
                ("input_list", list[sw_compdocs.document.TableDataRow]),
                ("input_key", slice),
                ("input_value", list[sw_compdocs.document.TableDataRow]),
                ("want_list", list[sw_compdocs.document.TableDataRow]),
            ],
        )

        for tc in [
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=slice(0, 2),
                input_value=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                ],
                want_list=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=slice(1, 3),
                input_value=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                ],
                want_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=slice(None, None),
                input_value=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                ],
                want_list=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=slice(None, None),
                input_value=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3")),
                    sw_compdocs.document.TableDataRow(("H1", "H2", "H3")),
                ],
                want_list=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3")),
                    sw_compdocs.document.TableDataRow(("H1", "H2", "H3")),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                data = sw_compdocs.document.TableData(tc.input_head, tc.input_list)
                data[tc.input_key] = tc.input_value
                got_list = list(data)
                self.assertEqual(got_list, tc.want_list)

    def test_exc_value_int(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_head", sw_compdocs.document.TableDataRow),
                ("input_list", list[sw_compdocs.document.TableDataRow]),
                ("input_key", int),
                ("input_value", sw_compdocs.document.TableDataRow),
            ],
        )

        for tc in [
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=1,
                input_value=sw_compdocs.document.TableDataRow(("E1", "E2")),
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=1,
                input_value=sw_compdocs.document.TableDataRow(("E1", "E2", "E3", "E4")),
            ),
        ]:
            with self.subTest(tc=tc):
                data = sw_compdocs.document.TableData(tc.input_head, tc.input_list)
                with self.assertRaises(ValueError):
                    data[tc.input_key] = tc.input_value
                got_list = list(data)
                self.assertEqual(got_list, tc.input_list)

    def test_exc_value_slice(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_head", sw_compdocs.document.TableDataRow),
                ("input_list", list[sw_compdocs.document.TableDataRow]),
                ("input_key", slice),
                ("input_value", list[sw_compdocs.document.TableDataRow]),
            ],
        )

        for tc in [
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=slice(None, None),
                input_value=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3", "E4")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=slice(None, None),
                input_value=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3", "F4")),
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3")),
                ],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=slice(None, None),
                input_value=[
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3", "G4")),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                data = sw_compdocs.document.TableData(tc.input_head, tc.input_list)
                with self.assertRaises(ValueError):
                    data[tc.input_key] = tc.input_value
                got_list = list(data)
                self.assertEqual(got_list, tc.input_list)


class TestTableDataDelItem(unittest.TestCase):
    def test(self) -> None:
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        del data[1]
        self.assertEqual(
            list[sw_compdocs.document.TableDataRow](data),
            list[sw_compdocs.document.TableDataRow](
                [
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ]
            ),
        )


class TestTableDataLen(unittest.TestCase):
    def test(self) -> None:
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        self.assertEqual(len(data), 3)


class TestTableDataRepr(unittest.TestCase):
    def test(self) -> None:
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        self.assertEqual(
            repr(data),
            "TableData(TableDataRow(['A1', 'A2', 'A3']), [TableDataRow(['B1', 'B2', 'B3']), TableDataRow(['C1', 'C2', 'C3']), TableDataRow(['D1', 'D2', 'D3'])])",
        )


class TestTableDataEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.document.TableData),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    [
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ],
                ),
                input_other=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    [
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ],
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    [
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ],
                ),
                input_other=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3+")),
                    [
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ],
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    [
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ],
                ),
                input_other=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    [
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3+")),
                    ],
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    [
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ],
                ),
                input_other=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestTableDataInsert(unittest.TestCase):
    def test_pass(self) -> None:
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        data.insert(1, sw_compdocs.document.TableDataRow(("C1", "C2", "C3")))
        self.assertEqual(
            list[sw_compdocs.document.TableDataRow](data),
            list[sw_compdocs.document.TableDataRow](
                [
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ]
            ),
        )

    def test_exc(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_item", sw_compdocs.document.TableDataRow),
                ("want_exc_type", type[Exception]),
            ],
        )

        for tc in [
            tt(
                input_item=sw_compdocs.document.TableDataRow(("B1", "B2")),
                want_exc_type=ValueError,
            ),
            tt(
                input_item=sw_compdocs.document.TableDataRow(("B1", "B2", "B3", "B4")),
                want_exc_type=ValueError,
            ),
        ]:
            with self.subTest(tc=tc):
                data = sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")), []
                )
                with self.assertRaises(tc.want_exc_type):
                    data.insert(0, tc.input_item)


class TestTableDataRowInit(unittest.TestCase):
    def test_pass(self) -> None:
        for input_list in [
            ["foo", "bar", "baz"],
            ["foo"],
        ]:
            with self.subTest(input_list=input_list):
                got_row = sw_compdocs.document.TableDataRow(input_list)
                got_list = list(got_row)
                self.assertEqual(got_list, input_list)

    def test_exc_value(self) -> None:
        with self.assertRaises(ValueError):
            sw_compdocs.document.TableDataRow([])


class TestTableDataRowGetItem(unittest.TestCase):
    def test(self) -> None:
        row = sw_compdocs.document.TableDataRow(("foo", "bar", "baz"))
        self.assertEqual(row[0], "foo")
        self.assertEqual(row[1], "bar")
        self.assertEqual(row[2], "baz")


class TestTableDataRowSetItem(unittest.TestCase):
    def test_pass_int(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_list", list[str]),
                ("input_key", int),
                ("input_value", str),
                ("want_list", list[str]),
            ],
        )

        for tc in [
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=0,
                input_value="qux",
                want_list=["qux", "bar", "baz"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=1,
                input_value="qux",
                want_list=["foo", "qux", "baz"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=2,
                input_value="qux",
                want_list=["foo", "bar", "qux"],
            ),
        ]:
            with self.subTest(tc=tc):
                row = sw_compdocs.document.TableDataRow(tc.input_list)
                row[tc.input_key] = tc.input_value
                got_list = list(row)
                self.assertEqual(got_list, tc.want_list)

    def test_pass_slice(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_list", list[str]),
                ("input_key", slice),
                ("input_value", list[str]),
                ("want_list", list[str]),
            ],
        )

        for tc in [
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(0, 2),
                input_value=["qux", "quux"],
                want_list=["qux", "quux", "baz"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(1, 3),
                input_value=["qux", "quux"],
                want_list=["foo", "qux", "quux"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(0, 3),
                input_value=["qux", "quux", "corge"],
                want_list=["qux", "quux", "corge"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=["qux", "quux", "corge"],
                want_list=["qux", "quux", "corge"],
            ),
        ]:
            with self.subTest(tc=tc):
                row = sw_compdocs.document.TableDataRow(tc.input_list)
                row[tc.input_key] = tc.input_value
                got_list = list(row)
                self.assertEqual(got_list, tc.want_list)

    def test_exc_value(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_list", list[str]),
                ("input_key", slice),
                ("input_value", list[str]),
            ],
        )

        for tc in [
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=["foo", "bar"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=["foo", "bar", "baz", "qux"],
            ),
        ]:
            with self.subTest(tc=tc):
                row = sw_compdocs.document.TableDataRow(tc.input_list)
                with self.assertRaises(ValueError):
                    row[tc.input_key] = tc.input_value
                got_list = list(row)
                self.assertEqual(got_list, tc.input_list)


class TestTableDataRowLen(unittest.TestCase):
    def test(self) -> None:
        row = sw_compdocs.document.TableDataRow(("foo", "bar", "baz"))
        self.assertEqual(len(row), 3)


class TestTableDataRowRepr(unittest.TestCase):
    def test(self) -> None:
        row = sw_compdocs.document.TableDataRow(("foo", "bar", "baz"))
        s = repr(row)
        self.assertEqual(s, "TableDataRow(['foo', 'bar', 'baz'])")


class TestTableDataRowEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.document.TableDataRow),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.document.TableDataRow(("foo", "bar", "baz")),
                input_other=sw_compdocs.document.TableDataRow(("foo", "bar", "baz")),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.document.TableDataRow(("foo", "bar", "baz")),
                input_other=sw_compdocs.document.TableDataRow(("foo", "bar", "qux")),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.document.TableDataRow(("foo", "bar", "baz")),
                input_other=["foo", "bar", "baz"],
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)
