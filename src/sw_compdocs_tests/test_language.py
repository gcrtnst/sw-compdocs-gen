import collections
import pathlib
import sw_compdocs.language
import tempfile
import unittest


class TestLanguageInit(unittest.TestCase):
    def test_pass(self):
        trans_list = [
            sw_compdocs.language.Translation(
                "id_0", "description_0", "en_0", "local_0"
            ),
            sw_compdocs.language.Translation(
                "id_1", "description_1", "en_1", "local_1"
            ),
        ]
        lang = sw_compdocs.language.Language(trans_list)
        self.assertEqual(list(lang), trans_list)

    def test_exc_type(self):
        for trans_list in [
            [
                None,
                sw_compdocs.language.Translation(
                    "id_1", "description_1", "en_1", "local_1"
                ),
            ],
            [
                sw_compdocs.language.Translation(
                    "id_0", "description_0", "en_0", "local_0"
                ),
                None,
            ],
        ]:
            with self.subTest(trans_list=trans_list):
                with self.assertRaises(TypeError):
                    sw_compdocs.language.Language(trans_list)


class TestLanguageFromFile(unittest.TestCase):
    def test_pass(self):
        for encoding in ["utf-8", "cp932"]:
            with self.subTest(encoding=encoding):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file = pathlib.Path(temp_dir, "language.tsv")
                    with open(temp_file, mode="wt", encoding=encoding, newline="") as f:
                        f.write(
                            "id\tdescription\ten\tlocal\n"
                            + "id_0\tdescription_0\ten_0\tlocal_0\n"
                            + "id_1\tdescription_1\ten_1\tlocal_1\n"
                        )

                    lang = sw_compdocs.language.Language.from_file(
                        temp_file, encoding=encoding
                    )
                    self.assertEqual(
                        list(lang),
                        [
                            sw_compdocs.language.Translation(
                                "id_0", "description_0", "en_0", "local_0"
                            ),
                            sw_compdocs.language.Translation(
                                "id_1", "description_1", "en_1", "local_1"
                            ),
                        ],
                    )

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
                f.write("id\tdescription\ten\tlocal\nid\tdescription\tEnglish\t日本語\n")

            lang = sw_compdocs.language.Language.from_file(
                temp_file, encoding="ascii", errors="replace"
            )
            self.assertEqual(
                list(lang),
                [
                    sw_compdocs.language.Translation(
                        "id", "description", "English", "\uFFFD" * 9
                    )
                ],
            )


class TestLanguageFromStr(unittest.TestCase):
    def test_pass(self):
        lang = sw_compdocs.language.Language.from_str(
            "id\tdescription\ten\tlocal\n"
            + "id_0\tdescription_0\ten_0\tlocal_0\n"
            + "id_1\tdescription_1\ten_1\tlocal_1\n"
        )
        self.assertEqual(
            list(lang),
            [
                sw_compdocs.language.Translation(
                    "id_0", "description_0", "en_0", "local_0"
                ),
                sw_compdocs.language.Translation(
                    "id_1", "description_1", "en_1", "local_1"
                ),
            ],
        )

    def test_error(self):
        with self.assertRaises(sw_compdocs.language.LanguageTSVError) as cm:
            sw_compdocs.language.Language.from_str("")
        self.assertEqual(cm.exception.msg, "invalid header")
        self.assertIs(cm.exception.file, None)
        self.assertEqual(cm.exception.line, 0)


