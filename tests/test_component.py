import lxml.etree
import os
import pathlib
import sw_compdocs._types
import sw_compdocs.component
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
                ("want_short_description", str),
                ("want_description", str),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element(
                    "tooltip_properties", short_description="a", description="b"
                ),
                want_short_description="a",
                want_description="b",
            ),
            tt(
                input_elem=lxml.etree.Element("tooltip_properties", description="b"),
                want_short_description="",
                want_description="b",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "tooltip_properties", short_description="a"
                ),
                want_short_description="a",
                want_description="",
            ),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component.TooltipProperties.from_xml_elem(
                    tc.input_elem
                )
                self.assertEqual(got.short_description, tc.want_short_description)
                self.assertEqual(got.description, tc.want_description)


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
                ("input_idx", int | None),
                ("want_idx", int),
                ("want_label", str),
                ("want_mode", sw_compdocs.component.LogicNodeMode),
                ("want_type", sw_compdocs.component.LogicNodeType),
                ("want_description", str),
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
                input_idx=52149,
                want_idx=52149,
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="description",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    mode="1",
                    type="2",
                    description="description",
                ),
                input_idx=52149,
                want_idx=52149,
                want_label="",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="description",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    type="2",
                    description="description",
                ),
                input_idx=52149,
                want_idx=52149,
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="description",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    description="description",
                ),
                input_idx=52149,
                want_idx=52149,
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.BOOL,
                want_description="description",
            ),
            tt(
                input_elem=lxml.etree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="2",
                ),
                input_idx=52149,
                want_idx=52149,
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="",
            ),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component.LogicNode.from_xml_elem(
                    tc.input_elem, idx=tc.input_idx
                )
                self.assertEqual(got.idx, tc.want_idx)
                self.assertEqual(got.label, tc.want_label)
                self.assertEqual(got.mode, tc.want_mode)
                self.assertEqual(got.type, tc.want_type)
                self.assertEqual(got.description, tc.want_description)

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


class TestLogicNodeListFromXMLElem(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_sub_list", list[lxml.etree._Element]),
                ("want_lns", sw_compdocs.component.LogicNodeList),
            ],
        )

        for tc in [
            tt(
                input_sub_list=[],
                want_lns=sw_compdocs.component.LogicNodeList(),
            ),
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", label="a"),
                    lxml.etree.Element("logic_node", label="b"),
                    lxml.etree.Element("logic_node", label="c"),
                ],
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0, label="a"),
                        sw_compdocs.component.LogicNode(idx=1, label="b"),
                        sw_compdocs.component.LogicNode(idx=2, label="c"),
                    ]
                ),
            ),
            tt(
                input_sub_list=[
                    lxml.etree.Element("logic_node", label="a"),
                    lxml.etree.Element("dummy", label="b"),
                    lxml.etree.Element("logic_node", label="c"),
                ],
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(idx=0, label="a"),
                        sw_compdocs.component.LogicNode(idx=1, label="c"),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                input_elem = lxml.etree.Element("logic_nodes")
                input_elem.extend(tc.input_sub_list)
                got_lns = sw_compdocs.component.LogicNodeList.from_xml_elem(input_elem)
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
</definition>
"""
        )

        defn = sw_compdocs.component.Definition.from_xml_elem(
            elem, file="clock.xml", key="clock"
        )
        self.assertEqual(defn.file, "clock.xml")
        self.assertEqual(defn.key, "clock")
        self.assertEqual(defn.name, "Clock")
        self.assertEqual(defn.category, sw_compdocs.component.Category.DISPLAYS)
        self.assertEqual(defn.mass, 1.0)
        self.assertEqual(defn.value, 100)
        self.assertEqual(defn.flags, sw_compdocs.component.Flags(8192))
        self.assertEqual(defn.tags, "basic")
        self.assertEqual(
            defn.tooltip_properties,
            sw_compdocs.component.TooltipProperties(
                short_description="An analogue clock display that outputs a number value representing the time of day.",
                description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
            ),
        )
        self.assertEqual(
            defn.logic_nodes,
            sw_compdocs.component.LogicNodeList(
                [
                    sw_compdocs.component.LogicNode(
                        idx=0,
                        label="Time",
                        mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                        type=sw_compdocs.component.LogicNodeType.FLOAT,
                        description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                    ),
                    sw_compdocs.component.LogicNode(
                        idx=1,
                        label="Backlight",
                        mode=sw_compdocs.component.LogicNodeMode.INPUT,
                        type=sw_compdocs.component.LogicNodeType.BOOL,
                        description="Enables the backlight when receiving an on signal.",
                    ),
                    sw_compdocs.component.LogicNode(
                        idx=2,
                        label="Electric",
                        mode=sw_compdocs.component.LogicNodeMode.INPUT,
                        type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                        description="Electrical power connection.",
                    ),
                ]
            ),
        )
        self.assertEqual(defn.voxel_min, sw_compdocs.component.VoxelPos(x=0, y=0, z=0))
        self.assertEqual(defn.voxel_max, sw_compdocs.component.VoxelPos(x=0, y=1, z=0))

    def test_pass_empty(self) -> None:
        elem = lxml.etree.Element("definition")
        defn = sw_compdocs.component.Definition.from_xml_elem(elem)
        self.assertIsNone(defn.file)
        self.assertEqual(defn.key, None)
        self.assertEqual(defn.name, "")
        self.assertEqual(defn.category, sw_compdocs.component.Category.BLOCKS)
        self.assertEqual(defn.mass, 0.0)
        self.assertEqual(defn.value, 0)
        self.assertEqual(defn.flags, sw_compdocs.component.Flags(0))
        self.assertEqual(defn.tags, "")
        self.assertEqual(
            defn.tooltip_properties, sw_compdocs.component.TooltipProperties()
        )
        self.assertEqual(defn.logic_nodes, sw_compdocs.component.LogicNodeList())
        self.assertEqual(defn.voxel_min, sw_compdocs.component.VoxelPos())
        self.assertEqual(defn.voxel_max, sw_compdocs.component.VoxelPos())

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
                ("input_key", str | None),
                ("input_recursive", bool),
                ("want_key", str | None),
            ],
        )

        for tc in [
            tt(
                input_key=None,
                input_recursive=False,
                want_key=None,
            ),
            tt(
                input_key="key",
                input_recursive=False,
                want_key="key",
            ),
            tt(
                input_key=None,
                input_recursive=True,
                want_key=None,
            ),
            tt(
                input_key="key",
                input_recursive=True,
                want_key="key",
            ),
        ]:
            with self.subTest(tc=tc):
                defn = sw_compdocs.component.Definition()
                defn.update_id(tc.input_key, recursive=tc.input_recursive)
                self.assertEqual(defn.key, tc.want_key)


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
                    self.assertEqual(defn.name, "name")
                    self.assertEqual(defn.tooltip_properties.description, "description")

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
                    self.assertEqual(defn.name, "name")
                    self.assertEqual(defn.tooltip_properties.description, "description")

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
        self.assertEqual(defn.name, "name")
        self.assertEqual(defn.tooltip_properties.description, "description")

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
        self.assertEqual(defn.name, "name")
        self.assertEqual(defn.tooltip_properties.description, "description")

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
