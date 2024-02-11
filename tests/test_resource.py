import pathlib
import sw_compdocs._types
import sw_compdocs.resource
import tempfile
import tomllib
import typing
import unittest


class TestResourceFileErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.resource.ResourceFileError("msg", file="file")
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("msg",))
        self.assertEqual(exc.msg, "msg")
        self.assertEqual(exc.file, "file")


class TestResourceFileErrorStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_msg", str),
                ("input_file", sw_compdocs._types.StrOrBytesPath | None),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_msg="msg",
                input_file=None,
                want_s="msg",
            ),
            tt(
                input_msg="msg",
                input_file="file",
                want_s="msg (in file 'file')",
            ),
            tt(
                input_msg="msg",
                input_file=b"file",
                want_s="msg (in file 'file')",
            ),
            tt(
                input_msg="msg",
                input_file=pathlib.PurePath("file"),
                want_s="msg (in file 'file')",
            ),
        ]:
            with self.subTest(tc=tc):
                exc = sw_compdocs.resource.ResourceFileError(
                    tc.input_msg, file=tc.input_file
                )
                got_s = str(exc)
                self.assertEqual(got_s, tc.want_s)


class TestTOMLFileDecodeErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.resource.TOMLFileDecodeError(1, 2, file="file")
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, (1, 2))
        self.assertEqual(exc.file, "file")


class TestTOMLFileDecodeErrorStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_args", list[object]),
                ("input_file", sw_compdocs._types.StrOrBytesPath | None),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_args=[],
                input_file=None,
                want_s="",
            ),
            tt(
                input_args=["msg"],
                input_file=None,
                want_s="msg",
            ),
            tt(
                input_args=[],
                input_file="file",
                want_s="(in file 'file')",
            ),
            tt(
                input_args=["msg"],
                input_file="file",
                want_s="msg (in file 'file')",
            ),
            tt(
                input_args=[],
                input_file=b"file",
                want_s="(in file 'file')",
            ),
            tt(
                input_args=[],
                input_file=pathlib.PurePath("file"),
                want_s="(in file 'file')",
            ),
        ]:
            with self.subTest(tc=tc):
                exc = sw_compdocs.resource.TOMLFileDecodeError(
                    *tc.input_args, file=tc.input_file
                )
                got_s = str(exc)
                self.assertEqual(got_s, tc.want_s)


class TestFormatTOMLString(unittest.TestCase):
    def test_pass(self) -> None:
        for input_s in [
            "",
            "\x00",
            "\x00 \x08 \x0c A \x7f \x80 ÿ \ud7ff \ue000 \uffff 𐀀 \U0010ffff",
            ' ""two quotes"" ',
            ' "one quote" ',
            " ''two quotes'' ",
            " 'one quote' ",
            '""two quotes""',
            '"one quote"',
            '"one"',
            "' there's one already\n'' two more\n''",
            "''two quotes''",
            "'one quote'",
            "But there are # some comments here.",
            'Closing with five quotes\n""',
            'Closing with four quotes\n"',
            "First line\n\t Followed by a tab",
            'String does not end here" but ends here\\',
            "String ends here\\",
            "The quick brown fox jumps over the lazy dog.",
            "There is no escape\\",
            "This string\nhas ' a quote character\nand more than\none newline\nin it.",
            "This string has a ' quote character.",
            "This string has a \\/ slash character.",
            "This string has a \\\\ backslash character.",
            "This string has a \\b backspace character.",
            "This string has a \\f form feed character.",
            "This string has a \\n new line character.",
            "This string has a \\r carriage return character.",
            "This string has a \\t tab character.",
            "This string has an \t unescaped tab character.",
            "We see no # comments here.",
            'When will it end? """...""" should be here"',
            "You are not drinking enough whisky.",
            "\\u0000 \\u0008 \\u000c \\U00000041 \\u007f \\u0080 \\u00ff \\ud7ff \\ue000 \\uffff \\U00010000 \\U0010ffff",
            "\\u0041",
            "\\u007f",
            "\\x64",
            "a",
            "a   \tb",
            "a \\\nb",
            "a \\\\\n  b",
            "a \\b",
            'aaa"""bbb',
            "aaa'''bbb",
            "ab",
            "b",
            "c",
            "heeee\ngeeee",
            'lol"""',
            "val\nue",
            "val\\nue",
            "val\\ue",
            "value\n",
            "value\\n",
            "|\x08.",
            "|\t.",
            "|\n.",
            "|\x0c.",
            "|\r.",
            "|\x1f.",
            '|".',
            "|\\.",
            "|\\u.",
            "|\\u0075.",
            "|\x7f.",
            "~ \x80 ÿ \ud7ff \ue000 \uffff 𐀀 \U0010ffff",
            "\xa0",
            "δ",
        ]:
            with self.subTest(input_s=input_s):
                enc_s = sw_compdocs.resource.format_toml_string(input_s)
                enc_toml = f"s = {enc_s}"
                dec_toml: dict[str, object] = tomllib.loads(enc_toml)
                dec_s = dec_toml["s"]
                self.assertEqual(dec_s, input_s)


