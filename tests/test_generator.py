import collections.abc
import sw_compdocs.component
import sw_compdocs.document
import sw_compdocs.generator
import sw_compdocs.language
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
                ("input_repl", str | None),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_label=None,
                input_key="LABEL",
                input_repl=None,
                want_s="LABEL",
            ),
            tt(
                input_label={"LABEL": "text {}"},
                input_key="LABEL",
                input_repl=None,
                want_s="text {}",
            ),
            tt(
                input_label=None,
                input_key="{}",
                input_repl="repl",
                want_s="{}",
            ),
            tt(
                input_label={"LABEL": "text {}"},
                input_key="LABEL",
                input_repl="repl",
                want_s="text repl",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.generator._label_get(
                    tc.input_label, tc.input_key, tc.input_repl
                )
                self.assertEqual(got_s, tc.want_s)

    def test_exc_label(self) -> None:
        with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
            sw_compdocs.generator._label_get({}, "LABEL")
        self.assertEqual(ctx.exception.key, "LABEL")

    def test_exc_placeholder(self) -> None:
        with self.assertRaises(
            sw_compdocs.generator.LabelMissingPlaceholderError
        ) as ctx:
            sw_compdocs.generator._label_get({"LABEL": "text"}, "LABEL", "repl")
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


class TestBindFormat(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("input_s", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_bind=None,
                input_s="$[var]",
                want_s="$[var]",
            ),
            tt(
                input_bind={"var": "text"},
                input_s="$[var]",
                want_s="text",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = sw_compdocs.generator._bind_format(tc.input_bind, tc.input_s)
                self.assertEqual(got_s, tc.want_s)


class TestClassifyLogic(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lns", sw_compdocs.component.LogicNodeList),
                (
                    "want_ret",
                    tuple[
                        list[sw_compdocs.component.LogicNode],
                        list[sw_compdocs.component.LogicNode],
                        list[sw_compdocs.component.LogicNode],
                    ],
                ),
            ],
        )

        for tc in [
            # empty
            tt(
                input_lns=sw_compdocs.component.LogicNodeList(),
                want_ret=([], [], []),
            ),
            # logic node mode type
            tt(
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
                want_ret=(
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
                    ],
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="OUTPUT"),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                        ),
                    ],
                    [
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
                            label=sw_compdocs.language.Text(en="ROPE"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ROPE,
                        ),
                    ],
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_ret = sw_compdocs.generator._classify_logic(tc.input_lns)
                self.assertEqual(got_ret, tc.want_ret)


class TestGenerateDocumentPropertyList(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp", sw_compdocs.component.Component),
                ("input_label", dict[str, str] | None),
                ("want_ul", sw_compdocs.document.UnorderedList),
            ],
        )

        for tc in [
            # normal
            tt(
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        file="file",
                        mass=10.0,
                        value=100,
                        tags="tags",
                        voxels=sw_compdocs.component.VoxelList(
                            [
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=-1, z=-2
                                    )
                                ),
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=1, z=2
                                    )
                                ),
                            ]
                        ),
                    )
                ),
                input_label={
                    "DOCUMENT_PROP_MASS": "Mass: {}",
                    "DOCUMENT_PROP_MASS_PARENT": "Parent Mass: {}",
                    "DOCUMENT_PROP_MASS_CHILD": "Child Mass: {}",
                    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_PARENT": "Parent Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_CHILD": "Child Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "Cost: ${}",
                    "DOCUMENT_PROP_TAGS": "Tags: {}",
                    "DOCUMENT_PROP_FILE": "File: {}",
                    "DOCUMENT_PROP_FILE_PARENT": "Parent File: {}",
                    "DOCUMENT_PROP_FILE_CHILD": "Child File: {}",
                },
                want_ul=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem("Mass: 10"),
                        sw_compdocs.document.ListItem("Dimensions (WxDxH): 1x5x3"),
                        sw_compdocs.document.ListItem("Cost: $100"),
                        sw_compdocs.document.ListItem("Tags: tags"),
                        sw_compdocs.document.ListItem("File: file"),
                    ]
                ),
            ),
            # multibody
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        file="multibody_a.xml",
                        mass=9.0,
                        value=100,
                        tags="parent",
                        voxels=sw_compdocs.component.VoxelList(
                            [
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=-1, z=-2
                                    )
                                ),
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=1, z=2
                                    )
                                ),
                            ]
                        ),
                        voxel_location_child=sw_compdocs.component.VoxelPos(
                            x=-5, y=0, z=0
                        ),
                    ),
                    child=sw_compdocs.component.Definition(
                        file="multibody_b.xml",
                        mass=1.0,
                        value=200,
                        tags="child",
                        voxels=sw_compdocs.component.VoxelList(
                            [
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=-3, z=-4
                                    )
                                ),
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=3, z=4
                                    )
                                ),
                            ]
                        ),
                    ),
                ),
                input_label={
                    "DOCUMENT_PROP_MASS": "Mass: {}",
                    "DOCUMENT_PROP_MASS_PARENT": "Parent Mass: {}",
                    "DOCUMENT_PROP_MASS_CHILD": "Child Mass: {}",
                    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_PARENT": "Parent Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_CHILD": "Child Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "Cost: ${}",
                    "DOCUMENT_PROP_TAGS": "Tags: {}",
                    "DOCUMENT_PROP_FILE": "File: {}",
                    "DOCUMENT_PROP_FILE_PARENT": "Parent File: {}",
                    "DOCUMENT_PROP_FILE_CHILD": "Child File: {}",
                },
                want_ul=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem(
                            "Mass: 10",
                            [
                                sw_compdocs.document.ListItem("Parent Mass: 9"),
                                sw_compdocs.document.ListItem("Child Mass: 1"),
                            ],
                        ),
                        sw_compdocs.document.ListItem(
                            "Dimensions (WxDxH): 6x9x7",
                            [
                                sw_compdocs.document.ListItem(
                                    "Parent Dimensions (WxDxH): 1x5x3"
                                ),
                                sw_compdocs.document.ListItem(
                                    "Child Dimensions (WxDxH): 1x9x7"
                                ),
                            ],
                        ),
                        sw_compdocs.document.ListItem("Cost: $100"),
                        sw_compdocs.document.ListItem("Tags: parent"),
                        sw_compdocs.document.ListItem("Parent File: multibody_a.xml"),
                        sw_compdocs.document.ListItem("Child File: multibody_b.xml"),
                    ]
                ),
            ),
            # mass format
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(mass=0.25),
                    child=sw_compdocs.component.Definition(mass=1.25),
                ),
                input_label={
                    "DOCUMENT_PROP_MASS": "Mass: {}",
                    "DOCUMENT_PROP_MASS_PARENT": "Parent Mass: {}",
                    "DOCUMENT_PROP_MASS_CHILD": "Child Mass: {}",
                    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_PARENT": "Parent Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_CHILD": "Child Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "Cost: ${}",
                    "DOCUMENT_PROP_TAGS": "Tags: {}",
                    "DOCUMENT_PROP_FILE": "File: {}",
                    "DOCUMENT_PROP_FILE_PARENT": "Parent File: {}",
                    "DOCUMENT_PROP_FILE_CHILD": "Child File: {}",
                },
                want_ul=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem(
                            "Mass: 1.5",
                            [
                                sw_compdocs.document.ListItem("Parent Mass: 0.25"),
                                sw_compdocs.document.ListItem("Child Mass: 1.25"),
                            ],
                        ),
                        sw_compdocs.document.ListItem(
                            "Dimensions (WxDxH): 1x1x1",
                            [
                                sw_compdocs.document.ListItem(
                                    "Parent Dimensions (WxDxH): 1x1x1"
                                ),
                                sw_compdocs.document.ListItem(
                                    "Child Dimensions (WxDxH): 1x1x1"
                                ),
                            ],
                        ),
                        sw_compdocs.document.ListItem("Cost: $0"),
                        sw_compdocs.document.ListItem("Tags: "),
                        sw_compdocs.document.ListItem("Parent File: "),
                        sw_compdocs.document.ListItem("Child File: "),
                    ]
                ),
            ),
            # file format normal
            tt(
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        file=b"path/to/definition.xml"
                    )
                ),
                input_label={
                    "DOCUMENT_PROP_MASS": "Mass: {}",
                    "DOCUMENT_PROP_MASS_PARENT": "Parent Mass: {}",
                    "DOCUMENT_PROP_MASS_CHILD": "Child Mass: {}",
                    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_PARENT": "Parent Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_CHILD": "Child Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "Cost: ${}",
                    "DOCUMENT_PROP_TAGS": "Tags: {}",
                    "DOCUMENT_PROP_FILE": "File: {}",
                    "DOCUMENT_PROP_FILE_PARENT": "Parent File: {}",
                    "DOCUMENT_PROP_FILE_CHILD": "Child File: {}",
                },
                want_ul=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem("Mass: 0"),
                        sw_compdocs.document.ListItem("Dimensions (WxDxH): 1x1x1"),
                        sw_compdocs.document.ListItem("Cost: $0"),
                        sw_compdocs.document.ListItem("Tags: "),
                        sw_compdocs.document.ListItem("File: definition.xml"),
                    ]
                ),
            ),
            # file format multibody
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        file=b"path/to/multibody_a.xml"
                    ),
                    child=sw_compdocs.component.Definition(
                        file=b"path/to/multibody_b.xml"
                    ),
                ),
                input_label={
                    "DOCUMENT_PROP_MASS": "Mass: {}",
                    "DOCUMENT_PROP_MASS_PARENT": "Parent Mass: {}",
                    "DOCUMENT_PROP_MASS_CHILD": "Child Mass: {}",
                    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_PARENT": "Parent Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_DIMS_CHILD": "Child Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "Cost: ${}",
                    "DOCUMENT_PROP_TAGS": "Tags: {}",
                    "DOCUMENT_PROP_FILE": "File: {}",
                    "DOCUMENT_PROP_FILE_PARENT": "Parent File: {}",
                    "DOCUMENT_PROP_FILE_CHILD": "Child File: {}",
                },
                want_ul=sw_compdocs.document.UnorderedList(
                    [
                        sw_compdocs.document.ListItem(
                            "Mass: 0",
                            [
                                sw_compdocs.document.ListItem("Parent Mass: 0"),
                                sw_compdocs.document.ListItem("Child Mass: 0"),
                            ],
                        ),
                        sw_compdocs.document.ListItem(
                            "Dimensions (WxDxH): 1x1x1",
                            [
                                sw_compdocs.document.ListItem(
                                    "Parent Dimensions (WxDxH): 1x1x1"
                                ),
                                sw_compdocs.document.ListItem(
                                    "Child Dimensions (WxDxH): 1x1x1"
                                ),
                            ],
                        ),
                        sw_compdocs.document.ListItem("Cost: $0"),
                        sw_compdocs.document.ListItem("Tags: "),
                        sw_compdocs.document.ListItem("Parent File: multibody_a.xml"),
                        sw_compdocs.document.ListItem("Child File: multibody_b.xml"),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_ul = sw_compdocs.generator.generate_document_property_list(
                    tc.input_comp, label=tc.input_label
                )
                self.assertEqual(got_ul, tc.want_ul)


class TestGenerateDocumentLogicTableNormal(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("input_ln_list", list[sw_compdocs.component.LogicNode]),
                ("want_tbl", sw_compdocs.document.Table),
            ],
        )

        for tc in [
            # empty
            tt(
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_ln_list=[],
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
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
                input_bind=None,
                input_ln_list=[
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(
                            id="def_test_node_0_label", en="label 0 $[label_0]"
                        ),
                        type=sw_compdocs.component.LogicNodeType.BOOL,
                        description=sw_compdocs.language.Text(
                            id="def_test_node_0_desc", en="desc 0 $[desc_0]"
                        ),
                    ),
                    sw_compdocs.component.LogicNode(
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
                                "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
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
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE": "種別",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC": "説明",
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
                input_bind={
                    "label_0": "label_0_fmt",
                    "desc_0": "desc_0_fmt",
                    "label_1": "label_1_fmt",
                    "desc_1": "desc_1_fmt",
                },
                input_ln_list=[
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(
                            id="def_test_node_0_label", en="label 0 $[label_0]"
                        ),
                        type=sw_compdocs.component.LogicNodeType.BOOL,
                        description=sw_compdocs.language.Text(
                            id="def_test_node_0_desc", en="desc 0 $[desc_0]"
                        ),
                    ),
                    sw_compdocs.component.LogicNode(
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
                got_tbl = sw_compdocs.generator.generate_document_logic_table_normal(
                    tc.input_ln_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_tbl, tc.want_tbl)

    def test_exc_label(self) -> None:
        lns = sw_compdocs.component.LogicNodeList()
        label_all = {
            "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE": "種別",
            "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL": "ラベル",
            "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC": "説明",
        }
        for key in label_all.keys():
            with self.subTest(label_key=key):
                label = label_all.copy()
                del label[key]
                with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
                    sw_compdocs.generator.generate_document_logic_table_normal(
                        lns, label=label
                    )
                self.assertEqual(ctx.exception.key, key)


class TestGenerateDocumentLogicNormal(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("input_lns", sw_compdocs.component.LogicNodeList),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_lns=sw_compdocs.component.LogicNodeList(),
                want_doc=sw_compdocs.document.Document(),
            ),
            # logic node mode type
            tt(
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="INPUT"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="OUTPUT"),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(en="CONNECTION"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
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
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "INPUT", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
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
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["power", "CONNECTION", ""]
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
                input_bind=None,
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(id="def_test_node_0_label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_0_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(id="def_test_node_1_label"),
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_1_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            label=sw_compdocs.language.Text(id="def_test_node_2_label"),
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description=sw_compdocs.language.Text(
                                id="def_test_node_2_desc"
                            ),
                        ),
                    ],
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック入力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
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
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
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
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
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
                got_doc = sw_compdocs.generator.generate_document_logic_normal(
                    tc.input_lns,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_doc, tc.want_doc)


class TestGenerateDocumentLogicTableMultibody(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_parent_ln_list", list[sw_compdocs.component.LogicNode]),
                ("input_child_ln_list", list[sw_compdocs.component.LogicNode]),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("want_tbl", sw_compdocs.document.Table),
            ],
        )

        for tc in [
            # empty
            tt(
                input_parent_ln_list=[],
                input_child_ln_list=[],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY",
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE",
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL",
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC",
                            ]
                        ),
                    ),
                ),
            ),
            # normal
            tt(
                input_parent_ln_list=[
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(en="Parent Label 0"),
                        type=sw_compdocs.component.LogicNodeType.BOOL,
                        description=sw_compdocs.language.Text(
                            en="Parent Description 0"
                        ),
                    ),
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(en="Parent Label 1"),
                        type=sw_compdocs.component.LogicNodeType.FLOAT,
                        description=sw_compdocs.language.Text(
                            en="Parent Description 1"
                        ),
                    ),
                ],
                input_child_ln_list=[
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(en="Child Label 0"),
                        type=sw_compdocs.component.LogicNodeType.VIDEO,
                        description=sw_compdocs.language.Text(en="Child Description 0"),
                    ),
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(en="Child Label 1"),
                        type=sw_compdocs.component.LogicNodeType.AUDIO,
                        description=sw_compdocs.language.Text(en="Child Description 1"),
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY",
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE",
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL",
                                "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                [
                                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT",
                                    "on/off",
                                    "Parent Label 0",
                                    "Parent Description 0",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                [
                                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT",
                                    "number",
                                    "Parent Label 1",
                                    "Parent Description 1",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                [
                                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD",
                                    "video",
                                    "Child Label 0",
                                    "Child Description 0",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                [
                                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD",
                                    "audio",
                                    "Child Label 1",
                                    "Child Description 1",
                                ]
                            ),
                        ],
                    ),
                ),
            ),
            # full
            tt(
                input_parent_ln_list=[
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(
                            id="def_multibody_a_node_0_label"
                        ),
                        type=sw_compdocs.component.LogicNodeType.BOOL,
                        description=sw_compdocs.language.Text(
                            id="def_multibody_a_node_0_desc"
                        ),
                    ),
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(
                            id="def_multibody_a_node_1_label"
                        ),
                        type=sw_compdocs.component.LogicNodeType.FLOAT,
                        description=sw_compdocs.language.Text(
                            id="def_multibody_a_node_1_desc"
                        ),
                    ),
                ],
                input_child_ln_list=[
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(
                            id="def_multibody_b_node_0_label"
                        ),
                        type=sw_compdocs.component.LogicNodeType.VIDEO,
                        description=sw_compdocs.language.Text(
                            id="def_multibody_b_node_0_desc"
                        ),
                    ),
                    sw_compdocs.component.LogicNode(
                        label=sw_compdocs.language.Text(
                            id="def_multibody_b_node_1_label"
                        ),
                        type=sw_compdocs.component.LogicNodeType.AUDIO,
                        description=sw_compdocs.language.Text(
                            id="def_multibody_b_node_1_desc"
                        ),
                    ),
                ],
                input_label={
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "親/子",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "種別",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "説明",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "親",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "子",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation("", "", "number", "数値"),
                        sw_compdocs.language.Translation("", "", "video", "映像"),
                        sw_compdocs.language.Translation("", "", "audio", "音声"),
                        sw_compdocs.language.Translation(
                            "def_multibody_a_node_0_label", "", "", "$[parent_label_0]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_multibody_a_node_0_desc", "", "", "$[parent_desc_0]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_multibody_a_node_1_label", "", "", "$[parent_label_1]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_multibody_a_node_1_desc", "", "", "$[parent_desc_1]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_multibody_b_node_0_label", "", "", "$[child_label_0]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_multibody_b_node_0_desc", "", "", "$[child_desc_0]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_multibody_b_node_1_label", "", "", "$[child_label_1]"
                        ),
                        sw_compdocs.language.Translation(
                            "def_multibody_b_node_1_desc", "", "", "$[child_desc_1]"
                        ),
                    ]
                ),
                input_bind={
                    "parent_label_0": "親部品/ロジック0/ラベル",
                    "parent_desc_0": "親部品/ロジック0/説明",
                    "parent_label_1": "親部品/ロジック1/ラベル",
                    "parent_desc_1": "親部品/ロジック1/説明",
                    "child_label_0": "子部品/ロジック0/ラベル",
                    "child_desc_0": "子部品/ロジック0/説明",
                    "child_label_1": "子部品/ロジック1/ラベル",
                    "child_desc_1": "子部品/ロジック1/説明",
                },
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "親/子",
                                "種別",
                                "ラベル",
                                "説明",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                [
                                    "親",
                                    "オン/オフ",
                                    "親部品/ロジック0/ラベル",
                                    "親部品/ロジック0/説明",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                [
                                    "親",
                                    "数値",
                                    "親部品/ロジック1/ラベル",
                                    "親部品/ロジック1/説明",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                [
                                    "子",
                                    "映像",
                                    "子部品/ロジック0/ラベル",
                                    "子部品/ロジック0/説明",
                                ]
                            ),
                            sw_compdocs.document.TableDataRow(
                                [
                                    "子",
                                    "音声",
                                    "子部品/ロジック1/ラベル",
                                    "子部品/ロジック1/説明",
                                ]
                            ),
                        ],
                    ),
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_tbl = sw_compdocs.generator.generate_document_logic_table_multibody(
                    tc.input_parent_ln_list,
                    tc.input_child_ln_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_tbl, tc.want_tbl)


