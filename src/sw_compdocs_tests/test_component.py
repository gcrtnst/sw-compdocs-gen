import lxml.etree
import os
import pathlib
import sw_compdocs._types
import sw_compdocs.component
import tempfile
import typing
import unittest


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
                    comp = sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(comp.cid, "test")
                    self.assertEqual(comp.name, "name")
                    self.assertEqual(comp.tooltip_properties.description, "description")

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
                    comp = sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(comp.cid, "test")
                    self.assertEqual(comp.name, "name")
                    self.assertEqual(comp.tooltip_properties.description, "description")

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
                        sw_compdocs.component.ComponentXMLError
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
                        sw_compdocs.component.ComponentXMLError
                    ) as ctx:
                        sw_compdocs.component.parse_xml_file(path)
                    self.assertEqual(ctx.exception.msg, "invalid voxel x 'invalid'")
                    self.assertEqual(ctx.exception.file, path)
                    self.assertEqual(ctx.exception.xpath, "/definition/voxel_min")


class TestParseXMLStr(unittest.TestCase):
    def test_pass(self) -> None:
        comp = sw_compdocs.component.parse_xml_str(
            """\
<definition name="name">
    <tooltip_properties description="description"/>
</definition>
""",
            cid="cid",
        )

        self.assertEqual(comp.cid, "cid")
        self.assertEqual(comp.name, "name")
        self.assertEqual(comp.tooltip_properties.description, "description")

    def test_pass_recover(self) -> None:
        comp = sw_compdocs.component.parse_xml_str(
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
            cid="cid",
        )

        self.assertEqual(comp.cid, "cid")
        self.assertEqual(comp.name, "name")
        self.assertEqual(comp.tooltip_properties.description, "description")

    def test_exc_root(self) -> None:
        with self.assertRaises(sw_compdocs.component.ComponentXMLError) as ctx:
            sw_compdocs.component.parse_xml_str(
                """\
<invalid name="name">
    <tooltip_properties description="description"/>
</invalid>
    """,
                cid="cid",
            )

        self.assertEqual(ctx.exception.msg, "invalid xml root tag 'invalid'")
        self.assertEqual(ctx.exception.file, None)
        self.assertEqual(ctx.exception.xpath, "/invalid")

    def test_exc_xml(self) -> None:
        with self.assertRaises(sw_compdocs.component.ComponentXMLError) as ctx:
            sw_compdocs.component.parse_xml_str(
                """\
<definition>
    <voxel_min x="invalid"/>
</definition>
""",
                cid="cid",
            )

        self.assertEqual(ctx.exception.msg, "invalid voxel x 'invalid'")
        self.assertEqual(ctx.exception.file, None)
        self.assertEqual(ctx.exception.xpath, "/definition/voxel_min")


class TestGenerateCID(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_file", sw_compdocs._types.StrOrBytesPath),
                ("want_cid", str),
            ],
        )

        for tc in [
            tt(
                input_file="01_block_test.xml",
                want_cid="01_block_test",
            ),
            tt(
                input_file="01_block_test.test.xml.xml",
                want_cid="01_block_test.test.xml",
            ),
            tt(
                input_file="01_block_test.dmy",
                want_cid="01_block_test",
            ),
            tt(
                input_file="01_block-.xml",
                want_cid="01_block-",
            ),
            tt(
                input_file=".xml",
                want_cid="",
            ),
            tt(
                input_file=b"01_block_test.xml",
                want_cid="01_block_test",
            ),
            tt(
                input_file=pathlib.PurePath("01_block_test.xml"),
                want_cid="01_block_test",
            ),
            tt(
                input_file=pathlib.PurePosixPath("/tmp/01_block_test.xml"),
                want_cid="01_block_test",
            ),
        ]:
            with self.subTest(tc=tc):
                got_id = sw_compdocs.component.generate_cid(tc.input_file)
                self.assertEqual(got_id, tc.want_cid)


