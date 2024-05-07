import copy
import lxml.etree
import os
import pathlib
import sw_compdocs._types
import sw_compdocs.component
import sw_compdocs.language
import tempfile
import typing
import unittest


class TestDefinitionXMLErrorInit(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.component.DefinitionXMLError("msg")
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("msg",))
        self.assertEqual(exc.msg, "msg")
        self.assertEqual(exc.file, None)
        self.assertEqual(exc.xpath, ".")


class TestDefinitionXMLErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.component.DefinitionXMLError("any useful message")
        exc.file = "01_block.xml"
        exc.prepend_xpath("logic_node[52149]")
        exc.prepend_xpath("logic_nodes")
        exc.prepend_xpath("definition")
        self.assertEqual(
            str(exc),
            "any useful message (in file '01_block.xml' at xpath './definition/logic_nodes/logic_node[52149]')",
        )

    def test_table(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_msg", str),
                ("input_file", sw_compdocs._types.StrOrBytesPath | None),
                ("input_xpath_list", list[str]),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_msg="msg",
                input_file=None,
                input_xpath_list=[],
                want_s="msg",
            ),
            tt(
                input_msg="msg",
                input_file="str",
                input_xpath_list=[],
                want_s="msg (in file 'str')",
            ),
            tt(
                input_msg="msg",
                input_file=b"bytes",
                input_xpath_list=[],
                want_s="msg (in file 'bytes')",
            ),
            tt(
                input_msg="msg",
                input_file=pathlib.PurePath("pathlike"),
                input_xpath_list=[],
                want_s="msg (in file 'pathlike')",
            ),
            tt(
                input_msg="msg",
                input_file=None,
                input_xpath_list=["foo"],
                want_s="msg (at xpath './foo')",
            ),
            tt(
                input_msg="msg",
                input_file="str",
                input_xpath_list=["foo"],
                want_s="msg (in file 'str' at xpath './foo')",
            ),
        ]:
            with self.subTest(tc=tc):
                exc = sw_compdocs.component.DefinitionXMLError(tc.input_msg)
                exc.file = tc.input_file
                for input_xpath_seg in tc.input_xpath_list:
                    exc.prepend_xpath(input_xpath_seg)

                got_s = str(exc)
                self.assertEqual(got_s, tc.want_s)


class TestDefinitionXMLErrorPrependXPath(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.component.DefinitionXMLError("msg")
        self.assertEqual(exc.xpath, ".")

        exc.prepend_xpath("logic_node[52149]")
        self.assertEqual(exc.xpath, "./logic_node[52149]")

        exc.prepend_xpath("logic_nodes")
        self.assertEqual(exc.xpath, "./logic_nodes/logic_node[52149]")

        exc.prepend_xpath("definition")
        self.assertEqual(exc.xpath, "./definition/logic_nodes/logic_node[52149]")

        exc.prepend_xpath("/")
        self.assertEqual(exc.xpath, "/definition/logic_nodes/logic_node[52149]")

    def test_exc_runtime(self) -> None:
        exc = sw_compdocs.component.DefinitionXMLError("msg")
        exc.prepend_xpath("xpath")
        exc.prepend_xpath("/")
        self.assertEqual(exc.xpath, "/xpath")

        for s in ["root", "/", "value/error"]:
            with self.subTest(s=s):
                with self.assertRaises(RuntimeError):
                    exc.prepend_xpath(s)
                self.assertEqual(exc.xpath, "/xpath")

    def test_exc_value(self) -> None:
        for s in ["", "logic_nodes/logic_node[52149]"]:
            with self.subTest(s=s):
                exc = sw_compdocs.component.DefinitionXMLError("msg")
                with self.assertRaises(ValueError):
                    exc.prepend_xpath(s)


class TestMultibodyLinkErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.component.MultibodyLinkError("parent_key", "child_key")
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("parent_key", "child_key"))
        self.assertEqual(exc.parent_key, "parent_key")
        self.assertEqual(exc.child_key, "child_key")


class TestMultibodyLinkErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.component.MultibodyLinkError("parent_key", "child_key")
        self.assertEqual(
            str(exc),
            "failed to link parent component 'parent_key' and child component 'child_key'",
        )


class TestMultibodyChildNotFoundErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.component.MultibodyChildNotFoundError(
            "parent_key", "child_key"
        )
        self.assertEqual(
            str(exc),
            "missing child component 'child_key' for parent component 'parent_key'",
        )


class TestMultibodyChildFlagNotSetErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.component.MultibodyChildFlagNotSetError(
            "parent_key", "child_key"
        )
        self.assertEqual(
            str(exc),
            "multibody child flag is not set for child component 'child_key' of parent component 'parent_key'",
        )


class TestGenerateKey(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_file", sw_compdocs._types.StrOrBytesPath),
                ("want_key", str),
            ],
        )

        for tc in [
            tt(
                input_file="01_block_test.xml",
                want_key="01_block_test",
            ),
            tt(
                input_file="01_block_test.test.xml.xml",
                want_key="01_block_test.test.xml",
            ),
            tt(
                input_file="01_block_test.dmy",
                want_key="01_block_test",
            ),
            tt(
                input_file="01_block-.xml",
                want_key="01_block-",
            ),
            tt(
                input_file=".xml",
                want_key="",
            ),
            tt(
                input_file=b"01_block_test.xml",
                want_key="01_block_test",
            ),
            tt(
                input_file=pathlib.PurePath("01_block_test.xml"),
                want_key="01_block_test",
            ),
            tt(
                input_file=pathlib.PurePosixPath("/tmp/01_block_test.xml"),
                want_key="01_block_test",
            ),
        ]:
            with self.subTest(tc=tc):
                got_id = sw_compdocs.component.generate_key(tc.input_file)
                self.assertEqual(got_id, tc.want_key)


class TestCategoryStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_category", sw_compdocs.component.Category),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_category=sw_compdocs.component.Category.BLOCKS,
                want_s="Blocks",
            ),
            tt(
                input_category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                want_s="Vehicle Control",
            ),
            tt(
                input_category=sw_compdocs.component.Category.MECHANICS,
                want_s="Mechanics",
            ),
            tt(
                input_category=sw_compdocs.component.Category.PROPULSION,
                want_s="Propulsion",
            ),
            tt(
                input_category=sw_compdocs.component.Category.SPECIALIST_EQUIPMENT,
                want_s="Specialist Equipment",
            ),
            tt(
                input_category=sw_compdocs.component.Category.LOGIC,
                want_s="Logic",
            ),
            tt(
                input_category=sw_compdocs.component.Category.DISPLAYS,
                want_s="Displays",
            ),
            tt(
                input_category=sw_compdocs.component.Category.SENSORS,
                want_s="Sensors",
            ),
            tt(
                input_category=sw_compdocs.component.Category.DECORATIVE,
                want_s="Decorative",
            ),
            tt(
                input_category=sw_compdocs.component.Category.FLUID,
                want_s="Fluid",
            ),
            tt(
                input_category=sw_compdocs.component.Category.ELECTRIC,
                want_s="Electric",
            ),
            tt(
                input_category=sw_compdocs.component.Category.JET_ENGINES,
                want_s="Jet Engines",
            ),
            tt(
                input_category=sw_compdocs.component.Category.WEAPONS,
                want_s="Weapons",
            ),
            tt(
                input_category=sw_compdocs.component.Category.MODULAR_ENGINES,
                want_s="Modular Engines",
            ),
            tt(
                input_category=sw_compdocs.component.Category.INDUSTRY,
                want_s="Industry",
            ),
            tt(
                input_category=sw_compdocs.component.Category.WINDOWS,
                want_s="Windows",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = str(tc.input_category)
                self.assertEqual(got_s, tc.want_s)


class TestTooltipPropertiesFromXMLElem(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_elem", lxml.etree._Element),
                ("input_key", str | None),
                ("want_prop", sw_compdocs.component.TooltipProperties),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element(
                    "tooltip_properties", short_description="a", description="b"
                ),
                input_key=None,
                want_prop=sw_compdocs.component.TooltipProperties(
                    key=None,
                    short_description=sw_compdocs.language.Text(en="a"),
                    description=sw_compdocs.language.Text(en="b"),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element("tooltip_properties", description="b"),
                input_key=None,
                want_prop=sw_compdocs.component.TooltipProperties(
                    key=None,
                    short_description=sw_compdocs.language.Text(),
                    description=sw_compdocs.language.Text(en="b"),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "tooltip_properties", short_description="a"
                ),
                input_key=None,
                want_prop=sw_compdocs.component.TooltipProperties(
                    key=None,
                    short_description=sw_compdocs.language.Text(en="a"),
                    description=sw_compdocs.language.Text(),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "tooltip_properties", short_description="a", description="b"
                ),
                input_key="key",
                want_prop=sw_compdocs.component.TooltipProperties(
                    key="key",
                    short_description=sw_compdocs.language.Text(
                        id="def_key_s_desc", en="a"
                    ),
                    description=sw_compdocs.language.Text(id="def_key_desc", en="b"),
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_prop = sw_compdocs.component.TooltipProperties.from_xml_elem(
                    tc.input_elem, key=tc.input_key
                )
                self.assertEqual(got_prop, tc.want_prop)


class TestTooltipPropertiesUpdateID(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_prop", sw_compdocs.component.TooltipProperties),
                ("input_key", str | None),
                ("input_recursive", bool),
                ("want_prop", sw_compdocs.component.TooltipProperties),
            ],
        )

        for tc in [
            tt(
                input_prop=sw_compdocs.component.TooltipProperties(
                    key="key",
                    short_description=sw_compdocs.language.Text(id="def_key_s_desc"),
                    description=sw_compdocs.language.Text(id="def_key_desc"),
                ),
                input_key=None,
                input_recursive=False,
                want_prop=sw_compdocs.component.TooltipProperties(),
            ),
            tt(
                input_prop=sw_compdocs.component.TooltipProperties(),
                input_key="key",
                input_recursive=False,
                want_prop=sw_compdocs.component.TooltipProperties(
                    key="key",
                    short_description=sw_compdocs.language.Text(id="def_key_s_desc"),
                    description=sw_compdocs.language.Text(id="def_key_desc"),
                ),
            ),
            tt(
                input_prop=sw_compdocs.component.TooltipProperties(
                    key="key",
                    short_description=sw_compdocs.language.Text(id="def_key_s_desc"),
                    description=sw_compdocs.language.Text(id="def_key_desc"),
                ),
                input_key=None,
                input_recursive=True,
                want_prop=sw_compdocs.component.TooltipProperties(),
            ),
            tt(
                input_prop=sw_compdocs.component.TooltipProperties(),
                input_key="key",
                input_recursive=True,
                want_prop=sw_compdocs.component.TooltipProperties(
                    key="key",
                    short_description=sw_compdocs.language.Text(id="def_key_s_desc"),
                    description=sw_compdocs.language.Text(id="def_key_desc"),
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                prop = copy.deepcopy(tc.input_prop)
                prop.update_id(tc.input_key, recursive=tc.input_recursive)
                self.assertEqual(prop, tc.want_prop)


class TestLogicNodeTypeStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_type", sw_compdocs.component.LogicNodeType),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_type=sw_compdocs.component.LogicNodeType.BOOL,
                want_s="on/off",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                want_s="number",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_s="power",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.WATER,
                want_s="fluid",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                want_s="electric",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.COMPOSITE,
                want_s="composite",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.VIDEO,
                want_s="video",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.AUDIO,
                want_s="audio",
            ),
            tt(
                input_type=sw_compdocs.component.LogicNodeType.ROPE,
                want_s="rope",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = str(tc.input_type)
                self.assertEqual(got_s, tc.want_s)


class TestLogicNodeFromXMLElem(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_elem", lxml.etree._Element),
                ("input_key", str | None),
                ("input_idx", int | None),
                ("want_ln", sw_compdocs.component.LogicNode),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="2",
                    description="description",
                ),
                input_key="key",
                input_idx=52149,
                want_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    idx=52149,
                    label=sw_compdocs.language.Text(
                        id="def_key_node_52149_label", en="label"
                    ),
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.TORQUE,
                    description=sw_compdocs.language.Text(
                        id="def_key_node_52149_desc", en="description"
                    ),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    mode="1",
                    type="2",
                    description="description",
                ),
                input_key="key",
                input_idx=52149,
                want_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    idx=52149,
                    label=sw_compdocs.language.Text(id="def_key_node_52149_label"),
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.TORQUE,
                    description=sw_compdocs.language.Text(
                        id="def_key_node_52149_desc", en="description"
                    ),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    type="2",
                    description="description",
                ),
                input_key="key",
                input_idx=52149,
                want_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    idx=52149,
                    label=sw_compdocs.language.Text(
                        id="def_key_node_52149_label", en="label"
                    ),
                    mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                    type=sw_compdocs.component.LogicNodeType.TORQUE,
                    description=sw_compdocs.language.Text(
                        id="def_key_node_52149_desc", en="description"
                    ),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    description="description",
                ),
                input_key="key",
                input_idx=52149,
                want_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    idx=52149,
                    label=sw_compdocs.language.Text(
                        id="def_key_node_52149_label", en="label"
                    ),
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.BOOL,
                    description=sw_compdocs.language.Text(
                        id="def_key_node_52149_desc", en="description"
                    ),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="2",
                ),
                input_key="key",
                input_idx=52149,
                want_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    idx=52149,
                    label=sw_compdocs.language.Text(
                        id="def_key_node_52149_label", en="label"
                    ),
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.TORQUE,
                    description=sw_compdocs.language.Text(id="def_key_node_52149_desc"),
                ),
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="2",
                    description="description",
                ),
                input_key=None,
                input_idx=None,
                want_ln=sw_compdocs.component.LogicNode(
                    key=None,
                    idx=None,
                    label=sw_compdocs.language.Text(en="label"),
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.TORQUE,
                    description=sw_compdocs.language.Text(en="description"),
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                got_ln = sw_compdocs.component.LogicNode.from_xml_elem(
                    tc.input_elem, key=tc.input_key, idx=tc.input_idx
                )
                self.assertEqual(got_ln, tc.want_ln)

    def test_exc_xml(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_elem", lxml.etree._Element),
                ("want_msg", str),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="a",
                    type="2",
                    description="description",
                ),
                want_msg="invalid logic node mode 'a'",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="2",
                    type="2",
                    description="description",
                ),
                want_msg="invalid logic node mode '2'",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="a",
                    description="description",
                ),
                want_msg="invalid logic node type 'a'",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="9",
                    description="description",
                ),
                want_msg="invalid logic node type '9'",
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.component.DefinitionXMLError) as ctx:
                    sw_compdocs.component.LogicNode.from_xml_elem(tc.input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, ".")


