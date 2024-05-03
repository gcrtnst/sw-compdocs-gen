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
            # mass format
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(
                    file="file",
                    mass=0.5,
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
                                ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0.5"]
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
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(
                    file="file",
                    mass=0.25,
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
                                ["DOCUMENT_PROP_TABLE_MASS_LABEL", "0.25"]
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
            # file format
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(
                    file=None,
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
                                ["DOCUMENT_PROP_TABLE_FILE_LABEL", ""]
                            ),
                        ],
                    )
                ),
            ),
            tt(
                input_label=None,
                input_defn=sw_compdocs.component.Definition(
                    file=b"path/to/definition.xml",
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
                        sw_compdocs.document.TableDataRow(["Label", "Value"]),
                        [
                            sw_compdocs.document.TableDataRow(["Mass", "10"]),
                            sw_compdocs.document.TableDataRow(["Dimensions", "1x5x3"]),
                            sw_compdocs.document.TableDataRow(["Cost", "100"]),
                            sw_compdocs.document.TableDataRow(["Tags", "tags"]),
                            sw_compdocs.document.TableDataRow(["File", "file"]),
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
                ("input_key", str),
                ("input_lns", sw_compdocs.component.LogicNodeList),
                ("want_tbl", sw_compdocs.document.Table),
            ],
        )

        for tc in [
            tt(
                input_label={
                    "DOCUMENT_LOGIC_TABLE_HEAD_TYPE": "種別",
                    "DOCUMENT_LOGIC_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_HEAD_DESC": "説明",
                },
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList([]),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [],
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
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
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
                    key="test",
                ),
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
            tt(
                input_label=None,
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
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
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
                    key="test",
                ),
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
            tt(
                input_label={
                    "DOCUMENT_LOGIC_TABLE_HEAD_TYPE": "種別",
                    "DOCUMENT_LOGIC_TABLE_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_HEAD_DESC": "説明",
                },
                input_lang=None,
                input_ctx={
                    "label_0": "label_0_fmt",
                    "desc_0": "desc_0_fmt",
                    "label_1": "label_1_fmt",
                    "desc_1": "desc_1_fmt",
                },
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
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
                    key="test",
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["on/off", "label 0 label_0_fmt", "desc 0 desc_0_fmt"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["number", "label 1 label_1_fmt", "desc 1 desc_1_fmt"]
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
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
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
                    key="test",
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["オン/オフ", "ラベル 0 $[label_0]", "説明 0 $[desc_0]"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["数値", "ラベル 1 $[label_1]", "説明 1 $[desc_1]"]
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
                            "def_test_node_3_label",
                            "",
                            "label 0 $[label_0]",
                            "ラベル 0 $[label_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_3_desc",
                            "",
                            "desc 0 $[desc_0]",
                            "説明 0 $[desc_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_label",
                            "",
                            "label 1 $[label_1]",
                            "ラベル 1 $[label_1]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_desc",
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
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=3,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_3_label", en="label 0 $[label_0]"
                            ),
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_3_desc", en="desc 0 $[desc_0]"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=5,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_5_label", en="label 1 $[label_1]"
                            ),
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_5_desc", en="desc 1 $[desc_1]"
                            ),
                        ),
                    ],
                    key="test",
                ),
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
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_-1_label",
                            "",
                            "label -1",
                            "ラベル -1",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_-1_desc",
                            "",
                            "desc -1",
                            "説明 -1",
                        ),
                    ]
                ),
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=-1,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_-1_label"
                            ),
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_-1_desc"
                            ),
                        )
                    ],
                    key="test",
                ),
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
                                    "オン/オフ",
                                    "ラベル -1",
                                    "説明 -1",
                                ]
                            )
                        ],
                    )
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_tbl = sw_compdocs.generator.generate_document_logic_table(
                    tc.input_key,
                    tc.input_lns,
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
                        "key", lns, label=label
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
                ("input_key", str),
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
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(),
                want_doc=sw_compdocs.document.Document(),
            ),
            # logic node type
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(en="desc"),
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
                                        ["on/off", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description=sw_compdocs.language.Text(en="desc"),
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
                                        ["number", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description=sw_compdocs.language.Text(en="desc"),
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
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
                                        ["power", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.WATER,
                            description=sw_compdocs.language.Text(en="desc"),
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
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
                                        ["fluid", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                            description=sw_compdocs.language.Text(en="desc"),
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
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
                                        ["electric", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.COMPOSITE,
                            description=sw_compdocs.language.Text(en="desc"),
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
                                        ["composite", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.VIDEO,
                            description=sw_compdocs.language.Text(en="desc"),
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
                                        ["video", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.AUDIO,
                            description=sw_compdocs.language.Text(en="desc"),
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
                                        ["audio", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ROPE,
                            description=sw_compdocs.language.Text(en="desc"),
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
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
                                        ["rope", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # logic node mode
            tt(
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="label"),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(en="desc"),
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
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
                                        ["on/off", "label", "desc"]
                                    )
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
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "ラベル"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "説明"
                        ),
                    ]
                ),
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=0,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_0_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_0_desc", en="desc"
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
                                        ["オン/オフ", "ラベル", "説明"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic outputs", "ロジック出力"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "ラベル"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "説明"
                        ),
                    ]
                ),
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=0,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_0_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_0_desc", en="desc"
                            ),
                        ),
                    ],
                    key="test",
                ),
                want_doc=sw_compdocs.document.Document(
                    [
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
                                        ["オン/オフ", "ラベル", "説明"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation("", "", "connections", "接続"),
                        sw_compdocs.language.Translation("", "", "power", "動力"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "ラベル"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "説明"
                        ),
                    ]
                ),
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=0,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_0_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_0_desc", en="desc"
                            ),
                        ),
                    ],
                    key="test",
                ),
                want_doc=sw_compdocs.document.Document(
                    [
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
                                        ["動力", "ラベル", "説明"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # logic idx
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic inputs", "logic inputs"
                        ),
                        sw_compdocs.language.Translation(
                            "", "", "logic outputs", "logic outputs"
                        ),
                        sw_compdocs.language.Translation(
                            "", "", "connections", "connections"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "on/off"),
                        sw_compdocs.language.Translation("", "", "power", "power"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "label 0"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "desc 0"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_label", "", "", "label 1"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_desc", "", "", "desc 1"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_2_label", "", "", "label 2"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_2_desc", "", "", "desc 2"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_3_label", "", "", "label 3"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_3_desc", "", "", "desc 3"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_4_label", "", "", "label 4"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_4_desc", "", "", "desc 4"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_label", "", "", "label 5"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_desc", "", "", "desc 5"
                        ),
                    ]
                ),
                input_ctx=None,
                input_key="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=0,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_0_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_0_desc", en="desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=1,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_1_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_1_desc", en="desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=2,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_2_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_2_desc", en="desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=3,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_3_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_3_desc", en="desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=4,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_4_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_4_desc", en="desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="test",
                            idx=5,
                            label=sw_compdocs.language.Text(
                                id="def_test_node_5_label", en="label"
                            ),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_5_desc", en="desc"
                            ),
                        ),
                    ],
                    key="test",
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
                                        ["on/off", "label 0", "desc 0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label 3", "desc 3"]
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
                                        ["on/off", "label 1", "desc 1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label 4", "desc 4"]
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
                                        ["power", "label 2", "desc 2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["power", "label 5", "desc 5"]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_logic(
                    tc.input_key,
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
            tt(  # normal
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file="clock.xml",
                    key="clock",
                    name=sw_compdocs.language.Text(id="def_clock_name", en="Clock"),
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_clock_s_desc",
                            en="An analogue clock display that outputs a number value representing the time of day.",
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_clock_desc",
                            en="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                        ),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=0,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_0_label", en="Time"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_0_desc",
                                    en="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=1,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_1_label", en="Backlight"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_1_desc",
                                    en="Enables the backlight when receiving an on signal.",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=2,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_2_label", en="Electric"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_2_desc",
                                    en="Electrical power connection.",
                                ),
                            ),
                        ],
                        key="clock",
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Paragraph(
                            "An analogue clock display that outputs a number value representing the time of day."
                        ),
                        sw_compdocs.document.Paragraph(
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display."
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
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", "clock.xml"]
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
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
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
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
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
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # deprecated
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file="clock.xml",
                    key="clock",
                    name=sw_compdocs.language.Text(id="def_clock_name", en="Clock"),
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags.IS_DEPRECATED,
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_clock_s_desc",
                            en="An analogue clock display that outputs a number value representing the time of day.",
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_clock_desc",
                            en="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                        ),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=0,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_0_label", en="Time"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_0_desc",
                                    en="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=1,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_1_label", en="Backlight"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_1_desc",
                                    en="Enables the backlight when receiving an on signal.",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=2,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_2_label", en="Electric"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_2_desc",
                                    en="Electrical power connection.",
                                ),
                            ),
                        ],
                        key="clock",
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_DEPRECATED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Paragraph(
                            "An analogue clock display that outputs a number value representing the time of day."
                        ),
                        sw_compdocs.document.Paragraph(
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display."
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
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", "clock.xml"]
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
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
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
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
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
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # label, lang
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
                            "number",
                            "数値",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_name",
                            "",
                            "Clock",
                            "時計",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_desc",
                            "",
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                            "時計に表示されている青い矢印が12時の方向です.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_s_desc",
                            "",
                            "An analogue clock display that outputs a number value representing the time of day.",
                            "ゲーム内の時刻に対応した数値信号を出力するアナログ時計です.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_0_label",
                            "",
                            "Time",
                            "ゲーム内の時刻",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_0_desc",
                            "",
                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                            "ゲーム内の時刻に対応した数値を0 (0:00) から1 (24:00) の範囲で出力します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_1_label",
                            "",
                            "Backlight",
                            "バックライト",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_1_desc",
                            "",
                            "Enables the backlight when receiving an on signal.",
                            "オン信号を受け取るとバックライトが点灯します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_2_label",
                            "",
                            "Electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_2_desc",
                            "",
                            "Electrical power connection.",
                            "電力網から電力を供給します.",
                        ),
                    ]
                ),
                input_ctx={},
                input_defn=sw_compdocs.component.Definition(
                    file="clock.xml",
                    key="clock",
                    name=sw_compdocs.language.Text(id="def_clock_name", en="Clock"),
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags.IS_DEPRECATED,
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_clock_s_desc",
                            en="An analogue clock display that outputs a number value representing the time of day.",
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_clock_desc",
                            en="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                        ),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=0,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_0_label", en="Time"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_0_desc",
                                    en="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=1,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_1_label", en="Backlight"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_1_desc",
                                    en="Enables the backlight when receiving an on signal.",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=2,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_2_label", en="Electric"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_2_desc",
                                    en="Electrical power connection.",
                                ),
                            ),
                        ],
                        key="clock",
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("時計"),
                        sw_compdocs.document.Callout(
                            "この部品は非推奨です。",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Paragraph(
                            "ゲーム内の時刻に対応した数値信号を出力するアナログ時計です."
                        ),
                        sw_compdocs.document.Paragraph(
                            "時計に表示されている青い矢印が12時の方向です."
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
                                    sw_compdocs.document.TableDataRow(["値段", "100"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["タグ", "basic"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["ファイル", "clock.xml"]
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
                                            "バックライト",
                                            "オン信号を受け取るとバックライトが点灯します.",
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
                                            "数値",
                                            "ゲーム内の時刻",
                                            "ゲーム内の時刻に対応した数値を0 (0:00) から1 (24:00) の範囲で出力します.",
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
            tt(  # label, lang, template
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
            tt(  # label, lang, template
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
                            "PROPERTIES",
                            "プロパティ",
                        ),
                        sw_compdocs.language.Translation(
                            "def_handle_name",
                            "",
                            "Handle",
                            "取っ手",
                        ),
                        sw_compdocs.language.Translation(
                            "def_handle_desc",
                            "",
                            "Interacting with [$[action_interact_left]] or [$[action_interact_right]] again will detach that hand. The handle can be used to drag vehicles around. If a vehicle is too heavy to move, you will be detached automatically when you move outside the handle's interaction range.",
                            "取っ手を掴んでいる時に [$[action_interact_left]]/[$[action_interact_right]] を押すと離すことができます. 軽い乗り物は取っ手を掴んでそのまま動かすことができます. プレイヤーが取っ手の範囲外まで移動した場合は自動的に手を離します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_handle_s_desc",
                            "",
                            "A handle that you can attach to by interacting with [$[action_interact_left]] or [$[action_interact_right]].",
                            "[$[action_interact_left]] や [$[action_interact_right]] を押して掴むことができる取っ手です.",
                        ),
                    ]
                ),
                input_ctx={"action_interact_left": "q", "action_interact_right": "e"},
                input_defn=sw_compdocs.component.Definition(
                    file="handle.xml",
                    key="handle",
                    name=sw_compdocs.language.Text(id="def_handle_name", en="Handle"),
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=5,
                    flags=sw_compdocs.component.Flags(0),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_handle_s_desc",
                            en="Interacting with [$[action_interact_left]] or [$[action_interact_right]] again will detach that hand. The handle can be used to drag vehicles around. If a vehicle is too heavy to move, you will be detached automatically when you move outside the handle's interaction range.",
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_handle_desc",
                            en="A handle that you can attach to by interacting with [$[action_interact_left]] or [$[action_interact_right]].",
                        ),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("取っ手"),
                        sw_compdocs.document.Paragraph(
                            "[q] や [e] を押して掴むことができる取っ手です."
                        ),
                        sw_compdocs.document.Paragraph(
                            "取っ手を掴んでいる時に [q]/[e] を押すと離すことができます. 軽い乗り物は取っ手を掴んでそのまま動かすことができます. プレイヤーが取っ手の範囲外まで移動した場合は自動的に手を離します."
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
                                    sw_compdocs.document.TableDataRow(["値段", "5"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["タグ", "basic"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["ファイル", "handle.xml"]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # omit short_description
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file="clock.xml",
                    key="clock",
                    name=sw_compdocs.language.Text(id="def_clock_name", en="Clock"),
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_clock_s_desc", en=""
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_clock_desc",
                            en="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                        ),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=0,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_0_label", en="Time"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_0_desc",
                                    en="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=1,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_1_label", en="Backlight"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_1_desc",
                                    en="Enables the backlight when receiving an on signal.",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=2,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_2_label", en="Electric"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_2_desc",
                                    en="Electrical power connection.",
                                ),
                            ),
                        ],
                        key="clock",
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Paragraph(
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display."
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
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", "clock.xml"]
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
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
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
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
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
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # omit description
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file="clock.xml",
                    key="clock",
                    name=sw_compdocs.language.Text(id="def_clock_name", en="Clock"),
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_clock_s_desc",
                            en="An analogue clock display that outputs a number value representing the time of day.",
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_clock_desc", en=""
                        ),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=0,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_0_label", en="Time"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_0_desc",
                                    en="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=1,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_1_label", en="Backlight"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_1_desc",
                                    en="Enables the backlight when receiving an on signal.",
                                ),
                            ),
                            sw_compdocs.component.LogicNode(
                                key="clock",
                                idx=2,
                                label=sw_compdocs.language.Text(
                                    id="def_clock_node_2_label", en="Electric"
                                ),
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description=sw_compdocs.language.Text(
                                    id="def_clock_node_2_desc",
                                    en="Electrical power connection.",
                                ),
                            ),
                        ],
                        key="clock",
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Paragraph(
                            "An analogue clock display that outputs a number value representing the time of day."
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
                                        ["DOCUMENT_PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["DOCUMENT_PROP_TABLE_FILE_LABEL", "clock.xml"]
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
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
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
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
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
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
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
                ("input_defn_list", list[sw_compdocs.component.Definition]),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_defn_list=[],
                input_label=None,
                input_lang=None,
                input_ctx=None,
                want_doc=sw_compdocs.document.Document(),
            ),
            # single
            tt(
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Blocks_1"),
                        category=sw_compdocs.component.Category.BLOCKS,
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
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        key="blocks_1",
                        name=sw_compdocs.language.Text(en="Blocks_3"),
                        value=1,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        key="blocks_2",
                        name=sw_compdocs.language.Text(en="Blocks_2"),
                        value=2,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        key="blocks_3",
                        name=sw_compdocs.language.Text(en="Blocks_1"),
                        value=3,
                        category=sw_compdocs.component.Category.BLOCKS,
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
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        key="blocks_3",
                        name=sw_compdocs.language.Text(en="Blocks_1"),
                        value=3,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        key="blocks_2",
                        name=sw_compdocs.language.Text(en="Blocks_1"),
                        value=2,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        key="blocks_1",
                        name=sw_compdocs.language.Text(en="Blocks_1"),
                        value=1,
                        category=sw_compdocs.component.Category.BLOCKS,
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
                    ],
                ),
            ),
            # sort category
            tt(
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="WINDOWS_0"),
                        category=sw_compdocs.component.Category.WINDOWS,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="INDUSTRY_0"),
                        category=sw_compdocs.component.Category.INDUSTRY,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="MODULAR_ENGINES_0"),
                        category=sw_compdocs.component.Category.MODULAR_ENGINES,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="WEAPONS_0"),
                        category=sw_compdocs.component.Category.WEAPONS,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="JET_ENGINES_0"),
                        category=sw_compdocs.component.Category.JET_ENGINES,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="ELECTRIC_0"),
                        category=sw_compdocs.component.Category.ELECTRIC,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="FLUID_0"),
                        category=sw_compdocs.component.Category.FLUID,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="DECORATIVE_0"),
                        category=sw_compdocs.component.Category.DECORATIVE,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="SENSORS_0"),
                        category=sw_compdocs.component.Category.SENSORS,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="DISPLAYS_0"),
                        category=sw_compdocs.component.Category.DISPLAYS,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="LOGIC_0"),
                        category=sw_compdocs.component.Category.LOGIC,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="SPECIALIST_EQUIPMENT_0"),
                        category=sw_compdocs.component.Category.SPECIALIST_EQUIPMENT,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="PROPULSION_0"),
                        category=sw_compdocs.component.Category.PROPULSION,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="MECHANICS_0"),
                        category=sw_compdocs.component.Category.MECHANICS,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="VEHICLE_CONTROL_0"),
                        category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="BLOCKS_0"),
                        category=sw_compdocs.component.Category.BLOCKS,
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
                    tc.input_defn_list,
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
                ("input_defn", sw_compdocs.component.Definition),
                ("want_record", list[str]),
            ],
        )

        for tc in [
            tt(  # normal
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file="test.xml",
                    name=sw_compdocs.language.Text(en="Name"),
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
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
                ),
                want_record=[
                    "Name",
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
            ),
            tt(  # file none
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    name=sw_compdocs.language.Text(en="Name"),
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
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
                ),
                want_record=[
                    "Name",
                    "",
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
            ),
            tt(  # file
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file=b"path/to/test.xml",
                    name=sw_compdocs.language.Text(en="Name"),
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
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
                ),
                want_record=[
                    "Name",
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
            ),
            tt(  # deprecated
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file="test.xml",
                    name=sw_compdocs.language.Text(en="Name"),
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags.IS_DEPRECATED,
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            en="short_description"
                        ),
                        description=sw_compdocs.language.Text(en="description"),
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                    voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                ),
                want_record=[
                    "Name",
                    "test.xml",
                    "Blocks",
                    "tags",
                    "TRUE",
                    "1",
                    "2",
                    "3",
                    "7",
                    "5",
                    "short_description",
                    "description",
                ],
            ),
            tt(  # mass
                input_lang=None,
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
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
            tt(  # lang
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "def_test_name", "", "", "名前"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_s_desc", "", "", "短い説明"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_desc", "", "", "説明"
                        ),
                    ]
                ),
                input_ctx=None,
                input_defn=sw_compdocs.component.Definition(
                    file="test.xml",
                    key="test",
                    name=sw_compdocs.language.Text(id="def_test_name", en="Name"),
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(
                            id="def_test_s_desc", en="short_description"
                        ),
                        description=sw_compdocs.language.Text(
                            id="def_test_desc", en="description"
                        ),
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                    voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                ),
                want_record=[
                    "名前",
                    "test.xml",
                    "Blocks",
                    "tags",
                    "FALSE",
                    "1",
                    "2",
                    "3",
                    "7",
                    "5",
                    "短い説明",
                    "説明",
                ],
            ),
            tt(  # template
                input_lang=None,
                input_ctx={
                    "name": "Name",
                    "s_desc": "short_description",
                    "desc": "description",
                },
                input_defn=sw_compdocs.component.Definition(
                    file="test.xml",
                    name=sw_compdocs.language.Text(en="$[name]"),
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description=sw_compdocs.language.Text(en="$[s_desc]"),
                        description=sw_compdocs.language.Text(en="$[desc]"),
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                    voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                ),
                want_record=[
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
                input_defn=sw_compdocs.component.Definition(
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
                        description=sw_compdocs.language.Text(id="def_test_desc"),
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                    voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                ),
                want_record=[
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
            ),
        ]:
            with self.subTest(tc=tc):
                got_record = sw_compdocs.generator.generate_sheet_component(
                    tc.input_defn, lang=tc.input_lang, ctx=tc.input_ctx
                )
                self.assertEqual(got_record, tc.want_record)


class TestGenerateSheetComponentList(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_defn_list", list[sw_compdocs.component.Definition]),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_ctx", collections.abc.Mapping[str, str] | None),
                ("want_record_list", list[list[str]]),
            ],
        )

        for tc in [
            tt(
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 1")
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 2")
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 3")
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
                input_defn_list=[
                    sw_compdocs.component.Definition(
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
                            description=sw_compdocs.language.Text(id="def_test_desc"),
                        ),
                        voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                        voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
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
                    tc.input_defn_list, lang=tc.input_lang, ctx=tc.input_ctx
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
                ("input_defn_list", list[sw_compdocs.component.Definition]),
                ("want_record_list", list[list[str]]),
            ],
        )

        for tc in [
            tt(  # normal
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 1")
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 2")
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 3")
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
            tt(  # sort
                input_label=None,
                input_lang=None,
                input_ctx=None,
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        key="a",
                        name=sw_compdocs.language.Text(en="Z"),
                        category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        value=1,
                    ),
                    sw_compdocs.component.Definition(
                        key="z",
                        name=sw_compdocs.language.Text(en="A"),
                        category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        value=2,
                    ),
                    sw_compdocs.component.Definition(
                        key="a",
                        name=sw_compdocs.language.Text(en="A"),
                        category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        value=3,
                    ),
                    sw_compdocs.component.Definition(
                        key="z",
                        name=sw_compdocs.language.Text(en="Z"),
                        category=sw_compdocs.component.Category.BLOCKS,
                        value=4,
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
            tt(  # label
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
                input_lang=None,
                input_ctx=None,
                input_defn_list=[
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 1")
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 2")
                    ),
                    sw_compdocs.component.Definition(
                        name=sw_compdocs.language.Text(en="Test 3")
                    ),
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
                input_label=None,
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
                input_defn_list=[
                    sw_compdocs.component.Definition(
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
                            description=sw_compdocs.language.Text(id="def_test_desc"),
                        ),
                        voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                        voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                    )
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
                    tc.input_defn_list,
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
