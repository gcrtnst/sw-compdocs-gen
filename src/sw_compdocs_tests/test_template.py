import sw_compdocs.template
import unittest


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