class TestLogicNodeUpdateID(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_ln", sw_compdocs.component.LogicNode),
                ("input_key", str | None),
                ("input_idx", int | None),
                ("input_recursive", bool),
                ("want_ln", sw_compdocs.component.LogicNode),
            ],
        )

        for tc in [
            tt(
                input_ln=sw_compdocs.component.LogicNode(),
                input_key="key",
                input_idx=52149,
                input_recursive=False,
                want_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    idx=52149,
                    label=sw_compdocs.language.Text(id="def_key_node_52149_label"),
                    description=sw_compdocs.language.Text(id="def_key_node_52149_desc"),
                ),
            ),
            tt(
                input_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    label=sw_compdocs.language.Text(id="def_key_node_52149_label"),
                    description=sw_compdocs.language.Text(id="def_key_node_52149_desc"),
                ),
                input_key=None,
                input_idx=52149,
                input_recursive=False,
                want_ln=sw_compdocs.component.LogicNode(idx=52149),
            ),
            tt(
                input_ln=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label=sw_compdocs.language.Text(id="def_key_node_52149_label"),
                    description=sw_compdocs.language.Text(id="def_key_node_52149_desc"),
                ),
                input_key="key",
                input_idx=None,
                input_recursive=False,
                want_ln=sw_compdocs.component.LogicNode(key="key"),
            ),
            tt(
                input_ln=sw_compdocs.component.LogicNode(),
                input_key="key",
                input_idx=52149,
                input_recursive=True,
                want_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    idx=52149,
                    label=sw_compdocs.language.Text(id="def_key_node_52149_label"),
                    description=sw_compdocs.language.Text(id="def_key_node_52149_desc"),
                ),
            ),
            tt(
                input_ln=sw_compdocs.component.LogicNode(
                    key="key",
                    label=sw_compdocs.language.Text(id="def_key_node_52149_label"),
                    description=sw_compdocs.language.Text(id="def_key_node_52149_desc"),
                ),
                input_key=None,
                input_idx=52149,
                input_recursive=True,
                want_ln=sw_compdocs.component.LogicNode(idx=52149),
            ),
            tt(
                input_ln=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label=sw_compdocs.language.Text(id="def_key_node_52149_label"),
                    description=sw_compdocs.language.Text(id="def_key_node_52149_desc"),
                ),
                input_key="key",
                input_idx=None,
                input_recursive=True,
                want_ln=sw_compdocs.component.LogicNode(key="key"),
            ),
        ]:
            with self.subTest(tc=tc):
                ln = copy.deepcopy(tc.input_ln)
                ln.update_id(tc.input_key, tc.input_idx, recursive=tc.input_recursive)
                self.assertEqual(ln, tc.want_ln)


class TestLogicNodeListInit(unittest.TestCase):
    def test(self) -> None:
        lst = [
            sw_compdocs.component.LogicNode(idx=0),
            sw_compdocs.component.LogicNode(idx=1),
            sw_compdocs.component.LogicNode(idx=2),
        ]
        lns = sw_compdocs.component.LogicNodeList(lst, key="key")
        self.assertEqual(list[sw_compdocs.component.LogicNode](lns), lst)
        self.assertEqual(lns.key, "key")


