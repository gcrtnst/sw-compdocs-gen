import collections
import pathlib
import sw_compdocs.language
import tempfile
import unittest


class TestLanguageFromFile(unittest.TestCase):
    def test_pass(self):
        for encoding in ["utf-8", "cp932"]:
            with self.subTest(encoding=encoding):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file = pathlib.Path(temp_dir, "language.tsv")
                    with open(temp_file, mode="wt", encoding=encoding, newline="") as f:
                        f.write("id\tdescription\ten\tlocal\n\t\tEnglish\t日本語\n")

                    lang = sw_compdocs.language.Language.from_file(
                        temp_file, encoding=encoding
                    )
                    self.assertEqual(dict(lang), {"English": "日本語"})

    def test_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "language.tsv")
            with open(temp_file, mode="wt", encoding="utf-8", newline="") as f:
                f.write("")

            with self.assertRaises(sw_compdocs.language.LanguageTSVError) as cm:
                sw_compdocs.language.Language.from_file(temp_file)
            self.assertEqual(cm.exception.msg, "invalid header")
            self.assertEqual(cm.exception.file, temp_file)
            self.assertEqual(cm.exception.line, 0)

    def test_encode(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "language.tsv")
            with open(temp_file, mode="wt", encoding="utf-8", newline="") as f:
                f.write("id\tdescription\ten\tlocal\n\t\tEnglish\t日本語\n")

            lang = sw_compdocs.language.Language.from_file(
                temp_file, encoding="ascii", errors="replace"
            )
            self.assertEqual(dict(lang), {"English": "\uFFFD" * 9})


class TestLanguageFromStr(unittest.TestCase):
    def test_pass(self):
        lang = sw_compdocs.language.Language.from_str(
            "id\tdescription\ten\tlocal\n\t\tEnglish\t日本語\n"
        )
        self.assertEqual(dict(lang), {"English": "日本語"})

    def test_error(self):
        with self.assertRaises(sw_compdocs.language.LanguageTSVError) as cm:
            sw_compdocs.language.Language.from_str("")
        self.assertEqual(cm.exception.msg, "invalid header")
        self.assertIs(cm.exception.file, None)
        self.assertEqual(cm.exception.line, 0)


class TestLanguageFromIO(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_f", "want_lang_d"))

        for tc in [
            tt(input_f=["id\tdescription\ten\tlocal\n"], want_lang_d={}),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "\t\t\t\n"],
                want_lang_d={"": ""},
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "\t\tEnglish\t日本語\n"],
                want_lang_d={"English": "日本語"},
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "\t\t foo \t bar \n"],
                want_lang_d={" foo ": " bar "},
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", '\t\t"foo"\t"bar"\n'],
                want_lang_d={'"foo"': '"bar"'},
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", '\t\t""\t""\n'],
                want_lang_d={'""': '""'},
            ),
            tt(
                input_f=[
                    "id\tdescription\ten\tlocal\n",
                    "\t\ta\tあ\n",
                    "\t\tb\tい\n",
                    "\t\tc\tう\n",
                ],
                want_lang_d={"a": "あ", "b": "い", "c": "う"},
            ),
        ]:
            with self.subTest(tc=tc):
                got_lang = sw_compdocs.language.Language._from_io(tc.input_f)
                self.assertIs(type(got_lang), sw_compdocs.language.Language)
                self.assertEqual(got_lang._d, tc.want_lang_d)

    def test_error(self):
        tt = collections.namedtuple("tt", ("input_f", "want_exc_msg", "want_exc_line"))

        for tc in [
            tt(
                input_f=["\na"],
                want_exc_msg="new-line character seen in unquoted field - do you need to open the file in universal-newline mode?",
                want_exc_line=1,
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "\na"],
                want_exc_msg="new-line character seen in unquoted field - do you need to open the file in universal-newline mode?",
                want_exc_line=2,
            ),
            tt(
                input_f=[],
                want_exc_msg="invalid header",
                want_exc_line=0,
            ),
            tt(
                input_f=["id,description,en,local\n"],
                want_exc_msg="invalid header",
                want_exc_line=1,
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal_\n"],
                want_exc_msg="invalid header",
                want_exc_line=1,
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "\t\t\n"],
                want_exc_msg="invalid number of fields",
                want_exc_line=2,
            ),
            tt(
                input_f=[
                    "id\tdescription\ten\tlocal\n",
                    "\t\t\t\t\n",
                ],
                want_exc_msg="invalid number of fields",
                want_exc_line=2,
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.language.LanguageTSVError) as cm:
                    sw_compdocs.language.Language._from_io(tc.input_f)
                self.assertEqual(cm.exception.msg, tc.want_exc_msg)
                self.assertIs(cm.exception.file, None)
                self.assertEqual(cm.exception.line, tc.want_exc_line)