class TestLanguageFromIO(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_f", "want_lang_l"))

        for tc in [
            tt(input_f=["id\tdescription\ten\tlocal\n"], want_lang_l=[]),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "\t\t\t\n"],
                want_lang_l=[
                    sw_compdocs.language.Translation("", "", "", ""),
                ],
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "id\tdesc\tEnglish\t日本語\n"],
                want_lang_l=[
                    sw_compdocs.language.Translation("id", "desc", "English", "日本語")
                ],
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", "\t\t foo \t bar \n"],
                want_lang_l=[
                    sw_compdocs.language.Translation("", "", " foo ", " bar ")
                ],
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", '\t\t"foo"\t"bar"\n'],
                want_lang_l=[
                    sw_compdocs.language.Translation("", "", '"foo"', '"bar"')
                ],
            ),
            tt(
                input_f=["id\tdescription\ten\tlocal\n", '\t\t""\t""\n'],
                want_lang_l=[
                    sw_compdocs.language.Translation("", "", '""', '""'),
                ],
            ),
            tt(
                input_f=[
                    "id\tdescription\ten\tlocal\n",
                    "0\tx\ta\tあ\n",
                    "1\ty\tb\tい\n",
                    "2\tz\tc\tう\n",
                ],
                want_lang_l=[
                    sw_compdocs.language.Translation("0", "x", "a", "あ"),
                    sw_compdocs.language.Translation("1", "y", "b", "い"),
                    sw_compdocs.language.Translation("2", "z", "c", "う"),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_lang = sw_compdocs.language.Language._from_io(tc.input_f)
                self.assertIs(type(got_lang), sw_compdocs.language.Language)
                self.assertEqual(list(got_lang), tc.want_lang_l)

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


class TestLanguageFindID(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt", ("input_lang", "input_id", "input_default", "want_trans")
        )

        for tc in [
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_2", "en_2", "local_2"
                        ),
                    ]
                ),
                input_id="id_0",
                input_default="default",
                want_trans=sw_compdocs.language.Translation(
                    "id_0", "description_0", "en_0", "local_0"
                ),
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_2", "en_2", "local_2"
                        ),
                    ]
                ),
                input_id="id_1",
                input_default="default",
                want_trans=sw_compdocs.language.Translation(
                    "id_1", "description_1", "en_1", "local_1"
                ),
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_2", "en_2", "local_2"
                        ),
                    ]
                ),
                input_id="id_2",
                input_default="default",
                want_trans="default",
            ),
        ]:
            with self.subTest(tc=tc):
                got_trans = tc.input_lang.find_id(tc.input_id, default=tc.input_default)
                self.assertEqual(got_trans, tc.want_trans)

    def test_exc_type(self):
        lang = sw_compdocs.language.Language()
        with self.assertRaises(TypeError):
            lang.find_id(None)


class TestLanguageFindIDAll(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_lang", "input_id", "want_trans_list"))

        for tc in [
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_2", "en_2", "local_2"
                        ),
                    ]
                ),
                input_id="id_0",
                want_trans_list=[
                    sw_compdocs.language.Translation(
                        "id_0", "description_0", "en_0", "local_0"
                    ),
                ],
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_2", "en_2", "local_2"
                        ),
                    ]
                ),
                input_id="id_1",
                want_trans_list=[
                    sw_compdocs.language.Translation(
                        "id_1", "description_1", "en_1", "local_1"
                    ),
                    sw_compdocs.language.Translation(
                        "id_1", "description_2", "en_2", "local_2"
                    ),
                ],
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_2", "en_2", "local_2"
                        ),
                    ]
                ),
                input_id="id_2",
                want_trans_list=[],
            ),
        ]:
            with self.subTest(tc=tc):
                got_trans_list = tc.input_lang.find_id_all(tc.input_id)
                self.assertEqual(got_trans_list, tc.want_trans_list)

    def test_exc_type(self):
        lang = sw_compdocs.language.Language()
        with self.assertRaises(TypeError):
            lang.find_id_all(None)


class TestLanguageFindEn(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt", ("input_lang", "input_en", "input_default", "want_trans")
        )

        for tc in [
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_2", "description_2", "en_1", "local_2"
                        ),
                    ]
                ),
                input_en="en_0",
                input_default="default",
                want_trans=sw_compdocs.language.Translation(
                    "id_0", "description_0", "en_0", "local_0"
                ),
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_2", "description_2", "en_1", "local_2"
                        ),
                    ]
                ),
                input_en="en_1",
                input_default="default",
                want_trans=sw_compdocs.language.Translation(
                    "id_1", "description_1", "en_1", "local_1"
                ),
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_2", "description_2", "en_1", "local_2"
                        ),
                    ]
                ),
                input_en="en_2",
                input_default="default",
                want_trans="default",
            ),
        ]:
            with self.subTest(tc=tc):
                got_trans = tc.input_lang.find_en(tc.input_en, default=tc.input_default)
                self.assertEqual(got_trans, tc.want_trans)

    def test_exc_type(self):
        lang = sw_compdocs.language.Language()
        with self.assertRaises(TypeError):
            lang.find_id(None)


