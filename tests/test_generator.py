import collections.abc
import sw_compdocs._types
import sw_compdocs.component
import sw_compdocs.document
import sw_compdocs.generator
import sw_compdocs.language
import sw_compdocs.template
import typing
import unittest


class TestLabelKeyErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.generator.LabelKeyError("key")
        exc_args: tuple[object] = exc.args
        self.assertEqual(exc_args, ("key",))
        self.assertEqual(exc.key, "key")


class TestLabelKeyErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.generator.LabelKeyError("key")
        self.assertEqual(str(exc), "missing label text for key 'key'")


class TestLabelGet(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_key", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_label=None,
                input_key="LABEL",
                want_s="LABEL",
            ),
            tt(
                input_label={"LABEL": "text"},
                input_key="LABEL",
                want_s="text",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.generator._label_get(tc.input_label, tc.input_key)
                self.assertEqual(got_s, tc.want_s)

    def test_exc_label(self) -> None:
        with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
            sw_compdocs.generator._label_get({}, "LABEL")
        self.assertEqual(ctx.exception.key, "LABEL")


class TestLangFindEn(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_lang_en", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_lang=None,
                input_lang_en="en",
                want_s="en",
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id", "description", "en", "local"
                        )
                    ]
                ),
                input_lang_en="en",
                want_s="local",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.generator._lang_find_en(
                    tc.input_lang, tc.input_lang_en
                )
                self.assertEqual(got_s, tc.want_s)


class TestLangTranslate(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_text", sw_compdocs.language.Text),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_lang=None,
                input_text=sw_compdocs.language.Text(id="id", en="en"),
                want_s="en",
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation("id", "", "", "local"),
                    ]
                ),
                input_text=sw_compdocs.language.Text(id="id", en="en"),
                want_s="local",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.generator._lang_translate(
                    tc.input_lang, tc.input_text
                )
                self.assertEqual(got_s, tc.want_s)


class TestCtxFormat(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("input_s", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_ctx=None,
                input_s="$[var]",
                want_s="$[var]",
            ),
            tt(
                input_ctx={"var": "text"},
                input_s="$[var]",
                want_s="text",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.generator._ctx_format(tc.input_ctx, tc.input_s)
                self.assertEqual(got_s, tc.want_s)


class TestGenerateDocumentPropertyTable(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_defn", sw_compdocs.component.Definition),
                ("want_tbl", sw_compdocs.document.Table),
            ],
        )

        for tc in [
            # normal
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(
                    file="file",
                    mass=10.0,
                    value=100,
                    tags="tags",
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=-1, z=-2),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=2),
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_MASS_LABEL", "10"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x5x3"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_COST_LABEL", "100"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_TAGS_LABEL", "tags"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_FILE_LABEL", "file"]
                            ),
                        ],
                    )
                ),
            ),
            # empty
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                            ),
                        ],
                    )
                ),
            ),
            # mass format
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(mass=0.25),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0.25"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                            ),
                        ],
                    )
                ),
            ),
            # file format
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(
                    file=b"path/to/definition.xml"
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["DOCUMENT_PROP_TABLE_FILE_LABEL", "definition.xml"]
                            ),
                        ],
                    )
                ),
            ),
            # label
            tt(
                input_label={
                    "DOCUMENT_PROP_TABLE_HEAD_LABEL": "Label",
                    "DOCUMENT_PROP_TABLE_HEAD_VALUE": "Value",
                    "DOCUMENT_PROP_TABLE_MASS_LABEL": "Mass",
                    "DOCUMENT_PROP_TABLE_DIMS_LABEL": "Dimensions",
                    "DOCUMENT_PROP_TABLE_COST_LABEL": "Cost",
                    "DOCUMENT_PROP_TABLE_TAGS_LABEL": "Tags",
                    "DOCUMENT_PROP_TABLE_FILE_LABEL": "File",
                },
                input_defn=sw_compdocs.component.Definition(),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["Label", "Value"]),
                        [
                            sw_compdocs.document.TableDataRow(["Mass", "0"]),
                            sw_compdocs.document.TableDataRow(["Dimensions", "1x1x1"]),
                            sw_compdocs.document.TableDataRow(["Cost", "0"]),
                            sw_compdocs.document.TableDataRow(["Tags", ""]),
                            sw_compdocs.document.TableDataRow(["File", ""]),
                        ],
                    )
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_tbl = sw_compdocs.generator.generate_document_property_table(
                    tc.input_defn, label=tc.input_label
                )
                self.assertEqual(got_tbl, tc.want_tbl)

    def test_exc_label(self) -> None:
        defn = sw_compdocs.component.Definition()
        label_all = {
            "DOCUMENT_PROP_TABLE_HEAD_LABEL": "Label",
            "DOCUMENT_PROP_TABLE_HEAD_VALUE": "Value",
            "DOCUMENT_PROP_TABLE_MASS_LABEL": "Mass",
            "DOCUMENT_PROP_TABLE_DIMS_LABEL": "Dimensions",
            "DOCUMENT_PROP_TABLE_COST_LABEL": "Cost",
            "DOCUMENT_PROP_TABLE_TAGS_LABEL": "Tags",
            "DOCUMENT_PROP_TABLE_FILE_LABEL": "File",
        }
        for key in label_all.keys():
            with self.subTest(label_key=key):
                label = label_all.copy()
                del label[key]
                with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
                    sw_compdocs.generator.generate_document_property_table(
                        defn, label=label
                    )
                self.assertEqual(ctx.exception.key, key)


