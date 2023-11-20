import collections
import sw_compdocs.document
import unittest


class TestDocumentInit(unittest.TestCase):
    def test_pass(self):
        for input_list in [
            [],
            [
                sw_compdocs.document.Heading("head"),
                sw_compdocs.document.Paragraph("para"),
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
            ],
        ]:
            with self.subTest(input_list=input_list):
                doc = sw_compdocs.document.Document(input_list)
                got_list = list(doc)
                self.assertEqual(got_list, input_list)

    def test_exc_type(self):
        for input_list in [
            [
                "head",
                sw_compdocs.document.Paragraph("para"),
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
            ],
            [
                sw_compdocs.document.Heading("head"),
                "para",
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
            ],
            [
                sw_compdocs.document.Heading("head"),
                sw_compdocs.document.Paragraph("para"),
                "tbl",
            ],
        ]:
            with self.subTest(input_list=input_list):
                with self.assertRaises(TypeError):
                    sw_compdocs.document.Document(input_list)


class TestDocumentGetItem(unittest.TestCase):
    def test(self):
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Heading("head"),
                sw_compdocs.document.Paragraph("para"),
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
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


class TestDocumentSetItem(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt", ("input_list", "input_key", "input_value", "want_list")
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
    def test(self):
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("bar"),
                sw_compdocs.document.Paragraph("baz"),
            ]
        )
        del doc[1]
        self.assertEqual(
            list(doc),
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("baz"),
            ],
        )


class TestDocumentLen(unittest.TestCase):
    def test(self):
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("bar"),
                sw_compdocs.document.Paragraph("baz"),
            ]
        )
        self.assertEqual(len(doc), 3)


class TestDocumentRepr(unittest.TestCase):
    def test(self):
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Heading("head"),
                sw_compdocs.document.Paragraph("para"),
                sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["tbl"])
                    )
                ),
            ]
        )

        want_s = (
            "Document(["
            + "Heading(text='head'), "
            + "Paragraph(text='para'), "
            + "Table(data=TableData(TableDataRow(['tbl']), []))"
            + "])"
        )
        got_s = repr(doc)
        self.assertEqual(got_s, want_s)


class TestDocumentEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

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
    def test_pass(self):
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("baz"),
            ]
        )
        doc.insert(1, sw_compdocs.document.Paragraph("bar"))
        self.assertEqual(
            list(doc),
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("bar"),
                sw_compdocs.document.Paragraph("baz"),
            ],
        )

    def test_exc_type(self):
        doc = sw_compdocs.document.Document(
            [
                sw_compdocs.document.Paragraph("foo"),
                sw_compdocs.document.Paragraph("baz"),
            ]
        )
        with self.assertRaises(TypeError):
            doc.insert(1, "bar")


class TestBlockInit(unittest.TestCase):
    def test(self):
        with self.assertRaises(NotImplementedError):
            sw_compdocs.document.Block()


class TestHeadingInit(unittest.TestCase):
    def test_pass(self):
        head = sw_compdocs.document.Heading("foo")
        self.assertEqual(head.text, "foo")

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.document.Heading(0)


class TestHeadingTextSetter(unittest.TestCase):
    def test_pass(self):
        head = sw_compdocs.document.Heading("foo")
        head.text = "bar"
        self.assertEqual(head.text, "bar")

    def test_exc_type(self):
        head = sw_compdocs.document.Heading("foo")
        with self.assertRaises(TypeError):
            head.text = 0


class TestHeadingRepr(unittest.TestCase):
    def test(self):
        head = sw_compdocs.document.Heading("foo")
        s = repr(head)
        self.assertEqual(s, "Heading(text='foo')")


class TestHeadingEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        for tc in [
            tt(
                input_self=sw_compdocs.document.Heading("foo"),
                input_other=sw_compdocs.document.Heading("foo"),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.document.Heading("foo"),
                input_other=sw_compdocs.document.Heading("bar"),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.document.Heading("foo"),
                input_other="foo",
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestParagraphInit(unittest.TestCase):
    def test_pass(self):
        para = sw_compdocs.document.Paragraph("foo")
        self.assertEqual(para.text, "foo")

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.document.Paragraph(0)


class TestParagraphTextSetter(unittest.TestCase):
    def test_pass(self):
        para = sw_compdocs.document.Paragraph("foo")
        para.text = "bar"
        self.assertEqual(para.text, "bar")

    def test_exc_type(self):
        para = sw_compdocs.document.Paragraph("foo")
        with self.assertRaises(TypeError):
            para.text = 0


class TestParagraphRepr(unittest.TestCase):
    def test(self):
        para = sw_compdocs.document.Paragraph("foo")
        s = repr(para)
        self.assertEqual(s, "Paragraph(text='foo')")


class TestParagraphEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        for tc in [
            tt(
                input_self=sw_compdocs.document.Paragraph("foo"),
                input_other=sw_compdocs.document.Paragraph("foo"),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.document.Paragraph("foo"),
                input_other=sw_compdocs.document.Paragraph("bar"),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.document.Paragraph("foo"),
                input_other="foo",
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestTableInit(unittest.TestCase):
    def test_pass(self):
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        tbl = sw_compdocs.document.Table(data)
        self.assertEqual(tbl.data, data)

    def test_exc_type(self):
        data = [
            sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
            sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
            sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
        ]
        with self.assertRaises(TypeError):
            sw_compdocs.document.Table(data)


class TestTableDataSetter(unittest.TestCase):
    def test_pass(self):
        data1 = sw_compdocs.document.TableData(sw_compdocs.document.TableDataRow("1"))
        data2 = sw_compdocs.document.TableData(sw_compdocs.document.TableDataRow("2"))

        tbl = sw_compdocs.document.Table(data1)
        tbl.data = data2
        self.assertEqual(tbl.data, data2)

    def test_exc_type(self):
        data1 = sw_compdocs.document.TableData(sw_compdocs.document.TableDataRow("1"))
        data2 = sw_compdocs.document.TableDataRow("2")

        tbl = sw_compdocs.document.Table(data1)
        with self.assertRaises(TypeError):
            tbl.data = data2


class TestTableRepr(unittest.TestCase):
    def test(self):
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        tbl = sw_compdocs.document.Table(data)
        s = repr(tbl)
        self.assertEqual(
            s,
            "Table(data=TableData(TableDataRow(['A1', 'A2', 'A3']), [TableDataRow(['B1', 'B2', 'B3']), TableDataRow(['C1', 'C2', 'C3']), TableDataRow(['D1', 'D2', 'D3'])]))",
        )


class TestTableEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        data1 = sw_compdocs.document.TableData(sw_compdocs.document.TableDataRow("1"))
        data2 = sw_compdocs.document.TableData(sw_compdocs.document.TableDataRow("2"))
        for tc in [
            tt(
                input_self=sw_compdocs.document.Table(data1),
                input_other=sw_compdocs.document.Table(data1),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.document.Table(data1),
                input_other=sw_compdocs.document.Table(data2),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.document.Table(data1),
                input_other=data1,
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestTableDataInit(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_head", "input_list"))

        for tc in [
            tt(
                input_head=sw_compdocs.document.TableDataRow(),
                input_list=[],
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(),
                input_list=[
                    sw_compdocs.document.TableDataRow(),
                    sw_compdocs.document.TableDataRow(),
                    sw_compdocs.document.TableDataRow(),
                ],
            ),
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

    def test_exc(self):
        tt = collections.namedtuple("tt", ("input_head", "input_list", "want_exc_type"))

        for tc in [
            tt(
                input_head=[],
                input_list=[],
                want_exc_type=TypeError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(),
                input_list=[
                    [],
                    sw_compdocs.document.TableDataRow(),
                    sw_compdocs.document.TableDataRow(),
                ],
                want_exc_type=TypeError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(),
                input_list=[
                    sw_compdocs.document.TableDataRow(),
                    [],
                    sw_compdocs.document.TableDataRow(),
                ],
                want_exc_type=TypeError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(),
                input_list=[
                    sw_compdocs.document.TableDataRow(),
                    sw_compdocs.document.TableDataRow(),
                    [],
                ],
                want_exc_type=TypeError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                want_exc_type=ValueError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3", "B4")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                want_exc_type=ValueError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                want_exc_type=ValueError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3", "C4")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                want_exc_type=ValueError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2")),
                ],
                want_exc_type=ValueError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3", "D4")),
                ],
                want_exc_type=ValueError,
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(tc.want_exc_type):
                    sw_compdocs.document.TableData(tc.input_head, tc.input_list)


class TestTableDataGetItem(unittest.TestCase):
    def test(self):
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
    def test_pass(self):
        tt = collections.namedtuple(
            "tt", ("input_head", "input_list", "input_key", "input_value", "want_list")
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

    def test_exc(self):
        tt = collections.namedtuple(
            "tt", ("input_head", "input_list", "input_key", "input_value", "want_exc")
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
                input_value=["E1", "E2", "E3"],
                want_exc=TypeError,
            ),
            tt(
                input_head=sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                input_list=[
                    sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                    sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                    sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                ],
                input_key=1,
                input_value=sw_compdocs.document.TableDataRow(("E1", "E2")),
                want_exc=ValueError,
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
                want_exc=ValueError,
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
                    ["E1", "E2", "E3"],
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3")),
                ],
                want_exc=TypeError,
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
                    ["F1", "F2", "F3"],
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3")),
                ],
                want_exc=TypeError,
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
                    ["G1", "G2", "G3"],
                ],
                want_exc=TypeError,
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
                    sw_compdocs.document.TableDataRow(("E1", "E2", "E3", "E4")),
                    sw_compdocs.document.TableDataRow(("F1", "F2", "F3")),
                    sw_compdocs.document.TableDataRow(("G1", "G2", "G3")),
                ],
                want_exc=ValueError,
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
                want_exc=ValueError,
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
                want_exc=ValueError,
            ),
        ]:
            with self.subTest(tc=tc):
                data = sw_compdocs.document.TableData(tc.input_head, tc.input_list)
                with self.assertRaises(tc.want_exc):
                    data[tc.input_key] = tc.input_value
                got_list = list(data)
                self.assertEqual(got_list, tc.input_list)


class TestTableDataDelItem(unittest.TestCase):
    def test(self):
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
            list(data),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )


class TestTableDataLen(unittest.TestCase):
    def test(self):
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
    def test(self):
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
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

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
    def test_pass(self):
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )
        data.insert(1, sw_compdocs.document.TableDataRow(("C1", "C2", "C3")))
        self.assertEqual(
            list(data),
            [
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ],
        )

    def test_exc(self):
        tt = collections.namedtuple("tt", ("input_item", "want_exc_type"))

        for tc in [
            tt(
                input_item=[],
                want_exc_type=TypeError,
            ),
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
    def test_pass(self):
        for input_list in [
            [],
            ["foo", "bar", "baz"],
        ]:
            with self.subTest(input_list=input_list):
                got_row = sw_compdocs.document.TableDataRow(input_list)
                got_list = list(got_row)
                self.assertEqual(got_list, input_list)

    def test_exc_type(self):
        for input_list in [
            [0],
            ["foo", 1, "baz"],
        ]:
            with self.subTest(input_list=input_list):
                with self.assertRaises(TypeError):
                    sw_compdocs.document.TableDataRow(input_list)


class TestTableDataRowGetItem(unittest.TestCase):
    def test(self):
        row = sw_compdocs.document.TableDataRow(("foo", "bar", "baz"))
        self.assertEqual(row[0], "foo")
        self.assertEqual(row[1], "bar")
        self.assertEqual(row[2], "baz")


class TestTableDataRowSetItem(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt", ("input_list", "input_key", "input_value", "want_list")
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

    def test_exc_value(self):
        tt = collections.namedtuple("tt", ("input_list", "input_key", "input_value"))

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
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=[0, 1],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=[0, 1, 2, 3],
            ),
        ]:
            with self.subTest(tc=tc):
                row = sw_compdocs.document.TableDataRow(tc.input_list)
                with self.assertRaises(ValueError):
                    row[tc.input_key] = tc.input_value
                got_list = list(row)
                self.assertEqual(got_list, tc.input_list)

    def test_exc_type(self):
        tt = collections.namedtuple("tt", ("input_list", "input_key", "input_value"))

        for tc in [
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=0,
                input_value=52149,
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=[52149, "bar", "baz"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=["foo", 52149, "baz"],
            ),
            tt(
                input_list=["foo", "bar", "baz"],
                input_key=slice(None, None),
                input_value=["foo", "bar", 52149],
            ),
        ]:
            with self.subTest(tc=tc):
                row = sw_compdocs.document.TableDataRow(tc.input_list)
                with self.assertRaises(TypeError):
                    row[tc.input_key] = tc.input_value
                got_list = list(row)
                self.assertEqual(got_list, tc.input_list)


class TestTableDataRowLen(unittest.TestCase):
    def test(self):
        row = sw_compdocs.document.TableDataRow(("foo", "bar", "baz"))
        self.assertEqual(len(row), 3)


class TestTableDataRowRepr(unittest.TestCase):
    def test(self):
        row = sw_compdocs.document.TableDataRow(("foo", "bar", "baz"))
        s = repr(row)
        self.assertEqual(s, "TableDataRow(['foo', 'bar', 'baz'])")


class TestTableDataRowEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

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