class TestDefinitionInit(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                (
                    "input_cid",
                    str,
                ),
                (
                    "input_name",
                    str,
                ),
                (
                    "input_category",
                    sw_compdocs.component.Category,
                ),
                (
                    "input_mass",
                    float,
                ),
                (
                    "input_value",
                    int,
                ),
                (
                    "input_flags",
                    sw_compdocs.component.Flags,
                ),
                (
                    "input_tags",
                    str,
                ),
                (
                    "input_tooltip_properties",
                    sw_compdocs.component.TooltipProperties,
                ),
                (
                    "input_logic_nodes",
                    sw_compdocs.component.LogicNodeList,
                ),
                (
                    "input_voxel_min",
                    sw_compdocs.component.VoxelPos,
                ),
                (
                    "input_voxel_max",
                    sw_compdocs.component.VoxelPos,
                ),
                (
                    "want_cid",
                    str,
                ),
                (
                    "want_name",
                    str,
                ),
                (
                    "want_category",
                    sw_compdocs.component.Category,
                ),
                (
                    "want_mass",
                    float,
                ),
                (
                    "want_value",
                    int,
                ),
                (
                    "want_flags",
                    sw_compdocs.component.Flags,
                ),
                (
                    "want_tags",
                    str,
                ),
                (
                    "want_tooltip_properties",
                    sw_compdocs.component.TooltipProperties,
                ),
                (
                    "want_logic_nodes",
                    sw_compdocs.component.LogicNodeList,
                ),
                (
                    "want_voxel_min",
                    sw_compdocs.component.VoxelPos,
                ),
                (
                    "want_voxel_max",
                    sw_compdocs.component.VoxelPos,
                ),
            ],
        )

        for tc in [
            tt(
                input_cid="clock",
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1.0,
                input_value=100,
                input_flags=sw_compdocs.component.Flags(8192),
                input_tags="basic",
                input_tooltip_properties=sw_compdocs.component.TooltipProperties(
                    short_description="An analogue clock display that outputs a number value representing the time of day.",
                    description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                ),
                input_logic_nodes=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="Time",
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                        ),
                        sw_compdocs.component.LogicNode(
                            label="Backlight",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="Enables the backlight when receiving an on signal.",
                        ),
                        sw_compdocs.component.LogicNode(
                            label="Electric",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                            description="Electrical power connection.",
                        ),
                    ]
                ),
                input_voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                input_voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                want_cid="clock",
                want_name="Clock",
                want_category=sw_compdocs.component.Category.DISPLAYS,
                want_mass=1.0,
                want_value=100,
                want_flags=sw_compdocs.component.Flags(8192),
                want_tags="basic",
                want_tooltip_properties=sw_compdocs.component.TooltipProperties(
                    short_description="An analogue clock display that outputs a number value representing the time of day.",
                    description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                ),
                want_logic_nodes=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="Time",
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                        ),
                        sw_compdocs.component.LogicNode(
                            label="Backlight",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="Enables the backlight when receiving an on signal.",
                        ),
                        sw_compdocs.component.LogicNode(
                            label="Electric",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                            description="Electrical power connection.",
                        ),
                    ]
                ),
                want_voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                want_voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
            ),
        ]:
            with self.subTest(tc=tc):
                got_comp = sw_compdocs.component.Definition(
                    cid=tc.input_cid,
                    name=tc.input_name,
                    category=tc.input_category,
                    mass=tc.input_mass,
                    value=tc.input_value,
                    flags=tc.input_flags,
                    tags=tc.input_tags,
                    tooltip_properties=tc.input_tooltip_properties,
                    logic_nodes=tc.input_logic_nodes,
                    voxel_min=tc.input_voxel_min,
                    voxel_max=tc.input_voxel_max,
                )
                self.assertEqual(got_comp.cid, tc.want_cid)
                self.assertEqual(got_comp.name, tc.want_name)
                self.assertEqual(got_comp.category, tc.want_category)
                self.assertEqual(got_comp.mass, tc.want_mass)
                self.assertEqual(got_comp.value, tc.want_value)
                self.assertEqual(got_comp.flags, tc.want_flags)
                self.assertEqual(got_comp.tags, tc.want_tags)
                self.assertEqual(
                    got_comp.tooltip_properties, tc.want_tooltip_properties
                )
                self.assertEqual(got_comp.logic_nodes, tc.want_logic_nodes)
                self.assertEqual(got_comp.voxel_min, tc.want_voxel_min)
                self.assertEqual(got_comp.voxel_max, tc.want_voxel_max)


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

        comp = sw_compdocs.component.Definition.from_xml_elem(elem, cid="clock")
        self.assertEqual(comp.cid, "clock")
        self.assertEqual(comp.name, "Clock")
        self.assertEqual(comp.category, sw_compdocs.component.Category.DISPLAYS)
        self.assertEqual(comp.mass, 1.0)
        self.assertEqual(comp.value, 100)
        self.assertEqual(comp.flags, sw_compdocs.component.Flags(8192))
        self.assertEqual(comp.tags, "basic")
        self.assertEqual(
            comp.tooltip_properties,
            sw_compdocs.component.TooltipProperties(
                short_description="An analogue clock display that outputs a number value representing the time of day.",
                description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
            ),
        )
        self.assertEqual(
            comp.logic_nodes,
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
        self.assertEqual(comp.voxel_min, sw_compdocs.component.VoxelPos(x=0, y=0, z=0))
        self.assertEqual(comp.voxel_max, sw_compdocs.component.VoxelPos(x=0, y=1, z=0))

    def test_pass_empty(self) -> None:
        elem = lxml.etree.Element("definition")
        comp = sw_compdocs.component.Definition.from_xml_elem(elem)
        self.assertEqual(comp.cid, "")
        self.assertEqual(comp.name, "")
        self.assertEqual(comp.category, sw_compdocs.component.Category.BLOCKS)
        self.assertEqual(comp.mass, 0.0)
        self.assertEqual(comp.value, 0)
        self.assertEqual(comp.flags, sw_compdocs.component.Flags(0))
        self.assertEqual(comp.tags, "")
        self.assertEqual(
            comp.tooltip_properties, sw_compdocs.component.TooltipProperties()
        )
        self.assertEqual(comp.logic_nodes, sw_compdocs.component.LogicNodeList())
        self.assertEqual(comp.voxel_min, sw_compdocs.component.VoxelPos())
        self.assertEqual(comp.voxel_max, sw_compdocs.component.VoxelPos())

    def test_exc_xml(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_elem", lxml.etree._Element),
                ("want_msg", str),
                ("want_xpath", str),
            ],
        )

        for tc in [
            tt(
                input_elem=lxml.etree.Element("definition", category="nan"),
                want_msg="invalid component category 'nan'",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", category="999"),
                want_msg="invalid component category '999'",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", mass="invalid"),
                want_msg="invalid component mass 'invalid'",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", value="nan"),
                want_msg="invalid component value 'nan'",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.Element("definition", flags="nan"),
                want_msg="invalid component flags 'nan'",
                want_xpath=".",
            ),
            tt(
                input_elem=lxml.etree.fromstring(
                    """<definition><logic_nodes><logic_node mode="999"/></logic_nodes></definition>"""
                ),
                want_msg="invalid logic node mode '999'",
                want_xpath="./logic_nodes/logic_node[1]",
            ),
            tt(
                input_elem=lxml.etree.fromstring(
                    """<definition><voxel_min x="nan"/></definition>"""
                ),
                want_msg="invalid voxel x 'nan'",
                want_xpath="./voxel_min",
            ),
            tt(
                input_elem=lxml.etree.fromstring(
                    """<definition><voxel_max x="nan"/></definition>"""
                ),
                want_msg="invalid voxel x 'nan'",
                want_xpath="./voxel_max",
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.component.ComponentXMLError) as ctx:
                    sw_compdocs.component.Definition.from_xml_elem(tc.input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, tc.want_xpath)


class TestDefinitionRepr(unittest.TestCase):
    def test(self) -> None:
        comp = sw_compdocs.component.Definition(
            cid="cid",
            name="name",
            category=sw_compdocs.component.Category.BLOCKS,
            mass=1.0,
            value=2,
            flags=sw_compdocs.component.Flags(0),
            tags="tags",
            tooltip_properties=sw_compdocs.component.TooltipProperties(),
            logic_nodes=sw_compdocs.component.LogicNodeList(),
            voxel_min=sw_compdocs.component.VoxelPos(x=0, y=1, z=2),
            voxel_max=sw_compdocs.component.VoxelPos(x=3, y=4, z=5),
        )
        self.assertEqual(
            repr(comp),
            "Definition(cid='cid', name='name', category=<Category.BLOCKS: 0>, mass=1.0, value=2, flags=<Flags: 0>, tags='tags', tooltip_properties=TooltipProperties(short_description='', description=''), logic_nodes=LogicNodeList([]), voxel_min=VoxelPos(x=0, y=1, z=2), voxel_max=VoxelPos(x=3, y=4, z=5))",
        )


class TestDefinitionEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.component.Definition),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=3.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=3,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        description="description"
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [sw_compdocs.component.LogicNode()]
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(z=1),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(z=1),
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.Definition(
                    cid="cid",
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=None,
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


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


class TestTooltipPropertiesInit(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_short_description", str),
                ("input_description", str),
                ("want_short_description", str),
                ("want_description", str),
            ],
        )

        for tc in [
            tt(
                input_short_description="",
                input_description="",
                want_short_description="",
                want_description="",
            ),
            tt(
                input_short_description="a",
                input_description="b",
                want_short_description="a",
                want_description="b",
            ),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component.TooltipProperties(
                    short_description=tc.input_short_description,
                    description=tc.input_description,
                )
                self.assertEqual(got.short_description, tc.want_short_description)
                self.assertEqual(got.description, tc.want_description)


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


class TestTooltipPropertiesRepr(unittest.TestCase):
    def test(self) -> None:
        tp = sw_compdocs.component.TooltipProperties(
            short_description="a", description="b"
        )
        self.assertEqual(
            repr(tp), "TooltipProperties(short_description='a', description='b')"
        )


class TestTooltipPropertiesEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.component.TooltipProperties),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="a", description="b"
                ),
                input_other=sw_compdocs.component.TooltipProperties(
                    short_description="a", description="b"
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="a", description="b"
                ),
                input_other=sw_compdocs.component.TooltipProperties(
                    short_description="c", description="b"
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="a", description="b"
                ),
                input_other=sw_compdocs.component.TooltipProperties(
                    short_description="a", description="c"
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="a", description="b"
                ),
                input_other="a",
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestTooltipPropertiesFullDescription(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.component.TooltipProperties),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="", description=""
                ),
                want_s="",
            ),
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="a", description=""
                ),
                want_s="a",
            ),
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="", description="b"
                ),
                want_s="b",
            ),
            tt(
                input_self=sw_compdocs.component.TooltipProperties(
                    short_description="a", description="b"
                ),
                want_s="a b",
            ),
        ]:
            with self.subTest(tc=tc):
                got_s = tc.input_self.full_description()
                self.assertEqual(got_s, tc.want_s)