class TestGenerateDocumentProperty(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_defn", sw_compdocs.component.Definition),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            tt(
                input_label=None,
                input_lang=None,
                input_defn=sw_compdocs.component.Definition(),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("PROPERTIES"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label={
                    "DOCUMENT_PROP_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_PROP_TABLE_HEAD_VALUE": "値",
                    "DOCUMENT_PROP_TABLE_MASS_LABEL": "重量",
                    "DOCUMENT_PROP_TABLE_DIMS_LABEL": "サイズ",
                    "DOCUMENT_PROP_TABLE_COST_LABEL": "値段",
                    "DOCUMENT_PROP_TABLE_TAGS_LABEL": "タグ",
                    "DOCUMENT_PROP_TABLE_FILE_LABEL": "ファイル",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "PROPERTIES", "プロパティ"
                        )
                    ]
                ),
                input_defn=sw_compdocs.component.Definition(),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("プロパティ"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["ラベル", "値"]),
                                [
                                    sw_compdocs.document.TableDataRow(["重量", "0"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["サイズ", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["値段", "0"]),
                                    sw_compdocs.document.TableDataRow(["タグ", ""]),
                                    sw_compdocs.document.TableDataRow(["ファイル", ""]),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_property(
                    tc.input_defn, label=tc.input_label, lang=tc.input_lang
                )
                self.assertEqual(got_doc, tc.want_doc)


class TestGenerateDocumentLogicTable(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("input_ln_list", list[sw_compdocs.component.LogicNode]),
                ("want_tbl", sw_compdocs.document.Table),
            ],
        )

        for tc in [
            # empty
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_ln_list=[],
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                            ]
                        ),
                        [],
                    )
                ),
            ),
            # normal
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_ln_list=[
                    sw_compdocs.component.LogicNode(
                        key="test",
                        idx=0,
                        label=sw_compdocs.language.Text(
                            id="def_test_node_0_label", en="label 0 $[label_0]"
                        ),
                        type=sw_compdocs.component.LogicNodeType.BOOL,
                        description=sw_compdocs.language.Text(
                            id="def_test_node_0_desc", en="desc 0 $[desc_0]"
                        ),
                    ),
                    sw_compdocs.component.LogicNode(
                        key="test",
                        idx=1,
                        label=sw_compdocs.language.Text(
                            id="def_test_node_1_label", en="label 1 $[label_1]"
                        ),
                        type=sw_compdocs.component.LogicNodeType.FLOAT,
                        description=sw_compdocs.language.Text(
                            id="def_test_node_1_desc", en="desc 1 $[desc_1]"
                        ),
                    ),
                ],
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                [
                                    "on/off",
                                    "label 0 $[label_0]",
                                    "desc 0 $[desc_0]",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["number", "label 1 $[label_1]", "desc 1 $[desc_1]"]
                            ),
                        ],
                    )
                ),
            ),
            tt(
                input_label={
                    "DOCUMENT_LOGIC_TABLE_HEAD_TYPE": "種別",
                    "DOCUMENT_LOGIC_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_HEAD_DESC": "説明",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "number",
                            "数値",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label",
                            "",
                            "label 0 $[label_0]",
                            "ラベル 0 $[label_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc",
                            "",
                            "desc 0 $[desc_0]",
                            "説明 0 $[desc_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_label",
                            "",
                            "label 1 $[label_1]",
                            "ラベル 1 $[label_1]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_desc",
                            "",
                            "desc 1 $[desc_1]",
                            "説明 1 $[desc_1]",
                        ),
                    ]
                ),
                input_ctx={
                    "label_0": "label_0_fmt",
                    "desc_0": "desc_0_fmt",
                    "label_1": "label_1_fmt",
                    "desc_1": "desc_1_fmt",
                },
                input_ln_list=[
                    sw_compdocs.component.LogicNode(
                        key="test",
                        idx=0,
                        label=sw_compdocs.language.Text(
                            id="def_test_node_0_label", en="label 0 $[label_0]"
                        ),
                        type=sw_compdocs.component.LogicNodeType.BOOL,
                        description=sw_compdocs.language.Text(
                            id="def_test_node_0_desc", en="desc 0 $[desc_0]"
                        ),
                    ),
                    sw_compdocs.component.LogicNode(
                        key="test",
                        idx=1,
                        label=sw_compdocs.language.Text(
                            id="def_test_node_1_label", en="label 1 $[label_1]"
                        ),
                        type=sw_compdocs.component.LogicNodeType.FLOAT,
                        description=sw_compdocs.language.Text(
                            id="def_test_node_1_desc", en="desc 1 $[desc_1]"
                        ),
                    ),
                ],
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [
                            sw_compdocs.document.TableDataRow(
                                [
                                    "オン/オフ",
                                    "ラベル 0 label_0_fmt",
                                    "説明 0 desc_0_fmt",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["数値", "ラベル 1 label_1_fmt", "説明 1 desc_1_fmt"]
                            ),
                        ],
                    )
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_tbl = sw_compdocs.generator.generate_document_logic_table(
                    tc.input_ln_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    ctx=tc.input_ctx,
                )
                self.assertEqual(got_tbl, tc.want_tbl)

    def test_exc_label(self) -> None:
        lns = sw_compdocs.component.LogicNodeList()
        label_all = {
            "DOCUMENT_LOGIC_TABLE_HEAD_TYPE": "種別",
            "DOCUMENT_LOGIC_TABLE_HEAD_LABEL": "ラベル",
            "DOCUMENT_LOGIC_TABLE_HEAD_DESC": "説明",
        }
        for key in label_all.keys():
            with self.subTest(label_key=key):
                label = label_all.copy()
                del label[key]
                with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
                    sw_compdocs.generator.generate_document_logic_table(
                        lns, label=label
                    )
                self.assertEqual(ctx.exception.key, key)