class TestLogicNodeListRepr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lns", sw_compdocs.component.LogicNodeList),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_lns=sw_compdocs.component.LogicNodeList([]),
                want_s="LogicNodeList([])",
            ),
            tt(
                input_lns=sw_compdocs.component.LogicNodeList([], key="key"),
                want_s="LogicNodeList([], key='key')",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = repr(tc.input_lns)
                self.assertEqual(got_s, tc.want_s)


class TestLogicNodeListEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.component.LogicNodeList),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=2),
                    ],
                    key="key",
                ),
                input_other=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=2),
                    ],
                    key="key",
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=2),
                    ],
                    key="key",
                ),
                input_other=None,
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=2),
                    ],
                    key="key",
                ),
                input_other=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=3),
                    ],
                    key="key",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=2),
                    ],
                    key="key",
                ),
                input_other=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=2),
                    ],
                    key="",
                ),
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestLogicNodeListFromXMLElem(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_sub_list", list[lxml.etree._Element]),
                ("input_key", str | None),
                ("want_lns", sw_compdocs.component.LogicNodeList),
            ],
        )

        for tc in [
            tt(
                input_sub_list=[],
                input_key=None,
                want_lns=sw_compdocs.component.LogicNodeList(),
            ),
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", label="a"),
                    lxml.etree.Element("logic_node", label="b"),
                    lxml.etree.Element("logic_node", label="c"),
                ],
                input_key=None,
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=0, label=sw_compdocs.language.Text(en="a")
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=1, label=sw_compdocs.language.Text(en="b")
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=2, label=sw_compdocs.language.Text(en="c")
                        ),
                    ]
                ),
            ),
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", label="a"),
                    lxml.etree.Element("dummy", label="b"),
                    lxml.etree.Element("logic_node", label="c"),
                ],
                input_key=None,
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=0, label=sw_compdocs.language.Text(en="a")
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=1, label=sw_compdocs.language.Text(en="c")
                        ),
                    ]
                ),
            ),
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", label="a"),
                    lxml.etree.Element("logic_node", label="b"),
                    lxml.etree.Element("logic_node", label="c"),
                ],
                input_key="key",
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=0,
                            label=sw_compdocs.language.Text(
                                id="def_key_node_0_label", en="a"
                            ),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_0_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=1,
                            label=sw_compdocs.language.Text(
                                id="def_key_node_1_label", en="b"
                            ),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_1_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=2,
                            label=sw_compdocs.language.Text(
                                id="def_key_node_2_label", en="c"
                            ),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_2_desc"
                            ),
                        ),
                    ],
                    key="key",
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                input_elem = lxml.etree.Element("logic_nodes")
                input_elem.extend(tc.input_sub_list)
                got_lns = sw_compdocs.component.LogicNodeList.from_xml_elem(
                    input_elem, key=tc.input_key
                )
                self.assertEqual(got_lns, tc.want_lns)

    def test_exc_xml(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_sub_list", list[lxml.etree._Element]),
                ("want_msg", str),
                ("want_xpath", str),
            ],
        )

        for tc in [
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", type="-1"),
                    lxml.etree.Element("logic_node", type="1"),
                    lxml.etree.Element("logic_node", type="2"),
                ],
                want_msg="invalid logic node type '-1'",
                want_xpath="./logic_node[1]",
            ),
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", type="0"),
                    lxml.etree.Element("logic_node", type="-1"),
                    lxml.etree.Element("logic_node", type="2"),
                ],
                want_msg="invalid logic node type '-1'",
                want_xpath="./logic_node[2]",
            ),
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", type="0"),
                    lxml.etree.Element("logic_node", type="1"),
                    lxml.etree.Element("logic_node", type="-1"),
                ],
                want_msg="invalid logic node type '-1'",
                want_xpath="./logic_node[3]",
            ),
        ]:
            with self.subTest(tc=tc):
                input_elem = lxml.etree.Element("logic_nodes")
                input_elem.extend(tc.input_sub_list)
                with self.assertRaises(sw_compdocs.component.DefinitionXMLError) as ctx:
                    sw_compdocs.component.LogicNodeList.from_xml_elem(input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, tc.want_xpath)


class TestLogicNodeListUpdateID(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lns", sw_compdocs.component.LogicNodeList),
                ("input_key", str | None),
                ("input_recursive", bool),
                ("want_lns", sw_compdocs.component.LogicNodeList),
            ],
        )

        for tc in [
            tt(
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=0,
                            label=sw_compdocs.language.Text(id="def_key_node_0_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_0_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=1,
                            label=sw_compdocs.language.Text(id="def_key_node_1_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_1_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=2,
                            label=sw_compdocs.language.Text(id="def_key_node_2_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_2_desc"
                            ),
                        ),
                    ],
                    key="key",
                ),
                input_key=None,
                input_recursive=False,
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=0,
                            label=sw_compdocs.language.Text(id="def_key_node_0_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_0_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=1,
                            label=sw_compdocs.language.Text(id="def_key_node_1_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_1_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=2,
                            label=sw_compdocs.language.Text(id="def_key_node_2_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_2_desc"
                            ),
                        ),
                    ],
                ),
            ),
            tt(
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(),
                        sw_compdocs.component.LogicNode(),
                        sw_compdocs.component.LogicNode(),
                    ],
                ),
                input_key="key",
                input_recursive=False,
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(),
                        sw_compdocs.component.LogicNode(),
                        sw_compdocs.component.LogicNode(),
                    ],
                    key="key",
                ),
            ),
            tt(
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=0,
                            label=sw_compdocs.language.Text(id="def_key_node_0_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_0_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=1,
                            label=sw_compdocs.language.Text(id="def_key_node_1_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_1_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=2,
                            label=sw_compdocs.language.Text(id="def_key_node_2_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_2_desc"
                            ),
                        ),
                    ],
                    key="key",
                ),
                input_key=None,
                input_recursive=True,
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0),
                        sw_compdocs.component.LogicNode(idx=1),
                        sw_compdocs.component.LogicNode(idx=2),
                    ],
                ),
            ),
            tt(
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(),
                        sw_compdocs.component.LogicNode(),
                        sw_compdocs.component.LogicNode(),
                    ],
                ),
                input_key="key",
                input_recursive=True,
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=0,
                            label=sw_compdocs.language.Text(id="def_key_node_0_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_0_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=1,
                            label=sw_compdocs.language.Text(id="def_key_node_1_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_1_desc"
                            ),
                        ),
                        sw_compdocs.component.LogicNode(
                            key="key",
                            idx=2,
                            label=sw_compdocs.language.Text(id="def_key_node_2_label"),
                            description=sw_compdocs.language.Text(
                                id="def_key_node_2_desc"
                            ),
                        ),
                    ],
                    key="key",
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                lns = copy.deepcopy(tc.input_lns)
                lns.update_id(tc.input_key, recursive=tc.input_recursive)
                self.assertEqual(lns, tc.want_lns)


class TestVoxelPosFromXMLElem(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_elem", lxml.etree._Element),
                ("want_x", int),
                ("want_y", int),
                ("want_z", int),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element(
                    "voxel_max",
                    x="1",
                    y="2",
                    z="3",
                ),
                want_x=1,
                want_y=2,
                want_z=3,
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "voxel_max",
                    y="2",
                    z="3",
                ),
                want_x=0,
                want_y=2,
                want_z=3,
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "voxel_max",
                    x="1",
                    z="3",
                ),
                want_x=1,
                want_y=0,
                want_z=3,
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "voxel_max",
                    x="1",
                    y="2",
                ),
                want_x=1,
                want_y=2,
                want_z=0,
            ),
        ]:
            with self.subTest(tc=tc):
                pos = sw_compdocs.component.VoxelPos.from_xml_elem(tc.input_elem)
                self.assertEqual(pos.x, tc.want_x)
                self.assertEqual(pos.y, tc.want_y)
                self.assertEqual(pos.z, tc.want_z)

    def test_exc_xml(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_elem", lxml.etree._Element),
                ("want_msg", str),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element("voxel_max", x="", y="2", z="3"),
                want_msg="invalid voxel x ''",
            ),
            tt(
                input_elem=lxml.etree.Element("voxel_max", x="1", y="", z="3"),
                want_msg="invalid voxel y ''",
            ),
            tt(
                input_elem=lxml.etree.Element("voxel_max", x="1", y="2", z=""),
                want_msg="invalid voxel z ''",
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.component.DefinitionXMLError) as ctx:
                    sw_compdocs.component.VoxelPos.from_xml_elem(tc.input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, ".")


