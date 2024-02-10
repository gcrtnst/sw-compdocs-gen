import collections.abc
import dataclasses
import enum
import lxml.etree
import os
import pathlib
import re
import typing

from . import _types
from . import container


class ComponentXMLError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: typing.Final[str] = msg
        self.file: _types.StrOrBytesPath | None = None
        self._xpath: str = "."
        self._xpath_list: list[str] = []

    @property
    def xpath(self) -> str:
        return self._xpath

    def __str__(self) -> str:
        file = os.fsdecode(self.file) if self.file is not None else None

        msg = self.msg
        if file is None and self.xpath != ".":
            msg = f"{self.msg} (at xpath {self.xpath!r})"
        if file is not None and self.xpath == ".":
            msg = f"{self.msg} (in file {file!r})"
        if file is not None and self.xpath != ".":
            msg = f"{self.msg} (in file {file!r} at xpath {self.xpath!r})"
        return msg

    def prepend_xpath(self, s: str) -> None:
        if len(self._xpath_list) >= 1 and self._xpath_list[0] == "/":
            raise RuntimeError

        if s == "/":
            self._xpath_list.insert(0, s)
            self._xpath = "/" + "/".join(self._xpath_list[1:])
            return
        if s != "" and s.find("/") == -1:
            self._xpath_list.insert(0, s)
            self._xpath = "./" + "/".join(self._xpath_list)
            return
        raise ValueError


def generate_cid(file: _types.StrOrBytesPath) -> str:
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


@dataclasses.dataclass
class TooltipProperties:
    _: dataclasses.KW_ONLY
    short_description: str = ""
    description: str = ""

    @classmethod
    def from_xml_elem(cls, elem: lxml.etree._Element) -> typing.Self:
        return cls(
            short_description=elem.get("short_description", cls.short_description),
            description=elem.get("description", cls.description),
        )

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


@dataclasses.dataclass
class LogicNode:
    _: dataclasses.KW_ONLY
    idx: int = 0
    label: str = ""
    mode: LogicNodeMode = LogicNodeMode.OUTPUT
    type: LogicNodeType = LogicNodeType.BOOL
    description: str = ""

    @classmethod
    def from_xml_elem(
        cls, elem: lxml.etree._Element, *, idx: int | None = None
    ) -> typing.Self:
        mode = cls.mode
        mode_attr = elem.get("mode")
        if mode_attr is not None:
            try:
                mode = LogicNodeMode(int(mode_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid logic node mode {mode_attr!r}"
                ) from exc

        typo = cls.type
        typo_attr = elem.get("type")
        if typo_attr is not None:
            try:
                typo = LogicNodeType(int(typo_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid logic node type {typo_attr!r}"
                ) from exc

        idx = idx if idx is not None else cls.idx
        label = elem.get("label", cls.label)
        description = elem.get("description", cls.description)
        return cls(idx=idx, label=label, mode=mode, type=typo, description=description)


class LogicNodeList(container.MutableSequence[LogicNode]):
    @classmethod
    def from_xml_elem(cls, elem: lxml.etree._Element) -> typing.Self:
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


@dataclasses.dataclass
class VoxelPos:
    _: dataclasses.KW_ONLY
    x: int = 0
    y: int = 0
    z: int = 0

    @classmethod
    def from_xml_elem(cls, elem: lxml.etree._Element) -> typing.Self:
        x = cls.x
        x_attr = elem.get("x")
        if x_attr is not None:
            try:
                x = int(x_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel x {x_attr!r}") from exc

        y = cls.y
        y_attr = elem.get("y")
        if y_attr is not None:
            try:
                y = int(y_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel y {y_attr!r}") from exc

        z = cls.z
        z_attr = elem.get("z")
        if z_attr is not None:
            try:
                z = int(z_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(f"invalid voxel z {z_attr!r}") from exc

        return cls(x=x, y=y, z=z)


@dataclasses.dataclass
class Definition:
    _: dataclasses.KW_ONLY
    cid: str = ""
    name: str = ""
    category: Category = Category.BLOCKS
    mass: float = 0.0
    value: int = 0
    flags: Flags = Flags(0)
    tags: str = ""
    tooltip_properties: TooltipProperties = dataclasses.field(
        default_factory=TooltipProperties
    )
    logic_nodes: LogicNodeList = dataclasses.field(default_factory=LogicNodeList)
    voxel_min: VoxelPos = dataclasses.field(default_factory=VoxelPos)
    voxel_max: VoxelPos = dataclasses.field(default_factory=VoxelPos)

    @classmethod
    def from_xml_elem(
        cls, elem: lxml.etree._Element, *, cid: str | None = None
    ) -> typing.Self:
        category = cls.category
        category_attr = elem.get("category")
        if category_attr is not None:
            try:
                category = Category(int(category_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component category {category_attr!r}"
                ) from exc

        mass = cls.mass
        mass_attr = elem.get("mass")
        if mass_attr is not None:
            try:
                mass = float(mass_attr)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component mass {mass_attr!r}"
                ) from exc

        value = cls.value
        value_attr = elem.get("value")
        if value_attr is not None:
            try:
                value = int(value_attr, base=10)
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component value {value_attr!r}"
                ) from exc

        flags = cls.flags
        flags_attr = elem.get("flags")
        if flags_attr is not None:
            try:
                flags = Flags(int(flags_attr, base=10))
            except ValueError as exc:
                raise ComponentXMLError(
                    f"invalid component flags {flags_attr!r}"
                ) from exc

        tooltip_properties = TooltipProperties()
        tooltip_properties_elem = elem.find("tooltip_properties")
        if tooltip_properties_elem is not None:
            try:
                tooltip_properties = TooltipProperties.from_xml_elem(
                    tooltip_properties_elem
                )
            except ComponentXMLError as exc:
                exc.prepend_xpath("tooltip_properties")
                raise

        logic_nodes = LogicNodeList()
        logic_nodes_elem = elem.find("logic_nodes")
        if logic_nodes_elem is not None:
            try:
                logic_nodes = LogicNodeList.from_xml_elem(logic_nodes_elem)
            except ComponentXMLError as exc:
                exc.prepend_xpath("logic_nodes")
                raise

        voxel_min = VoxelPos()
        voxel_min_elem = elem.find("voxel_min")
        if voxel_min_elem is not None:
            try:
                voxel_min = VoxelPos.from_xml_elem(voxel_min_elem)
            except ComponentXMLError as exc:
                exc.prepend_xpath("voxel_min")
                raise

        voxel_max = VoxelPos()
        voxel_max_elem = elem.find("voxel_max")
        if voxel_max_elem is not None:
            try:
                voxel_max = VoxelPos.from_xml_elem(voxel_max_elem)
            except ComponentXMLError as exc:
                exc.prepend_xpath("voxel_max")
                raise

        cid = cid if cid is not None else cls.cid
        name = elem.get("name", cls.name)
        tags = elem.get("tags", cls.tags)
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


# lxml.etree.XMLParser is generic in stub but not at runtime.
# To avoid errors, we use string literal annotation.
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


def parse_xml_file(file: _types.StrOrBytesPath) -> Definition:
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
