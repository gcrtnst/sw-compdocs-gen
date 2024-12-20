import argparse
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


class TestShowHideAction(unittest.TestCase):
    def test_default(self) -> None:
        argp = argparse.ArgumentParser(
            prog="test", add_help=False, allow_abbrev=False, exit_on_error=False
        )
        argp.add_argument(
            "--show-flag", action=sw_compdocs.main.ShowHideAction, default="default"
        )
        argv = argp.parse_args([])
        self.assertEqual(argv.show_flag, "default")

    def test_show(self) -> None:
        argp = argparse.ArgumentParser(
            prog="test", add_help=False, allow_abbrev=False, exit_on_error=False
        )
        argp.add_argument(
            "--show-flag", action=sw_compdocs.main.ShowHideAction, default="default"
        )
        argv = argp.parse_args(["--show-flag"])
        self.assertEqual(argv.show_flag, True)

    def test_hide(self) -> None:
        argp = argparse.ArgumentParser(
            prog="test", add_help=False, allow_abbrev=False, exit_on_error=False
        )
        argp.add_argument(
            "--show-flag", action=sw_compdocs.main.ShowHideAction, default="default"
        )
        argv = argp.parse_args(["--hide-flag"])
        self.assertEqual(argv.show_flag, False)

    def test_exc_value(self) -> None:
        for name_or_flags in [
            ["name"],
            ["--flag"],
            ["--hide-flag"],
            ["--show-flag", "--hide-flag"],
        ]:
            with self.subTest(name_or_flags=name_or_flags):
                argp = argparse.ArgumentParser(
                    prog="test", add_help=False, allow_abbrev=False, exit_on_error=False
                )
                with self.assertRaises(ValueError) as ctx:
                    argp.add_argument(
                        *name_or_flags, action=sw_compdocs.main.ShowHideAction
                    )
                self.assertIs(type(ctx.exception), ValueError)