class TestLanguageFindEnAll(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_lang", "input_en", "want_trans_list"))

        for tc in [
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_2", "description_2", "en_1", "local_2"
                        ),
                    ]
                ),
                input_en="en_0",
                want_trans_list=[
                    sw_compdocs.language.Translation(
                        "id_0", "description_0", "en_0", "local_0"
                    ),
                ],
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_2", "description_2", "en_1", "local_2"
                        ),
                    ]
                ),
                input_en="en_1",
                want_trans_list=[
                    sw_compdocs.language.Translation(
                        "id_1", "description_1", "en_1", "local_1"
                    ),
                    sw_compdocs.language.Translation(
                        "id_2", "description_2", "en_1", "local_2"
                    ),
                ],
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id_0", "description_0", "en_0", "local_0"
                        ),
                        sw_compdocs.language.Translation(
                            "id_1", "description_1", "en_1", "local_1"
                        ),
                        sw_compdocs.language.Translation(
                            "id_2", "description_2", "en_1", "local_2"
                        ),
                    ]
                ),
                input_en="en_2",
                want_trans_list=[],
            ),
        ]:
            with self.subTest(tc=tc):
                got_trans_list = tc.input_lang.find_en_all(tc.input_en)
                self.assertEqual(got_trans_list, tc.want_trans_list)

    def test_exc_type(self):
        lang = sw_compdocs.language.Language()
        with self.assertRaises(TypeError):
            lang.find_id_all(None)


class TestTranslationInit(unittest.TestCase):
    def test_pass(self):
        input_id = "id"
        input_description = "description"
        input_en = "en"
        input_local = "local"
        trans = sw_compdocs.language.Translation(
            input_id, input_description, input_en, input_local
        )
        self.assertIs(trans.id, input_id)
        self.assertIs(trans.description, input_description)
        self.assertIs(trans.en, input_en)
        self.assertIs(trans.local, input_local)

    def test_exc_type(self):
        tt = collections.namedtuple(
            "tt", ("input_id", "input_description", "input_en", "input_local")
        )

        for tc in [
            tt(
                input_id=b"id",
                input_description="description",
                input_en="en",
                input_local="local",
            ),
            tt(
                input_id="id",
                input_description=b"description",
                input_en="en",
                input_local="local",
            ),
            tt(
                input_id="id",
                input_description="description",
                input_en=b"en",
                input_local="local",
            ),
            tt(
                input_id="id",
                input_description="description",
                input_en="en",
                input_local=b"local",
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(TypeError):
                    sw_compdocs.language.Translation(
                        tc.input_id, tc.input_description, tc.input_en, tc.input_local
                    )


class TestTranslationIDSetter(unittest.TestCase):
    def test_pass(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        trans.id = "set"
        self.assertEqual(trans.id, "set")

    def test_exc_type(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        with self.assertRaises(TypeError):
            trans.id = b"set"


class TestTranslationDescriptionSetter(unittest.TestCase):
    def test_pass(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        trans.description = "set"
        self.assertEqual(trans.description, "set")

    def test_exc_type(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        with self.assertRaises(TypeError):
            trans.description = b"set"


class TestTranslationEnSetter(unittest.TestCase):
    def test_pass(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        trans.en = "set"
        self.assertEqual(trans.en, "set")

    def test_exc_type(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        with self.assertRaises(TypeError):
            trans.en = b"set"


class TestTranslationLocalSetter(unittest.TestCase):
    def test_pass(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        trans.local = "set"
        self.assertEqual(trans.local, "set")

    def test_exc_type(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        with self.assertRaises(TypeError):
            trans.local = b"set"


class TestTranslationRepr(unittest.TestCase):
    def test(self):
        trans = sw_compdocs.language.Translation("id", "description", "en", "local")
        self.assertEqual(repr(trans), "Translation('id', 'description', 'en', 'local')")


class TestTranslationEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        for tc in [
            tt(
                input_self=sw_compdocs.language.Translation(
                    "id", "description", "en", "local"
                ),
                input_other=sw_compdocs.language.Translation(
                    "id", "description", "en", "local"
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.language.Translation(
                    "id", "description", "en", "local"
                ),
                input_other=sw_compdocs.language.Translation(
                    "diff", "description", "en", "local"
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.language.Translation(
                    "id", "description", "en", "local"
                ),
                input_other=sw_compdocs.language.Translation(
                    "id", "diff", "en", "local"
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.language.Translation(
                    "id", "description", "en", "local"
                ),
                input_other=sw_compdocs.language.Translation(
                    "id", "description", "diff", "local"
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.language.Translation(
                    "id", "description", "en", "local"
                ),
                input_other=sw_compdocs.language.Translation(
                    "id", "description", "en", "diff"
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.language.Translation(
                    "id", "description", "en", "local"
                ),
                input_other=None,
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


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
