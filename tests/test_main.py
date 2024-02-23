import collections.abc
import csv
import errno
import io
import lxml.etree
import pathlib
import sw_compdocs.component
import sw_compdocs.generator
import sw_compdocs.language
import sw_compdocs.main
import sw_compdocs.resource
import sw_compdocs.steamfind
import sw_compdocs.template
import sw_compdocs.wraperr
import sys
import tempfile
import typing
import unittest
import unittest.mock


class TestFormatOSError(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple("tt", [("input_exc", OSError), ("want_s", str)])

        for tc in [
            tt(
                input_exc=OSError("message"),
                want_s="message",
            ),
            tt(
                input_exc=OSError(errno.ENOENT, "strerror"),
                want_s="strerror",
            ),
            tt(
                input_exc=OSError(errno.ENOENT, "strerror", "filename"),
                want_s="strerror (file: 'filename')",
            ),
            tt(
                input_exc=OSError(errno.ENOENT, "strerror", "filename", 2),
                want_s="strerror (file: 'filename')",
            ),
            tt(
                input_exc=OSError(errno.ENOENT, "strerror", "filename", 2, "filename2"),
                want_s="strerror (file: 'filename', 'filename2')",
            ),
            tt(
                input_exc=OSError(
                    errno.ENOENT, "strerror", b"filename", 2, b"filename2"
                ),
                want_s="strerror (file: 'filename', 'filename2')",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.main.format_os_error(tc.input_exc)
                self.assertEqual(got_s, tc.want_s)


class TestFromatSyntaxError(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple("tt", [("input_exc", SyntaxError), ("want_s", str)])

        for tc in [
            tt(
                input_exc=SyntaxError("message"),
                want_s="message",
            ),
            tt(
                input_exc=SyntaxError("message", ("filename", None, None, None)),
                want_s="message (file 'filename')",
            ),
            tt(
                input_exc=SyntaxError("message", (None, 1, None, None)),
                want_s="message (line 1)",
            ),
            tt(
                input_exc=SyntaxError("message", (None, None, 2, None)),
                want_s="message (column 2)",
            ),
            tt(
                input_exc=SyntaxError("message", ("filename", 1, None, None)),
                want_s="message (file 'filename', line 1)",
            ),
            tt(
                input_exc=SyntaxError("message", ("filename", None, 2, None)),
                want_s="message (file 'filename', column 2)",
            ),
            tt(
                input_exc=SyntaxError("message", (None, 1, 2, None)),
                want_s="message (line 1, column 2)",
            ),
            tt(
                input_exc=SyntaxError("message", ("filename", 1, 2, None)),
                want_s="message (file 'filename', line 1, column 2)",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.main.format_syntax_error(tc.input_exc)
                self.assertEqual(got_s, tc.want_s)


class TestRun(unittest.TestCase):
    def test_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            doc_file = pathlib.Path(temp_dir, "out.md")
            comp_dir = pathlib.Path(temp_dir, "definitions")
            comp_dir.mkdir()
            sw_compdocs.main.run(doc_file=doc_file, comp_dir=comp_dir)

            with open(doc_file, mode="r", encoding="utf-8", newline="\n") as fp:
                got_md = fp.read()
            self.assertEqual(got_md, "")

    def test_all(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            doc_file = pathlib.Path(temp_dir, "out.md")

            comp_dir = pathlib.Path(temp_dir, "definitions")
            comp_dir.mkdir()

            comp_file = pathlib.Path(comp_dir, "test_01.xml")
            with open(comp_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            comp_file = pathlib.Path(comp_dir, "test_02.xml")
            with open(comp_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            comp_file = pathlib.Path(comp_dir, "dummy")
            comp_file.mkdir()

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
PROP_TABLE_HEAD_LABEL = "ラベル"
PROP_TABLE_HEAD_VALUE = "値"
PROP_TABLE_MASS_LABEL = "重量"
PROP_TABLE_DIMS_LABEL = "サイズ（WxDxH）"
PROP_TABLE_COST_LABEL = "価格"
PROP_TABLE_TAGS_LABEL = "タグ"
"""
                )

            lang_file = pathlib.Path(temp_dir, "japanese.tsv")
            lang_list = [
                ["id", "description", "en", "local"],
                ["", "", "PROPERTIES", "プロパティ"],
                ["def_test_01_name", "", "", "テスト 01"],
                ["def_test_01_s_desc", "", "", "$[template_01]"],
                ["def_test_01_desc", "", "", ""],
                ["def_test_02_name", "", "", "テスト 02"],
                ["def_test_02_s_desc", "", "", "$[template_02]"],
                ["def_test_02_desc", "", "", ""],
            ]
            with open(lang_file, mode="x", encoding="utf-8", newline="\n") as fp:
                w = csv.writer(fp, dialect=sw_compdocs.language.LanguageTSVDialect)
                w.writerows(lang_list)

            template_file = pathlib.Path(temp_dir, "template.toml")
            with open(template_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[template]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            sw_compdocs.main.run(
                doc_file=doc_file,
                comp_dir=comp_dir,
                label_file=label_file,
                lang_file=lang_file,
                template_file=template_file,
                doc_encoding="shift-jis",
                doc_newline="\r\n",
            )

            with open(doc_file, mode="r", encoding="shift-jis", newline="\r\n") as fp:
                got_md = fp.read()
            got_md = got_md.replace("\r\n", "\n")

            want_md = """\
# Blocks

## テスト 01

テンプレート 01

### プロパティ

| ラベル | 値 |
| --- | --- |
| 重量 | 1 |
| サイズ（WxDxH） | 1x1x1 |
| 価格 | 0 |
| タグ |  |

## テスト 02

テンプレート 02

### プロパティ

| ラベル | 値 |
| --- | --- |
| 重量 | 2 |
| サイズ（WxDxH） | 1x1x1 |
| 価格 | 0 |
| タグ |  |
"""
            self.assertEqual(got_md, want_md)


class TestMain(unittest.TestCase):
    def test_argp(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_args", collections.abc.Sequence[str]),
                ("want_call_args", unittest.mock._Call),
            ],
        )

        for tc in [
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    doc_file="path/to/output",
                    comp_dir="path/to/definitions",
                    label_file=None,
                    lang_file=None,
                    template_file=None,
                    doc_encoding="utf-8",
                    doc_newline="\n",
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--label",
                    "path/to/label",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    doc_file="path/to/output",
                    comp_dir="path/to/definitions",
                    label_file="path/to/label",
                    lang_file=None,
                    template_file=None,
                    doc_encoding="utf-8",
                    doc_newline="\n",
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--language",
                    "path/to/language",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    doc_file="path/to/output",
                    comp_dir="path/to/definitions",
                    label_file=None,
                    lang_file="path/to/language",
                    template_file=None,
                    doc_encoding="utf-8",
                    doc_newline="\n",
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--template",
                    "path/to/template",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    doc_file="path/to/output",
                    comp_dir="path/to/definitions",
                    label_file=None,
                    lang_file=None,
                    template_file="path/to/template",
                    doc_encoding="utf-8",
                    doc_newline="\n",
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--encoding",
                    "shift-jis",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    doc_file="path/to/output",
                    comp_dir="path/to/definitions",
                    label_file=None,
                    lang_file=None,
                    template_file=None,
                    doc_encoding="shift-jis",
                    doc_newline="\n",
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--newline",
                    "CR",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    doc_file="path/to/output",
                    comp_dir="path/to/definitions",
                    label_file=None,
                    lang_file=None,
                    template_file=None,
                    doc_encoding="utf-8",
                    doc_newline="\r",
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--newline",
                    "CRLF",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    doc_file="path/to/output",
                    comp_dir="path/to/definitions",
                    label_file=None,
                    lang_file=None,
                    template_file=None,
                    doc_encoding="utf-8",
                    doc_newline="\r\n",
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                with (
                    unittest.mock.patch.object(sw_compdocs.main, "run") as mock,
                    unittest.mock.patch.object(sys, "stdout", new=io.StringIO()),
                    unittest.mock.patch.object(sys, "stderr", new=io.StringIO()),
                ):
                    sw_compdocs.main.main(args=tc.input_args)

                mock_call_args: object = mock.call_args
                self.assertEqual(mock_call_args, tc.want_call_args)

    def test_argp_definitions_default(self) -> None:
        definitions = sw_compdocs.steamfind.find_definitions()
        if definitions is None:
            self.skipTest("Definitions folder not found")

        with (
            unittest.mock.patch.object(sw_compdocs.main, "run") as mock,
            unittest.mock.patch.object(sys, "stdout", new=io.StringIO()),
            unittest.mock.patch.object(sys, "stderr", new=io.StringIO()),
        ):
            sw_compdocs.main.main(args=["path/to/output"])

        mock_call_args: object = mock.call_args
        self.assertEqual(
            mock_call_args,
            unittest.mock.call(
                doc_file="path/to/output",
                comp_dir=str(definitions),
                label_file=None,
                lang_file=None,
                template_file=None,
                doc_encoding="utf-8",
                doc_newline="\n",
            ),
        )

    def test_argp_definitions_required(self) -> None:
        if sw_compdocs.steamfind.find_definitions() is not None:
            self.skipTest("Definitions folder found")

        with (
            self.assertRaises(SystemExit) as ctx,
            unittest.mock.patch.object(sw_compdocs.main, "run") as mock,
            unittest.mock.patch.object(sys, "stdout", new=io.StringIO()),
            unittest.mock.patch.object(sys, "stderr", new=io.StringIO()),
        ):
            sw_compdocs.main.main(args=["path/to/output"])
        self.assertEqual(ctx.exception.code, 2)

        mock_call_args: object = mock.call_args
        self.assertIsNone(mock_call_args)

    def test_argp_newline_invalid(self) -> None:
        with (
            self.assertRaises(SystemExit) as ctx,
            unittest.mock.patch.object(sw_compdocs.main, "run") as mock,
            unittest.mock.patch.object(sys, "stdout", new=io.StringIO()),
            unittest.mock.patch.object(sys, "stderr", new=io.StringIO()),
        ):
            sw_compdocs.main.main(
                args=[
                    "--definitions",
                    "path/to/definitions",
                    "--newline",
                    "LFCR",
                    "path/to/output",
                ]
            )
        self.assertEqual(ctx.exception.code, 2)

        mock_call_args: object = mock.call_args
        self.assertIsNone(mock_call_args)

    def test_except(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_exc", Exception),
                ("want_stderr", str),
            ],
        )

        for tc in [
            tt(
                input_exc=sw_compdocs.component.ComponentXMLError("message"),
                want_stderr="sw_compdocs: error: message\n",
            ),
            tt(
                input_exc=sw_compdocs.generator.LabelKeyError("key"),
                want_stderr="sw_compdocs: error: missing label text for key 'key'\n",
            ),
            tt(
                input_exc=sw_compdocs.language.LanguageTSVError("message"),
                want_stderr="sw_compdocs: error: message\n",
            ),
            tt(
                input_exc=sw_compdocs.language.LanguageFindIDError("id"),
                want_stderr="sw_compdocs: error: missing translation for id 'id'\n",
            ),
            tt(
                input_exc=sw_compdocs.language.LanguageFindEnError("english text"),
                want_stderr="sw_compdocs: error: missing translation for text 'english text'\n",
            ),
            tt(
                input_exc=sw_compdocs.resource.ResourceFileError(
                    "message", file="path/to/resource.toml"
                ),
                want_stderr="sw_compdocs: error: message (in file 'path/to/resource.toml')\n",
            ),
            tt(
                input_exc=sw_compdocs.resource.TOMLFileDecodeError(
                    "message", file="path/to/resource.toml"
                ),
                want_stderr="sw_compdocs: error: message (in file 'path/to/resource.toml')\n",
            ),
            tt(
                input_exc=sw_compdocs.template.TemplateKeyError("key"),
                want_stderr="sw_compdocs: error: missing replacement string for placeholder $[key]\n",
            ),
            tt(
                input_exc=sw_compdocs.wraperr.UnicodeEncodeFileError(
                    "encoding", "object", 0, 1, "reason", filename="path/to/file"
                ),
                want_stderr="sw_compdocs: error: 'encoding' codec can't encode character '\\x6f' in file 'path/to/file': reason\n",
            ),
            tt(
                input_exc=sw_compdocs.wraperr.UnicodeDecodeFileError(
                    "encoding", b"object", 0, 1, "reason", filename="path/to/file"
                ),
                want_stderr="sw_compdocs: error: 'encoding' codec can't decode byte 0x6f in file 'path/to/file': reason\n",
            ),
            tt(
                input_exc=sw_compdocs.wraperr.UnicodeTranslateFileError(
                    "object", 0, 1, "reason", filename="path/to/file"
                ),
                want_stderr="sw_compdocs: error: can't translate character '\\x6f' in file 'path/to/file': reason\n",
            ),
            tt(
                input_exc=lxml.etree.XMLSyntaxError(
                    "message", 0, 1, 3, filename="path/to/xml"
                ),
                want_stderr="sw_compdocs: error: message (file 'path/to/xml', line 1, column 2)\n",
            ),
            tt(
                input_exc=OSError(errno.ENOENT, "strerror", "filename", 2, "filename2"),
                want_stderr="sw_compdocs: error: strerror (file: 'filename', 'filename2')\n",
            ),
        ]:
            with self.subTest(tc=tc):
                stderr = io.StringIO()
                with (
                    self.assertRaises(SystemExit) as ctx,
                    unittest.mock.patch.object(sw_compdocs.main, "run") as mock,
                    unittest.mock.patch.object(sys, "stdout", new=io.StringIO()),
                    unittest.mock.patch.object(sys, "stderr", new=stderr),
                ):
                    mock.side_effect = tc.input_exc
                    sw_compdocs.main.main(
                        prog="sw_compdocs",
                        args=[
                            "--definitions",
                            "path/to/definitions",
                            "path/to/output",
                        ],
                    )
                self.assertEqual(ctx.exception.code, 1)
                self.assertEqual(stderr.getvalue(), tc.want_stderr)

    def test_except_unhandled(self) -> None:
        stderr = io.StringIO()
        with (
            self.assertRaises(Exception),
            unittest.mock.patch.object(sw_compdocs.main, "run") as mock,
            unittest.mock.patch.object(sys, "stdout", new=io.StringIO()),
            unittest.mock.patch.object(sys, "stderr", new=stderr),
        ):
            mock.side_effect = Exception()
            sw_compdocs.main.main(
                args=[
                    "--definitions",
                    "path/to/definitions",
                    "path/to/output",
                ]
            )
        self.assertEqual(stderr.getvalue(), "")

    def test_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            doc_file = pathlib.Path(temp_dir, "out.md")

            comp_dir = pathlib.Path(temp_dir, "definitions")
            comp_dir.mkdir()

            comp_file = pathlib.Path(comp_dir, "test_01.xml")
            with open(comp_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            comp_file = pathlib.Path(comp_dir, "test_02.xml")
            with open(comp_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
PROP_TABLE_HEAD_LABEL = "ラベル"
PROP_TABLE_HEAD_VALUE = "値"
PROP_TABLE_MASS_LABEL = "重量"
PROP_TABLE_DIMS_LABEL = "サイズ（WxDxH）"
PROP_TABLE_COST_LABEL = "価格"
PROP_TABLE_TAGS_LABEL = "タグ"
"""
                )

            lang_file = pathlib.Path(temp_dir, "japanese.tsv")
            lang_list = [
                ["id", "description", "en", "local"],
                ["", "", "PROPERTIES", "プロパティ"],
                ["def_test_01_name", "", "", "テスト 01"],
                ["def_test_01_s_desc", "", "", "$[template_01]"],
                ["def_test_01_desc", "", "", ""],
                ["def_test_02_name", "", "", "テスト 02"],
                ["def_test_02_s_desc", "", "", "$[template_02]"],
                ["def_test_02_desc", "", "", ""],
            ]
            with open(lang_file, mode="x", encoding="utf-8", newline="\n") as fp:
                w = csv.writer(fp, dialect=sw_compdocs.language.LanguageTSVDialect)
                w.writerows(lang_list)

            template_file = pathlib.Path(temp_dir, "template.toml")
            with open(template_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[template]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                unittest.mock.patch.object(sys, "stdout", new=stdout),
                unittest.mock.patch.object(sys, "stderr", new=stderr),
            ):
                sw_compdocs.main.main(
                    args=[
                        "--definitions",
                        str(comp_dir),
                        "--label",
                        str(label_file),
                        "--language",
                        str(lang_file),
                        "--template",
                        str(template_file),
                        "--encoding",
                        "shift-jis",
                        "--newline",
                        "CRLF",
                        str(doc_file),
                    ]
                )
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")

            with open(doc_file, mode="r", encoding="shift-jis", newline="\r\n") as fp:
                got_md = fp.read()
            got_md = got_md.replace("\r\n", "\n")

            want_md = """\
# Blocks

## テスト 01

テンプレート 01

### プロパティ

| ラベル | 値 |
| --- | --- |
| 重量 | 1 |
| サイズ（WxDxH） | 1x1x1 |
| 価格 | 0 |
| タグ |  |

## テスト 02

テンプレート 02

### プロパティ

| ラベル | 値 |
| --- | --- |
| 重量 | 2 |
| サイズ（WxDxH） | 1x1x1 |
| 価格 | 0 |
| タグ |  |
"""
            self.assertEqual(got_md, want_md)
