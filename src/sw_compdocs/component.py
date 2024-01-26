import collections.abc
import enum
import lxml.etree
import os
import pathlib
import re
import typing

from . import container
from . import validator


_T = typing.TypeVar("_T")


def _coalesce(value: _T | None, default: _T) -> _T:
    if value is None:
        return default
    return value


class ComponentXMLError(Exception):
    @property
    def msg(self) -> str:
        return self._msg

    @property
    def file(self) -> validator.StrOrBytesPath | None:
        return self._file

    @file.setter
    def file(self, value: validator.StrOrBytesPath | None) -> None:
        if value is not None and not validator.is_pathlike(value):
            raise TypeError
        self._file = value

    @property
    def xpath(self) -> str:
        return self._xpath

    def __init__(self, msg: str) -> None:
        if type(msg) is not str:
            raise TypeError

        super().__init__(msg)
        self._msg = msg
        self._file = None
        self._xpath = "."
        self._xpath_list: list[str] = []

    def __str__(self) -> str:
        file = os.fsdecode(self.file) if self.file is not None else "<component.xml>"
        return f"{file}: {self.xpath}: {self.msg}"

    def prepend_xpath(self, s: str) -> None:
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


def generate_cid(file: validator.StrOrBytesPath) -> str:
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

    def __str__(self) -> str:
        cls = type(self)
        if self is cls.BLOCKS:
            return "Blocks"
        if self is cls.VEHICLE_CONTROL:
            return "Vehicle Control"
        if self is cls.MECHANICS:
            return "Mechanics"
        if self is cls.PROPULSION:
            return "Propulsion"
        if self is cls.SPECIALIST_EQUIPMENT:
            return "Specialist Equipment"
        if self is cls.LOGIC:
            return "Logic"
        if self is cls.DISPLAYS:
            return "Displays"
        if self is cls.SENSORS:
            return "Sensors"
        if self is cls.DECORATIVE:
            return "Decorative"
        if self is cls.FLUID:
            return "Fluid"
        if self is cls.ELECTRIC:
            return "Electric"
        if self is cls.JET_ENGINES:
            return "Jet Engines"
        if self is cls.WEAPONS:
            return "Weapons"
        if self is cls.MODULAR_ENGINES:
            return "Modular Engines"
        if self is cls.INDUSTRY:
            return "Industry"
        if self is cls.WINDOWS:
            return "Windows"
        typing.assert_never(self)


@enum.unique
class Flags(enum.Flag, boundary=enum.KEEP):
    IS_DEPRECATED = 1 << 29