class TestGenerateDocumentLogicMultibody(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_parent_lns", sw_compdocs.component.LogicNodeList),
                ("input_child_lns", sw_compdocs.component.LogicNodeList),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_parent_lns=sw_compdocs.component.LogicNodeList(),
                input_child_lns=sw_compdocs.component.LogicNodeList(),
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc=sw_compdocs.document.Document(),
            ),
            # parent in
            tt(
                input_parent_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                        )
                    ]
                ),
                input_child_lns=sw_compdocs.component.LogicNodeList(),
                input_label={
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "親/子",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "説明",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "親",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "子",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic inputs", "ロジック入力"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation("", "", "", ""),
                    ]
                ),
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック入力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["親/子", "型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["親", "オン/オフ", "", ""]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # parent out
            tt(
                input_parent_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                        )
                    ]
                ),
                input_child_lns=sw_compdocs.component.LogicNodeList(),
                input_label={
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "親/子",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "説明",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "親",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "子",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic outputs", "ロジック出力"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation("", "", "", ""),
                    ]
                ),
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック出力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["親/子", "型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["親", "オン/オフ", "", ""]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # parent conn
            tt(
                input_parent_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                        )
                    ]
                ),
                input_child_lns=sw_compdocs.component.LogicNodeList(),
                input_label={
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "親/子",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "説明",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "親",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "子",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation("", "", "connections", "接続"),
                        sw_compdocs.language.Translation("", "", "power", "動力"),
                        sw_compdocs.language.Translation("", "", "", ""),
                    ]
                ),
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("接続"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["親/子", "型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["親", "動力", "", ""]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # child in
            tt(
                input_parent_lns=sw_compdocs.component.LogicNodeList(),
                input_child_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                        )
                    ]
                ),
                input_label={
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "親/子",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "説明",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "親",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "子",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic inputs", "ロジック入力"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation("", "", "", ""),
                    ]
                ),
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック入力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["親/子", "型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["子", "オン/オフ", "", ""]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # child out
            tt(
                input_parent_lns=sw_compdocs.component.LogicNodeList(),
                input_child_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                        )
                    ]
                ),
                input_label={
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "親/子",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "説明",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "親",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "子",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic outputs", "ロジック出力"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation("", "", "", ""),
                    ]
                ),
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック出力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["親/子", "型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["子", "オン/オフ", "", ""]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # parent conn
            tt(
                input_parent_lns=sw_compdocs.component.LogicNodeList(),
                input_child_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                        )
                    ]
                ),
                input_label={
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "親/子",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "説明",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "親",
                    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "子",
                },
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation("", "", "connections", "接続"),
                        sw_compdocs.language.Translation("", "", "power", "動力"),
                        sw_compdocs.language.Translation("", "", "", ""),
                    ]
                ),
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("接続"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["親/子", "型", "ラベル", "説明"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["子", "動力", "", ""]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_logic_multibody(
                    tc.input_parent_lns,
                    tc.input_child_lns,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_doc, tc.want_doc)


class TestGenerateDocumentComponent(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("input_comp", sw_compdocs.component.Component),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition()
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading(""),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                    ]
                ),
            ),
            # deprecated, orphan
            tt(
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        flags=sw_compdocs.component.Flags.IS_DEPRECATED
                        | sw_compdocs.component.Flags.MULTIBODY_CHILD
                    )
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading(" (Deprecated)"),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_DEPRECATED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_ORPHANED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                    ]
                ),
            ),
            # text
            tt(
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
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
                    )
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Name"),
                        sw_compdocs.document.Paragraph("Short Description"),
                        sw_compdocs.document.Paragraph("Description"),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("logic inputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC",
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
            # label, lang, keybindings
            tt(
                input_label={
                    "DOCUMENT_DEPRECATED_TEXT": "この部品は非推奨です。",
                    "DOCUMENT_ORPHANED_TEXT": "この部品は孤児です。親部品が見当たりません。",
                    "DOCUMENT_PROP_MASS": "重量: {}",
                    "DOCUMENT_PROP_DIMS": "サイズ (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "値段: ${}",
                    "DOCUMENT_PROP_TAGS": "タグ: {}",
                    "DOCUMENT_PROP_FILE": "ファイル: {}",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC": "説明",
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
                input_bind={
                    "def_dummy_desc_placeholder": "説明",
                    "def_dummy_s_desc_placeholder": "短い説明",
                    "def_dummy_node_0_label_placeholder": "ノードラベル",
                    "def_dummy_node_0_desc_placeholder": "ノード説明",
                },
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        key="dummy",
                        name=sw_compdocs.language.Text(id="def_dummy_name"),
                        flags=sw_compdocs.component.Flags.IS_DEPRECATED
                        | sw_compdocs.component.Flags.MULTIBODY_CHILD,
                        tooltip_properties=sw_compdocs.component.TooltipProperties(
                            short_description=sw_compdocs.language.Text(
                                id="def_dummy_s_desc"
                            ),
                            description=sw_compdocs.language.Text(id="def_dummy_desc"),
                        ),
                        logic_nodes=sw_compdocs.component.LogicNodeList(
                            [
                                sw_compdocs.component.LogicNode(
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
                        ),
                    )
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("部品名 (Deprecated)"),
                        sw_compdocs.document.Callout(
                            "この部品は非推奨です。",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Callout(
                            "この部品は孤児です。親部品が見当たりません。",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Paragraph("短い説明"),
                        sw_compdocs.document.Paragraph("説明"),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("重量: 0"),
                                sw_compdocs.document.ListItem("サイズ (WxDxH): 1x1x1"),
                                sw_compdocs.document.ListItem("値段: $0"),
                                sw_compdocs.document.ListItem("タグ: "),
                                sw_compdocs.document.ListItem("ファイル: "),
                            ]
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
                    "DOCUMENT_PROP_MASS": "重量: {}",
                    "DOCUMENT_PROP_DIMS": "サイズ (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "値段: ${}",
                    "DOCUMENT_PROP_TAGS": "タグ: {}",
                    "DOCUMENT_PROP_FILE": "ファイル: {}",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE": "型",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL": "ラベル",
                    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC": "説明",
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
                input_bind={"action_interact_left": "q", "action_interact_right": "e"},
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
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
                        ),
                        voxels=sw_compdocs.component.VoxelList(
                            [
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=0, z=0
                                    )
                                ),
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=0, y=1, z=0
                                    )
                                ),
                            ]
                        ),
                    )
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
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("重量: 1"),
                                sw_compdocs.document.ListItem("サイズ (WxDxH): 1x1x2"),
                                sw_compdocs.document.ListItem("値段: $10"),
                                sw_compdocs.document.ListItem("タグ: basic"),
                                sw_compdocs.document.ListItem(
                                    "ファイル: button_push.xml"
                                ),
                            ]
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
            # multibody
            tt(
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(),
                    child=sw_compdocs.component.Definition(
                        logic_nodes=sw_compdocs.component.LogicNodeList(
                            [sw_compdocs.component.LogicNode()]
                        )
                    ),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading(""),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem(
                                    "DOCUMENT_PROP_MASS",
                                    [
                                        sw_compdocs.document.ListItem(
                                            "DOCUMENT_PROP_MASS_PARENT"
                                        ),
                                        sw_compdocs.document.ListItem(
                                            "DOCUMENT_PROP_MASS_CHILD"
                                        ),
                                    ],
                                ),
                                sw_compdocs.document.ListItem(
                                    "DOCUMENT_PROP_DIMS",
                                    [
                                        sw_compdocs.document.ListItem(
                                            "DOCUMENT_PROP_DIMS_PARENT"
                                        ),
                                        sw_compdocs.document.ListItem(
                                            "DOCUMENT_PROP_DIMS_CHILD"
                                        ),
                                    ],
                                ),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem(
                                    "DOCUMENT_PROP_FILE_PARENT"
                                ),
                                sw_compdocs.document.ListItem(
                                    "DOCUMENT_PROP_FILE_CHILD"
                                ),
                            ]
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY",
                                        "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE",
                                        "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL",
                                        "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD",
                                            "on/off",
                                            "",
                                            "",
                                        ]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_component(
                    tc.input_comp,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_doc, tc.want_doc)

    def test_exc_label(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(
                flags=sw_compdocs.component.Flags.IS_DEPRECATED
            )
        )
        with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
            sw_compdocs.generator.generate_document_component(comp, label={})
        self.assertEqual(ctx.exception.key, "DOCUMENT_DEPRECATED_TEXT")