class TestGenerateDocumentLogic(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("input_lns", sw_compdocs.component.LogicNodeList),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_lns=sw_compdocs.component.LogicNodeList(),
                want_doc=sw_compdocs.document.Document(),
            ),
            # logic node mode type
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="BOOL"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="FLOAT"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="TORQUE"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="WATER"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.WATER,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="ELECTRIC"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="COMPOSITE"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.COMPOSITE,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="VIDEO"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.VIDEO,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="AUDIO"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.AUDIO,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="ROPE"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ROPE,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="OUTPUT"),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic inputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "BOOL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["number", "FLOAT", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["composite", "COMPOSITE", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["video", "VIDEO", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["audio", "AUDIO", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "OUTPUT", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["power", "TORQUE", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["fluid", "WATER", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["electric", "ELECTRIC", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["rope", "ROPE", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # lang
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic inputs", "ロジック入力"
                        ),
                        sw_compdocs.language.Translation(
                            "", "", "logic outputs", "ロジック出力"
                        ),
                        sw_compdocs.language.Translation("", "", "connections", "接続"),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation("", "", "power", "動力"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "IN"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", ""
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_label", "", "", "OUT"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_desc", "", "", ""
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_2_label", "", "", "CONN"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_2_desc", "", "", ""
                        ),
                    ]
                ),
                input_ctx=None,
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=0,
                            label=sw_compdocs.language.Text(id="def_test_node_0_label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_0_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=1,
                            label=sw_compdocs.language.Text(id="def_test_node_1_label"),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_1_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=2,
                            label=sw_compdocs.language.Text(id="def_test_node_2_label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_2_desc"
                            ),
                        ),
                    ],
                    key="test",
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック入力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["オン/オフ", "IN", ""]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック出力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["オン/オフ", "OUT", ""]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("接続"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["動力", "CONN", ""]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_logic(
                    tc.input_lns,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    ctx=tc.input_ctx,
                )
                self.assertEqual(got_doc, tc.want_doc)


class TestGenerateDocumentComponent(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("input_defn", sw_compdocs.component.Definition),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading(""),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # deprecated
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    flags=sw_compdocs.component.Flags.IS_DEPRECATED
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading(""),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_DEPRECATED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # text
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    name=sw_compdocs.language.Text(en="Name"),
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            en="Short Description"
                        ),
                        description=sw_compdocs.language.Text(en="Description"),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                label=sw_compdocs.language.Text(en="Node Label"),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    en="Node Description"
                                ),
                            ),
                        ],
                    ),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Name"),
                        sw_compdocs.document.Paragraph("Short Description"),
                        sw_compdocs.document.Paragraph("Description"),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic inputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "Node Label", "Node Description"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # label, lang, template
            tt(
                input_label={
                    "DOCUMENT_DEPRECATED_TEXT": "この部品は非推奨です。",
                    "DOCUMENT_PROP_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_PROP_TABLE_HEAD_VALUE": "値",
                    "DOCUMENT_PROP_TABLE_MASS_LABEL": "重量",
                    "DOCUMENT_PROP_TABLE_DIMS_LABEL": "サイズ(WxDxH)",
                    "DOCUMENT_PROP_TABLE_COST_LABEL": "値段",
                    "DOCUMENT_PROP_TABLE_TAGS_LABEL": "タグ",
                    "DOCUMENT_PROP_TABLE_FILE_LABEL": "ファイル",
                    "DOCUMENT_LOGIC_TABLE_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_HEAD_DESC": "説明",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "logic inputs",
                            "ロジック入力",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "PROPERTIES",
                            "プロパティ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "def_dummy_name",
                            "",
                            "",
                            "部品名",
                        ),
                        sw_compdocs.language.Translation(
                            "def_dummy_desc",
                            "",
                            "",
                            "$[def_dummy_desc_placeholder]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_dummy_s_desc",
                            "",
                            "",
                            "$[def_dummy_s_desc_placeholder]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_dummy_node_0_label",
                            "",
                            "",
                            "$[def_dummy_node_0_label_placeholder]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_dummy_node_0_desc",
                            "",
                            "",
                            "$[def_dummy_node_0_desc_placeholder]",
                        ),
                    ]
                ),
                input_ctx={
                    "def_dummy_desc_placeholder": "説明",
                    "def_dummy_s_desc_placeholder": "短い説明",
                    "def_dummy_node_0_label_placeholder": "ノードラベル",
                    "def_dummy_node_0_desc_placeholder": "ノード説明",
                },
                input_defn=sw_compdocs.component.Definition(
                    key="dummy",
                    name=sw_compdocs.language.Text(id="def_dummy_name"),
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        key="dummy",
                        short_description=sw_compdocs.language.Text(
                            id="def_dummy_s_desc"
                        ),
                        description=sw_compdocs.language.Text(id="def_dummy_desc"),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                key="dummy",
                                idx=0,
                                label=sw_compdocs.language.Text(
                                    id="def_dummy_node_0_label"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_dummy_node_0_desc"
                                ),
                            ),
                        ],
                        key="dummy",
                    ),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("部品名"),
                        sw_compdocs.document.Paragraph("短い説明"),
                        sw_compdocs.document.Paragraph("説明"),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["ラベル", "値"]),
                                [
                                    sw_compdocs.document.TableDataRow(["重量", "0"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["サイズ(WxDxH)", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["値段", "0"]),
                                    sw_compdocs.document.TableDataRow(["タグ", ""]),
                                    sw_compdocs.document.TableDataRow(["ファイル", ""]),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック入力", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["オン/オフ", "ノードラベル", "ノード説明"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # button_push
            tt(
                input_label={
                    "DOCUMENT_PROP_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_PROP_TABLE_HEAD_VALUE": "値",
                    "DOCUMENT_PROP_TABLE_MASS_LABEL": "重量",
                    "DOCUMENT_PROP_TABLE_DIMS_LABEL": "サイズ(WxDxH)",
                    "DOCUMENT_PROP_TABLE_COST_LABEL": "値段",
                    "DOCUMENT_PROP_TABLE_TAGS_LABEL": "タグ",
                    "DOCUMENT_PROP_TABLE_FILE_LABEL": "ファイル",
                    "DOCUMENT_LOGIC_TABLE_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_HEAD_DESC": "説明",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "logic inputs",
                            "ロジック入力",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "logic outputs",
                            "ロジック出力",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "connections",
                            "接続",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "PROPERTIES",
                            "プロパティ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_name",
                            "",
                            "Push Button",
                            "押しボタン",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_desc",
                            "",
                            "An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs.",
                            "外部入力でボタンのオン/オフを制御することができ, 複数のボタンを同時に制御できます.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_s_desc",
                            "",
                            "A button that outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal when not interacting.",
                            "[$[action_interact_left]]/[$[action_interact_right]] を押している間のみオン信号を出力するボタンです.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_0_label",
                            "",
                            "Pressed",
                            "オン",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_0_desc",
                            "",
                            "Outputs an on signal when you interact wtih [$[action_interact_left]]/[$[action_interact_right]], and an off signal otherwise.",
                            "[$[action_interact_left]]/[$[action_interact_right]] を押している間のみオン信号を出力します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_1_label",
                            "",
                            "External Input",
                            "外部入力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_1_desc",
                            "",
                            "Allows an external on/off signal to control whether or not the button is pressed.",
                            "外部からのオン/オフ信号の入力でボタンのオン/オフを制御できます.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_2_label",
                            "",
                            "Electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_2_desc",
                            "",
                            "Electrical power connection.",
                            "電力網から電力を供給します.",
                        ),
                    ]
                ),
                input_ctx={"action_interact_left": "q", "action_interact_right": "e"},
                input_defn=sw_compdocs.component.Definition(
                    file="button_push.xml",
                    key="button_push",
                    name=sw_compdocs.language.Text(
                        id="def_button_push_name", en="Push Button"
                    ),
                    category=sw_compdocs.component.Category.MECHANICS,
                    mass=1.0,
                    value=10,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_button_push_s_desc",
                            en="A button that outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal when not interacting.",
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_button_push_desc",
                            en="An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs.",
                        ),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                key="button_push",
                                idx=0,
                                label=sw_compdocs.language.Text(
                                    id="def_button_push_node_0_label", en="Pressed"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_button_push_node_0_desc",
                                    en="Outputs an on signal when you interact wtih [$[action_interact_left]]/[$[action_interact_right]], and an off signal otherwise.",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="button_push",
                                idx=1,
                                label=sw_compdocs.language.Text(
                                    id="def_button_push_node_1_label",
                                    en="External Input",
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_button_push_node_1_desc",
                                    en="Allows an external on/off signal to control whether or not the button is pressed.",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="button_push",
                                idx=2,
                                label=sw_compdocs.language.Text(
                                    id="def_button_push_node_2_label", en="Electric"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description=sw_compdocs.language.Text(
                                    id="def_button_push_node_2_desc",
                                    en="Electrical power connection.",
                                ),
                            ),
                        ],
                        key="button_push",
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("押しボタン"),
                        sw_compdocs.document.Paragraph(
                            "[q]/[e] を押している間のみオン信号を出力するボタンです."
                        ),
                        sw_compdocs.document.Paragraph(
                            "外部入力でボタンのオン/オフを制御することができ, 複数のボタンを同時に制御できます."
                        ),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["ラベル", "値"]),
                                [
                                    sw_compdocs.document.TableDataRow(["重量", "1"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["サイズ(WxDxH)", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["値段", "10"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["タグ", "basic"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["ファイル", "button_push.xml"]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック入力", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "オン/オフ",
                                            "外部入力",
                                            "外部からのオン/オフ信号の入力でボタンのオン/オフを制御できます.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック出力", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "オン/オフ",
                                            "オン",
                                            "[q]/[e] を押している間のみオン信号を出力します.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("接続", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "電力",
                                            "電力",
                                            "電力網から電力を供給します.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_component(
                    tc.input_defn,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    ctx=tc.input_ctx,
                )
                self.assertEqual(got_doc, tc.want_doc)

    def test_exc_label(self) -> None:
        defn = sw_compdocs.component.Definition(
            flags=sw_compdocs.component.Flags.IS_DEPRECATED
        )
        with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
            sw_compdocs.generator.generate_document_component(defn, label={})
        self.assertEqual(ctx.exception.key, "DOCUMENT_DEPRECATED_TEXT")


class TestGenerateDocumentComponentList(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_defn_list", list[sw_compdocs.component.Definition]),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            tt(
                input_defn_list=[],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(),
            ),
            tt(
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="A")
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="B")
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("A", level=1),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("B", level=1),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        key="test",
                        name=sw_compdocs.language.Text(id="def_test_name", en="Test"),
                        tooltip_properties=sw_compdocs.component.TooltipProperties(
                            short_description=sw_compdocs.language.Text(
                                id="def_test_s_desc", en="Short Description"
                            ),
                            description=sw_compdocs.language.Text(
                                id="def_test_desc", en="Description"
                            ),
                        ),
                    ),
                ],
                input_label={
                    "DOCUMENT_PROP_TABLE_HEAD_LABEL": "Label",
                    "DOCUMENT_PROP_TABLE_HEAD_VALUE": "Value",
                    "DOCUMENT_PROP_TABLE_MASS_LABEL": "Mass",
                    "DOCUMENT_PROP_TABLE_DIMS_LABEL": "Dimensions (WxDxH)",
                    "DOCUMENT_PROP_TABLE_COST_LABEL": "Cost",
                    "DOCUMENT_PROP_TABLE_TAGS_LABEL": "Tags",
                    "DOCUMENT_PROP_TABLE_FILE_LABEL": "File",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "PROPERTIES", "プロパティ"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_name", "", "", "テスト"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_s_desc", "", "", "短い説明 $[s_desc]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_desc", "", "", "長い説明 $[desc]"
                        ),
                    ]
                ),
                input_ctx={"s_desc": "foo", "desc": "bar"},
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("テスト", level=1),
                        sw_compdocs.document.Paragraph("短い説明 foo"),
                        sw_compdocs.document.Paragraph("長い説明 bar"),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["Label", "Value"]),
                                [
                                    sw_compdocs.document.TableDataRow(["Mass", "0"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["Dimensions (WxDxH)", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["Cost", "0"]),
                                    sw_compdocs.document.TableDataRow(["Tags", ""]),
                                    sw_compdocs.document.TableDataRow(["File", ""]),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_component_list(
                    tc.input_defn_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    ctx=tc.input_ctx,
                )
                self.assertEqual(got_doc, tc.want_doc)


class TestGenerateDocument(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_comp_list=[],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(),
            ),
            # single
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
            # sort defn_list name
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_1",
                            name=sw_compdocs.language.Text(en="Blocks_3"),
                            value=1,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_2",
                            name=sw_compdocs.language.Text(en="Blocks_2"),
                            value=2,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_3",
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            value=3,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "3"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_2", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_3", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
            # sort defn_list key
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key=None,
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            value=4,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_3",
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            value=3,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_2",
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            value=2,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_1",
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            value=1,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "3"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "4"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
            # sort category
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="WINDOWS_0"),
                            category=sw_compdocs.component.Category.WINDOWS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="INDUSTRY_0"),
                            category=sw_compdocs.component.Category.INDUSTRY,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="MODULAR_ENGINES_0"),
                            category=sw_compdocs.component.Category.MODULAR_ENGINES,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="WEAPONS_0"),
                            category=sw_compdocs.component.Category.WEAPONS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="JET_ENGINES_0"),
                            category=sw_compdocs.component.Category.JET_ENGINES,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="ELECTRIC_0"),
                            category=sw_compdocs.component.Category.ELECTRIC,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="FLUID_0"),
                            category=sw_compdocs.component.Category.FLUID,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="DECORATIVE_0"),
                            category=sw_compdocs.component.Category.DECORATIVE,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="SENSORS_0"),
                            category=sw_compdocs.component.Category.SENSORS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="DISPLAYS_0"),
                            category=sw_compdocs.component.Category.DISPLAYS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="LOGIC_0"),
                            category=sw_compdocs.component.Category.LOGIC,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="SPECIALIST_EQUIPMENT_0"),
                            category=sw_compdocs.component.Category.SPECIALIST_EQUIPMENT,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="PROPULSION_0"),
                            category=sw_compdocs.component.Category.PROPULSION,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="MECHANICS_0"),
                            category=sw_compdocs.component.Category.MECHANICS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="VEHICLE_CONTROL_0"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="BLOCKS_0"),
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("BLOCKS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Vehicle Control", level=1),
                        sw_compdocs.document.Heading("VEHICLE_CONTROL_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Mechanics", level=1),
                        sw_compdocs.document.Heading("MECHANICS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Propulsion", level=1),
                        sw_compdocs.document.Heading("PROPULSION_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Specialist Equipment", level=1),
                        sw_compdocs.document.Heading("SPECIALIST_EQUIPMENT_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Logic", level=1),
                        sw_compdocs.document.Heading("LOGIC_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Displays", level=1),
                        sw_compdocs.document.Heading("DISPLAYS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Sensors", level=1),
                        sw_compdocs.document.Heading("SENSORS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Decorative", level=1),
                        sw_compdocs.document.Heading("DECORATIVE_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Fluid", level=1),
                        sw_compdocs.document.Heading("FLUID_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Electric", level=1),
                        sw_compdocs.document.Heading("ELECTRIC_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Jet Engines", level=1),
                        sw_compdocs.document.Heading("JET_ENGINES_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Weapons", level=1),
                        sw_compdocs.document.Heading("WEAPONS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Modular Engines", level=1),
                        sw_compdocs.document.Heading("MODULAR_ENGINES_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Industry", level=1),
                        sw_compdocs.document.Heading("INDUSTRY_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Windows", level=1),
                        sw_compdocs.document.Heading("WINDOWS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_PROP_TABLE_HEAD_LABEL",
                                        "DOCUMENT_PROP_TABLE_HEAD_VALUE",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
            # label, lang, template
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="test",
                            name=sw_compdocs.language.Text(
                                id="def_test_name", en="Test"
                            ),
                            tooltip_properties=sw_compdocs.component.TooltipProperties(
                                short_description=sw_compdocs.language.Text(
                                    id="def_test_s_desc", en="Short Description"
                                ),
                                description=sw_compdocs.language.Text(
                                    id="def_test_desc", en="Description"
                                ),
                            ),
                        )
                    ),
                ],
                input_label={
                    "DOCUMENT_PROP_TABLE_HEAD_LABEL": "Label",
                    "DOCUMENT_PROP_TABLE_HEAD_VALUE": "Value",
                    "DOCUMENT_PROP_TABLE_MASS_LABEL": "Mass",
                    "DOCUMENT_PROP_TABLE_DIMS_LABEL": "Dimensions (WxDxH)",
                    "DOCUMENT_PROP_TABLE_COST_LABEL": "Cost",
                    "DOCUMENT_PROP_TABLE_TAGS_LABEL": "Tags",
                    "DOCUMENT_PROP_TABLE_FILE_LABEL": "File",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "PROPERTIES", "プロパティ"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_name", "", "", "テスト"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_s_desc", "", "", "短い説明 $[s_desc]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_desc", "", "", "長い説明 $[desc]"
                        ),
                    ]
                ),
                input_ctx={"s_desc": "foo", "desc": "bar"},
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("テスト", level=2),
                        sw_compdocs.document.Paragraph("短い説明 foo"),
                        sw_compdocs.document.Paragraph("長い説明 bar"),
                        sw_compdocs.document.Heading("プロパティ", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["Label", "Value"]),
                                [
                                    sw_compdocs.document.TableDataRow(["Mass", "0"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["Dimensions (WxDxH)", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["Cost", "0"]),
                                    sw_compdocs.document.TableDataRow(["Tags", ""]),
                                    sw_compdocs.document.TableDataRow(["File", ""]),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document(
                    tc.input_comp_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    ctx=tc.input_ctx,
                )
                self.assertEqual(got_doc, tc.want_doc)


class TestGenerateSheetComponent(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("input_comp", sw_compdocs.component.Component),
                ("want_record", list[str]),
            ],
        )

        for tc in [
            tt(  # empty
                input_lang=None,
                input_ctx=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition()
                ),
                want_record=[
                    "",
                    "",
                    "Blocks",
                    "",
                    "FALSE",
                    "0",
                    "0",
                    "1",
                    "1",
                    "1",
                    "",
                    "",
                ],
            ),
            tt(  # normal
                input_lang=None,
                input_ctx=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        file="test.xml",
                        name=sw_compdocs.language.Text(en="Name"),
                        category=sw_compdocs.component.Category.BLOCKS,
                        mass=0.25,
                        value=2,
                        tags="tags",
                        tooltip_properties=sw_compdocs.component.TooltipProperties(
                            short_description=sw_compdocs.language.Text(
                                en="short_description"
                            ),
                            description=sw_compdocs.language.Text(en="description"),
                        ),
                        voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                        voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                    )
                ),
                want_record=[
                    "Name",
                    "test.xml",
                    "Blocks",
                    "tags",
                    "FALSE",
                    "0.25",
                    "2",
                    "3",
                    "7",
                    "5",
                    "short_description",
                    "description",
                ],
            ),
            tt(  # file
                input_lang=None,
                input_ctx=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(file=b"path/to/test.xml")
                ),
                want_record=[
                    "",
                    "test.xml",
                    "Blocks",
                    "",
                    "FALSE",
                    "0",
                    "0",
                    "1",
                    "1",
                    "1",
                    "",
                    "",
                ],
            ),
            tt(  # deprecated
                input_lang=None,
                input_ctx=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        flags=sw_compdocs.component.Flags.IS_DEPRECATED
                    )
                ),
                want_record=[
                    "",
                    "",
                    "Blocks",
                    "",
                    "TRUE",
                    "0",
                    "0",
                    "1",
                    "1",
                    "1",
                    "",
                    "",
                ],
            ),
            tt(  # lang, template
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "def_test_name", "", "", "$[name]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_s_desc", "", "", "$[s_desc]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_desc", "", "", "$[desc]"
                        ),
                    ]
                ),
                input_ctx={
                    "name": "Name",
                    "s_desc": "short_description",
                    "desc": "description",
                },
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        key="test",
                        name=sw_compdocs.language.Text(id="def_test_name"),
                        tooltip_properties=sw_compdocs.component.TooltipProperties(
                            short_description=sw_compdocs.language.Text(
                                id="def_test_s_desc"
                            ),
                            description=sw_compdocs.language.Text(id="def_test_desc"),
                        ),
                    )
                ),
                want_record=[
                    "$[name]",
                    "",
                    "Blocks",
                    "",
                    "FALSE",
                    "0",
                    "0",
                    "1",
                    "1",
                    "1",
                    "short_description",
                    "description",
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_record = sw_compdocs.generator.generate_sheet_component(
                    tc.input_comp, lang=tc.input_lang, ctx=tc.input_ctx
                )
                self.assertEqual(got_record, tc.want_record)


class TestGenerateSheetComponentList(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("want_record_list", list[list[str]]),
            ],
        )

        for tc in [
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Test 1")
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Test 2")
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Test 3")
                        )
                    ),
                ],
                input_lang=None,
                input_ctx=None,
                want_record_list=[
                    [
                        "Test 1",
                        "",
                        "Blocks",
                        "",
                        "FALSE",
                        "0",
                        "0",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                    [
                        "Test 2",
                        "",
                        "Blocks",
                        "",
                        "FALSE",
                        "0",
                        "0",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                    [
                        "Test 3",
                        "",
                        "Blocks",
                        "",
                        "FALSE",
                        "0",
                        "0",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                ],
            ),
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            file="test.xml",
                            key="test",
                            name=sw_compdocs.language.Text(id="def_test_name"),
                            category=sw_compdocs.component.Category.BLOCKS,
                            mass=1.0,
                            value=2,
                            tags="tags",
                            tooltip_properties=sw_compdocs.component.TooltipProperties(
                                short_description=sw_compdocs.language.Text(
                                    id="def_test_s_desc"
                                ),
                                description=sw_compdocs.language.Text(
                                    id="def_test_desc"
                                ),
                            ),
                            voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                            voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                        )
                    )
                ],
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "def_test_name", "", "", "$[name]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_s_desc", "", "", "$[s_desc]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_desc", "", "", "$[desc]"
                        ),
                    ]
                ),
                input_ctx={
                    "name": "Name",
                    "s_desc": "short_description",
                    "desc": "description",
                },
                want_record_list=[
                    [
                        "$[name]",
                        "test.xml",
                        "Blocks",
                        "tags",
                        "FALSE",
                        "1",
                        "2",
                        "3",
                        "7",
                        "5",
                        "short_description",
                        "description",
                    ]
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_record_list = sw_compdocs.generator.generate_sheet_component_list(
                    tc.input_comp_list, lang=tc.input_lang, ctx=tc.input_ctx
                )
                self.assertEqual(got_record_list, tc.want_record_list)


class TestGenerateSheet(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("want_record_list", list[list[str]]),
            ],
        )

        for tc in [
            tt(  # sort
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="a",
                            name=sw_compdocs.language.Text(en="Z"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=1,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key=None,
                            name=sw_compdocs.language.Text(en="A"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=2,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="z",
                            name=sw_compdocs.language.Text(en="A"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=3,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="a",
                            name=sw_compdocs.language.Text(en="A"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=4,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="z",
                            name=sw_compdocs.language.Text(en="Z"),
                            category=sw_compdocs.component.Category.BLOCKS,
                            value=5,
                        )
                    ),
                ],
                want_record_list=[
                    [
                        "SHEET_HEAD_NAME",
                        "SHEET_HEAD_FILE",
                        "SHEET_HEAD_CATEGORY",
                        "SHEET_HEAD_TAGS",
                        "SHEET_HEAD_DEPRECATED",
                        "SHEET_HEAD_MASS",
                        "SHEET_HEAD_COST",
                        "SHEET_HEAD_WIDTH",
                        "SHEET_HEAD_DEPTH",
                        "SHEET_HEAD_HEIGHT",
                        "SHEET_HEAD_SDESC",
                        "SHEET_HEAD_DESC",
                    ],
                    [
                        "Z",
                        "",
                        "Blocks",
                        "",
                        "FALSE",
                        "0",
                        "5",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                    [
                        "A",
                        "",
                        "Vehicle Control",
                        "",
                        "FALSE",
                        "0",
                        "4",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                    [
                        "A",
                        "",
                        "Vehicle Control",
                        "",
                        "FALSE",
                        "0",
                        "3",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                    [
                        "A",
                        "",
                        "Vehicle Control",
                        "",
                        "FALSE",
                        "0",
                        "2",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                    [
                        "Z",
                        "",
                        "Vehicle Control",
                        "",
                        "FALSE",
                        "0",
                        "1",
                        "1",
                        "1",
                        "1",
                        "",
                        "",
                    ],
                ],
            ),
            tt(  # label, lang, ctx
                input_label={
                    "SHEET_HEAD_NAME": "Name",
                    "SHEET_HEAD_FILE": "File",
                    "SHEET_HEAD_CATEGORY": "Category",
                    "SHEET_HEAD_TAGS": "Tags",
                    "SHEET_HEAD_DEPRECATED": "Deprecated",
                    "SHEET_HEAD_MASS": "Mass",
                    "SHEET_HEAD_COST": "Cost",
                    "SHEET_HEAD_WIDTH": "Width",
                    "SHEET_HEAD_DEPTH": "Depth",
                    "SHEET_HEAD_HEIGHT": "Height",
                    "SHEET_HEAD_SDESC": "Short Description",
                    "SHEET_HEAD_DESC": "Description",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "def_test_name", "", "", "$[name]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_s_desc", "", "", "$[s_desc]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_desc", "", "", "$[desc]"
                        ),
                    ]
                ),
                input_ctx={
                    "name": "Name",
                    "s_desc": "short_description",
                    "desc": "description",
                },
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            file="test.xml",
                            key="test",
                            name=sw_compdocs.language.Text(id="def_test_name"),
                            category=sw_compdocs.component.Category.BLOCKS,
                            mass=1.0,
                            value=2,
                            tags="tags",
                            tooltip_properties=sw_compdocs.component.TooltipProperties(
                                short_description=sw_compdocs.language.Text(
                                    id="def_test_s_desc"
                                ),
                                description=sw_compdocs.language.Text(
                                    id="def_test_desc"
                                ),
                            ),
                            voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                            voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                        )
                    )
                ],
                want_record_list=[
                    [
                        "Name",
                        "File",
                        "Category",
                        "Tags",
                        "Deprecated",
                        "Mass",
                        "Cost",
                        "Width",
                        "Depth",
                        "Height",
                        "Short Description",
                        "Description",
                    ],
                    [
                        "$[name]",
                        "test.xml",
                        "Blocks",
                        "tags",
                        "FALSE",
                        "1",
                        "2",
                        "3",
                        "7",
                        "5",
                        "short_description",
                        "description",
                    ],
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_record_list = sw_compdocs.generator.generate_sheet(
                    tc.input_comp_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    ctx=tc.input_ctx,
                )
                self.assertEqual(got_record_list, tc.want_record_list)

    def test_exc_label(self) -> None:
        label_all = {
            "SHEET_HEAD_NAME": "Name",
            "SHEET_HEAD_FILE": "File",
            "SHEET_HEAD_CATEGORY": "Category",
            "SHEET_HEAD_TAGS": "Tags",
            "SHEET_HEAD_DEPRECATED": "Deprecated",
            "SHEET_HEAD_MASS": "Mass",
            "SHEET_HEAD_COST": "Cost",
            "SHEET_HEAD_WIDTH": "Width",
            "SHEET_HEAD_DEPTH": "Depth",
            "SHEET_HEAD_HEIGHT": "Height",
            "SHEET_HEAD_SDESC": "Short Description",
            "SHEET_HEAD_DESC": "Description",
        }
        for key in label_all.keys():
            with self.subTest(label_key=key):
                label = label_all.copy()
                del label[key]
                with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
                    sw_compdocs.generator.generate_sheet([], label=label)
                self.assertEqual(ctx.exception.key, key)