class TestDefinitionFromXMLElem(unittest.TestCase):
    def test_pass_clock(self) -> None:
        elem = lxml.etree.fromstring(
            """\
<definition name="Clock" category="6" mass="1" value="100" flags="8192" tags="basic">
	<tooltip_properties description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display." short_description="An analogue clock display that outputs a number value representing the time of day."/>
	<logic_nodes>
		<logic_node label="Time" mode="0" type="1" description="The time as a factor of a day, from 0 (midnight) to 1 (midnight)."/>
		<logic_node label="Backlight" mode="1" type="0" description="Enables the backlight when receiving an on signal."/>
		<logic_node label="Electric" mode="1" type="4" description="Electrical power connection." flags="0"/>
	</logic_nodes>
	<voxel_min x="0" y="0" z="0"/>
	<voxel_max x="0" y="1" z="0"/>
	<voxel_location_child x="0" y="0" z="0"/>
</definition>
"""
        )

        defn = sw_compdocs.component.Definition.from_xml_elem(
            elem, file="clock.xml", key="clock"
        )
        self.assertEqual(defn.file, "clock.xml")
        self.assertEqual(defn.key, "clock")
        self.assertEqual(
            defn.name, sw_compdocs.language.Text(id="def_clock_name", en="Clock")
        )
        self.assertEqual(defn.category, sw_compdocs.component.Category.DISPLAYS)
        self.assertEqual(defn.mass, 1.0)
        self.assertEqual(defn.value, 100)
        self.assertEqual(defn.flags, sw_compdocs.component.Flags(8192))
        self.assertEqual(defn.tags, "basic")
        self.assertEqual(defn.child_name, "")
        self.assertEqual(
            defn.tooltip_properties,
            sw_compdocs.component.TooltipProperties(
                key="clock",
                short_description=sw_compdocs.language.Text(
                    id="def_clock_s_desc",
                    en="An analogue clock display that outputs a number value representing the time of day.",
                ),
                description=sw_compdocs.language.Text(
                    id="def_clock_desc",
                    en="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                ),
            ),
        )
        self.assertEqual(
            defn.logic_nodes,
            sw_compdocs.component.LogicNodeList(
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
        )
        self.assertEqual(defn.voxel_min, sw_compdocs.component.VoxelPos(x=0, y=0, z=0))
        self.assertEqual(defn.voxel_max, sw_compdocs.component.VoxelPos(x=0, y=1, z=0))
        self.assertEqual(
            defn.voxel_location_child, sw_compdocs.component.VoxelPos(x=0, y=0, z=0)
        )

    def test_pass_pivot(self) -> None:
        elem = lxml.etree.fromstring(
            """\
<definition name="Pivot" category="2" type="7" mass="1" value="20" flags="64" tags="hinge" hild_name="multibody_pivot_b">
	<logic_nodes/>
	<voxel_min x="0" y="0" z="0"/>
	<voxel_max x="0" y="1" z="0"/>
	<voxel_location_child x="0" y="2" z="0"/>
	<tooltip_properties description="The pivot can rotate to 0.25 turns in both directions." short_description="A basic pivot that can move freely."/>
</definition>
"""
        )

        defn = sw_compdocs.component.Definition.from_xml_elem(
            elem, file="multibody_pivot_a.xml", key="multibody_pivot_a"
        )
        self.assertEqual(defn.file, "multibody_pivot_a.xml")
        self.assertEqual(defn.key, "multibody_pivot_a")
        self.assertEqual(
            defn.name,
            sw_compdocs.language.Text(id="def_multibody_pivot_a_name", en="Pivot"),
        )
        self.assertEqual(defn.category, sw_compdocs.component.Category.MECHANICS)
        self.assertEqual(defn.mass, 1.0)
        self.assertEqual(defn.value, 20)
        self.assertEqual(defn.flags, sw_compdocs.component.Flags(64))
        self.assertEqual(defn.tags, "hinge")
        self.assertEqual(
            defn.tooltip_properties,
            sw_compdocs.component.TooltipProperties(
                key="multibody_pivot_a",
                short_description=sw_compdocs.language.Text(
                    id="def_multibody_pivot_a_s_desc",
                    en="A basic pivot that can move freely.",
                ),
                description=sw_compdocs.language.Text(
                    id="def_multibody_pivot_a_desc",
                    en="The pivot can rotate to 0.25 turns in both directions.",
                ),
            ),
        )
        self.assertEqual(
            defn.logic_nodes,
            sw_compdocs.component.LogicNodeList(key="multibody_pivot_a"),
        )
        self.assertEqual(defn.voxel_min, sw_compdocs.component.VoxelPos(x=0, y=0, z=0))
        self.assertEqual(defn.voxel_max, sw_compdocs.component.VoxelPos(x=0, y=1, z=0))
        self.assertEqual(
            defn.voxel_location_child, sw_compdocs.component.VoxelPos(x=0, y=2, z=0)
        )

    def test_pass_empty(self) -> None:
        elem = lxml.etree.Element("definition")
        defn = sw_compdocs.component.Definition.from_xml_elem(elem)
        self.assertIsNone(defn.file)
        self.assertEqual(defn.key, None)
        self.assertEqual(defn.name, sw_compdocs.language.Text())
        self.assertEqual(defn.category, sw_compdocs.component.Category.BLOCKS)
        self.assertEqual(defn.mass, 0.0)
        self.assertEqual(defn.value, 0)
        self.assertEqual(defn.flags, sw_compdocs.component.Flags(0))
        self.assertEqual(defn.tags, "")
        self.assertEqual(defn.child_name, "")
        self.assertEqual(
            defn.tooltip_properties, sw_compdocs.component.TooltipProperties()
        )
        self.assertEqual(defn.logic_nodes, sw_compdocs.component.LogicNodeList())
        self.assertEqual(defn.voxel_min, sw_compdocs.component.VoxelPos())
        self.assertEqual(defn.voxel_max, sw_compdocs.component.VoxelPos())
        self.assertEqual(defn.voxel_location_child, sw_compdocs.component.VoxelPos())

    def test_pass_empty_key(self) -> None:
        elem = lxml.etree.Element("definition")
        defn = sw_compdocs.component.Definition.from_xml_elem(elem, key="key")
        self.assertIsNone(defn.file)
        self.assertEqual(defn.key, "key")
        self.assertEqual(defn.name, sw_compdocs.language.Text(id="def_key_name"))
        self.assertEqual(defn.category, sw_compdocs.component.Category.BLOCKS)
        self.assertEqual(defn.mass, 0.0)
        self.assertEqual(defn.value, 0)
        self.assertEqual(defn.flags, sw_compdocs.component.Flags(0))
        self.assertEqual(defn.tags, "")
        self.assertEqual(defn.child_name, "")
        self.assertEqual(
            defn.tooltip_properties,
            sw_compdocs.component.TooltipProperties(
                key="key",
                short_description=sw_compdocs.language.Text(id="def_key_s_desc"),
                description=sw_compdocs.language.Text(id="def_key_desc"),
            ),
        )
        self.assertEqual(
            defn.logic_nodes, sw_compdocs.component.LogicNodeList(key="key")
        )
        self.assertEqual(defn.voxel_min, sw_compdocs.component.VoxelPos())
        self.assertEqual(defn.voxel_max, sw_compdocs.component.VoxelPos())
        self.assertEqual(defn.voxel_location_child, sw_compdocs.component.VoxelPos())

    def test_exc_xml(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_elem", lxml.etree._Element),
                ("input_file", sw_compdocs._types.StrOrBytesPath | None),
                ("want_msg", str),
                ("want_file", sw_compdocs._types.StrOrBytesPath | None),
                ("want_xpath", str),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element("definition", category="nan"),
                input_file="file",
                want_msg="invalid component category 'nan'",
                want_file="file",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", category="999"),
                input_file="file",
                want_msg="invalid component category '999'",
                want_file="file",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", mass="invalid"),
                input_file="file",
                want_msg="invalid component mass 'invalid'",
                want_file="file",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", value="nan"),
                input_file="file",
                want_msg="invalid component value 'nan'",
                want_file="file",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", flags="nan"),
                input_file="file",
                want_msg="invalid component flags 'nan'",
                want_file="file",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.fromstring(
                    """<definition><logic_nodes><logic_node mode="999"/></logic_nodes></definition>"""
                ),
                input_file="file",
                want_msg="invalid logic node mode '999'",
                want_file="file",
                want_xpath="./logic_nodes/logic_node[1]",
            ),
            tt(
                input_elem=lxml.etree.fromstring(
                    """<definition><voxel_min x="nan"/></definition>"""
                ),
                input_file="file",
                want_msg="invalid voxel x 'nan'",
                want_file="file",
                want_xpath="./voxel_min",
            ),
            tt(
                input_elem=lxml.etree.fromstring(
                    """<definition><voxel_max x="nan"/></definition>"""
                ),
                input_file="file",
                want_msg="invalid voxel x 'nan'",
                want_file="file",
                want_xpath="./voxel_max",
            ),
            tt(
                input_elem=lxml.etree.fromstring(
                    """<definition><voxel_location_child x="nan"/></definition>"""
                ),
                input_file="file",
                want_msg="invalid voxel x 'nan'",
                want_file="file",
                want_xpath="./voxel_location_child",
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.component.DefinitionXMLError) as ctx:
                    sw_compdocs.component.Definition.from_xml_elem(
                        tc.input_elem, file=tc.input_file
                    )
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, tc.want_file)
                self.assertEqual(ctx.exception.xpath, tc.want_xpath)


class TestDefinitionUpdateID(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_defn", sw_compdocs.component.Definition),
                ("input_key", str | None),
                ("input_recursive", bool),
                ("want_defn", sw_compdocs.component.Definition),
            ],
        )

        for tc in [
            tt(
                input_defn=sw_compdocs.component.Definition(
                    key="key",
                    name=sw_compdocs.language.Text(id="def_key_name"),
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        key="key",
                        short_description=sw_compdocs.language.Text(
                            id="def_key_s_desc"
                        ),
                        description=sw_compdocs.language.Text(id="def_key_desc"),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(key="key"),
                ),
                input_key=None,
                input_recursive=False,
                want_defn=sw_compdocs.component.Definition(
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        key="key",
                        short_description=sw_compdocs.language.Text(
                            id="def_key_s_desc"
                        ),
                        description=sw_compdocs.language.Text(id="def_key_desc"),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(key="key"),
                ),
            ),
            tt(
                input_defn=sw_compdocs.component.Definition(),
                input_key="key",
                input_recursive=False,
                want_defn=sw_compdocs.component.Definition(
                    key="key", name=sw_compdocs.language.Text(id="def_key_name")
                ),
            ),
            tt(
                input_defn=sw_compdocs.component.Definition(
                    key="key",
                    name=sw_compdocs.language.Text(id="def_key_name"),
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        key="key",
                        short_description=sw_compdocs.language.Text(
                            id="def_key_s_desc"
                        ),
                        description=sw_compdocs.language.Text(id="def_key_desc"),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(key="key"),
                ),
                input_key=None,
                input_recursive=True,
                want_defn=sw_compdocs.component.Definition(),
            ),
            tt(
                input_defn=sw_compdocs.component.Definition(),
                input_key="key",
                input_recursive=True,
                want_defn=sw_compdocs.component.Definition(
                    key="key",
                    name=sw_compdocs.language.Text(id="def_key_name"),
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        key="key",
                        short_description=sw_compdocs.language.Text(
                            id="def_key_s_desc"
                        ),
                        description=sw_compdocs.language.Text(id="def_key_desc"),
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(key="key"),
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                defn = copy.deepcopy(tc.input_defn)
                defn.update_id(tc.input_key, recursive=tc.input_recursive)
                self.assertEqual(defn, tc.want_defn)


class TestComponentName(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(
                name=sw_compdocs.language.Text(id="id", en="en")
            )
        )

        name = comp.name()
        self.assertEqual(name, sw_compdocs.language.Text(id="id", en="en"))

        name.id = ""
        self.assertEqual(comp.name().id, "id")
        self.assertEqual(comp.defn.name.id, "id")


class TestComponentShortDescription(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(
                tooltip_properties=sw_compdocs.component.TooltipProperties(
                    short_description=sw_compdocs.language.Text(id="id", en="en")
                )
            )
        )

        short_description = comp.short_description()
        self.assertEqual(short_description, sw_compdocs.language.Text(id="id", en="en"))

        short_description.id = ""
        self.assertEqual(comp.short_description().id, "id")
        self.assertEqual(comp.defn.tooltip_properties.short_description.id, "id")


class TestComponentDescription(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(
                tooltip_properties=sw_compdocs.component.TooltipProperties(
                    description=sw_compdocs.language.Text(id="id", en="en")
                )
            )
        )

        description = comp.description()
        self.assertEqual(description, sw_compdocs.language.Text(id="id", en="en"))

        description.id = ""
        self.assertEqual(comp.description().id, "id")
        self.assertEqual(comp.defn.tooltip_properties.description.id, "id")


class TestComponentCategory(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(
                category=sw_compdocs.component.Category.VEHICLE_CONTROL
            )
        )
        self.assertEqual(
            comp.category(), sw_compdocs.component.Category.VEHICLE_CONTROL
        )


class TestComponentMass(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(mass=0.25)
        )
        self.assertEqual(comp.mass(), 0.25)


class TestComponentValue(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(value=100)
        )
        self.assertEqual(comp.value(), 100)


class TestComponentTags(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(tags="tags")
        )
        self.assertEqual(comp.tags(), "tags")


class TestComponentVoxelMin(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(
                voxel_min=sw_compdocs.component.VoxelPos(x=1, y=2, z=3)
            )
        )

        voxel_min = comp.voxel_min()
        self.assertEqual(voxel_min, sw_compdocs.component.VoxelPos(x=1, y=2, z=3))

        voxel_min.x = 0
        self.assertEqual(comp.voxel_min().x, 1)
        self.assertEqual(comp.defn.voxel_min.x, 1)


class TestComponentVoxelMax(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Component(
            defn=sw_compdocs.component.Definition(
                voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3)
            )
        )

        voxel_max = comp.voxel_max()
        self.assertEqual(voxel_max, sw_compdocs.component.VoxelPos(x=1, y=2, z=3))

        voxel_max.x = 0
        self.assertEqual(comp.voxel_max().x, 1)
        self.assertEqual(comp.defn.voxel_max.x, 1)


class TestMultibodyMass(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Multibody(
            defn=sw_compdocs.component.Definition(mass=9.0),
            child=sw_compdocs.component.Definition(mass=1.0),
        )
        self.assertEqual(comp.mass(), 10.0)


class TestMultibodyVoxelMin(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp", sw_compdocs.component.Multibody),
                ("want_voxel_min", sw_compdocs.component.VoxelPos),
            ],
        )

        for tc in [
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(
                            x=1, y=2, z=3
                        ),
                    ),
                    child=sw_compdocs.component.Definition(),
                ),
                want_voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
            ),
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(x=-4),
                    ),
                    child=sw_compdocs.component.Definition(
                        voxel_min=sw_compdocs.component.VoxelPos(x=-5),
                    ),
                ),
                want_voxel_min=sw_compdocs.component.VoxelPos(x=-9, y=-2, z=-3),
            ),
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(y=-4),
                    ),
                    child=sw_compdocs.component.Definition(
                        voxel_min=sw_compdocs.component.VoxelPos(y=-5),
                    ),
                ),
                want_voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-9, z=-3),
            ),
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(z=-4),
                    ),
                    child=sw_compdocs.component.Definition(
                        voxel_min=sw_compdocs.component.VoxelPos(z=-5),
                    ),
                ),
                want_voxel_min=sw_compdocs.component.VoxelPos(x=-1, y=-2, z=-9),
            ),
        ]:
            with self.subTest(tc=tc):
                got_voxel_min = tc.input_comp.voxel_min()
                self.assertEqual(got_voxel_min, tc.want_voxel_min)


