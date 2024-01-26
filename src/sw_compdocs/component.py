import enum
import lxml.etree
import os
import pathlib
import re

from . import container
from . import validator


def _coalesce(value, default):
    if value is None:
        return default
    return value


class ComponentXMLError(Exception):
    @property
    def msg(self):
        return self._msg

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if value is not None and not validator.is_pathlike(value):
            raise TypeError
        self._file = value

    @property
    def xpath(self):
        return self._xpath

    def __init__(self, msg):
        if type(msg) is not str:
            raise TypeError

        super().__init__(msg)
        self._msg = msg
        self._file = None
        self._xpath = "."
        self._xpath_list = []

    def __str__(self):
        file = os.fsdecode(self.file) if self.file is not None else "<component.xml>"
        return f"{file}: {self.xpath}: {self.msg}"

    def prepend_xpath(self, s):
        if len(self._xpath_list) >= 1 and self._xpath_list[0] == "/":
            raise RuntimeError

        if type(s) is not str:
            raise TypeError

        if s == "/":
            self._xpath_list.insert(0, s)
            self._xpath = "/" + "/".join(self._xpath_list[1:])
            return
        if s != "" and s.find("/") == -1:
            self._xpath_list.insert(0, s)
            self._xpath = "./" + "/".join(self._xpath_list)
            return
        raise ValueError


def generate_cid(file):
    if not isinstance(file, pathlib.PurePath):
        file = os.fsdecode(file)
        file = pathlib.PurePath(file)
    name = file.name

    # Using regular expression instead of file.stem because pathlib.PurePath.stem does
    # not match the behavior of Stormworks. For example, pathlib.PurePath(".xml").stem
    # produces ".xml", while Stormworks produces "".
    stem = re.sub(r"\.[^.]*\Z", "", name)
    return stem


@enum.unique
class Category(enum.Enum):
    BLOCKS = 0
    VEHICLE_CONTROL = 1
    MECHANICS = 2
    PROPULSION = 3
    SPECIALIST_EQUIPMENT = 4
    LOGIC = 5
    DISPLAYS = 6
    SENSORS = 7
    DECORATIVE = 8
    FLUID = 9
    ELECTRIC = 10
    JET_ENGINES = 11
    WEAPONS = 12
    MODULAR_ENGINES = 13
    INDUSTRY = 14
    WINDOWS = 15

    def __str__(self):
        if self is self.BLOCKS:
            return "Blocks"
        if self is self.VEHICLE_CONTROL:
            return "Vehicle Control"
        if self is self.MECHANICS:
            return "Mechanics"
        if self is self.PROPULSION:
            return "Propulsion"
        if self is self.SPECIALIST_EQUIPMENT:
            return "Specialist Equipment"
        if self is self.LOGIC:
            return "Logic"
        if self is self.DISPLAYS:
            return "Displays"
        if self is self.SENSORS:
            return "Sensors"
        if self is self.DECORATIVE:
            return "Decorative"
        if self is self.FLUID:
            return "Fluid"
        if self is self.ELECTRIC:
            return "Electric"
        if self is self.JET_ENGINES:
            return "Jet Engines"
        if self is self.WEAPONS:
            return "Weapons"
        if self is self.MODULAR_ENGINES:
            return "Modular Engines"
        if self is self.INDUSTRY:
            return "Industry"
        if self is self.WINDOWS:
            return "Windows"
        raise Exception


@enum.unique
class Flags(enum.Flag, boundary=enum.KEEP):
    IS_DEPRECATED = 1 << 29


class TooltipProperties:
    @property
    def short_description(self):
        return self._short_description

    @short_description.setter
    def short_description(self, value):
        if type(value) is not str:
            raise TypeError
        self._short_description = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if type(value) is not str:
            raise TypeError
        self._description = value

    def __init__(self, *, short_description=None, description=None):
        self.short_description = _coalesce(short_description, "")
        self.description = _coalesce(description, "")

    @classmethod
    def from_xml_elem(cls, elem):
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        return cls(
            short_description=elem.get("short_description"),
            description=elem.get("description"),
        )

    def __repr__(self):
        return f"{type(self).__name__}(short_description={self.short_description!r}, description={self.description!r})"

    def __eq__(self, other):
        if type(self) is type(other):
            return (
                self.short_description == other.short_description
                and self.description == other.description
            )
        return super().__eq__(other)

    def full_description(self):
        if self.short_description == "" and self.description == "":
            return ""
        elif self.short_description == "":
            return self.description
        elif self.description == "":
            return self.short_description
        return self.short_description + " " + self.description


@enum.unique
class LogicNodeMode(enum.Enum):
    OUTPUT = 0
    INPUT = 1


@enum.unique
class LogicNodeType(enum.Enum):
    BOOL = 0
    FLOAT = 1
    TORQUE = 2
    WATER = 3
    ELECTRIC = 4
    COMPOSITE = 5
    VIDEO = 6
    AUDIO = 7
    ROPE = 8

    def __str__(self):
        if self is self.BOOL:
            return "on/off"
        if self is self.FLOAT:
            return "number"
        if self is self.TORQUE:
            return "power"
        if self is self.WATER:
            return "fluid"
        if self is self.ELECTRIC:
            return "electric"
        if self is self.COMPOSITE:
            return "composite"
        if self is self.VIDEO:
            return "video"
        if self is self.AUDIO:
            return "audio"
        if self is self.ROPE:
            return "rope"
        raise Exception