class TestGenerateDocumentComponentList(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            tt(
                input_comp_list=[],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc=sw_compdocs.document.Document(),
            ),
            tt(
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="A")
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="B")
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("A", level=1),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("B", level=1),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                    ]
                ),
            ),
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
                    "DOCUMENT_PROP_MASS": "重量: {}",
                    "DOCUMENT_PROP_DIMS": "サイズ (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "値段: ${}",
                    "DOCUMENT_PROP_TAGS": "タグ: {}",
                    "DOCUMENT_PROP_FILE": "ファイル: {}",
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
                input_bind={"s_desc": "foo", "desc": "bar"},
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("テスト", level=1),
                        sw_compdocs.document.Paragraph("短い説明 foo"),
                        sw_compdocs.document.Paragraph("長い説明 bar"),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("重量: 0"),
                                sw_compdocs.document.ListItem("サイズ (WxDxH): 1x1x1"),
                                sw_compdocs.document.ListItem("値段: $0"),
                                sw_compdocs.document.ListItem("タグ: "),
                                sw_compdocs.document.ListItem("ファイル: "),
                            ]
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_component_list(
                    tc.input_comp_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_doc, tc.want_doc)


class TestGenerateDocumentCategory(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_category", sw_compdocs.component.Category),
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                input_comp_list=[],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks"),
                    ]
                ),
            ),
            # single
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
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
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                    ],
                ),
            ),
            # sort deprecated and orphaned
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Blocks_A"),
                            category=sw_compdocs.component.Category.BLOCKS,
                            flags=sw_compdocs.component.Flags.MULTIBODY_CHILD
                            | sw_compdocs.component.Flags.IS_DEPRECATED,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Blocks_B"),
                            category=sw_compdocs.component.Category.BLOCKS,
                            flags=sw_compdocs.component.Flags.MULTIBODY_CHILD,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Blocks_C"),
                            category=sw_compdocs.component.Category.BLOCKS,
                            flags=sw_compdocs.component.Flags.IS_DEPRECATED,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            name=sw_compdocs.language.Text(en="Blocks_D"),
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_D", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_C (Deprecated)", level=2),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_DEPRECATED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_B", level=2),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_ORPHANED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_A (Deprecated)", level=2),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_DEPRECATED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Callout(
                            "DOCUMENT_ORPHANED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                    ],
                ),
            ),
            # sort defn_list name
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_1",
                            name=sw_compdocs.language.Text(en="Blocks_C"),
                            value=1,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_2",
                            name=sw_compdocs.language.Text(en="Blocks_B"),
                            value=2,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_3",
                            name=sw_compdocs.language.Text(en="Blocks_a"),
                            value=3,
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_a", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_B", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_C", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                    ],
                ),
            ),
            # sort defn_list key
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key=None,
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            tooltip_properties=sw_compdocs.component.TooltipProperties(
                                short_description=sw_compdocs.language.Text(en="4"),
                            ),
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_3",
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            tooltip_properties=sw_compdocs.component.TooltipProperties(
                                short_description=sw_compdocs.language.Text(en="3"),
                            ),
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_2",
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            tooltip_properties=sw_compdocs.component.TooltipProperties(
                                short_description=sw_compdocs.language.Text(en="2"),
                            ),
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="blocks_1",
                            name=sw_compdocs.language.Text(en="Blocks_1"),
                            tooltip_properties=sw_compdocs.component.TooltipProperties(
                                short_description=sw_compdocs.language.Text(en="1"),
                            ),
                        )
                    ),
                ],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Paragraph("1"),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Paragraph("2"),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Paragraph("3"),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Paragraph("4"),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                            ]
                        ),
                    ],
                ),
            ),
            # label, lang, keybindings
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
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
                    "DOCUMENT_PROP_MASS": "Mass: {}",
                    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "Cost: ${}",
                    "DOCUMENT_PROP_TAGS": "Tags: {}",
                    "DOCUMENT_PROP_FILE": "File: {}",
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
                input_bind={"s_desc": "foo", "desc": "bar"},
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("テスト", level=2),
                        sw_compdocs.document.Paragraph("短い説明 foo"),
                        sw_compdocs.document.Paragraph("長い説明 bar"),
                        sw_compdocs.document.Heading("プロパティ", level=3),
                        sw_compdocs.document.UnorderedList(
                            [
                                sw_compdocs.document.ListItem("Mass: 0"),
                                sw_compdocs.document.ListItem(
                                    "Dimensions (WxDxH): 1x1x1"
                                ),
                                sw_compdocs.document.ListItem("Cost: $0"),
                                sw_compdocs.document.ListItem("Tags: "),
                                sw_compdocs.document.ListItem("File: "),
                            ]
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc = sw_compdocs.generator.generate_document_category(
                    tc.input_category,
                    tc.input_comp_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_doc, tc.want_doc)

    def test_exc_value(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_category", sw_compdocs.component.Category),
                ("input_comp_list", list[sw_compdocs.component.Component]),
            ],
        )

        for tc in [
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
            ),
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                ],
            ),
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.BLOCKS,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        )
                    ),
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(ValueError):
                    sw_compdocs.generator.generate_document_category(
                        tc.input_category, tc.input_comp_list
                    )