class TestMultibodyVoxelMax(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp", sw_compdocs.component.Multibody),
                ("want_voxel_max", sw_compdocs.component.VoxelPos),
            ],
        )

        for tc in [
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(
                            x=-1, y=-2, z=-3
                        ),
                    ),
                    child=sw_compdocs.component.Definition(),
                ),
                want_voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
            ),
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(x=4),
                    ),
                    child=sw_compdocs.component.Definition(
                        voxel_max=sw_compdocs.component.VoxelPos(x=5),
                    ),
                ),
                want_voxel_max=sw_compdocs.component.VoxelPos(x=9, y=2, z=3),
            ),
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(y=4),
                    ),
                    child=sw_compdocs.component.Definition(
                        voxel_max=sw_compdocs.component.VoxelPos(y=5),
                    ),
                ),
                want_voxel_max=sw_compdocs.component.VoxelPos(x=1, y=9, z=3),
            ),
            tt(
                input_comp=sw_compdocs.component.Multibody(
                    defn=sw_compdocs.component.Definition(
                        voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                        voxel_location_child=sw_compdocs.component.VoxelPos(z=4),
                    ),
                    child=sw_compdocs.component.Definition(
                        voxel_max=sw_compdocs.component.VoxelPos(z=5),
                    ),
                ),
                want_voxel_max=sw_compdocs.component.VoxelPos(x=1, y=2, z=9),
            ),
        ]:
            with self.subTest(tc=tc):
                got_voxel_max = tc.input_comp.voxel_max()
                self.assertEqual(got_voxel_max, tc.want_voxel_max)