class LogicNode:
    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, value):
        if type(value) is not int:
            raise TypeError
        if value < 0:
            raise ValueError
        self._idx = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if type(value) is not str:
            raise TypeError
        self._label = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if type(value) is not LogicNodeMode:
            raise TypeError
        self._mode = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if type(value) is not LogicNodeType:
            raise TypeError
        self._type = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if type(value) is not str:
            raise TypeError
        self._description = value

    def __init__(self, *, idx=None, label=None, mode=None, type=None, description=None):
        self.idx = _coalesce(idx, 0)
        self.label = _coalesce(label, "")
        self.mode = _coalesce(mode, LogicNodeMode.OUTPUT)
        self.type = _coalesce(type, LogicNodeType.BOOL)
        self.description = _coalesce(description, "")

    @classmethod
    def from_xml_elem(cls, elem, *, idx=None):
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        label = elem.get("label")
        mode = elem.get("mode")
        typo = elem.get("type")
        description = elem.get("description")

        if mode is not None:
            mode_raw = mode
            try:
                mode = int(mode, base=10)
                mode = LogicNodeMode(mode)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid logic node mode {mode_raw!r}"
                ) from exc

        if typo is not None:
            typo_raw = typo
            try:
                typo = int(typo, base=10)
                typo = LogicNodeType(typo)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid logic node type {typo_raw!r}"
                ) from exc

        return cls(idx=idx, label=label, mode=mode, type=typo, description=description)

    def __repr__(self):
        return f"{type(self).__name__}(idx={self.idx!r}, label={self.label!r}, mode={self.mode!r}, type={self.type!r}, description={self.description!r})"

    def __eq__(self, other):
        if type(self) is type(other):
            return (
                self.idx == other.idx
                and self.label == other.label
                and self.mode == other.mode
                and self.type == other.type
                and self.description == other.description
            )
        return super().__eq__(other)


class LogicNodeList(container.MutableSequence):
    @classmethod
    def from_xml_elem(cls, elem):
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        def generate():
            tag = "logic_node"
            for idx, sub in enumerate(elem.findall(tag)):
                try:
                    ln = LogicNode.from_xml_elem(sub, idx=idx)
                except ComponentXMLError as exc:
                    exc.prepend_xpath(f"{tag}[{idx + 1}]")
                    raise
                yield ln

        return cls(generate())

    def _check_value(self, value):
        if not isinstance(value, LogicNode):
            raise TypeError


