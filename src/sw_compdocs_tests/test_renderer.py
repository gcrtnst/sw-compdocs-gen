import collections
import sw_compdocs.document
import sw_compdocs.renderer
import unittest


class TestRenderMarkdown(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_doc", "want_text"))

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
                    (
                        sw_compdocs.document.Heading("foo"),
                        sw_compdocs.document.Paragraph("bar"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(("baz",)), []
                            )
                        ),
                    )
                ),
                want_text="# foo\n\nbar\n\n| baz |\n| --- |\n",
            ),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown(tc.input_doc)
                self.assertEqual(got_text, tc.want_text)

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.renderer.render_markdown([])


class TestRenderMarkdownBlock(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_blk", "want_text"))

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
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_block(tc.input_blk)
                self.assertEqual(got_text, tc.want_text)

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.renderer.render_markdown_block("foo")


class TestRenderMarkdownHeading(unittest.TestCase):
    def test_pass(self):
        text = sw_compdocs.renderer.render_markdown_heading(
            sw_compdocs.document.Heading("foo")
        )
        self.assertEqual(text, "# foo\n")

    def test_pass_level(self):
        text = sw_compdocs.renderer.render_markdown_heading(
            sw_compdocs.document.Heading("foo", level=6)
        )
        self.assertEqual(text, "###### foo\n")

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.renderer.render_markdown_heading("foo")


class TestRenderMarkdownParagraph(unittest.TestCase):
    def test_pass(self):
        text = sw_compdocs.renderer.render_markdown_paragraph(
            sw_compdocs.document.Paragraph("foo")
        )
        self.assertEqual(text, "foo\n")

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.renderer.render_markdown_paragraph("foo")


class TestRenderMarkdownTable(unittest.TestCase):
    def test_pass(self):
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

    def test_exc_type(self):
        data = sw_compdocs.document.TableData(
            sw_compdocs.document.TableDataRow(("A1", "A2", "A3")),
            (
                sw_compdocs.document.TableDataRow(("B1", "B2", "B3")),
                sw_compdocs.document.TableDataRow(("C1", "C2", "C3")),
                sw_compdocs.document.TableDataRow(("D1", "D2", "D3")),
            ),
        )
        with self.assertRaises(TypeError):
            sw_compdocs.renderer.render_markdown_table(data)


class TestRenderMarkdownTableData(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_data", "want_text"))

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

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.renderer.render_markdown_table_data([])


class TestRenderMarkdownTableDataRow(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_row", "want_text"))

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

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.renderer.render_markdown_table_data_row(["foo"])


class TestRenderMarkdownTableDataDelimiter(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_n", "want_text"))

        for tc in [
            tt(input_n=1, want_text="| --- |\n"),
            tt(input_n=3, want_text="| --- | --- | --- |\n"),
        ]:
            with self.subTest(tc=tc):
                got_text = sw_compdocs.renderer.render_markdown_table_data_delimiter(
                    tc.input_n
                )
                self.assertEqual(got_text, tc.want_text)

    def test_exc(self):
        tt = collections.namedtuple("tt", ("input_n", "want_exc_type"))

        for tc in [
            tt(input_n=1.0, want_exc_type=TypeError),
            tt(input_n=0, want_exc_type=ValueError),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(tc.want_exc_type):
                    sw_compdocs.renderer.render_markdown_table_data_delimiter(
                        tc.input_n
                    )