class TestParseXMLFile(unittest.TestCase):
    def test_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "test.xml")
            with open(temp_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition name="name">
    <tooltip_properties description="description"/>
</definition>
"""
                )

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_file),
                os.fsencode(temp_file),
                temp_file,
            ]
            for path in path_list:
                with self.subTest(path=path):
                    defn = sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(defn.file, path)
                    self.assertEqual(defn.key, "test")
                    self.assertEqual(defn.name.en, "name")
                    self.assertEqual(
                        defn.tooltip_properties.description.en, "description"
                    )

    def test_pass_recover(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "test.xml")
            with open(temp_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition name="name">
    <voxels>
        <voxel>
            <physics_shape_rotation 00="1" 01="0" 02="0" 10="0" 11="1" 12="0" 20="0" 21="0" 22="1"/>
        </voxel>
    </voxels>
    <tooltip_properties description="description"/>
</definition>
"""
                )

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_file),
                os.fsencode(temp_file),
                temp_file,
            ]
            for path in path_list:
                with self.subTest(path=path):
                    defn = sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(defn.file, path)
                    self.assertEqual(defn.key, "test")
                    self.assertEqual(defn.name.en, "name")
                    self.assertEqual(
                        defn.tooltip_properties.description.en, "description"
                    )

    def test_exc_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "test.xml")
            with open(temp_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<invalid name="name">
    <tooltip_properties description="description"/>
</invalid>
"""
                )

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_file),
                os.fsencode(temp_file),
                temp_file,
            ]
            for path in path_list:
                with self.subTest(path=path):
                    with self.assertRaises(
                        sw_compdocs.component.DefinitionXMLError
                    ) as ctx:
                        sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(
                        ctx.exception.msg, "invalid xml root tag 'invalid'"
                    )
                    self.assertEqual(ctx.exception.file, path)
                    self.assertEqual(ctx.exception.xpath, "/invalid")

    def test_exc_xml(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "test.xml")
            with open(temp_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition>
    <voxel_min x="invalid"/>
</definition>
"""
                )

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_file),
                os.fsencode(temp_file),
                temp_file,
            ]
            for path in path_list:
                with self.subTest(path=path):
                    with self.assertRaises(
                        sw_compdocs.component.DefinitionXMLError
                    ) as ctx:
                        sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(ctx.exception.msg, "invalid voxel x 'invalid'")
                    self.assertEqual(ctx.exception.file, path)
                    self.assertEqual(ctx.exception.xpath, "/definition/voxel_min")

    def test_exc_parse(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir, "test.xml")
            with open(temp_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(" ")

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_file),
                os.fsencode(temp_file),
                temp_file,
            ]
            for path in path_list:
                with self.subTest(path=path):
                    with self.assertRaises(
                        sw_compdocs.component.DefinitionXMLError
                    ) as ctx:
                        sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(ctx.exception.msg, "invalid xml")
                    self.assertEqual(ctx.exception.file, path)
                    self.assertEqual(ctx.exception.xpath, "/")


