import collections.abc
import sw_compdocs.template
import typing
import unittest


class TestTemplateKeyErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.template.TemplateKeyError("key")
        self.assertEqual(exc.key, "key")


class TestTemplateKeyErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.template.TemplateKeyError("key")
        s = str(exc)
        self.assertEqual(s, "missing replacement string for placeholder $[key]")


class TestTemplateFormatterInit(unittest.TestCase):
    def test_validate_pass(self) -> None:
        for mapping in [
            {"a": ""},
            {"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_": ""},
            {"a": "x"},
            {"action_down": "s"},
            {"a": "日本語もOK"},
            {"a": "", "b": ""},
            {"a": "x", "b": "y"},
        ]:
            with self.subTest(mapping=mapping):
                ren = sw_compdocs.template.TemplateFormatter(mapping)
                self.assertEqual(ren._d, mapping)
                self.assertIsNot(ren._d, mapping)


class TestTemplateFormatterFormat(unittest.TestCase):
    def test_key_error(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_mapping", collections.abc.Mapping[str, str]),
                ("input_s", str),
                ("want_key", str),
            ],
        )

        for tc in [
            tt(input_mapping={"bar": "baz"}, input_s="$[foo]", want_key="foo"),
            tt(input_mapping={}, input_s="$[foo\n]", want_key="foo\n"),
            tt(input_mapping={"foo": "bar"}, input_s="$[foo] $[baz]", want_key="baz"),
        ]:
            with self.subTest(tc=tc):
                ren = sw_compdocs.template.TemplateFormatter(tc.input_mapping)
                with self.assertRaises(sw_compdocs.template.TemplateKeyError) as cm:
                    ren.format(tc.input_s)
                self.assertEqual(cm.exception.key, tc.want_key)

    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_mapping", collections.abc.Mapping[str, str]),
                ("input_s", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(input_mapping={}, input_s="", want_s=""),
            tt(input_mapping={"foo": "bar"}, input_s="foo", want_s="foo"),
            tt(input_mapping={"foo": "bar"}, input_s="$foo", want_s="$foo"),
            tt(input_mapping={"foo": "bar"}, input_s="${foo}", want_s="${foo}"),
            tt(input_mapping={"foo": "bar"}, input_s="$[foo", want_s="$[foo"),
            tt(input_mapping={"foo": "bar"}, input_s="$[foo]", want_s="bar"),
            tt(input_mapping={"foo": "$[foo]"}, input_s="$[foo]", want_s="$[foo]"),
            tt(input_mapping={"foo": r"\n"}, input_s="$[foo]", want_s=r"\n"),
            tt(
                input_mapping={"foo": "bar", "baz": "qux"},
                input_s="foo $[foo] baz $[baz]",
                want_s="foo bar baz qux",
            ),
        ]:
            with self.subTest(tc=tc):
                ren = sw_compdocs.template.TemplateFormatter(tc.input_mapping)
                got_s = ren.format(tc.input_s)
                self.assertEqual(got_s, tc.want_s)
