import collections
import sw_compdocs.template
import unittest


class TestTemplateRendererInit(unittest.TestCase):
    def test_validate_pass(self):
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
                ren = sw_compdocs.template.TemplateRenderer(mapping)
                self.assertEqual(ren._d, mapping)
                self.assertIsNot(ren._d, mapping)

    def test_validate_error(self):
        tt = collections.namedtuple("tt", ("input_mapping", "want_exc_args"))

        for tc in [
            tt(
                input_mapping=[],
                want_exc_args=("template mapping must be mapping, not 'list'",),
            ),
            tt(
                input_mapping={0: ""},
                want_exc_args=("template mapping entry key must be str, not 'int'",),
            ),
            tt(
                input_mapping={"": 0},
                want_exc_args=("template mapping entry value must be str, not 'int'",),
            ),
            tt(
                input_mapping={"a": "", 0: ""},
                want_exc_args=("template mapping entry key must be str, not 'int'",),
            ),
            tt(
                input_mapping={"a": "", "": 0},
                want_exc_args=("template mapping entry value must be str, not 'int'",),
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.template.TemplateMappingError) as cm:
                    sw_compdocs.template.TemplateRenderer(tc.input_mapping)
                self.assertEqual(cm.exception.args, tc.want_exc_args)


class TestTemplateRendererRender(unittest.TestCase):
    def test_type_error(self):
        ren = sw_compdocs.template.TemplateRenderer({})
        with self.assertRaises(TypeError):
            ren.render(0)

    def test_key_error(self):
        tt = collections.namedtuple("tt", ("input_mapping", "input_s", "want_key"))

        for tc in [
            tt(input_mapping={"bar": "baz"}, input_s="$[foo]", want_key="foo"),
            tt(input_mapping={}, input_s="$[foo\n]", want_key="foo\n"),
            tt(input_mapping={"foo": "bar"}, input_s="$[foo] $[baz]", want_key="baz"),
        ]:
            with self.subTest(tc=tc):
                ren = sw_compdocs.template.TemplateRenderer(tc.input_mapping)
                with self.assertRaises(sw_compdocs.template.TemplateKeyError) as cm:
                    ren.render(tc.input_s)
                self.assertEqual(cm.exception.key, tc.want_key)

    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_mapping", "input_s", "want_s"))

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
                ren = sw_compdocs.template.TemplateRenderer(tc.input_mapping)
                got_s = ren.render(tc.input_s)
                self.assertEqual(got_s, tc.want_s)


class TestAsMapping(unittest.TestCase):
    def test_validate_pass(self):
        for input_v, want_mapping in [
            (
                {"a": ""},
                {"a": ""},
            ),
            (
                {"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_": ""},
                {"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_": ""},
            ),
            (
                {"a": "x"},
                {"a": "x"},
            ),
            (
                {"action_down": "s"},
                {"action_down": "s"},
            ),
            (
                {"a": "日本語もOK"},
                {"a": "日本語もOK"},
            ),
            (
                {"a": "", "b": ""},
                {"a": "", "b": ""},
            ),
            (
                {"a": "x", "b": "y"},
                {"a": "x", "b": "y"},
            ),
        ]:
            with self.subTest(v=input_v):
                got_mapping = sw_compdocs.template.as_mapping(input_v)
                self.assertEqual(got_mapping, want_mapping)
                self.assertIsNot(got_mapping, input_v)

    def test_validate_type_error(self):
        for v in [
            [],
            {0: ""},
            {"": 0},
            {"a": "", 0: ""},
            {"a": "", "": 0},
        ]:
            with self.subTest(v=v):
                with self.assertRaises(TypeError):
                    sw_compdocs.template.as_mapping(v)


class TestSubstitute(unittest.TestCase):
    def test_validate_type_error(self):
        for input_s, input_mapping in [
            (0, {}),
            ("", []),
            ("$[foo]", {"foo": 0}),
        ]:
            with self.assertRaises(TypeError):
                sw_compdocs.template.substitute(input_s, input_mapping)

    def test_substitute_pass(self):
        for input_s, input_mapping, want_s in [
            (
                "",
                {},
                "",
            ),
            (
                "foo",
                {"foo": "bar"},
                "foo",
            ),
            (
                "$foo",
                {"foo": "bar"},
                "$foo",
            ),
            (
                "${foo}",
                {"foo": "bar"},
                "${foo}",
            ),
            (
                "$[foo",
                {"foo": "bar"},
                "$[foo",
            ),
            (
                "$[foo]",
                {"foo": "bar"},
                "bar",
            ),
            (
                "$[foo]",
                {"foo": "bar", "baz": 0},
                "bar",
            ),
            (
                "$[foo]",
                {"foo": "$[foo]"},
                "$[foo]",
            ),
            (
                "$[foo]",
                {"foo": r"\n"},
                r"\n",
            ),
            (
                "foo $[foo] baz $[baz]",
                {"foo": "bar", "baz": "qux"},
                "foo bar baz qux",
            ),
        ]:
            with self.subTest(s=input_s, mapping=input_mapping):
                got_s = sw_compdocs.template.substitute(input_s, input_mapping)
                self.assertEqual(got_s, want_s)

    def test_substitute_key_error(self):
        for input_s, input_mapping, want_key in [
            (
                "$[foo]",
                {"bar": "baz"},
                "foo",
            ),
            (
                "$[foo\n]",
                {},
                "foo\n",
            ),
            (
                "$[foo] $[baz]",
                {"foo": "bar"},
                "baz",
            ),
        ]:
            with self.subTest(s=input_s, mapping=input_mapping):
                with self.assertRaises(sw_compdocs.template.TemplateKeyError) as cm:
                    sw_compdocs.template.substitute(input_s, input_mapping)
                self.assertEqual(cm.exception.key, want_key)


class TestTemplateKeyErrorInit(unittest.TestCase):
    def test(self):
        exc = sw_compdocs.template.TemplateKeyError("key")
        self.assertEqual(exc.key, "key")


class TestTemplateKeyErrorStr(unittest.TestCase):
    def test(self):
        exc = sw_compdocs.template.TemplateKeyError("key")
        s = str(exc)
        self.assertEqual(s, "missing key 'key' in template mapping")