class TestGenerateDocument(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("want_doc_dict", dict[str, sw_compdocs.document.Document]),
            ],
        )

        for tc in [
            # empty
            tt(
                input_comp_list=[],
                input_label=None,
                input_lang=None,
                input_bind=None,
                want_doc_dict={},
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
                input_bind=None,
                want_doc_dict={
                    "00_BLOCKS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Blocks", level=1),
                            sw_compdocs.document.Heading("Blocks_1", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ],
                    )
                },
            ),
            # multiple category
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
                input_bind=None,
                want_doc_dict={
                    "00_BLOCKS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Blocks", level=1),
                            sw_compdocs.document.Heading("BLOCKS_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "01_VEHICLE_CONTROL": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Vehicle Control", level=1),
                            sw_compdocs.document.Heading("VEHICLE_CONTROL_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "02_MECHANICS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Mechanics", level=1),
                            sw_compdocs.document.Heading("MECHANICS_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "03_PROPULSION": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Propulsion", level=1),
                            sw_compdocs.document.Heading("PROPULSION_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "04_SPECIALIST_EQUIPMENT": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading(
                                "Specialist Equipment", level=1
                            ),
                            sw_compdocs.document.Heading(
                                "SPECIALIST_EQUIPMENT_0", level=2
                            ),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "05_LOGIC": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Logic", level=1),
                            sw_compdocs.document.Heading("LOGIC_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "06_DISPLAYS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Displays", level=1),
                            sw_compdocs.document.Heading("DISPLAYS_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "07_SENSORS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Sensors", level=1),
                            sw_compdocs.document.Heading("SENSORS_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "08_DECORATIVE": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Decorative", level=1),
                            sw_compdocs.document.Heading("DECORATIVE_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "09_FLUID": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Fluid", level=1),
                            sw_compdocs.document.Heading("FLUID_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "10_ELECTRIC": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Electric", level=1),
                            sw_compdocs.document.Heading("ELECTRIC_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "11_JET_ENGINES": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Jet Engines", level=1),
                            sw_compdocs.document.Heading("JET_ENGINES_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "12_WEAPONS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Weapons", level=1),
                            sw_compdocs.document.Heading("WEAPONS_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "13_MODULAR_ENGINES": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Modular Engines", level=1),
                            sw_compdocs.document.Heading("MODULAR_ENGINES_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "14_INDUSTRY": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Industry", level=1),
                            sw_compdocs.document.Heading("INDUSTRY_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ]
                    ),
                    "15_WINDOWS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Windows", level=1),
                            sw_compdocs.document.Heading("WINDOWS_0", level=2),
                            sw_compdocs.document.Heading("PROPERTIES", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_MASS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_DIMS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_COST"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_TAGS"),
                                    sw_compdocs.document.ListItem("DOCUMENT_PROP_FILE"),
                                ]
                            ),
                        ],
                    ),
                },
            ),
            # label, lang, keybindings
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
                    "DOCUMENT_PROP_MASS": "Mass: {}",
                    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
                    "DOCUMENT_PROP_COST": "Cost: ${}",
                    "DOCUMENT_PROP_TAGS": "Tags: {}",
                    "DOCUMENT_PROP_FILE": "File: {}",
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
                input_bind={"s_desc": "foo", "desc": "bar"},
                want_doc_dict={
                    "00_BLOCKS": sw_compdocs.document.Document(
                        [
                            sw_compdocs.document.Heading("Blocks", level=1),
                            sw_compdocs.document.Heading("テスト", level=2),
                            sw_compdocs.document.Paragraph("短い説明 foo"),
                            sw_compdocs.document.Paragraph("長い説明 bar"),
                            sw_compdocs.document.Heading("プロパティ", level=3),
                            sw_compdocs.document.UnorderedList(
                                [
                                    sw_compdocs.document.ListItem("Mass: 0"),
                                    sw_compdocs.document.ListItem(
                                        "Dimensions (WxDxH): 1x1x1"
                                    ),
                                    sw_compdocs.document.ListItem("Cost: $0"),
                                    sw_compdocs.document.ListItem("Tags: "),
                                    sw_compdocs.document.ListItem("File: "),
                                ]
                            ),
                        ]
                    )
                },
            ),
        ]:
            with self.subTest(tc=tc):
                got_doc_dict = sw_compdocs.generator.generate_document(
                    tc.input_comp_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_doc_dict, tc.want_doc_dict)