class TestLogicNodeListInit(unittest.TestCase):
    def test_pass(self) -> None:
        ln_list = [
            sw_compdocs.component.LogicNode(label="a"),
            sw_compdocs.component.LogicNode(label="b"),
            sw_compdocs.component.LogicNode(label="c"),
            sw_compdocs.component.LogicNode(label="d"),
        ]
        lns = sw_compdocs.component.LogicNodeList(ln_list)
        self.assertEqual(lns._l, ln_list)


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
                with self.assertRaises(sw_compdocs.component.ComponentXMLError) as ctx:
                    sw_compdocs.component.LogicNodeList.from_xml_elem(input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, tc.want_xpath)


class TestLogicNodeInit(unittest.TestCase):
    def test_pass(self) -> None:
        ln = sw_compdocs.component.LogicNode(
            idx=52149,
            label="label",
            mode=sw_compdocs.component.LogicNodeMode.INPUT,
            type=sw_compdocs.component.LogicNodeType.FLOAT,
            description="description",
        )
        self.assertEqual(ln.idx, 52149)
        self.assertEqual(ln.label, "label")
        self.assertEqual(ln.mode, sw_compdocs.component.LogicNodeMode.INPUT)
        self.assertEqual(ln.type, sw_compdocs.component.LogicNodeType.FLOAT)
        self.assertEqual(ln.description, "description")


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
                with self.assertRaises(sw_compdocs.component.ComponentXMLError) as ctx:
                    sw_compdocs.component.LogicNode.from_xml_elem(tc.input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, ".")


