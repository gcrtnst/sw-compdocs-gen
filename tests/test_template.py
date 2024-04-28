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


class TestFormat(unittest.TestCase):
    def test_key_error(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_template", str),
                ("input_mapping", collections.abc.Mapping[str, str]),
                ("want_key", str),
            ],
        )

        for tc in [
            tt(input_template="$[foo]", input_mapping={"bar": "baz"}, want_key="foo"),
            tt(input_template="$[foo\n]", input_mapping={}, want_key="foo\n"),
            tt(
                input_template="$[foo] $[baz]",
                input_mapping={"foo": "bar"},
                want_key="baz",
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.template.TemplateKeyError) as ctx:
                    sw_compdocs.template.format(tc.input_template, tc.input_mapping)
                self.assertEqual(ctx.exception.key, tc.want_key)

    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_template", str),
                ("input_mapping", collections.abc.Mapping[str, str]),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(input_template="", input_mapping={}, want_s=""),
            tt(input_template="foo", input_mapping={"foo": "bar"}, want_s="foo"),
            tt(input_template="$foo", input_mapping={"foo": "bar"}, want_s="$foo"),
            tt(input_template="${foo}", input_mapping={"foo": "bar"}, want_s="${foo}"),
            tt(input_template="$[foo", input_mapping={"foo": "bar"}, want_s="$[foo"),
            tt(input_template="$[foo]", input_mapping={"foo": "bar"}, want_s="bar"),
            tt(
                input_template="$[foo]",
                input_mapping={"foo": "$[foo]"},
                want_s="$[foo]",
            ),
            tt(input_template="$[foo]", input_mapping={"foo": r"\n"}, want_s=r"\n"),
            tt(
                input_template="foo $[foo] baz $[baz]",
                input_mapping={"foo": "bar", "baz": "qux"},
                want_s="foo bar baz qux",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.template.format(tc.input_template, tc.input_mapping)
                self.assertEqual(got_s, tc.want_s)