class TestGenerateSheetComponent(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("input_comp", sw_compdocs.component.Component),
                ("want_record", list[str]),
            ],
        )

        for tc in [
            tt(  # empty
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition()
                ),
                want_record=[
                    "",  # Name
                    "",  # File
                    "Blocks",  # Category
                    "",  # Tags
                    "FALSE",  # Multibody
                    "FALSE",  # Deprecated
                    "FALSE",  # Orphaned
                    "0",  # Cost
                    "0",  # Mass
                    "1",  # Width
                    "1",  # Depth
                    "1",  # Height
                    "",  # Short Description
                    "",  # Description
                ],
            ),
            tt(  # normal
                input_lang=None,
                input_bind=None,
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
                        voxels=sw_compdocs.component.VoxelList(
                            [
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=-1, y=-2, z=-3
                                    )
                                ),
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=1, y=2, z=3
                                    )
                                ),
                            ]
                        ),
                    )
                ),
                want_record=[
                    "Name",  # Name
                    "test.xml",  # File
                    "Blocks",  # Category
                    "tags",  # Tags
                    "FALSE",  # Multibody
                    "FALSE",  # Deprecated
                    "FALSE",  # Orphaned
                    "2",  # Cost
                    "0.25",  # Mass
                    "3",  # Width
                    "7",  # Depth
                    "5",  # Height
                    "short_description",  # Short Description
                    "description",  # Description
                ],
            ),
            tt(  # multibody
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        file="multibody_a.xml",
                        name=sw_compdocs.language.Text(en="Name"),
                        category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                        mass=1.25,
                        value=2,
                        tags="tags",
                        tooltip_properties=sw_compdocs.component.TooltipProperties(
                            short_description=sw_compdocs.language.Text(
                                en="short_description"
                            ),
                            description=sw_compdocs.language.Text(en="description"),
                        ),
                        voxels=sw_compdocs.component.VoxelList(
                            [
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=-1, y=-2, z=-3
                                    )
                                ),
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=1, y=2, z=3
                                    )
                                ),
                            ]
                        ),
                    ),
                    child=sw_compdocs.component.Definition(
                        file="multibody_b.xml",
                        mass=0.25,
                        voxels=sw_compdocs.component.VoxelList(
                            [
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=-4, y=-5, z=-6
                                    )
                                ),
                                sw_compdocs.component.Voxel(
                                    position=sw_compdocs.component.VoxelPos(
                                        x=4, y=5, z=6
                                    )
                                ),
                            ]
                        ),
                    ),
                ),
                want_record=[
                    "Name",  # Name
                    "multibody_a.xml",  # File
                    "Vehicle Control",  # Category
                    "tags",  # Tags
                    "TRUE",  # Multibody
                    "FALSE",  # Deprecated
                    "FALSE",  # Orphaned
                    "2",  # Cost
                    "1.5",  # Mass
                    "9",  # Width
                    "13",  # Depth
                    "11",  # Height
                    "short_description",  # Short Description
                    "description",  # Description
                ],
            ),
            tt(  # file
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        file=b"path/to/multibody_a.xml"
                    ),
                    child=sw_compdocs.component.Definition(
                        file=b"path/to/multibody_b.xml"
                    ),
                ),
                want_record=[
                    "",  # Name
                    "multibody_a.xml",  # File
                    "Blocks",  # Category
                    "",  # Tags
                    "TRUE",  # Multibody
                    "FALSE",  # Deprecated
                    "FALSE",  # Orphaned
                    "0",  # Cost
                    "0",  # Mass
                    "1",  # Width
                    "1",  # Depth
                    "1",  # Height
                    "",  # Short Description
                    "",  # Description
                ],
            ),
            tt(  # deprecated
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        flags=sw_compdocs.component.Flags.IS_DEPRECATED
                    )
                ),
                want_record=[
                    " (Deprecated)",  # Name
                    "",  # File
                    "Blocks",  # Category
                    "",  # Tags
                    "FALSE",  # Multibody
                    "TRUE",  # Deprecated
                    "FALSE",  # Orphaned
                    "0",  # Cost
                    "0",  # Mass
                    "1",  # Width
                    "1",  # Depth
                    "1",  # Height
                    "",  # Short Description
                    "",  # Description
                ],
            ),
            tt(  # orphan
                input_lang=None,
                input_bind=None,
                input_comp=sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        flags=sw_compdocs.component.Flags.MULTIBODY_CHILD
                    )
                ),
                want_record=[
                    "",  # Name
                    "",  # File
                    "Blocks",  # Category
                    "",  # Tags
                    "FALSE",  # Multibody
                    "FALSE",  # Deprecated
                    "TRUE",  # Orphaned
                    "0",  # Cost
                    "0",  # Mass
                    "1",  # Width
                    "1",  # Depth
                    "1",  # Height
                    "",  # Short Description
                    "",  # Description
                ],
            ),
            tt(  # lang, keybindings
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
                input_bind={
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
                    "$[name]",  # Name
                    "",  # File
                    "Blocks",  # Category
                    "",  # Tags
                    "FALSE",  # Multibody
                    "FALSE",  # Deprecated
                    "FALSE",  # Orphaned
                    "0",  # Cost
                    "0",  # Mass
                    "1",  # Width
                    "1",  # Depth
                    "1",  # Height
                    "short_description",  # Short Description
                    "description",  # Description
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_record = sw_compdocs.generator.generate_sheet_component(
                    tc.input_comp, lang=tc.input_lang, bind=tc.input_bind
                )
                self.assertEqual(got_record, tc.want_record)


class TestGenerateSheetComponentList(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
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
                input_bind=None,
                want_record_list=[
                    [
                        "Test 1",  # Name
                        "",  # File
                        "Blocks",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "0",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "Test 2",  # Name
                        "",  # File
                        "Blocks",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "0",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "Test 3",  # Name
                        "",  # File
                        "Blocks",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "0",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
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
                            voxels=sw_compdocs.component.VoxelList(
                                [
                                    sw_compdocs.component.Voxel(
                                        position=sw_compdocs.component.VoxelPos(
                                            x=-1, y=-2, z=-3
                                        )
                                    ),
                                    sw_compdocs.component.Voxel(
                                        position=sw_compdocs.component.VoxelPos(
                                            x=1, y=2, z=3
                                        )
                                    ),
                                ]
                            ),
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
                input_bind={
                    "name": "Name",
                    "s_desc": "short_description",
                    "desc": "description",
                },
                want_record_list=[
                    [
                        "$[name]",  # Name
                        "test.xml",  # File
                        "Blocks",  # Category
                        "tags",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "2",  # Cost
                        "1",  # Mass
                        "3",  # Width
                        "7",  # Depth
                        "5",  # Height
                        "short_description",  # Short Description
                        "description",  # Description
                    ]
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_record_list = sw_compdocs.generator.generate_sheet_component_list(
                    tc.input_comp_list, lang=tc.input_lang, bind=tc.input_bind
                )
                self.assertEqual(got_record_list, tc.want_record_list)


class TestGenerateSheet(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", collections.abc.Mapping[str, str] | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_bind", collections.abc.Mapping[str, str] | None),
                ("input_comp_list", list[sw_compdocs.component.Component]),
                ("want_record_list", list[list[str]]),
            ],
        )

        for tc in [
            tt(  # sort
                input_label=None,
                input_lang=None,
                input_bind=None,
                input_comp_list=[
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="a",
                            name=sw_compdocs.language.Text(en="a"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=1,
                            flags=sw_compdocs.component.Flags.MULTIBODY_CHILD,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="a",
                            name=sw_compdocs.language.Text(en="a"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=2,
                            flags=sw_compdocs.component.Flags.IS_DEPRECATED,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="a",
                            name=sw_compdocs.language.Text(en="Z"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=3,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key=None,
                            name=sw_compdocs.language.Text(en="a"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=4,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="z",
                            name=sw_compdocs.language.Text(en="a"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=5,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="a",
                            name=sw_compdocs.language.Text(en="a"),
                            category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                            value=6,
                        )
                    ),
                    sw_compdocs.component.Component(
                        defn=sw_compdocs.component.Definition(
                            key="z",
                            name=sw_compdocs.language.Text(en="Z"),
                            category=sw_compdocs.component.Category.BLOCKS,
                            value=7,
                        )
                    ),
                ],
                want_record_list=[
                    [
                        "SHEET_HEAD_NAME",
                        "SHEET_HEAD_FILE",
                        "SHEET_HEAD_CATEGORY",
                        "SHEET_HEAD_TAGS",
                        "SHEET_HEAD_MULTIBODY",
                        "SHEET_HEAD_DEPRECATED",
                        "SHEET_HEAD_ORPHANED",
                        "SHEET_HEAD_COST",
                        "SHEET_HEAD_MASS",
                        "SHEET_HEAD_DIMS_WIDTH",
                        "SHEET_HEAD_DIMS_DEPTH",
                        "SHEET_HEAD_DIMS_HEIGHT",
                        "SHEET_HEAD_SDESC",
                        "SHEET_HEAD_DESC",
                    ],
                    [
                        "Z",  # Name
                        "",  # File
                        "Blocks",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "7",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "a",  # Name
                        "",  # File
                        "Vehicle Control",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "6",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "a",  # Name
                        "",  # File
                        "Vehicle Control",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "5",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "a",  # Name
                        "",  # File
                        "Vehicle Control",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "4",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "Z",  # Name
                        "",  # File
                        "Vehicle Control",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "3",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "a (Deprecated)",  # Name
                        "",  # File
                        "Vehicle Control",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "TRUE",  # Deprecated
                        "FALSE",  # Orphaned
                        "2",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                    [
                        "a",  # Name
                        "",  # File
                        "Vehicle Control",  # Category
                        "",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "TRUE",  # Orphaned
                        "1",  # Cost
                        "0",  # Mass
                        "1",  # Width
                        "1",  # Depth
                        "1",  # Height
                        "",  # Short Description
                        "",  # Description
                    ],
                ],
            ),
            tt(  # label, lang, bind
                input_label={
                    "SHEET_HEAD_NAME": "Name",
                    "SHEET_HEAD_FILE": "File",
                    "SHEET_HEAD_CATEGORY": "Category",
                    "SHEET_HEAD_TAGS": "Tags",
                    "SHEET_HEAD_MULTIBODY": "Multibody",
                    "SHEET_HEAD_DEPRECATED": "Deprecated",
                    "SHEET_HEAD_ORPHANED": "Orphaned",
                    "SHEET_HEAD_COST": "Cost",
                    "SHEET_HEAD_MASS": "Mass",
                    "SHEET_HEAD_DIMS_WIDTH": "Width",
                    "SHEET_HEAD_DIMS_DEPTH": "Depth",
                    "SHEET_HEAD_DIMS_HEIGHT": "Height",
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
                input_bind={
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
                            voxels=sw_compdocs.component.VoxelList(
                                [
                                    sw_compdocs.component.Voxel(
                                        position=sw_compdocs.component.VoxelPos(
                                            x=-1, y=-2, z=-3
                                        )
                                    ),
                                    sw_compdocs.component.Voxel(
                                        position=sw_compdocs.component.VoxelPos(
                                            x=1, y=2, z=3
                                        )
                                    ),
                                ]
                            ),
                        )
                    )
                ],
                want_record_list=[
                    [
                        "Name",
                        "File",
                        "Category",
                        "Tags",
                        "Multibody",
                        "Deprecated",
                        "Orphaned",
                        "Cost",
                        "Mass",
                        "Width",
                        "Depth",
                        "Height",
                        "Short Description",
                        "Description",
                    ],
                    [
                        "$[name]",  # Name
                        "test.xml",  # File
                        "Blocks",  # Category
                        "tags",  # Tags
                        "FALSE",  # Multibody
                        "FALSE",  # Deprecated
                        "FALSE",  # Orphaned
                        "2",  # Cost
                        "1",  # Mass
                        "3",  # Width
                        "7",  # Depth
                        "5",  # Height
                        "short_description",  # Short Description
                        "description",  # Description
                    ],
                ],
            ),
        ]:
            with self.subTest(tc=tc):
                got_record_list = sw_compdocs.generator.generate_sheet(
                    tc.input_comp_list,
                    label=tc.input_label,
                    lang=tc.input_lang,
                    bind=tc.input_bind,
                )
                self.assertEqual(got_record_list, tc.want_record_list)

    def test_exc_label(self) -> None:
        label_all = {
            "SHEET_HEAD_NAME": "Name",
            "SHEET_HEAD_FILE": "File",
            "SHEET_HEAD_CATEGORY": "Category",
            "SHEET_HEAD_TAGS": "Tags",
            "SHEET_HEAD_MULTIBODY": "Multibody",
            "SHEET_HEAD_DEPRECATED": "Deprecated",
            "SHEET_HEAD_ORPHANED": "Orphaned",
            "SHEET_HEAD_COST": "Cost",
            "SHEET_HEAD_MASS": "Mass",
            "SHEET_HEAD_DIMS_WIDTH": "Width",
            "SHEET_HEAD_DIMS_DEPTH": "Depth",
            "SHEET_HEAD_DIMS_HEIGHT": "Height",
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
