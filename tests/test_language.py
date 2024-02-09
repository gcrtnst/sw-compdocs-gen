import collections.abc
import pathlib
import sw_compdocs._types
import sw_compdocs.language
import tempfile
import typing
import unittest


class TestLanguageTSVErrorInit(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.language.LanguageTSVError("msg")
        self.assertEqual(exc.msg, "msg")
        self.assertEqual(exc.file, None)
        self.assertEqual(exc.line, None)


class TestLanguageTSVErrorStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_exc_msg", str),
                ("input_exc_file", sw_compdocs._types.StrOrBytesPath | None),
                ("input_exc_line", int | None),
                ("want_s", str),
            ],
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


class TestLanguageFindIDErrorInit(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.language.LanguageFindIDError("id")
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("id",))
        self.assertEqual(exc.id, "id")


class TestLanguageFindIDErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.language.LanguageFindIDError("id")
        self.assertEqual(str(exc), "missing translation for id 'id'")


class TestLanguageFindEnErrorInit(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.language.LanguageFindEnError("en")
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("en",))
        self.assertEqual(exc.en, "en")


class TestLanguageFindEnErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.language.LanguageFindEnError("en")
        self.assertEqual(str(exc), "missing translation for text 'en'")


class TestLanguageFromIO(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_f", collections.abc.Iterable[str]),
                ("want_lang_l", list[sw_compdocs.language.Translation]),
            ],
        )

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
                self.assertEqual(
                    list[sw_compdocs.language.Translation](got_lang), tc.want_lang_l
                )

    def test_error(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_f", collections.abc.Iterable[str]),
                ("want_exc_msg", str),
                ("want_exc_line", int),
            ],
        )

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


class TestLanguageFromFile(unittest.TestCase):
    def test_pass(self) -> None:
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
                        list[sw_compdocs.language.Translation](lang),
                        list[sw_compdocs.language.Translation](
                            [
                                sw_compdocs.language.Translation(
                                    "id_0", "description_0", "en_0", "local_0"
                                ),
                                sw_compdocs.language.Translation(
                                    "id_1", "description_1", "en_1", "local_1"
                                ),
                            ]
                        ),
                    )

    def test_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "language.tsv")
            with open(temp_file, mode="wt", encoding="utf-8", newline="") as f:
                f.write("")

            with self.assertRaises(sw_compdocs.language.LanguageTSVError) as cm:
                sw_compdocs.language.Language.from_file(temp_file)
            self.assertEqual(cm.exception.msg, "invalid header")
            self.assertEqual(cm.exception.file, temp_file)
            self.assertEqual(cm.exception.line, 0)

    def test_encode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "language.tsv")
            with open(temp_file, mode="wt", encoding="utf-8", newline="") as f:
                f.write(
                    "id\tdescription\ten\tlocal\nid\tdescription\tEnglish\t日本語\n"
                )

            lang = sw_compdocs.language.Language.from_file(
                temp_file, encoding="ascii", errors="replace"
            )
            self.assertEqual(
                list[sw_compdocs.language.Translation](lang),
                list[sw_compdocs.language.Translation](
                    [
                        sw_compdocs.language.Translation(
                            "id", "description", "English", "\uFFFD" * 9
                        )
                    ]
                ),
            )


class TestLanguageFromStr(unittest.TestCase):
    def test_pass(self) -> None:
        lang = sw_compdocs.language.Language.from_str(
            "id\tdescription\ten\tlocal\n"
            + "id_0\tdescription_0\ten_0\tlocal_0\n"
            + "id_1\tdescription_1\ten_1\tlocal_1\n"
        )
        self.assertEqual(
            list[sw_compdocs.language.Translation](lang),
            list[sw_compdocs.language.Translation](
                [
                    sw_compdocs.language.Translation(
                        "id_0", "description_0", "en_0", "local_0"
                    ),
                    sw_compdocs.language.Translation(
                        "id_1", "description_1", "en_1", "local_1"
                    ),
                ]
            ),
        )

    def test_error(self) -> None:
        with self.assertRaises(sw_compdocs.language.LanguageTSVError) as cm:
            sw_compdocs.language.Language.from_str("")
        self.assertEqual(cm.exception.msg, "invalid header")
        self.assertIs(cm.exception.file, None)
        self.assertEqual(cm.exception.line, 0)


class TestLanguageFindIDAll(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language),
                ("input_id", str),
                ("want_trans_list", list[sw_compdocs.language.Translation]),
            ],
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


class TestLanguageFindID(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language),
                ("input_id", str),
                ("want_trans", sw_compdocs.language.Translation),
            ],
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
                want_trans=sw_compdocs.language.Translation(
                    "id_1", "description_1", "en_1", "local_1"
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_trans = tc.input_lang.find_id(tc.input_id)
                self.assertEqual(got_trans, tc.want_trans)

    def test_exc_find(self) -> None:
        lang = sw_compdocs.language.Language(
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
        )
        with self.assertRaises(sw_compdocs.language.LanguageFindIDError) as ctx:
            lang.find_id("id_2")
        self.assertEqual(ctx.exception.id, "id_2")


class TestLanguageFindEnAll(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language),
                ("input_en", str),
                ("want_trans_list", list[sw_compdocs.language.Translation]),
            ],
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


class TestLanguageFindEn(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language),
                ("input_en", str),
                ("want_trans", sw_compdocs.language.Translation),
            ],
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
                want_trans=sw_compdocs.language.Translation(
                    "id_1", "description_1", "en_1", "local_1"
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_trans = tc.input_lang.find_en(tc.input_en)
                self.assertEqual(got_trans, tc.want_trans)

    def test_exc_find(self) -> None:
        lang = sw_compdocs.language.Language(
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
        )
        with self.assertRaises(sw_compdocs.language.LanguageFindEnError) as ctx:
            lang.find_en("en_2")
        self.assertEqual(ctx.exception.en, "en_2")