class TestLogicNodeRepr(unittest.TestCase):
    def test(self) -> None:
        ln = sw_compdocs.component.LogicNode(
            idx=52149,
            label="label",
            mode=sw_compdocs.component.LogicNodeMode.INPUT,
            type=sw_compdocs.component.LogicNodeType.FLOAT,
            description="description",
        )
        self.assertEqual(
            repr(ln),
            f"LogicNode(idx=52149, label='label', mode={sw_compdocs.component.LogicNodeMode.INPUT!r}, type={sw_compdocs.component.LogicNodeType.FLOAT!r}, description='description')",
        )


class TestLogicNodeEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.component.LogicNode),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    idx=52150,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="labe1",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.TORQUE,
                    description="description",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="descriptiom",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    idx=52149,
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=None,
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


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


class TestVoxelPosInit(unittest.TestCase):
    def test_pass(self) -> None:
        pos = sw_compdocs.component.VoxelPos(x=1, y=2, z=3)
        self.assertEqual(pos.x, 1)
        self.assertEqual(pos.y, 2)
        self.assertEqual(pos.z, 3)


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
                with self.assertRaises(sw_compdocs.component.ComponentXMLError) as ctx:
                    sw_compdocs.component.VoxelPos.from_xml_elem(tc.input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, ".")


