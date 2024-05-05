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
from . import language


class DefinitionXMLError(Exception):
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
            msg = f"{self.msg} (at xpath '{self.xpath}')"
        if file is not None and self.xpath == ".":
            msg = f"{self.msg} (in file '{file}')"
        if file is not None and self.xpath != ".":
            msg = f"{self.msg} (in file '{file}' at xpath '{self.xpath}')"
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


def generate_key(file: _types.StrOrBytesPath) -> str:
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
    key: str | None = None
    short_description: language.Text = dataclasses.field(default_factory=language.Text)
    description: language.Text = dataclasses.field(default_factory=language.Text)

    @classmethod
    def from_xml_elem(
        cls, elem: lxml.etree._Element, *, key: str | None = None
    ) -> typing.Self:
        short_description = language.Text(en=elem.get("short_description", ""))
        description = language.Text(en=elem.get("description", ""))

        self = cls(short_description=short_description, description=description)
        self.update_id(key, recursive=False)
        return self

    def update_id(self, key: str | None, *, recursive: bool = True) -> None:
        self.short_description.id = f"def_{key}_s_desc" if key is not None else None
        self.description.id = f"def_{key}_desc" if key is not None else None
        self.key = key


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
    key: str | None = None
    idx: int | None = None
    label: language.Text = dataclasses.field(default_factory=language.Text)
    mode: LogicNodeMode = LogicNodeMode.OUTPUT
    type: LogicNodeType = LogicNodeType.BOOL
    description: language.Text = dataclasses.field(default_factory=language.Text)

    @classmethod
    def from_xml_elem(
        cls,
        elem: lxml.etree._Element,
        *,
        key: str | None = None,
        idx: int | None = None,
    ) -> typing.Self:
        label = language.Text(en=elem.get("label", ""))
        description = language.Text(en=elem.get("description", ""))

        mode = cls.mode
        mode_attr = elem.get("mode")
        if mode_attr is not None:
            try:
                mode = LogicNodeMode(int(mode_attr, base=10))
            except ValueError as exc:
                raise DefinitionXMLError(
                    f"invalid logic node mode {mode_attr!r}"
                ) from exc

        typo = cls.type
        typo_attr = elem.get("type")
        if typo_attr is not None:
            try:
                typo = LogicNodeType(int(typo_attr, base=10))
            except ValueError as exc:
                raise DefinitionXMLError(
                    f"invalid logic node type {typo_attr!r}"
                ) from exc

        self = cls(label=label, mode=mode, type=typo, description=description)
        self.update_id(key, idx, recursive=False)
        return self

    def update_id(
        self, key: str | None, idx: int | None, *, recursive: bool = True
    ) -> None:
        label_id = None
        description_id = None
        if key is not None and idx is not None:
            label_id = f"def_{key}_node_{idx:d}_label"
            description_id = f"def_{key}_node_{idx:d}_desc"

        self.label.id = label_id
        self.description.id = description_id
        self.key = key
        self.idx = idx


class LogicNodeList(container.MutableSequence[LogicNode]):
    def __init__(
        self,
        iterable: collections.abc.Iterable[LogicNode] = (),
        *,
        key: str | None = None,
    ) -> None:
        super().__init__(iterable)
        self.key: str | None = key

    def __repr__(self) -> str:
        if self.key is None:
            return f"{type(self).__name__}({self._l!r})"
        return f"{type(self).__name__}({self._l!r}, key={self.key!r})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            if self.key != other.key:
                return False
        return super().__eq__(other)

    @classmethod
    def from_xml_elem(
        cls, elem: lxml.etree._Element, *, key: str | None = None
    ) -> typing.Self:
        def generate() -> collections.abc.Iterator[LogicNode]:
            tag = "logic_node"
            for idx, sub in enumerate(elem.findall(tag)):
                try:
                    ln = LogicNode.from_xml_elem(sub, key=key, idx=idx)
                except DefinitionXMLError as exc:
                    exc.prepend_xpath(f"{tag}[{idx + 1}]")
                    raise
                yield ln

        self = cls(generate())
        self.update_id(key, recursive=False)
        return self

    def update_id(self, key: str | None, *, recursive: bool = True) -> None:
        if recursive:
            for idx, ln in enumerate(self):
                ln.update_id(key, idx)

        self.key = key


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
                raise DefinitionXMLError(f"invalid voxel x {x_attr!r}") from exc

        y = cls.y
        y_attr = elem.get("y")
        if y_attr is not None:
            try:
                y = int(y_attr, base=10)
            except ValueError as exc:
                raise DefinitionXMLError(f"invalid voxel y {y_attr!r}") from exc

        z = cls.z
        z_attr = elem.get("z")
        if z_attr is not None:
            try:
                z = int(z_attr, base=10)
            except ValueError as exc:
                raise DefinitionXMLError(f"invalid voxel z {z_attr!r}") from exc

        return cls(x=x, y=y, z=z)


