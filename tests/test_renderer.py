import sw_compdocs.document
import sw_compdocs.renderer
import typing
import unittest


class TestRenderMarkdownHeading(unittest.TestCase):
    def test_pass(self) -> None:
        text = sw_compdocs.renderer.render_markdown_heading(
            sw_compdocs.document.Heading("foo")
        )
        self.assertEqual(text, "# foo\n")

    def test_pass_level(self) -> None:
        text = sw_compdocs.renderer.render_markdown_heading(
            sw_compdocs.document.Heading("foo", level=6)
        )
        self.assertEqual(text, "###### foo\n")

    def test_exc_value(self) -> None:
        for level in [0, 7]:
            with self.subTest(level=level):
                with self.assertRaises(ValueError):
                    sw_compdocs.renderer.render_markdown_heading(
                        sw_compdocs.document.Heading("foo", level=level)
                    )


class TestRenderMarkdownParagraph(unittest.TestCase):
    def test_pass(self) -> None:
        text = sw_compdocs.renderer.render_markdown_paragraph(
            sw_compdocs.document.Paragraph("foo")
        )
        self.assertEqual(text, "foo\n")


class TestRenderMarkdownListUnordered(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_ul", sw_compdocs.document.UnorderedList),
                ("want_text", str),
            ],
        )

        for tc in [
            # empty
            tt(
                input_ul=sw_compdocs.document.UnorderedList(),
                want_text="",
            ),
            # flat
            tt(
                input_ul=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem("a"),
                        sw_compdocs.document.ListItem("b"),
                        sw_compdocs.document.ListItem("c"),
                    ]
                ),
                want_text="- a\n- b\n- c\n",
            ),
            # nested
            tt(
                input_ul=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem(
                            "a",
                            [
                                sw_compdocs.document.ListItem(
                                    "b",
                                    [
                                        sw_compdocs.document.ListItem("c"),
                                    ],
                                )
                            ],
                        ),
                    ]
                ),
                want_text="- a\n  - b\n    - c\n",
            ),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_list_unordered(
                    tc.input_ul
                )
                self.assertEqual(got_text, tc.want_text)


class TestRenderMarkdownTableDataDelimiter(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple("tt", [("input_n", int), ("want_text", str)])

        for tc in [
            tt(input_n=1, want_text="| --- |\n"),
            tt(input_n=3, want_text="| --- | --- | --- |\n"),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_table_data_delimiter(
                    tc.input_n
                )
                self.assertEqual(got_text, tc.want_text)

    def test_exc_value(self) -> None:
        with self.assertRaises(ValueError):
            sw_compdocs.renderer.render_markdown_table_data_delimiter(0)


class TestRenderMarkdownTableDataRow(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_row", sw_compdocs.document.TableDataRow),
                ("want_text", str),
            ],
        )

        for tc in [
            tt(
                input_row=sw_compdocs.document.TableDataRow(("foo",)),
                want_text="| foo |\n",
            ),
            tt(
                input_row=sw_compdocs.document.TableDataRow(("foo", "bar", "baz")),
                want_text="| foo | bar | baz |\n",
            ),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_table_data_row(
                    tc.input_row
                )
                self.assertEqual(got_text, tc.want_text)


class TestRenderMarkdownTableData(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_data", sw_compdocs.document.TableData),
                ("want_text", str),
            ],
        )

        for tc in [
            tt(
                input_data=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1",)),
                    (),
                ),
                want_text="| A1 |\n| --- |\n",
            ),
            tt(
                input_data=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1",)),
                    (
                        sw_compdocs.document.TableDataRow(("B1",)),
                        sw_compdocs.document.TableDataRow(("C1",)),
                        sw_compdocs.document.TableDataRow(("D1",)),
                    ),
                ),
                want_text="| A1 |\n| --- |\n| B1 |\n| C1 |\n| D1 |\n",
            ),
            tt(
                input_data=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    (),
                ),
                want_text="| A1 | A2 | A3 |\n| --- | --- | --- |\n",
            ),
            tt(
                input_data=sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    (
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ),
                ),
                want_text="| A1 | A2 | A3 |\n| --- | --- | --- |\n| B1 | B2 | B3 |\n| C1 | C2 | C3 |\n| D1 | D2 | D3 |\n",
            ),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_table_data(
                    tc.input_data
                )
                self.assertEqual(got_text, tc.want_text)