class VoxelPos:
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if type(value) is not int:
            raise TypeError
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if type(value) is not int:
            raise TypeError
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if type(value) is not int:
            raise TypeError
        self._z = value

    def __init__(self, *, x=None, y=None, z=None):
        self.x = _coalesce(x, 0)
        self.y = _coalesce(y, 0)
        self.z = _coalesce(z, 0)

    @classmethod
    def from_xml_elem(cls, elem):
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        x = elem.get("x")
        y = elem.get("y")
        z = elem.get("z")

        if x is not None:
            try:
                x = int(x, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel x {x!r}") from exc

        if y is not None:
            try:
                y = int(y, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel y {y!r}") from exc

        if z is not None:
            try:
                z = int(z, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel z {z!r}") from exc

        return cls(x=x, y=y, z=z)

    def __repr__(self):
        return f"{type(self).__name__}(x={self.x!r}, y={self.y!r}, z={self.z!r})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return super().__eq__(other)


class Definition:
    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self, value):
        if type(value) is not str:
            raise TypeError
        self._cid = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if type(value) is not str:
            raise TypeError
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if type(value) is not Category:
            raise TypeError
        self._category = value

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        if type(value) is not float:
            raise TypeError
        self._mass = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if type(value) is not int:
            raise TypeError
        self._value = value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        if type(value) is not Flags:
            raise TypeError
        self._flags = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if type(value) is not str:
            raise TypeError
        self._tags = value

    @property
    def tooltip_properties(self):
        return self._tooltip_properties

    @tooltip_properties.setter
    def tooltip_properties(self, value):
        if type(value) is not TooltipProperties:
            raise TypeError
        self._tooltip_properties = value

    @property
    def logic_nodes(self):
        return self._logic_nodes

    @logic_nodes.setter
    def logic_nodes(self, value):
        if type(value) is not LogicNodeList:
            raise TypeError
        self._logic_nodes = value

    @property
    def voxel_min(self):
        return self._voxel_min

    @voxel_min.setter
    def voxel_min(self, value):
        if type(value) is not VoxelPos:
            raise TypeError
        self._voxel_min = value

    @property
    def voxel_max(self):
        return self._voxel_max

    @voxel_max.setter
    def voxel_max(self, value):
        if type(value) is not VoxelPos:
            raise TypeError
        self._voxel_max = value

    def __init__(
        self,
        *,
        cid=None,
        name=None,
        category=None,
        mass=None,
        value=None,
        flags=None,
        tags=None,
        tooltip_properties=None,
        logic_nodes=None,
        voxel_min=None,
        voxel_max=None,
    ):
        self.cid = _coalesce(cid, "")
        self.name = _coalesce(name, "")
        self.category = _coalesce(category, Category.BLOCKS)
        self.mass = _coalesce(mass, 0.0)
        self.value = _coalesce(value, 0)
        self.flags = _coalesce(flags, Flags(0))
        self.tags = _coalesce(tags, "")
        self.tooltip_properties = _coalesce(tooltip_properties, TooltipProperties())
        self.logic_nodes = _coalesce(logic_nodes, LogicNodeList())
        self.voxel_min = _coalesce(voxel_min, VoxelPos())
        self.voxel_max = _coalesce(voxel_max, VoxelPos())

    @classmethod
    def from_xml_elem(cls, elem, *, cid=None):
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        name = elem.get("name")
        category = elem.get("category")
        mass = elem.get("mass")
        value = elem.get("value")
        flags = elem.get("flags")
        tags = elem.get("tags")
        tooltip_properties = elem.find("tooltip_properties")
        logic_nodes = elem.find("logic_nodes")
        voxel_min = elem.find("voxel_min")
        voxel_max = elem.find("voxel_max")

        if category is not None:
            category_raw = category
            try:
                category = int(category, base=10)
                category = Category(category)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component category {category_raw!r}"
                ) from exc

        if mass is not None:
            try:
                mass = float(mass)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid component mass {mass!r}") from exc

        if value is not None:
            try:
                value = int(value, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid component value {value!r}") from exc

        if flags is not None:
            flags_raw = flags
            try:
                flags = int(flags, base=10)
                flags = Flags(flags)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component flags {flags_raw!r}"
                ) from exc

        if tooltip_properties is not None:
            try:
                tooltip_properties = TooltipProperties.from_xml_elem(tooltip_properties)
            except ComponentXMLError as exc:
                exc.prepend_xpath("tooltip_properties")
                raise

        if logic_nodes is not None:
            try:
                logic_nodes = LogicNodeList.from_xml_elem(logic_nodes)
            except ComponentXMLError as exc:
                exc.prepend_xpath("logic_nodes")
                raise

        if voxel_min is not None:
            try:
                voxel_min = VoxelPos.from_xml_elem(voxel_min)
            except ComponentXMLError as exc:
                exc.prepend_xpath("voxel_min")
                raise

        if voxel_max is not None:
            try:
                voxel_max = VoxelPos.from_xml_elem(voxel_max)
            except ComponentXMLError as exc:
                exc.prepend_xpath("voxel_max")
                raise

        return cls(
            cid=cid,
            name=name,
            category=category,
            mass=mass,
            value=value,
            flags=flags,
            tags=tags,
            tooltip_properties=tooltip_properties,
            logic_nodes=logic_nodes,
            voxel_min=voxel_min,
            voxel_max=voxel_max,
        )

    def __repr__(self):
        return f"{type(self).__name__}(cid={self.cid!r}, name={self.name!r}, category={self.category!r}, mass={self.mass!r}, value={self.value!r}, flags={self.flags!r}, tags={self.tags!r}, tooltip_properties={self.tooltip_properties!r}, logic_nodes={self.logic_nodes}, voxel_min={self.voxel_min!r}, voxel_max={self.voxel_max})"

    def __eq__(self, other):
        if type(self) is type(other):
            return (
                self.cid == other.cid
                and self.name == other.name
                and self.category == other.category
                and self.mass == other.mass
                and self.value == other.value
                and self.flags == other.flags
                and self.tags == other.tags
                and self.tooltip_properties == other.tooltip_properties
                and self.logic_nodes == other.logic_nodes
                and self.voxel_min == other.voxel_min
                and self.voxel_max == other.voxel_max
            )
        return super().__eq__(other)


def _new_xml_parser():
    # Stormworks uses XML with invalid attribute names.
    # To avoid errors, we enable the recover option.
    # https://nona-takahara.github.io/blog/entry10.html
    return lxml.etree.XMLParser(recover=True)


def _parse_xml_root(elem, *, cid=None):
    if elem.tag != "definition":
        exc = ComponentXMLError(f"invalid xml root tag {elem.tag!r}")
        exc.prepend_xpath(elem.tag)
        exc.prepend_xpath("/")
        raise exc

    try:
        return Definition.from_xml_elem(elem, cid=cid)
    except ComponentXMLError as exc:
        exc.prepend_xpath(elem.tag)
        exc.prepend_xpath("/")
        raise


def parse_xml_file(file):
    if not validator.is_pathlike(file):
        raise TypeError

    cid = generate_cid(file)
    tree = lxml.etree.parse(file, parser=_new_xml_parser())
    elem = tree.getroot()

    try:
        return _parse_xml_root(elem, cid=cid)
    except ComponentXMLError as exc:
        exc.file = file
        raise


def parse_xml_str(s, *, cid=None):
    elem = lxml.etree.fromstring(s, parser=_new_xml_parser())
    return _parse_xml_root(elem, cid=cid)