class TooltipProperties:
    @property
    def short_description(self) -> str:
        return self._short_description

    @short_description.setter
    def short_description(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._short_description = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._description = value

    def __init__(
        self, *, short_description: str | None = None, description: str | None = None
    ) -> None:
        self.short_description = _coalesce(short_description, "")
        self.description = _coalesce(description, "")

    @classmethod
    def from_xml_elem(cls, elem: lxml.etree._Element) -> typing.Self:
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        return cls(
            short_description=elem.get("short_description"),
            description=elem.get("description"),
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(short_description={self.short_description!r}, description={self.description!r})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return (
                self.short_description == other.short_description
                and self.description == other.description
            )
        return super().__eq__(other)

    def full_description(self) -> str:
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

    def __str__(self) -> str:
        cls = type(self)
        if self is cls.BOOL:
            return "on/off"
        if self is cls.FLOAT:
            return "number"
        if self is cls.TORQUE:
            return "power"
        if self is cls.WATER:
            return "fluid"
        if self is cls.ELECTRIC:
            return "electric"
        if self is cls.COMPOSITE:
            return "composite"
        if self is cls.VIDEO:
            return "video"
        if self is cls.AUDIO:
            return "audio"
        if self is cls.ROPE:
            return "rope"
        typing.assert_never(self)


class LogicNode:
    @property
    def idx(self) -> int:
        return self._idx

    @idx.setter
    def idx(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError
        if value < 0:
            raise ValueError
        self._idx = value

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._label = value

    @property
    def mode(self) -> LogicNodeMode:
        return self._mode

    @mode.setter
    def mode(self, value: LogicNodeMode) -> None:
        if type(value) is not LogicNodeMode:
            raise TypeError
        self._mode = value

    @property
    def type(self) -> LogicNodeType:
        return self._type

    @type.setter
    def type(self, value: LogicNodeType) -> None:
        if type(value) is not LogicNodeType:
            raise TypeError
        self._type = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._description = value

    def __init__(
        self,
        *,
        idx: int | None = None,
        label: str | None = None,
        mode: LogicNodeMode | None = None,
        type: LogicNodeType | None = None,
        description: str | None = None,
    ):
        self.idx = _coalesce(idx, 0)
        self.label = _coalesce(label, "")
        self.mode = _coalesce(mode, LogicNodeMode.OUTPUT)
        self.type = _coalesce(type, LogicNodeType.BOOL)
        self.description = _coalesce(description, "")

    @classmethod
    def from_xml_elem(
        cls, elem: lxml.etree._Element, *, idx: int | None = None
    ) -> typing.Self:
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        label = elem.get("label")
        mode_attr = elem.get("mode")
        typo_attr = elem.get("type")
        description = elem.get("description")

        mode = None
        if mode_attr is not None:
            try:
                mode = LogicNodeMode(int(mode_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid logic node mode {mode_attr!r}"
                ) from exc

        typo = None
        if typo_attr is not None:
            try:
                typo = LogicNodeType(int(typo_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid logic node type {typo_attr!r}"
                ) from exc

        return cls(idx=idx, label=label, mode=mode, type=typo, description=description)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(idx={self.idx!r}, label={self.label!r}, mode={self.mode!r}, type={self.type!r}, description={self.description!r})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return (
                self.idx == other.idx
                and self.label == other.label
                and self.mode == other.mode
                and self.type == other.type
                and self.description == other.description
            )
        return super().__eq__(other)


class LogicNodeList(container.MutableSequence[LogicNode]):
    @classmethod
    def from_xml_elem(cls, elem: lxml.etree._Element) -> typing.Self:
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        def generate() -> collections.abc.Iterator[LogicNode]:
            tag = "logic_node"
            for idx, sub in enumerate(elem.findall(tag)):
                try:
                    ln = LogicNode.from_xml_elem(sub, idx=idx)
                except ComponentXMLError as exc:
                    exc.prepend_xpath(f"{tag}[{idx + 1}]")
                    raise
                yield ln

        return cls(generate())

    def _check_value(self, value: LogicNode) -> None:
        if not isinstance(value, LogicNode):
            raise TypeError


class VoxelPos:
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError
        self._y = value

    @property
    def z(self) -> int:
        return self._z

    @z.setter
    def z(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError
        self._z = value

    def __init__(
        self, *, x: int | None = None, y: int | None = None, z: int | None = None
    ):
        self.x = _coalesce(x, 0)
        self.y = _coalesce(y, 0)
        self.z = _coalesce(z, 0)

    @classmethod
    def from_xml_elem(cls, elem: lxml.etree._Element) -> typing.Self:
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        x_attr = elem.get("x")
        y_attr = elem.get("y")
        z_attr = elem.get("z")

        x = None
        if x_attr is not None:
            try:
                x = int(x_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel x {x_attr!r}") from exc

        y = None
        if y_attr is not None:
            try:
                y = int(y_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel y {y_attr!r}") from exc

        z = None
        if z_attr is not None:
            try:
                z = int(z_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel z {z_attr!r}") from exc

        return cls(x=x, y=y, z=z)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.x!r}, y={self.y!r}, z={self.z!r})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self.x == other.x and self.y == other.y and self.z == other.z
        return super().__eq__(other)


class Definition:
    @property
    def cid(self) -> str:
        return self._cid

    @cid.setter
    def cid(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._cid = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._name = value

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, value: Category) -> None:
        if type(value) is not Category:
            raise TypeError
        self._category = value

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, value: float) -> None:
        if type(value) is not float:
            raise TypeError
        self._mass = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError
        self._value = value

    @property
    def flags(self) -> Flags:
        return self._flags

    @flags.setter
    def flags(self, value: Flags) -> None:
        if type(value) is not Flags:
            raise TypeError
        self._flags = value

    @property
    def tags(self) -> str:
        return self._tags

    @tags.setter
    def tags(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._tags = value

    @property
    def tooltip_properties(self) -> TooltipProperties:
        return self._tooltip_properties

    @tooltip_properties.setter
    def tooltip_properties(self, value: TooltipProperties) -> None:
        if type(value) is not TooltipProperties:
            raise TypeError
        self._tooltip_properties = value

    @property
    def logic_nodes(self) -> LogicNodeList:
        return self._logic_nodes

    @logic_nodes.setter
    def logic_nodes(self, value: LogicNodeList) -> None:
        if type(value) is not LogicNodeList:
            raise TypeError
        self._logic_nodes = value

    @property
    def voxel_min(self) -> VoxelPos:
        return self._voxel_min

    @voxel_min.setter
    def voxel_min(self, value: VoxelPos) -> None:
        if type(value) is not VoxelPos:
            raise TypeError
        self._voxel_min = value

    @property
    def voxel_max(self) -> VoxelPos:
        return self._voxel_max

    @voxel_max.setter
    def voxel_max(self, value: VoxelPos) -> None:
        if type(value) is not VoxelPos:
            raise TypeError
        self._voxel_max = value

    def __init__(
        self,
        *,
        cid: str | None = None,
        name: str | None = None,
        category: Category | None = None,
        mass: float | None = None,
        value: int | None = None,
        flags: Flags | None = None,
        tags: str | None = None,
        tooltip_properties: TooltipProperties | None = None,
        logic_nodes: LogicNodeList | None = None,
        voxel_min: VoxelPos | None = None,
        voxel_max: VoxelPos | None = None,
    ) -> None:
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
    def from_xml_elem(
        cls, elem: lxml.etree._Element, *, cid: str | None = None
    ) -> typing.Self:
        if not isinstance(elem, lxml.etree._Element):
            raise TypeError

        name = elem.get("name")
        category_attr = elem.get("category")
        mass_attr = elem.get("mass")
        value_attr = elem.get("value")
        flags_attr = elem.get("flags")
        tags = elem.get("tags")
        tooltip_properties_elem = elem.find("tooltip_properties")
        logic_nodes_elem = elem.find("logic_nodes")
        voxel_min_elem = elem.find("voxel_min")
        voxel_max_elem = elem.find("voxel_max")

        category = None
        if category_attr is not None:
            try:
                category = Category(int(category_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component category {category_attr!r}"
                ) from exc

        mass = None
        if mass_attr is not None:
            try:
                mass = float(mass_attr)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component mass {mass_attr!r}"
                ) from exc

        value = None
        if value_attr is not None:
            try:
                value = int(value_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component value {value_attr!r}"
                ) from exc

        flags = None
        if flags_attr is not None:
            try:
                flags = Flags(int(flags_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component flags {flags_attr!r}"
                ) from exc

        tooltip_properties = None
        if tooltip_properties_elem is not None:
            try:
                tooltip_properties = TooltipProperties.from_xml_elem(
                    tooltip_properties_elem
                )
            except ComponentXMLError as exc:
                exc.prepend_xpath("tooltip_properties")
                raise

        logic_nodes = None
        if logic_nodes_elem is not None:
            try:
                logic_nodes = LogicNodeList.from_xml_elem(logic_nodes_elem)
            except ComponentXMLError as exc:
                exc.prepend_xpath("logic_nodes")
                raise

        voxel_min = None
        if voxel_min_elem is not None:
            try:
                voxel_min = VoxelPos.from_xml_elem(voxel_min_elem)
            except ComponentXMLError as exc:
                exc.prepend_xpath("voxel_min")
                raise

        voxel_max = None
        if voxel_max_elem is not None:
            try:
                voxel_max = VoxelPos.from_xml_elem(voxel_max_elem)
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

    def __repr__(self) -> str:
        return f"{type(self).__name__}(cid={self.cid!r}, name={self.name!r}, category={self.category!r}, mass={self.mass!r}, value={self.value!r}, flags={self.flags!r}, tags={self.tags!r}, tooltip_properties={self.tooltip_properties!r}, logic_nodes={self.logic_nodes}, voxel_min={self.voxel_min!r}, voxel_max={self.voxel_max})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

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


# lxml.etree.XMLParser is generic in stub but not at runtime.
# To avoid errors, we use string literal type.
def _new_xml_parser() -> "lxml.etree.XMLParser[lxml.etree._Element]":
    # Stormworks uses XML with invalid attribute names.
    # To avoid errors, we enable the recover option.
    # https://nona-takahara.github.io/blog/entry10.html
    return lxml.etree.XMLParser(recover=True)


def _parse_xml_root(elem: lxml.etree._Element, *, cid: str | None = None) -> Definition:
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


def parse_xml_file(file: validator.StrOrBytesPath) -> Definition:
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


def parse_xml_str(s: str, *, cid: str | None = None) -> Definition:
    elem = lxml.etree.fromstring(s, parser=_new_xml_parser())
    return _parse_xml_root(elem, cid=cid)