@dataclasses.dataclass
class Definition:
    _: dataclasses.KW_ONLY
    file: _types.StrOrBytesPath | None = None
    key: str | None = None
    name: language.Text = dataclasses.field(default_factory=language.Text)
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
        cls,
        elem: lxml.etree._Element,
        *,
        file: _types.StrOrBytesPath | None = None,
        key: str | None = None,
    ) -> typing.Self:
        name = language.Text(en=elem.get("name", ""))
        tags = elem.get("tags", cls.tags)

        category = cls.category
        category_attr = elem.get("category")
        if category_attr is not None:
            try:
                category = Category(int(category_attr, base=10))
            except ValueError as base_exc:
                exc = DefinitionXMLError(
                    f"invalid component category {category_attr!r}"
                )
                exc.file = file
                raise exc from base_exc

        mass = cls.mass
        mass_attr = elem.get("mass")
        if mass_attr is not None:
            try:
                mass = float(mass_attr)
            except ValueError as base_exc:
                exc = DefinitionXMLError(f"invalid component mass {mass_attr!r}")
                exc.file = file
                raise exc from base_exc

        value = cls.value
        value_attr = elem.get("value")
        if value_attr is not None:
            try:
                value = int(value_attr, base=10)
            except ValueError as base_exc:
                exc = DefinitionXMLError(f"invalid component value {value_attr!r}")
                exc.file = file
                raise exc from base_exc

        flags = cls.flags
        flags_attr = elem.get("flags")
        if flags_attr is not None:
            try:
                flags = Flags(int(flags_attr, base=10))
            except ValueError as base_exc:
                exc = DefinitionXMLError(f"invalid component flags {flags_attr!r}")
                exc.file = file
                raise exc from base_exc

        tooltip_properties_elem = elem.find("tooltip_properties")
        if tooltip_properties_elem is None:
            tooltip_properties_elem = lxml.etree.Element("tooltip_properties")
        try:
            tooltip_properties = TooltipProperties.from_xml_elem(
                tooltip_properties_elem, key=key
            )
        except DefinitionXMLError as exc:
            exc.file = file
            exc.prepend_xpath("tooltip_properties")
            raise

        logic_nodes_elem = elem.find("logic_nodes")
        if logic_nodes_elem is None:
            logic_nodes_elem = lxml.etree.Element("logic_nodes")
        try:
            logic_nodes = LogicNodeList.from_xml_elem(logic_nodes_elem, key=key)
        except DefinitionXMLError as exc:
            exc.file = file
            exc.prepend_xpath("logic_nodes")
            raise

        voxel_min_elem = elem.find("voxel_min")
        if voxel_min_elem is None:
            voxel_min_elem = lxml.etree.Element("voxel_min")
        try:
            voxel_min = VoxelPos.from_xml_elem(voxel_min_elem)
        except DefinitionXMLError as exc:
            exc.file = file
            exc.prepend_xpath("voxel_min")
            raise

        voxel_max_elem = elem.find("voxel_max")
        if voxel_max_elem is None:
            voxel_max_elem = lxml.etree.Element("voxel_max")
        try:
            voxel_max = VoxelPos.from_xml_elem(voxel_max_elem)
        except DefinitionXMLError as exc:
            exc.file = file
            exc.prepend_xpath("voxel_max")
            raise

        self = cls(
            file=file,
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
        self.update_id(key, recursive=False)
        return self

    def update_id(self, key: str | None, *, recursive: bool = True) -> None:
        if recursive:
            self.tooltip_properties.update_id(key, recursive=True)
            self.logic_nodes.update_id(key, recursive=True)

        self.name.id = f"def_{key}_name" if key is not None else None
        self.key = key


@dataclasses.dataclass
class Component:
    _: dataclasses.KW_ONLY
    defn: Definition

    def name(self) -> language.Text:
        return dataclasses.replace(self.defn.name)

    def short_description(self) -> language.Text:
        return dataclasses.replace(self.defn.tooltip_properties.short_description)

    def description(self) -> language.Text:
        return dataclasses.replace(self.defn.tooltip_properties.description)

    def category(self) -> Category:
        return self.defn.category

    def mass(self) -> float:
        return self.defn.mass

    def value(self) -> int:
        return self.defn.value

    def tags(self) -> str:
        return self.defn.tags

    def voxel_min(self) -> VoxelPos:
        return dataclasses.replace(self.defn.voxel_min)

    def voxel_max(self) -> VoxelPos:
        return dataclasses.replace(self.defn.voxel_max)


# lxml.etree.XMLParser is generic in stub but not at runtime.
# To avoid errors, we use string literal annotation.
def _new_xml_parser() -> "lxml.etree.XMLParser[lxml.etree._Element]":
    # Stormworks uses XML with invalid attribute names.
    # To avoid errors, we enable the recover option.
    # https://nona-takahara.github.io/blog/entry10.html
    return lxml.etree.XMLParser(recover=True)


def _parse_xml_root(
    elem: lxml.etree._Element | None,
    *,
    file: _types.StrOrBytesPath | None = None,
    key: str | None = None,
) -> Definition:
    # elem may be None if the XML is invalid.
    if elem is None:
        exc = DefinitionXMLError("invalid xml")
        exc.file = file
        exc.prepend_xpath("/")
        raise exc

    if elem.tag != "definition":
        exc = DefinitionXMLError(f"invalid xml root tag {elem.tag!r}")
        exc.file = file
        exc.prepend_xpath(elem.tag)
        exc.prepend_xpath("/")
        raise exc

    try:
        return Definition.from_xml_elem(elem, file=file, key=key)
    except DefinitionXMLError as exc:
        exc.prepend_xpath(elem.tag)
        exc.prepend_xpath("/")
        raise


def parse_xml_file(file: _types.StrOrBytesPath) -> Definition:
    key = generate_key(file)
    tree = lxml.etree.parse(file, parser=_new_xml_parser())
    elem: lxml.etree._Element | None = tree.getroot()
    return _parse_xml_root(elem, file=file, key=key)


def parse_xml_str(s: str, *, key: str | None = None) -> Definition:
    elem: lxml.etree._Element | None
    elem = lxml.etree.fromstring(s, parser=_new_xml_parser())
    return _parse_xml_root(elem, key=key)


def load_defn_dict(defn_dir: _types.StrOrBytesPath) -> dict[str, Definition]:
    # Avoid 'Expression type contains "Any"' warning from mypy
    path_cls: type[pathlib.Path] = pathlib.Path

    if not isinstance(defn_dir, path_cls):
        defn_dir = os.fsdecode(defn_dir)
        defn_dir = pathlib.Path(defn_dir)

    defn_dict = {}
    for defn_file in defn_dir.glob("*.xml"):
        if not defn_file.is_file():
            continue

        defn = parse_xml_file(defn_file)
        assert defn.key is not None
        defn_dict[defn.key] = defn
    return defn_dict


def load_comp_list(defn_dir: _types.StrOrBytesPath) -> list[Component]:
    defn_dict = load_defn_dict(defn_dir)
    return [Component(defn=defn) for defn in defn_dict.values()]