class TestRenderMarkdownTable(unittest.TestCase):
    def test_pass(self) -> None:
        text = sw_compdocs.renderer.render_markdown_table(
            sw_compdocs.document.Table(
                sw_compdocs.document.TableData(
                    sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                    (
                        sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                        sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                        sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                    ),
                )
            )
        )
        self.assertEqual(
            text,
            "| A1 | A2 | A3 |\n| --- | --- | --- |\n| B1 | B2 | B3 |\n| C1 | C2 | C3 |\n| D1 | D2 | D3 |\n",
        )


class TestRenderMarkdownCallout(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_callout", sw_compdocs.document.Callout),
                ("want_text", str),
            ],
        )

        for tc in [
            tt(
                input_callout=sw_compdocs.document.Callout(
                    "", kind=sw_compdocs.document.CalloutKind.NOTE
                ),
                want_text="> [!NOTE]\n> \n",
            ),
            tt(
                input_callout=sw_compdocs.document.Callout(
                    "", kind=sw_compdocs.document.CalloutKind.WARNING
                ),
                want_text="> [!WARNING]\n> \n",
            ),
            tt(
                input_callout=sw_compdocs.document.Callout("callout"),
                want_text="> [!NOTE]\n> callout\n",
            ),
            tt(
                input_callout=sw_compdocs.document.Callout("\nline 1\nline 2\n"),
                want_text="> [!NOTE]\n> \n> line 1\n> line 2\n> \n",
            ),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_callout(
                    tc.input_callout
                )
                self.assertEqual(got_text, tc.want_text)


class TestRenderMarkdownBlock(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_blk", sw_compdocs.document.Block),
                ("want_text", str),
            ],
        )

        for tc in [
            tt(
                input_blk=sw_compdocs.document.Heading("foo"),
                want_text="# foo\n",
            ),
            tt(
                input_blk=sw_compdocs.document.Paragraph("foo"),
                want_text="foo\n",
            ),
            tt(
                input_blk=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem("a"),
                        sw_compdocs.document.ListItem("b"),
                        sw_compdocs.document.ListItem("c"),
                    ]
                ),
                want_text="- a\n- b\n- c\n",
            ),
            tt(
                input_blk=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
                        (
                            sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                            sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                            sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
                        ),
                    )
                ),
                want_text="| A1 | A2 | A3 |\n| --- | --- | --- |\n| B1 | B2 | B3 |\n| C1 | C2 | C3 |\n| D1 | D2 | D3 |\n",
            ),
            tt(
                input_blk=sw_compdocs.document.Callout(
                    "callout", kind=sw_compdocs.document.CalloutKind.NOTE
                ),
                want_text="> [!NOTE]\n> callout\n",
            ),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_block(tc.input_blk)
                self.assertEqual(got_text, tc.want_text)


class TestRenderMarkdown(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_doc", sw_compdocs.document.Document),
                ("want_text", str),
            ],
        )

        for tc in [
            tt(
                input_doc=sw_compdocs.document.Document(()),
                want_text="",
            ),
            tt(
                input_doc=sw_compdocs.document.Document(
                    (sw_compdocs.document.Heading("foo"),)
                ),
                want_text="# foo\n",
            ),
            tt(
                input_doc=sw_compdocs.document.Document(
                    (sw_compdocs.document.Paragraph("foo"),)
                ),
                want_text="foo\n",
            ),
            tt(
                input_doc=sw_compdocs.document.Document(
                    (
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(("foo",)), []
                            )
                        ),
                    )
                ),
                want_text="| foo |\n| --- |\n",
            ),
            tt(
                input_doc=sw_compdocs.document.Document(
                    (sw_compdocs.document.Callout("foo"),)
                ),
                want_text="> [!NOTE]\n> foo\n",
            ),
            tt(
                input_doc=sw_compdocs.document.Document(
                    (
                        sw_compdocs.document.Heading("foo"),
                        sw_compdocs.document.Paragraph("bar"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(("baz",)), []
                            )
                        ),
                        sw_compdocs.document.Callout("qux"),
                    )
                ),
                want_text="# foo\n\nbar\n\n| baz |\n| --- |\n\n> [!NOTE]\n> qux\n",
            ),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown(tc.input_doc)
                self.assertEqual(got_text, tc.want_text)