class TestFormatTOMLKey(unittest.TestCase):
    def test_pass(self) -> None:
        for input_key in [
            "",
            "\x00",
            "\x08",
            "\x08 \x0c A \x7f \x80 ÿ \ud7ff \ue000 \uffff 𐀀 \U0010ffff",
            "\ttab\ttab\t",
            "\n",
            " c d ",
            " tbl ",
            '"',
            '"quoted"',
            "-",
            "---",
            "-key",
            "0",
            "000111",
            "001",
            "1",
            "10e3",
            "111",
            "123",
            "1key",
            "2",
            "2018_10",
            "34-11",
            "=~!@$^&*()_+-`1234567890[]|/?><.,;:'=",
            "M",
            "NAME",
            "Name",
            "Section",
            "\\u0000",
            "_",
            "___",
            "_key",
            "a",
            "a b",
            "a-a-a",
            "a.b",
            "alpha",
            "answer",
            "arr",
            "b",
            "backsp\x08\x08",
            "c",
            "count",
            "d",
            "dance-with",
            "dot",
            "dots",
            "e",
            "f",
            "false",
            "few",
            "first",
            "g",
            "h",
            "i",
            "inf",
            "inline",
            "j",
            "k",
            "key",
            "key.with.dots",
            "l",
            "l ~ \x80 ÿ \ud7ff \ue000 \uffff 𐀀 \U0010ffff",
            "last",
            "many",
            "name",
            "nan",
            "one1two2",
            "plain",
            "plain_table",
            "polka",
            "quote",
            "sectioN",
            "section",
            "table",
            "tbl",
            "top",
            "true",
            "under_score",
            "with-dash",
            "with.dot",
            "withdot",
            "x",
            "~ \x80 ÿ \ud7ff \ue000 \uffff 𐀀 \U0010ffff",
            "À",
            "Μ",
            "μ",
        ]:
            with self.subTest(input_key=input_key):
                enc_key = sw_compdocs.resource.format_toml_key(input_key)
                enc_toml = f"{enc_key} = 0"
                dec_toml: dict[str, object] = tomllib.loads(enc_toml)
                dec_key = next(iter(dec_toml.keys()))
                self.assertEqual(dec_key, input_key)


class TestLoadTOMLTable(unittest.TestCase):
    def test_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "resource.toml")
            with open(temp_file, mode="w", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[resource]
key_1 = "val_1"
key_2 = "val_2"
"""
                )

            want_tbl = {"key_1": "val_1", "key_2": "val_2"}
            got_tbl = sw_compdocs.resource.load_toml_table(temp_file, "resource")
            self.assertEqual(got_tbl, want_tbl)

    def test_exc_decode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "resource.toml")
            with open(temp_file, mode="w", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[resource]
key_1 = "val_1"
key_2 = "val_2
"""
                )

            with self.assertRaises(sw_compdocs.resource.TOMLFileDecodeError) as ctx:
                sw_compdocs.resource.load_toml_table(temp_file, "resource")
            self.assertEqual(ctx.exception.file, temp_file)

            want_args = ("Illegal character '\\n' (at line 3, column 15)",)
            got_args: tuple[object, ...] = ctx.exception.args
            self.assertEqual(got_args, want_args)

    def test_exc_resource(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_s", str),
                ("input_table_key", str),
                ("want_exc_msg", str),
            ],
        )

        for tc in [
            tt(
                input_s="""\
[resource]
key_1 = "val_1"
key_2 = "val_2"
""",
                input_table_key="nonexistent",
                want_exc_msg="table 'nonexistent' does not exist",
            ),
            tt(
                input_s="""\
resource = []
""",
                input_table_key="resource",
                want_exc_msg="expected table for 'resource', but found list",
            ),
            tt(
                input_s="""\
[resource]
key_1 = 1
key_2 = "val_2"
""",
                input_table_key="resource",
                want_exc_msg="expected string value for 'resource.key_1', but found int",
            ),
            tt(
                input_s="""\
[resource]
key_1 = "val_1"
key_2 = 2
""",
                input_table_key="resource",
                want_exc_msg="expected string value for 'resource.key_2', but found int",
            ),
        ]:
            with self.subTest(tc=tc):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file = pathlib.Path(temp_dir, "resource.toml")
                    with open(
                        temp_file, mode="w", encoding="utf-8", newline="\n"
                    ) as fp:
                        fp.write(tc.input_s)

                    with self.assertRaises(
                        sw_compdocs.resource.ResourceFileError
                    ) as ctx:
                        sw_compdocs.resource.load_toml_table(
                            temp_file, tc.input_table_key
                        )
                    self.assertEqual(ctx.exception.msg, tc.want_exc_msg)
                    self.assertEqual(ctx.exception.file, temp_file)
