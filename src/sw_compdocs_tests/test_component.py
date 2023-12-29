import collections
import pathlib
import sw_compdocs.component
import unittest
import xml.etree.ElementTree


class TestDefinitionInit(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt",
            (
                "input_name",
                "input_category",
                "input_mass",
                "input_value",
                "input_flags",
                "input_tags",
                "input_tooltip_properties",
                "input_logic_nodes",
                "input_voxel_min",
                "input_voxel_max",
                "want_name",
                "want_category",
                "want_mass",
                "want_value",
                "want_flags",
                "want_tags",
                "want_tooltip_properties",
                "want_logic_nodes",
                "want_voxel_min",
                "want_voxel_max",
            ),
        )

        for tc in [
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
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
                want_name="Clock",
                want_category=sw_compdocs.component.Category.DISPLAYS,
                want_mass=1,
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
            tt(
                input_name=None,
                input_category=None,
                input_mass=None,
                input_value=None,
                input_flags=None,
                input_tags=None,
                input_tooltip_properties=None,
                input_logic_nodes=None,
                input_voxel_min=None,
                input_voxel_max=None,
                want_name="",
                want_category=sw_compdocs.component.Category.BLOCKS,
                want_mass=0,
                want_value=0,
                want_flags=sw_compdocs.component.Flags(0),
                want_tags="",
                want_tooltip_properties=sw_compdocs.component.TooltipProperties(),
                want_logic_nodes=sw_compdocs.component.LogicNodeList(),
                want_voxel_min=sw_compdocs.component.VoxelPos(),
                want_voxel_max=sw_compdocs.component.VoxelPos(),
            ),
        ]:
            with self.subTest(tc=tc):
                got_comp = sw_compdocs.component.Definition(
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

    def test_exc_type(self):
        tt = collections.namedtuple(
            "tt",
            (
                "input_name",
                "input_category",
                "input_mass",
                "input_value",
                "input_flags",
                "input_tags",
                "input_tooltip_properties",
                "input_logic_nodes",
                "input_voxel_min",
                "input_voxel_max",
            ),
        )

        for tc in [
            tt(
                input_name=b"Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
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
            ),
            tt(
                input_name="Clock",
                input_category=6,
                input_mass=1,
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
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass="1",
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
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
                input_value="100",
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
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
                input_value=100,
                input_flags=8192,
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
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
                input_value=100,
                input_flags=sw_compdocs.component.Flags(8192),
                input_tags=b"basic",
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
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
                input_value=100,
                input_flags=sw_compdocs.component.Flags(8192),
                input_tags="basic",
                input_tooltip_properties="An analogue clock display that outputs a number value representing the time of day.",
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
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
                input_value=100,
                input_flags=sw_compdocs.component.Flags(8192),
                input_tags="basic",
                input_tooltip_properties=sw_compdocs.component.TooltipProperties(
                    short_description="An analogue clock display that outputs a number value representing the time of day.",
                    description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                ),
                input_logic_nodes=[
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
                ],
                input_voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                input_voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
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
                input_voxel_min=(0, 0, 0),
                input_voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
            ),
            tt(
                input_name="Clock",
                input_category=sw_compdocs.component.Category.DISPLAYS,
                input_mass=1,
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
                input_voxel_max=(0, 1, 0),
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(TypeError):
                    sw_compdocs.component.Definition(
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


class TestDefinitionNameSetter(unittest.TestCase):
    def test_pass(self):
        comp = sw_compdocs.component.Definition()
        comp.name = "name"
        self.assertEqual(comp.name, "name")

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.name = None


class TestDefinitionCategorySetter(unittest.TestCase):
    def test_pass(self):
        comp = sw_compdocs.component.Definition()
        comp.category = sw_compdocs.component.Category.VEHICLE_CONTROL
        self.assertEqual(comp.category, sw_compdocs.component.Category.VEHICLE_CONTROL)

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.category = None


class TestDefinitionMassSetter(unittest.TestCase):
    def test_pass(self):
        comp = sw_compdocs.component.Definition()
        comp.mass = 52149
        self.assertEqual(comp.mass, 52149)

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.mass = None


class TestDefinitionValueSetter(unittest.TestCase):
    def test_pass(self):
        comp = sw_compdocs.component.Definition()
        comp.value = 52149
        self.assertEqual(comp.value, 52149)

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.value = None


class TestDefinitionFlagsSetter(unittest.TestCase):
    def test_pass(self):
        comp = sw_compdocs.component.Definition()
        comp.flags = sw_compdocs.component.Flags(8192)
        self.assertEqual(comp.flags, sw_compdocs.component.Flags(8192))

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.flags = None


class TestDefinitionTagsSetter(unittest.TestCase):
    def test_pass(self):
        comp = sw_compdocs.component.Definition()
        comp.tags = "basic"
        self.assertEqual(comp.tags, "basic")

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.tags = None


class TestDefinitionTooltipPropertiesSetter(unittest.TestCase):
    def test_pass(self):
        tooltip_properties = sw_compdocs.component.TooltipProperties()

        comp = sw_compdocs.component.Definition()
        comp.tooltip_properties = tooltip_properties
        self.assertIs(comp.tooltip_properties, tooltip_properties)

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.tooltip_properties = None


class TestDefinitionLogicNodesSetter(unittest.TestCase):
    def test_pass(self):
        logic_nodes = sw_compdocs.component.LogicNodeList()

        comp = sw_compdocs.component.Definition()
        comp.logic_nodes = logic_nodes
        self.assertIs(comp.logic_nodes, logic_nodes)

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.logic_nodes = None


class TestDefinitionVoxelMinSetter(unittest.TestCase):
    def test_pass(self):
        voxel_min = sw_compdocs.component.VoxelPos()

        comp = sw_compdocs.component.Definition()
        comp.voxel_min = voxel_min
        self.assertIs(comp.voxel_min, voxel_min)

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.voxel_min = None


class TestDefinitionVoxelMaxSetter(unittest.TestCase):
    def test_pass(self):
        voxel_max = sw_compdocs.component.VoxelPos()

        comp = sw_compdocs.component.Definition()
        comp.voxel_max = voxel_max
        self.assertIs(comp.voxel_max, voxel_max)

    def test_exc_type(self):
        comp = sw_compdocs.component.Definition()
        with self.assertRaises(TypeError):
            comp.voxel_max = None


class TestDefinitionFromXMLElem(unittest.TestCase):
    def test_pass_clock(self):
        elem = xml.etree.ElementTree.fromstring(
            """\
<?xml version="1.0" encoding="UTF-8"?>
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

        comp = sw_compdocs.component.Definition.from_xml_elem(elem)
        self.assertEqual(comp.name, "Clock")
        self.assertEqual(comp.category, sw_compdocs.component.Category.DISPLAYS)
        self.assertEqual(comp.mass, 1)
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
        )
        self.assertEqual(comp.voxel_min, sw_compdocs.component.VoxelPos(x=0, y=0, z=0))
        self.assertEqual(comp.voxel_max, sw_compdocs.component.VoxelPos(x=0, y=1, z=0))

    def test_pass_empty(self):
        elem = xml.etree.ElementTree.Element("definition")
        comp = sw_compdocs.component.Definition.from_xml_elem(elem)
        self.assertEqual(comp.name, "")
        self.assertEqual(comp.category, sw_compdocs.component.Category.BLOCKS)
        self.assertEqual(comp.mass, 0)
        self.assertEqual(comp.value, 0)
        self.assertEqual(comp.flags, sw_compdocs.component.Flags(0))
        self.assertEqual(comp.tags, "")
        self.assertEqual(
            comp.tooltip_properties, sw_compdocs.component.TooltipProperties()
        )
        self.assertEqual(comp.logic_nodes, sw_compdocs.component.LogicNodeList())
        self.assertEqual(comp.voxel_min, sw_compdocs.component.VoxelPos())
        self.assertEqual(comp.voxel_max, sw_compdocs.component.VoxelPos())

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.component.Definition.from_xml_elem(None)

    def test_exc_xml(self):
        tt = collections.namedtuple("tt", ("input_elem", "want_msg", "want_xpath"))

        for tc in [
            tt(
                input_elem=xml.etree.ElementTree.Element("definition", category="nan"),
                want_msg="invalid component category 'nan'",
                want_xpath=".",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element("definition", category="999"),
                want_msg="invalid component category '999'",
                want_xpath=".",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element("definition", mass="nan"),
                want_msg="invalid component mass 'nan'",
                want_xpath=".",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element("definition", value="nan"),
                want_msg="invalid component value 'nan'",
                want_xpath=".",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element("definition", flags="nan"),
                want_msg="invalid component flags 'nan'",
                want_xpath=".",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element("definition", flags="999"),
                want_msg="invalid component flags '999'",
                want_xpath=".",
            ),
            tt(
                input_elem=xml.etree.ElementTree.fromstring(
                    """<definition><logic_nodes><logic_node mode="999"/></logic_nodes></definition>"""
                ),
                want_msg="invalid logic node mode '999'",
                want_xpath="./logic_nodes/logic_node[1]",
            ),
            tt(
                input_elem=xml.etree.ElementTree.fromstring(
                    """<definition><voxel_min x="nan"/></definition>"""
                ),
                want_msg="invalid voxel x 'nan'",
                want_xpath="./voxel_min",
            ),
            tt(
                input_elem=xml.etree.ElementTree.fromstring(
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
    def test(self):
        comp = sw_compdocs.component.Definition(
            name="name",
            category=sw_compdocs.component.Category.BLOCKS,
            mass=1,
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
            "Definition(name='name', category=<Category.BLOCKS: 0>, mass=1, value=2, flags=<Flags: 0>, tags='tags', tooltip_properties=TooltipProperties(short_description='', description=''), logic_nodes=LogicNodeList([]), voxel_min=VoxelPos(x=0, y=1, z=2), voxel_max=VoxelPos(x=3, y=4, z=5))",
        )


class TestDefinitionEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        for tc in [
            tt(
                input_self=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=3,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
                    value=2,
                    flags=sw_compdocs.component.Flags(0),
                    tags="tags",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(),
                    voxel_max=sw_compdocs.component.VoxelPos(),
                ),
                input_other=sw_compdocs.component.Definition(
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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
                    name="name",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1,
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


class TestTooltipPropertiesInit(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt",
            (
                "input_short_description",
                "input_description",
                "want_short_description",
                "want_description",
            ),
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
            tt(
                input_short_description=None,
                input_description="b",
                want_short_description="",
                want_description="b",
            ),
            tt(
                input_short_description="a",
                input_description=None,
                want_short_description="a",
                want_description="",
            ),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component.TooltipProperties(
                    short_description=tc.input_short_description,
                    description=tc.input_description,
                )
                self.assertEqual(got.short_description, tc.want_short_description)
                self.assertEqual(got.description, tc.want_description)

    def test_exc_type(self):
        tt = collections.namedtuple(
            "tt", ("input_short_description", "input_description")
        )

        for tc in [
            tt(input_short_description=0, input_description=""),
            tt(input_short_description="", input_description=0),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(TypeError):
                    sw_compdocs.component.TooltipProperties(
                        short_description=tc.input_short_description,
                        description=tc.input_description,
                    )


class TestTooltipPropertiesShortDescriptionSetter(unittest.TestCase):
    def test_pass(self):
        tp = sw_compdocs.component.TooltipProperties()
        tp.short_description = "a"
        self.assertEqual(tp.short_description, "a")

    def test_exc_type(self):
        tp = sw_compdocs.component.TooltipProperties()
        with self.assertRaises(TypeError):
            tp.short_description = None


class TestTooltipPropertiesDescriptionSetter(unittest.TestCase):
    def test_pass(self):
        tp = sw_compdocs.component.TooltipProperties()
        tp.description = "b"
        self.assertEqual(tp.description, "b")

    def test_exc_type(self):
        tp = sw_compdocs.component.TooltipProperties()
        with self.assertRaises(TypeError):
            tp.description = None


class TestTooltipPropertiesFromXMLElem(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt", ("input_elem", "want_short_description", "want_description")
        )

        for tc in [
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "tooltip_properties", short_description="a", description="b"
                ),
                want_short_description="a",
                want_description="b",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "tooltip_properties", description="b"
                ),
                want_short_description="",
                want_description="b",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
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

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.component.TooltipProperties.from_xml_elem(None)


class TestTooltipPropertiesRepr(unittest.TestCase):
    def test(self):
        tp = sw_compdocs.component.TooltipProperties(
            short_description="a", description="b"
        )
        self.assertEqual(
            repr(tp), "TooltipProperties(short_description='a', description='b')"
        )


class TestTooltipPropertiesEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

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
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "want_s"))

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
    def test_pass(self):
        lns = sw_compdocs.component.LogicNodeList(
            [
                sw_compdocs.component.LogicNode(label="a"),
                sw_compdocs.component.LogicNode(label="b"),
                sw_compdocs.component.LogicNode(label="c"),
                sw_compdocs.component.LogicNode(label="d"),
            ]
        )
        self.assertEqual(
            lns[:],
            [
                sw_compdocs.component.LogicNode(label="a"),
                sw_compdocs.component.LogicNode(label="b"),
                sw_compdocs.component.LogicNode(label="c"),
                sw_compdocs.component.LogicNode(label="d"),
            ],
        )

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.component.LogicNodeList(
                [
                    sw_compdocs.component.LogicNode(label="a"),
                    sw_compdocs.component.LogicNode(label="b"),
                    sw_compdocs.component.LogicNode(label="c"),
                    None,
                ]
            )


class TestLogicNodeListFromXMLElem(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_sub_list", "want_lns"))

        for tc in [
            tt(
                input_sub_list=[],
                want_lns=sw_compdocs.component.LogicNodeList(),
            ),
            tt(
                input_sub_list=[
                    xml.etree.ElementTree.Element("logic_node", label="a"),
                    xml.etree.ElementTree.Element("logic_node", label="b"),
                    xml.etree.ElementTree.Element("logic_node", label="c"),
                ],
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(label="a"),
                        sw_compdocs.component.LogicNode(label="b"),
                        sw_compdocs.component.LogicNode(label="c"),
                    ]
                ),
            ),
            tt(
                input_sub_list=[
                    xml.etree.ElementTree.Element("logic_node", label="a"),
                    xml.etree.ElementTree.Element("dummy", label="b"),
                    xml.etree.ElementTree.Element("logic_node", label="c"),
                ],
                want_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(label="a"),
                        sw_compdocs.component.LogicNode(label="c"),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                input_elem = xml.etree.ElementTree.Element("logic_nodes")
                input_elem.extend(tc.input_sub_list)
                got_lns = sw_compdocs.component.LogicNodeList.from_xml_elem(input_elem)
                self.assertEqual(got_lns, tc.want_lns)

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.component.LogicNodeList.from_xml_elem(None)

    def test_exc_xml(self):
        tt = collections.namedtuple("tt", ("input_sub_list", "want_msg", "want_xpath"))

        for tc in [
            tt(
                input_sub_list=[
                    xml.etree.ElementTree.Element("logic_node", type="-1"),
                    xml.etree.ElementTree.Element("logic_node", type="1"),
                    xml.etree.ElementTree.Element("logic_node", type="2"),
                ],
                want_msg="invalid logic node type '-1'",
                want_xpath="./logic_node[1]",
            ),
            tt(
                input_sub_list=[
                    xml.etree.ElementTree.Element("logic_node", type="0"),
                    xml.etree.ElementTree.Element("logic_node", type="-1"),
                    xml.etree.ElementTree.Element("logic_node", type="2"),
                ],
                want_msg="invalid logic node type '-1'",
                want_xpath="./logic_node[2]",
            ),
            tt(
                input_sub_list=[
                    xml.etree.ElementTree.Element("logic_node", type="0"),
                    xml.etree.ElementTree.Element("logic_node", type="1"),
                    xml.etree.ElementTree.Element("logic_node", type="-1"),
                ],
                want_msg="invalid logic node type '-1'",
                want_xpath="./logic_node[3]",
            ),
        ]:
            with self.subTest(tc=tc):
                input_elem = xml.etree.ElementTree.Element("logic_nodes")
                input_elem.extend(tc.input_sub_list)
                with self.assertRaises(sw_compdocs.component.ComponentXMLError) as ctx:
                    sw_compdocs.component.LogicNodeList.from_xml_elem(input_elem)
                self.assertEqual(ctx.exception.msg, tc.want_msg)
                self.assertEqual(ctx.exception.file, None)
                self.assertEqual(ctx.exception.xpath, tc.want_xpath)


class TestLogicNodeInit(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt",
            (
                "input_label",
                "input_mode",
                "input_type",
                "input_description",
                "want_label",
                "want_mode",
                "want_type",
                "want_description",
            ),
        )

        for tc in [
            tt(
                input_label="label",
                input_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                input_description="description",
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.FLOAT,
                want_description="description",
            ),
            tt(
                input_label=None,
                input_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                input_description="description",
                want_label="",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.FLOAT,
                want_description="description",
            ),
            tt(
                input_label="label",
                input_mode=None,
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                input_description="description",
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                want_type=sw_compdocs.component.LogicNodeType.FLOAT,
                want_description="description",
            ),
            tt(
                input_label="label",
                input_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                input_type=None,
                input_description="description",
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.BOOL,
                want_description="description",
            ),
            tt(
                input_label="label",
                input_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                input_description=None,
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.FLOAT,
                want_description="",
            ),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component.LogicNode(
                    label=tc.input_label,
                    mode=tc.input_mode,
                    type=tc.input_type,
                    description=tc.input_description,
                )
                self.assertEqual(got.label, tc.want_label)
                self.assertEqual(got.mode, tc.want_mode)
                self.assertEqual(got.type, tc.want_type)
                self.assertEqual(got.description, tc.want_description)

    def test_exc_type(self):
        tt = collections.namedtuple(
            "tt", ("input_label", "input_mode", "input_type", "input_description")
        )

        for tc in [
            tt(
                input_label=0,
                input_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                input_description="description",
            ),
            tt(
                input_label="label",
                input_mode=0,
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                input_description="description",
            ),
            tt(
                input_label="label",
                input_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                input_type=0,
                input_description="description",
            ),
            tt(
                input_label="label",
                input_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                input_type=sw_compdocs.component.LogicNodeType.FLOAT,
                input_description=0,
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(TypeError):
                    sw_compdocs.component.LogicNode(
                        label=tc.input_label,
                        mode=tc.input_mode,
                        type=tc.input_type,
                        description=tc.input_description,
                    )


class TestLogicNodeLabelSetter(unittest.TestCase):
    def test_pass(self):
        ln = sw_compdocs.component.LogicNode()
        ln.label = "label"
        self.assertEqual(ln.label, "label")

    def test_exc_type(self):
        ln = sw_compdocs.component.LogicNode()
        with self.assertRaises(TypeError):
            ln.label = None


class TestLogicNodeModeSetter(unittest.TestCase):
    def test_pass(self):
        ln = sw_compdocs.component.LogicNode()
        ln.mode = sw_compdocs.component.LogicNodeMode.INPUT
        self.assertEqual(ln.mode, sw_compdocs.component.LogicNodeMode.INPUT)

    def test_exc_type(self):
        ln = sw_compdocs.component.LogicNode()
        with self.assertRaises(TypeError):
            ln.mode = None


class TestLogicNodeTypeSetter(unittest.TestCase):
    def test_pass(self):
        ln = sw_compdocs.component.LogicNode()
        ln.type = sw_compdocs.component.LogicNodeType.FLOAT
        self.assertEqual(ln.type, sw_compdocs.component.LogicNodeType.FLOAT)

    def test_exc_type(self):
        ln = sw_compdocs.component.LogicNode()
        with self.assertRaises(TypeError):
            ln.type = None


class TestLogicNodeDescriptionSetter(unittest.TestCase):
    def test_pass(self):
        ln = sw_compdocs.component.LogicNode()
        ln.description = "description"
        self.assertEqual(ln.description, "description")

    def test_exc_type(self):
        ln = sw_compdocs.component.LogicNode()
        with self.assertRaises(TypeError):
            ln.description = None


class TestLogicNodeFromXMLElem(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt",
            ("input_elem", "want_label", "want_mode", "want_type", "want_description"),
        )

        for tc in [
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="2",
                    description="description",
                ),
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="description",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    mode="1",
                    type="2",
                    description="description",
                ),
                want_label="",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="description",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    label="label",
                    type="2",
                    description="description",
                ),
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="description",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    description="description",
                ),
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.BOOL,
                want_description="description",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="2",
                ),
                want_label="label",
                want_mode=sw_compdocs.component.LogicNodeMode.INPUT,
                want_type=sw_compdocs.component.LogicNodeType.TORQUE,
                want_description="",
            ),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component.LogicNode.from_xml_elem(tc.input_elem)
                self.assertEqual(got.label, tc.want_label)
                self.assertEqual(got.mode, tc.want_mode)
                self.assertEqual(got.type, tc.want_type)
                self.assertEqual(got.description, tc.want_description)

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.component.LogicNode.from_xml_elem(None)

    def test_exc_xml(self):
        tt = collections.namedtuple("tt", ("input_elem", "want_msg"))

        for tc in [
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    label="label",
                    mode="a",
                    type="2",
                    description="description",
                ),
                want_msg="invalid logic node mode 'a'",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    label="label",
                    mode="2",
                    type="2",
                    description="description",
                ),
                want_msg="invalid logic node mode '2'",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "logic_node",
                    label="label",
                    mode="1",
                    type="a",
                    description="description",
                ),
                want_msg="invalid logic node type 'a'",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
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
    def test(self):
        ln = sw_compdocs.component.LogicNode(
            label="label",
            mode=sw_compdocs.component.LogicNodeMode.INPUT,
            type=sw_compdocs.component.LogicNodeType.FLOAT,
            description="description",
        )
        self.assertEqual(
            repr(ln),
            f"LogicNode(label='label', mode={sw_compdocs.component.LogicNodeMode.INPUT!r}, type={sw_compdocs.component.LogicNodeType.FLOAT!r}, description='description')",
        )


class TestLogicNodeEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

        for tc in [
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                want_eq=True,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    label="labe1",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.TORQUE,
                    description="description",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="description",
                ),
                input_other=sw_compdocs.component.LogicNode(
                    label="label",
                    mode=sw_compdocs.component.LogicNodeMode.INPUT,
                    type=sw_compdocs.component.LogicNodeType.FLOAT,
                    description="descriptiom",
                ),
                want_eq=False,
            ),
            tt(
                input_self=sw_compdocs.component.LogicNode(
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


class TestVoxelPosInit(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple(
            "tt", ("input_x", "input_y", "input_z", "want_x", "want_y", "want_z")
        )

        for tc in [
            tt(input_x=1, input_y=2, input_z=3, want_x=1, want_y=2, want_z=3),
            tt(input_x=None, input_y=2, input_z=3, want_x=0, want_y=2, want_z=3),
            tt(input_x=1, input_y=None, input_z=3, want_x=1, want_y=0, want_z=3),
            tt(input_x=1, input_y=2, input_z=None, want_x=1, want_y=2, want_z=0),
        ]:
            with self.subTest(tc=tc):
                pos = sw_compdocs.component.VoxelPos(
                    x=tc.input_x, y=tc.input_y, z=tc.input_z
                )
                self.assertEqual(pos.x, tc.want_x)
                self.assertEqual(pos.y, tc.want_y)
                self.assertEqual(pos.z, tc.want_z)

    def test_exc_type(self):
        tt = collections.namedtuple("tt", ("input_x", "input_y", "input_z"))

        for tc in [
            tt(input_x="1", input_y=2, input_z=3),
            tt(input_x=1, input_y="2", input_z=3),
            tt(input_x=1, input_y=2, input_z="3"),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(TypeError):
                    sw_compdocs.component.VoxelPos(
                        x=tc.input_x, y=tc.input_y, z=tc.input_z
                    )


class TestVoxelPosXSetter(unittest.TestCase):
    def test_pass(self):
        pos = sw_compdocs.component.VoxelPos()
        pos.x = 52149
        self.assertEqual(pos.x, 52149)

    def test_exc_type(self):
        pos = sw_compdocs.component.VoxelPos(x=52149)
        with self.assertRaises(TypeError):
            pos.x = None
        self.assertEqual(pos.x, 52149)


class TestVoxelPosYSetter(unittest.TestCase):
    def test_pass(self):
        pos = sw_compdocs.component.VoxelPos()
        pos.y = 52149
        self.assertEqual(pos.y, 52149)

    def test_exc_type(self):
        pos = sw_compdocs.component.VoxelPos(y=52149)
        with self.assertRaises(TypeError):
            pos.y = None
        self.assertEqual(pos.y, 52149)


class TestVoxelPosZSetter(unittest.TestCase):
    def test_pass(self):
        pos = sw_compdocs.component.VoxelPos()
        pos.z = 52149
        self.assertEqual(pos.z, 52149)

    def test_exc_type(self):
        pos = sw_compdocs.component.VoxelPos(z=52149)
        with self.assertRaises(TypeError):
            pos.z = None
        self.assertEqual(pos.z, 52149)


class TestVoxelPosFromXMLElem(unittest.TestCase):
    def test_pass(self):
        tt = collections.namedtuple("tt", ("input_elem", "want_x", "want_y", "want_z"))

        for tc in [
            tt(
                input_elem=xml.etree.ElementTree.Element(
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
                input_elem=xml.etree.ElementTree.Element(
                    "voxel_max",
                    y="2",
                    z="3",
                ),
                want_x=0,
                want_y=2,
                want_z=3,
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "voxel_max",
                    x="1",
                    z="3",
                ),
                want_x=1,
                want_y=0,
                want_z=3,
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
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

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.component.VoxelPos.from_xml_elem(None)

    def test_exc_xml(self):
        tt = collections.namedtuple("tt", ("input_elem", "want_msg"))

        for tc in [
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "voxel_max", x="", y="2", z="3"
                ),
                want_msg="invalid voxel x ''",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "voxel_max", x="1", y="", z="3"
                ),
                want_msg="invalid voxel y ''",
            ),
            tt(
                input_elem=xml.etree.ElementTree.Element(
                    "voxel_max", x="1", y="2", z=""
                ),
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
    def test(self):
        pos = sw_compdocs.component.VoxelPos(x=1, y=2, z=3)
        self.assertEqual(str(pos), "VoxelPos(x=1, y=2, z=3)")


class TestVoxelPosEq(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_self", "input_other", "want_eq"))

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
    def test_pass(self):
        exc = sw_compdocs.component.ComponentXMLError("msg")
        self.assertEqual(exc.args, ("msg",))
        self.assertEqual(exc.msg, "msg")
        self.assertEqual(exc.file, None)
        self.assertEqual(exc.xpath, ".")

    def test_exc_type(self):
        with self.assertRaises(TypeError):
            sw_compdocs.component.ComponentXMLError(None)


class TestComponentXMLErrorFileSetter(unittest.TestCase):
    def test_pass(self):
        for file in ["file", b"file", pathlib.PurePath("file")]:
            with self.subTest(file=file):
                exc = sw_compdocs.component.ComponentXMLError("msg")
                exc.file = file
                self.assertIs(exc.file, file)

    def test_pass_none(self):
        exc = sw_compdocs.component.ComponentXMLError("msg")
        self.assertEqual(exc.file, None)

        exc.file = "file"
        self.assertEqual(exc.file, "file")

        exc.file = None
        self.assertEqual(exc.file, None)

    def test_exc_type(self):
        exc = sw_compdocs.component.ComponentXMLError("msg")
        with self.assertRaises(TypeError):
            exc.file = 0


class TestComponentXMLErrorStr(unittest.TestCase):
    def test(self):
        exc = sw_compdocs.component.ComponentXMLError("any useful message")
        exc.file = "01_block.xml"
        exc.prepend_xpath("logic_node[52149]")
        exc.prepend_xpath("logic_nodes")
        exc.prepend_xpath("definition")
        self.assertEqual(
            str(exc),
            "01_block.xml: ./definition/logic_nodes/logic_node[52149]: any useful message",
        )

    def test_table(self):
        tt = collections.namedtuple("tt", ("input_file", "want_s"))

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
    def test_pass(self):
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

    def test_exc_runtime(self):
        exc = sw_compdocs.component.ComponentXMLError("msg")
        exc.prepend_xpath("xpath")
        exc.prepend_xpath("/")
        self.assertEqual(exc.xpath, "/xpath")

        for s in ["root", "/", "value/error", None]:
            with self.subTest(s=s):
                with self.assertRaises(RuntimeError):
                    exc.prepend_xpath(s)
                self.assertEqual(exc.xpath, "/xpath")

    def test_exc_type(self):
        exc = sw_compdocs.component.ComponentXMLError("msg")
        with self.assertRaises(TypeError):
            exc.prepend_xpath(None)

    def test_exc_value(self):
        for s in ["", "logic_nodes/logic_node[52149]"]:
            with self.subTest(s=s):
                exc = sw_compdocs.component.ComponentXMLError("msg")
                with self.assertRaises(ValueError):
                    exc.prepend_xpath(s)


class TestCoalesce(unittest.TestCase):
    def test(self):
        tt = collections.namedtuple("tt", ("input_value", "input_default", "want"))

        for tc in [
            tt(input_value=0, input_default=1, want=0),
            tt(input_value=None, input_default=1, want=1),
        ]:
            with self.subTest(tc=tc):
                got = sw_compdocs.component._coalesce(tc.input_value, tc.input_default)
                self.assertEqual(got, tc.want)