class TestLanguageGetItem(unittest.TestCase):
    def test_pass(self):
        lang = sw_compdocs.language.Language.from_str(
            "id\tdescription\ten\tlocal\n\t\tfoo\tbar\n"
        )
        val = lang["foo"]
        self.assertEqual(val, "bar")

    def test_error(self):
        lang = sw_compdocs.language.Language.from_str(
            "id\tdescription\ten\tlocal\n\t\tfoo\tbar\n"
        )

        with self.assertRaises(sw_compdocs.language.LanguageKeyError) as cm:
            lang["baz"]
        self.assertEqual(cm.exception.key, "baz")


class TestLanguageIter(unittest.TestCase):
    def test(self):
        lang = sw_compdocs.language.Language.from_str(
            "id\tdescription\ten\tlocal\n\t\tfoo\tふー\n\t\tbar\tばー\n\t\tbaz\tばず\n"
        )

        keys = list(lang)
        self.assertEqual(keys, ["foo", "bar", "baz"])


class TestLanguageLen(unittest.TestCase):
    def test(self):
        lang = sw_compdocs.language.Language.from_str(
            "id\tdescription\ten\tlocal\n\t\tfoo\tふー\n\t\tbar\tばー\n\t\tbaz\tばず\n"
        )

        l = len(lang)
        self.assertEqual(l, 3)


class TestLanguageTSVErrorInit(unittest.TestCase):
    def test_pass(self):
        exc = sw_compdocs.language.LanguageTSVError("msg")
        self.assertEqual(exc.msg, "msg")
        self.assertEqual(exc.file, None)
        self.assertEqual(exc.line, None)

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.language.LanguageTSVError(None)


class TestLanguageTSVErrorFileSetter(unittest.TestCase):
    def test_pass(self):
        for file in [
            None,
            "file",
            b"file",
            pathlib.PurePath("file"),
        ]:
            with self.subTest(file=file):
                exc = sw_compdocs.language.LanguageTSVError("msg")
                exc.file = file
                self.assertIs(exc.file, file)

    def test_exc_type(self):
        exc = sw_compdocs.language.LanguageTSVError("msg")
        exc.file = None
        with self.assertRaises(TypeError):
            exc.file = 0
        self.assertIs(exc.file, None)


class TestLanguageTSVErrorLineSetter(unittest.TestCase):
    def test_pass(self):
        for line in [None, 52149]:
            with self.subTest(line=line):
                exc = sw_compdocs.language.LanguageTSVError("msg")
                exc.line = line
                self.assertIs(exc.line, line)

    def test_exc_type(self):
        exc = sw_compdocs.language.LanguageTSVError("msg")
        exc.line = None
        with self.assertRaises(TypeError):
            exc.line = "52149"
        self.assertIs(exc.line, None)


class TestLanguageTSVErrorStr(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple(
            "tt", ("input_exc_msg", "input_exc_file", "input_exc_line", "want_s")
        )

        for tc in [
            tt(
                input_exc_msg="msg",
                input_exc_file=None,
                input_exc_line=None,
                want_s="<language.tsv>: line ?: msg",
            ),
            tt(
                input_exc_msg="msg",
                input_exc_file="file",
                input_exc_line=None,
                want_s="file: line ?: msg",
            ),
            tt(
                input_exc_msg="msg",
                input_exc_file=None,
                input_exc_line=52149,
                want_s="<language.tsv>: line 52149: msg",
            ),
            tt(
                input_exc_msg="msg",
                input_exc_file="file",
                input_exc_line=52149,
                want_s="file: line 52149: msg",
            ),
        ]:
            with self.subTest(tc=tc):
                input_exc = sw_compdocs.language.LanguageTSVError(tc.input_exc_msg)
                input_exc.file = tc.input_exc_file
                input_exc.line = tc.input_exc_line
                got_s = str(input_exc)
                self.assertEqual(got_s, tc.want_s)


class TestLanguageKeyErrorInit(unittest.TestCase):
    def test(self):
        exc = sw_compdocs.language.LanguageKeyError("key")
        self.assertEqual(exc.key, "key")


class TestLanguageKeyErrorStr(unittest.TestCase):
    def test(self):
        exc = sw_compdocs.language.LanguageKeyError("key")
        s = str(exc)
        self.assertEqual(s, "missing translation for 'key'")