class TestParseXMLStr(unittest.TestCase):
    def test_pass(self) -> None:
        defn = sw_compdocs.component.parse_xml_str(
            """\
<definition name="name">
    <tooltip_properties description="description"/>
</definition>
""",
            key="key",
        )

        self.assertIsNone(defn.file)
        self.assertEqual(defn.key, "key")
        self.assertEqual(defn.name.en, "name")
        self.assertEqual(defn.tooltip_properties.description.en, "description")

    def test_pass_recover(self) -> None:
        defn = sw_compdocs.component.parse_xml_str(
            """\
<definition name="name">
    <voxels>
        <voxel>
            <physics_shape_rotation 00="1" 01="0" 02="0" 10="0" 11="1" 12="0" 20="0" 21="0" 22="1"/>
        </voxel>
    </voxels>
    <tooltip_properties description="description"/>
</definition>
""",
            key="key",
        )

        self.assertIsNone(defn.file)
        self.assertEqual(defn.key, "key")
        self.assertEqual(defn.name.en, "name")
        self.assertEqual(defn.tooltip_properties.description.en, "description")

    def test_exc_root(self) -> None:
        with self.assertRaises(sw_compdocs.component.DefinitionXMLError) as ctx:
            sw_compdocs.component.parse_xml_str(
                """\
<invalid name="name">
    <tooltip_properties description="description"/>
</invalid>
    """,
                key="key",
            )

        self.assertEqual(ctx.exception.msg, "invalid xml root tag 'invalid'")
        self.assertEqual(ctx.exception.file, None)
        self.assertEqual(ctx.exception.xpath, "/invalid")

    def test_exc_xml(self) -> None:
        with self.assertRaises(sw_compdocs.component.DefinitionXMLError) as ctx:
            sw_compdocs.component.parse_xml_str(
                """\
<definition>
    <voxel_min x="invalid"/>
</definition>
""",
                key="key",
            )

        self.assertEqual(ctx.exception.msg, "invalid voxel x 'invalid'")
        self.assertEqual(ctx.exception.file, None)
        self.assertEqual(ctx.exception.xpath, "/definition/voxel_min")

    def test_exc_parse(self) -> None:
        with self.assertRaises(sw_compdocs.component.DefinitionXMLError) as ctx:
            sw_compdocs.component.parse_xml_str(" ")
        self.assertEqual(ctx.exception.msg, "invalid xml")
        self.assertEqual(ctx.exception.file, None)
        self.assertEqual(ctx.exception.xpath, "/")


class TestLoadDefnDict(unittest.TestCase):
    def test_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            want_defn_dict: dict[str, sw_compdocs.component.Definition] = {}

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_dir),
                os.fsencode(temp_dir),
                pathlib.Path(temp_dir),
            ]
            for path in path_list:
                with self.subTest(path=path):
                    got_defn_dict = sw_compdocs.component.load_defn_dict(path)
                    self.assertEqual(got_defn_dict, want_defn_dict)

    def test_normal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dmy1_file = pathlib.Path(temp_dir, "dmy1.xml")
            with open(dmy1_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition name="Dummy 1"/>
"""
                )

            dmy2_file = pathlib.Path(temp_dir, "dmy2.xml")
            with open(dmy2_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition name="Dummy 2"/>
"""
                )

            dmy3_dir = pathlib.Path(temp_dir, "dmy3.xml")
            dmy3_dir.mkdir()

            want_defn_dict = {
                "dmy1": sw_compdocs.component.Definition(
                    file=dmy1_file, name=sw_compdocs.language.Text(en="Dummy 1")
                ),
                "dmy2": sw_compdocs.component.Definition(
                    file=dmy2_file, name=sw_compdocs.language.Text(en="Dummy 2")
                ),
            }
            for key, defn in want_defn_dict.items():
                defn.update_id(key)

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_dir),
                os.fsencode(temp_dir),
                pathlib.Path(temp_dir),
            ]
            for path in path_list:
                with self.subTest(path=path):
                    got_defn_dict = sw_compdocs.component.load_defn_dict(path)
                    self.assertEqual(got_defn_dict, want_defn_dict)


class TestLoadCompList(unittest.TestCase):
    def test_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_dir),
                os.fsencode(temp_dir),
                pathlib.Path(temp_dir),
            ]
            for path in path_list:
                with self.subTest(path=path):
                    comp_list = sw_compdocs.component.load_comp_list(path)
                    self.assertEqual(comp_list, list[sw_compdocs.component.Component]())

    def test_normal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dmy1_file = pathlib.Path(temp_dir, "dmy1.xml")
            with open(dmy1_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition name="Dummy 1"/>
"""
                )

            dmy2_file = pathlib.Path(temp_dir, "dmy2.xml")
            with open(dmy2_file, mode="xt", encoding="utf-8", newline="\r\n") as f:
                f.write(
                    """\
<?xml version="1.0" encoding="UTF-8"?>
<definition name="Dummy 2"/>
"""
                )

            want_comp_list = [
                sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        key="dmy1",
                        file=dmy1_file,
                        name=sw_compdocs.language.Text(en="Dummy 1"),
                    )
                ),
                sw_compdocs.component.Component(
                    defn=sw_compdocs.component.Definition(
                        key="dmy2",
                        file=dmy2_file,
                        name=sw_compdocs.language.Text(en="Dummy 2"),
                    )
                ),
            ]
            for comp in want_comp_list:
                comp.defn.update_id(comp.defn.key)

            path_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(temp_dir),
                os.fsencode(temp_dir),
                pathlib.Path(temp_dir),
            ]
            for path in path_list:
                with self.subTest(path=path):
                    got_comp_list = sw_compdocs.component.load_comp_list(path)
                    self.assertEqual(got_comp_list, want_comp_list)