class TestVoxelPosRepr(unittest.TestCase):
    def test(self) -> None:
        pos = sw_compdocs.component.VoxelPos(x=1, y=2, z=3)
        self.assertEqual(str(pos), "VoxelPos(x=1, y=2, z=3)")


class TestVoxelPosEq(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_self", sw_compdocs.component.VoxelPos),
                ("input_other", object),
                ("want_eq", bool),
            ],
        )

        for tc in [
            tt(
                input_self=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                input_other=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                input_other=sw_compdocs.component.VoxelPos(x=0, y=2, z=3),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                input_other=sw_compdocs.component.VoxelPos(x=1, y=0, z=3),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                input_other=sw_compdocs.component.VoxelPos(x=1, y=2, z=0),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.VoxelPos(x=1, y=2, z=3),
                input_other=None,
                want_eq=False,
            ),
        ]:
            with self.subTest(tc=tc):
                got_eq = tc.input_self == tc.input_other
                self.assertEqual(got_eq, tc.want_eq)


class TestComponentXMLErrorInit(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.component.ComponentXMLError("msg")
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("msg",))
        self.assertEqual(exc.msg, "msg")
        self.assertEqual(exc.file, None)
        self.assertEqual(exc.xpath, ".")


class TestComponentXMLErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.component.ComponentXMLError("any useful message")
        exc.file = "01_block.xml"
        exc.prepend_xpath("logic_node[52149]")
        exc.prepend_xpath("logic_nodes")
        exc.prepend_xpath("definition")
        self.assertEqual(
            str(exc),
            "01_block.xml: ./definition/logic_nodes/logic_node[52149]: any useful message",
        )

    def test_table(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_file", sw_compdocs._types.StrOrBytesPath | None),
                ("want_s", str),
            ],
        )

        exc = sw_compdocs.component.ComponentXMLError("msg")
        for tc in [
            tt(input_file=None, want_s="<component.xml>: .: msg"),
            tt(input_file="str", want_s="str: .: msg"),
            tt(input_file=b"bytes", want_s="bytes: .: msg"),
            tt(input_file=pathlib.PurePath("pathlike"), want_s="pathlike: .: msg"),
        ]:
            with self.subTest(tc=tc):
                exc.file = tc.input_file
                got_s = str(exc)
                self.assertEqual(got_s, tc.want_s)


class TestComponentXMLErrorPrependXPath(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.component.ComponentXMLError("msg")
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
        exc = sw_compdocs.component.ComponentXMLError("msg")
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
                exc = sw_compdocs.component.ComponentXMLError("msg")
                with self.assertRaises(ValueError):
                    exc.prepend_xpath(s)


class TestCoalesce(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_value", object | None),
                ("input_default", object),
                ("want", object),
            ],
        )

        for tc in [
            tt(input_value=0, input_default=1, want=0),
            tt(input_value=None, input_default=1, want=1),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component._coalesce(tc.input_value, tc.input_default)
                self.assertEqual(got, tc.want)