class TestRun(unittest.TestCase):
    def test_document_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = pathlib.Path(temp_dir, "out")
            out_dir.mkdir()
            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()
            sw_compdocs.main.run(out_path=out_dir, defn_dir=defn_dir)
            self.assertIsNone(next(out_dir.iterdir(), None))

    def test_document_all(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = pathlib.Path(temp_dir, "out")
            out_dir.mkdir()

            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()

            defn_file = pathlib.Path(defn_dir, "test_01.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "test_02.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "dummy")
            defn_file.mkdir()

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
DOCUMENT_PROP_MASS = "重量：{}"
DOCUMENT_PROP_DIMS = "サイズ (WxDxH)：{}"
DOCUMENT_PROP_COST = "価格：${}"
DOCUMENT_PROP_TAGS = "タグ：{}"
DOCUMENT_PROP_FILE = "ファイル：{}"
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

            bind_file = pathlib.Path(temp_dir, "keybindings.toml")
            with open(bind_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[keybindings]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            sw_compdocs.main.run(
                out_path=out_dir,
                defn_dir=defn_dir,
                label_file=label_file,
                lang_file=lang_file,
                bind_file=bind_file,
                out_mode="document",
                out_encoding="shift-jis",
                out_newline="\r\n",
            )

            out_file = pathlib.Path(out_dir, "00_BLOCKS.md")
            with open(out_file, mode="r", encoding="shift-jis", newline="\r\n") as fp:
                got_md = fp.read()

            want_md = """\
# Blocks

## テスト 01

テンプレート 01

### プロパティ

- 重量：1
- サイズ (WxDxH)：1x1x1
- 価格：$0
- タグ：
- ファイル：test_01.xml

## テスト 02

テンプレート 02

### プロパティ

- 重量：2
- サイズ (WxDxH)：1x1x1
- 価格：$0
- タグ：
- ファイル：test_02.xml
"""
            want_md = want_md.replace("\n", "\r\n")
            self.assertEqual(got_md, want_md)

    def test_document_encoding_newline_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = pathlib.Path(temp_dir, "out")
            out_dir.mkdir()

            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()

            defn_file = pathlib.Path(defn_dir, "test_01.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "test_02.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "dummy")
            defn_file.mkdir()

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
DOCUMENT_PROP_MASS = "重量：{}"
DOCUMENT_PROP_DIMS = "サイズ (WxDxH)：{}"
DOCUMENT_PROP_COST = "価格：${}"
DOCUMENT_PROP_TAGS = "タグ：{}"
DOCUMENT_PROP_FILE = "ファイル：{}"
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

            bind_file = pathlib.Path(temp_dir, "keybindings.toml")
            with open(bind_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[keybindings]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            sw_compdocs.main.run(
                out_path=out_dir,
                defn_dir=defn_dir,
                label_file=label_file,
                lang_file=lang_file,
                bind_file=bind_file,
                out_mode="document",
            )

            out_file = pathlib.Path(out_dir, "00_BLOCKS.md")
            with open(out_file, mode="r", encoding="utf-8", newline="\n") as fp:
                got_md = fp.read()

            want_md = """\
# Blocks

## テスト 01

テンプレート 01

### プロパティ

- 重量：1
- サイズ (WxDxH)：1x1x1
- 価格：$0
- タグ：
- ファイル：test_01.xml

## テスト 02

テンプレート 02

### プロパティ

- 重量：2
- サイズ (WxDxH)：1x1x1
- 価格：$0
- タグ：
- ファイル：test_02.xml
"""
            self.assertEqual(got_md, want_md)

    def test_document_exc_unicode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = pathlib.Path(temp_dir, "out")
            out_dir.mkdir()

            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()

            defn_file = pathlib.Path(defn_dir, "test_01.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "test_02.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "dummy")
            defn_file.mkdir()

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
DOCUMENT_PROP_MASS = "重量：{}"
DOCUMENT_PROP_DIMS = "サイズ (WxDxH)：{}"
DOCUMENT_PROP_COST = "価格：${}"
DOCUMENT_PROP_TAGS = "タグ：{}"
DOCUMENT_PROP_FILE = "ファイル：{}"
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

            bind_file = pathlib.Path(temp_dir, "keybindings.toml")
            with open(bind_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[keybindings]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            with self.assertRaises(sw_compdocs.wraperr.UnicodeEncodeFileError) as ctx:
                sw_compdocs.main.run(
                    out_path=out_dir,
                    defn_dir=defn_dir,
                    label_file=label_file,
                    lang_file=lang_file,
                    bind_file=bind_file,
                    out_mode="document",
                    out_encoding="ascii",
                    out_newline="\r\n",
                )

            out_file = pathlib.Path(out_dir, "00_BLOCKS.md")
            self.assertEqual(ctx.exception.filename, out_file)

    def test_sheet_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_file = pathlib.Path(temp_dir, "out.csv")
            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()
            sw_compdocs.main.run(
                out_path=out_file,
                defn_dir=defn_dir,
                out_mode="sheet",
                out_encoding="utf-8",
                out_newline="\n",
            )

            with open(out_file, mode="r", encoding="utf-8", newline="\n") as fp:
                got_md = fp.read()

            want_md = "Name,File,Category,Tags,Multibody,Deprecated,Orphaned,Cost,Mass,Width,Depth,Height,Short Description,Description\n"
            self.assertEqual(got_md, want_md)

    def test_sheet_all(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_file = pathlib.Path(temp_dir, "out.csv")

            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()

            defn_file = pathlib.Path(defn_dir, "test_01.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "test_02.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "dummy")
            defn_file.mkdir()

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
SHEET_HEAD_NAME = "Name"
SHEET_HEAD_FILE = "File"
SHEET_HEAD_CATEGORY = "Category"
SHEET_HEAD_TAGS = "Tags"
SHEET_HEAD_MULTIBODY = "Multibody"
SHEET_HEAD_DEPRECATED = "Deprecated"
SHEET_HEAD_ORPHANED = "Orphaned"
SHEET_HEAD_COST = "Cost"
SHEET_HEAD_MASS = "Mass"
SHEET_HEAD_DIMS_WIDTH = "Width"
SHEET_HEAD_DIMS_DEPTH = "Depth"
SHEET_HEAD_DIMS_HEIGHT = "Height"
SHEET_HEAD_SDESC = "Short Description"
SHEET_HEAD_DESC = "Description"
"""
                )

            lang_file = pathlib.Path(temp_dir, "japanese.tsv")
            lang_list = [
                ["id", "description", "en", "local"],
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

            bind_file = pathlib.Path(temp_dir, "keybindings.toml")
            with open(bind_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[keybindings]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            sw_compdocs.main.run(
                out_path=out_file,
                defn_dir=defn_dir,
                label_file=label_file,
                lang_file=lang_file,
                bind_file=bind_file,
                out_mode="sheet",
                out_encoding="shift-jis",
                out_newline="\n",
            )

            with open(out_file, mode="r", encoding="shift-jis", newline="\n") as fp:
                got_md = fp.read()

            want_md = """\
Name,File,Category,Tags,Multibody,Deprecated,Orphaned,Cost,Mass,Width,Depth,Height,Short Description,Description
テスト 01,test_01.xml,Blocks,,FALSE,FALSE,FALSE,0,1,1,1,1,テンプレート 01,
テスト 02,test_02.xml,Blocks,,FALSE,FALSE,FALSE,0,2,1,1,1,テンプレート 02,
"""
            self.assertEqual(got_md, want_md)

    def test_sheet_encoding_newline_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_file = pathlib.Path(temp_dir, "out.csv")

            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()

            defn_file = pathlib.Path(defn_dir, "test_01.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "test_02.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "dummy")
            defn_file.mkdir()

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
SHEET_HEAD_NAME = "Name"
SHEET_HEAD_FILE = "File"
SHEET_HEAD_CATEGORY = "Category"
SHEET_HEAD_TAGS = "Tags"
SHEET_HEAD_MULTIBODY = "Multibody"
SHEET_HEAD_DEPRECATED = "Deprecated"
SHEET_HEAD_ORPHANED = "Orphaned"
SHEET_HEAD_COST = "Cost"
SHEET_HEAD_MASS = "Mass"
SHEET_HEAD_DIMS_WIDTH = "Width"
SHEET_HEAD_DIMS_DEPTH = "Depth"
SHEET_HEAD_DIMS_HEIGHT = "Height"
SHEET_HEAD_SDESC = "Short Description"
SHEET_HEAD_DESC = "Description"
"""
                )

            lang_file = pathlib.Path(temp_dir, "japanese.tsv")
            lang_list = [
                ["id", "description", "en", "local"],
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

            bind_file = pathlib.Path(temp_dir, "keybindings.toml")
            with open(bind_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[keybindings]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            sw_compdocs.main.run(
                out_path=out_file,
                defn_dir=defn_dir,
                label_file=label_file,
                lang_file=lang_file,
                bind_file=bind_file,
                out_mode="sheet",
            )

            with open(out_file, mode="r", encoding="utf-8", newline="\r\n") as fp:
                got_md = fp.read()

            want_md = """\
Name,File,Category,Tags,Multibody,Deprecated,Orphaned,Cost,Mass,Width,Depth,Height,Short Description,Description
テスト 01,test_01.xml,Blocks,,FALSE,FALSE,FALSE,0,1,1,1,1,テンプレート 01,
テスト 02,test_02.xml,Blocks,,FALSE,FALSE,FALSE,0,2,1,1,1,テンプレート 02,
"""
            want_md = want_md.replace("\n", "\r\n")
            self.assertEqual(got_md, want_md)

    def test_sheet_exc_unicode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_file = pathlib.Path(temp_dir, "out.csv")

            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()

            defn_file = pathlib.Path(defn_dir, "test_01.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "test_02.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="2"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "dummy")
            defn_file.mkdir()

            label_file = pathlib.Path(temp_dir, "label.toml")
            with open(label_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[label]
SHEET_HEAD_NAME = "Name"
SHEET_HEAD_FILE = "File"
SHEET_HEAD_CATEGORY = "Category"
SHEET_HEAD_TAGS = "Tags"
SHEET_HEAD_MULTIBODY = "Multibody"
SHEET_HEAD_DEPRECATED = "Deprecated"
SHEET_HEAD_ORPHANED = "Orphaned"
SHEET_HEAD_COST = "Cost"
SHEET_HEAD_MASS = "Mass"
SHEET_HEAD_DIMS_WIDTH = "Width"
SHEET_HEAD_DIMS_DEPTH = "Depth"
SHEET_HEAD_DIMS_HEIGHT = "Height"
SHEET_HEAD_SDESC = "Short Description"
SHEET_HEAD_DESC = "Description"
"""
                )

            lang_file = pathlib.Path(temp_dir, "japanese.tsv")
            lang_list = [
                ["id", "description", "en", "local"],
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

            bind_file = pathlib.Path(temp_dir, "keybindings.toml")
            with open(bind_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[keybindings]
template_01 = "テンプレート 01"
template_02 = "テンプレート 02"
"""
                )

            with self.assertRaises(sw_compdocs.wraperr.UnicodeEncodeFileError) as ctx:
                sw_compdocs.main.run(
                    out_path=out_file,
                    defn_dir=defn_dir,
                    label_file=label_file,
                    lang_file=lang_file,
                    bind_file=bind_file,
                    out_mode="sheet",
                    out_encoding="ascii",
                    out_newline="\r\n",
                )
            self.assertEqual(ctx.exception.filename, out_file)

    def test_filter(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_show_deprecated", bool),
                ("input_show_orphaned", bool),
                ("want_csv", str),
            ],
        )
        self.maxDiff = None

        for tc in [
            tt(
                input_show_deprecated=True,
                input_show_orphaned=True,
                want_csv="""\
Name,File,Category,Tags,Multibody,Deprecated,Orphaned,Cost,Mass,Width,Depth,Height,Short Description,Description
,01_normal.xml,Blocks,,FALSE,FALSE,FALSE,0,0,1,1,1,,
 (Deprecated),02_deprecated.xml,Blocks,,FALSE,TRUE,FALSE,0,0,1,1,1,,
,03_orphan.xml,Blocks,,FALSE,FALSE,TRUE,0,0,1,1,1,,
""",
            ),
            tt(
                input_show_deprecated=False,
                input_show_orphaned=True,
                want_csv="""\
Name,File,Category,Tags,Multibody,Deprecated,Orphaned,Cost,Mass,Width,Depth,Height,Short Description,Description
,01_normal.xml,Blocks,,FALSE,FALSE,FALSE,0,0,1,1,1,,
,03_orphan.xml,Blocks,,FALSE,FALSE,TRUE,0,0,1,1,1,,
""",
            ),
            tt(
                input_show_deprecated=True,
                input_show_orphaned=False,
                want_csv="""\
Name,File,Category,Tags,Multibody,Deprecated,Orphaned,Cost,Mass,Width,Depth,Height,Short Description,Description
,01_normal.xml,Blocks,,FALSE,FALSE,FALSE,0,0,1,1,1,,
 (Deprecated),02_deprecated.xml,Blocks,,FALSE,TRUE,FALSE,0,0,1,1,1,,
""",
            ),
        ]:
            with self.subTest(tc=tc):
                with tempfile.TemporaryDirectory() as temp_dir:
                    out_file = pathlib.Path(temp_dir, "out.csv")

                    defn_dir = pathlib.Path(temp_dir, "definitions")
                    defn_dir.mkdir()

                    defn_file = pathlib.Path(defn_dir, "01_normal.xml")
                    with open(
                        defn_file, mode="x", encoding="utf-8", newline="\r\n"
                    ) as fp:
                        fp.write(
                            """\
<?xml version="1.0" encoding="UTF-8"?>
<definition/>
        """
                        )

                    defn_file = pathlib.Path(defn_dir, "02_deprecated.xml")
                    with open(
                        defn_file, mode="x", encoding="utf-8", newline="\r\n"
                    ) as fp:
                        fp.write(
                            """\
<?xml version="1.0" encoding="UTF-8"?>
<definition flags="536870912"/>
        """
                        )

                    defn_file = pathlib.Path(defn_dir, "03_orphan.xml")
                    with open(
                        defn_file, mode="x", encoding="utf-8", newline="\r\n"
                    ) as fp:
                        fp.write(
                            """\
<?xml version="1.0" encoding="UTF-8"?>
<definition flags="128"/>
        """
                        )

                    sw_compdocs.main.run(
                        out_path=out_file,
                        defn_dir=defn_dir,
                        show_deprecated=tc.input_show_deprecated,
                        show_orphaned=tc.input_show_orphaned,
                        out_mode="sheet",
                        out_encoding="utf-8",
                        out_newline="\n",
                    )

                    with open(out_file, mode="r", encoding="utf-8", newline="\n") as fp:
                        got_csv = fp.read()
                    self.assertEqual(got_csv, tc.want_csv)


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


class TestParseError(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_exc", lxml.etree.ParseError),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_exc=lxml.etree.ParseError("message", 0, 1, 1),
                want_s="message",
            ),
            tt(
                input_exc=lxml.etree.ParseError(
                    "message", 0, 1, 1, filename="filename"
                ),
                want_s="message (in file 'filename')",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.main.format_parse_error(tc.input_exc)
                self.assertEqual(got_s, tc.want_s)


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
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--show-deprecated",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--hide-deprecated",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=False,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--show-orphaned",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=True,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--hide-orphaned",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
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
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file="path/to/label",
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
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
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file="path/to/language",
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--keybindings",
                    "path/to/keybindings",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file="path/to/keybindings",
                    out_mode="document",
                    out_encoding=None,
                    out_newline=None,
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--mode",
                    "sheet",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="sheet",
                    out_encoding=None,
                    out_newline=None,
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
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding="shift-jis",
                    out_newline=None,
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
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline="\r",
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
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="document",
                    out_encoding=None,
                    out_newline="\r\n",
                ),
            ),
            tt(
                input_args=[
                    "--definitions",
                    "path/to/definitions",
                    "--mode",
                    "sheet",
                    "--newline",
                    "LF",
                    "path/to/output",
                ],
                want_call_args=unittest.mock.call(
                    out_path="path/to/output",
                    defn_dir="path/to/definitions",
                    show_deprecated=True,
                    show_orphaned=False,
                    label_file=None,
                    lang_file=None,
                    bind_file=None,
                    out_mode="sheet",
                    out_encoding=None,
                    out_newline="\n",
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
                out_path="path/to/output",
                defn_dir=str(definitions),
                show_deprecated=True,
                show_orphaned=False,
                label_file=None,
                lang_file=None,
                bind_file=None,
                out_mode="document",
                out_encoding=None,
                out_newline=None,
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

    def test_argp_invalid(self) -> None:
        for input_args in [
            [
                "--definitions",
                "path/to/definitions",
                "--mode",
                "invalid",
                "path/to/output",
            ],
            [
                "--definitions",
                "path/to/definitions",
                "--newline",
                "LFCR",
                "path/to/output",
            ],
        ]:
            with (
                self.assertRaises(SystemExit) as ctx,
                unittest.mock.patch.object(sw_compdocs.main, "run") as mock,
                unittest.mock.patch.object(sys, "stdout", new=io.StringIO()),
                unittest.mock.patch.object(sys, "stderr", new=io.StringIO()),
            ):
                sw_compdocs.main.main(args=input_args)
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
                input_exc=sw_compdocs.component.DefinitionXMLError("message"),
                want_stderr="sw_compdocs: error: message\n",
            ),
            tt(
                input_exc=sw_compdocs.component.MultibodyLinkError(
                    "parent_key", "child_key"
                ),
                want_stderr="sw_compdocs: error: failed to link parent component 'parent_key' and child component 'child_key'\n",
            ),
            tt(
                input_exc=sw_compdocs.generator.LabelKeyError("key"),
                want_stderr="sw_compdocs: error: missing label text for key 'key'\n",
            ),
            tt(
                input_exc=sw_compdocs.generator.LabelMissingPlaceholderError("key"),
                want_stderr="sw_compdocs: error: missing placeholder in label text for key 'key'\n",
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
                want_stderr="sw_compdocs: error: message (in file 'path/to/xml')\n",
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
            out_dir = pathlib.Path(temp_dir, "out")
            out_dir.mkdir()

            defn_dir = pathlib.Path(temp_dir, "definitions")
            defn_dir.mkdir()

            defn_file = pathlib.Path(defn_dir, "test_01.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
                fp.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition mass="1"/>
"""
                )

            defn_file = pathlib.Path(defn_dir, "test_02.xml")
            with open(defn_file, mode="x", encoding="utf-8", newline="\r\n") as fp:
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
DOCUMENT_PROP_MASS = "重量：{}"
DOCUMENT_PROP_DIMS = "サイズ (WxDxH)：{}"
DOCUMENT_PROP_COST = "価格：${}"
DOCUMENT_PROP_TAGS = "タグ：{}"
DOCUMENT_PROP_FILE = "ファイル：{}"
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

            bind_file = pathlib.Path(temp_dir, "keybindings.toml")
            with open(bind_file, mode="x", encoding="utf-8", newline="\n") as fp:
                fp.write(
                    """\
[keybindings]
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
                        str(defn_dir),
                        "--label",
                        str(label_file),
                        "--language",
                        str(lang_file),
                        "--keybindings",
                        str(bind_file),
                        "--encoding",
                        "shift-jis",
                        "--newline",
                        "CRLF",
                        str(out_dir),
                    ]
                )
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")

            out_file = pathlib.Path(out_dir, "00_BLOCKS.md")
            with open(out_file, mode="r", encoding="shift-jis", newline="\r\n") as fp:
                got_md = fp.read()
            got_md = got_md.replace("\r\n", "\n")

            want_md = """\
# Blocks

## テスト 01

テンプレート 01

### プロパティ

- 重量：1
- サイズ (WxDxH)：1x1x1
- 価格：$0
- タグ：
- ファイル：test_01.xml

## テスト 02

テンプレート 02

### プロパティ

- 重量：2
- サイズ (WxDxH)：1x1x1
- 価格：$0
- タグ：
- ファイル：test_02.xml
"""
            self.assertEqual(got_md, want_md)
