import collections.abc
import os
import tomllib
import typing

from . import _types
from . import component
from . import document
from . import language
from . import template


class LabelFileError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: typing.Final[str] = msg
        self.file: _types.StrOrBytesPath | None = None

    def __str__(self) -> str:
        file = os.fsdecode(self.file) if self.file is not None else "<label.toml>"
        return f"{file}: {self.msg}"


class LabelKeyError(KeyError):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key: typing.Final[str] = key

    def __str__(self) -> str:
        return f"missing label text for key {self.key!r}"


class LabelDict(collections.abc.Mapping[str, str]):
    def __init__(self, mapping: collections.abc.Mapping[str, str] = {}) -> None:
        self._d: dict[str, str] = dict(mapping)

    @classmethod
    def _from_toml(cls, toml: dict[str, object]) -> typing.Self:
        obj = toml.get("label")
        if obj is None:
            raise LabelFileError("missing label table")
        if not isinstance(obj, collections.abc.Mapping):
            raise LabelFileError(f"invalid label table type: {type(obj).__name__}")

        mapping: dict[str, str] = {}
        for k, v in obj.items():
            if not isinstance(k, str):
                # In TOML, keys are always strings.
                # If a non-string key is given, it is a bug in tomllib.
                raise Exception
            if not isinstance(v, str):
                raise LabelFileError(f"expected string for label text: {v!r}")
            mapping[k] = v
        return cls(mapping)

    @classmethod
    def from_toml_file(cls, file: _types.StrOrBytesPath) -> typing.Self:
        with open(file, mode="rb") as fp:
            toml: dict[str, object] = tomllib.load(fp)

        try:
            return cls._from_toml(toml)
        except LabelFileError as exc:
            exc.file = file
            raise

    @classmethod
    def from_toml_str(cls, s: str) -> typing.Self:
        toml: dict[str, object] = tomllib.loads(s)
        return cls._from_toml(toml)

    def __getitem__(self, key: str) -> str:
        try:
            return self._d[key]
        except KeyError as exc:
            raise LabelKeyError(key) from exc

    def __iter__(self) -> collections.abc.Iterator[str]:
        return iter(self._d)

    def __len__(self) -> int:
        return len(self._d)


class DocumentGenerator:
    def __init__(
        self,
        *,
        label: LabelDict | None = None,
        lang: language.Language | None = None,
        fmt: template.TemplateFormatter | None = None,
    ) -> None:
        self.label: LabelDict | None = label
        self.lang: language.Language | None = lang
        self.fmt: template.TemplateFormatter | None = fmt

    def _label_get(self, s: str) -> str:
        if self.label is not None:
            s = self.label[s]
        return s

    def _lang_find_id(self, lang_id: str, lang_en: str) -> str:
        if self.lang is None:
            return lang_en
        return self.lang.find_id(lang_id).local

    def _lang_find_en(self, lang_en: str) -> str:
        if self.lang is None:
            return lang_en
        return self.lang.find_en(lang_en).local

    def _fmt_format(self, s: str) -> str:
        if self.fmt is not None:
            s = self.fmt.format(s)
        return s

    def generate_property_table(self, comp: component.Definition) -> document.Table:
        head = document.TableDataRow(
            [
                self._label_get("PROP_TABLE_HEAD_LABEL"),
                self._label_get("PROP_TABLE_HEAD_VALUE"),
            ]
        )
        data = document.TableData(head)

        mass_label = self._label_get("PROP_TABLE_MASS_LABEL")
        mass_value = f"{comp.mass:g}"
        data.append(document.TableDataRow([mass_label, mass_value]))

        dims_w = comp.voxel_max.x - comp.voxel_min.x + 1
        dims_h = comp.voxel_max.y - comp.voxel_min.y + 1
        dims_d = comp.voxel_max.z - comp.voxel_min.z + 1
        dims_label = self._label_get("PROP_TABLE_DIMS_LABEL")
        dims_value = f"{dims_w:d}x{dims_d:d}x{dims_h:d}"
        data.append(document.TableDataRow([dims_label, dims_value]))

        cost_label = self._label_get("PROP_TABLE_COST_LABEL")
        cost_value = f"{comp.value:d}"
        data.append(document.TableDataRow([cost_label, cost_value]))

        tags_label = self._label_get("PROP_TABLE_TAGS_LABEL")
        data.append(document.TableDataRow([tags_label, comp.tags]))
        return document.Table(data)

    def generate_property(self, comp: component.Definition) -> document.Document:
        return document.Document(
            [
                document.Heading(self._lang_find_en("PROPERTIES")),
                self.generate_property_table(comp),
            ]
        )

    def generate_logic_table(
        self, cid: str, lns: component.LogicNodeList
    ) -> document.Table:
        head = document.TableDataRow(
            [
                self._label_get("LOGIC_TABLE_HEAD_TYPE"),
                self._label_get("LOGIC_TABLE_HEAD_LABEL"),
                self._label_get("LOGIC_TABLE_HEAD_DESC"),
            ]
        )
        data = document.TableData(head)
        for ln in lns:
            lang_id_label = f"def_{cid}_node_{ln.idx:d}_label"
            lang_id_desc = f"def_{cid}_node_{ln.idx:d}_desc"

            ln_type = self._lang_find_en(str(ln.type))
            ln_label = self._lang_find_id(lang_id_label, ln.label)
            ln_label = self._fmt_format(ln_label)
            ln_desc = self._lang_find_id(lang_id_desc, ln.description)
            ln_desc = self._fmt_format(ln_desc)
            data.append(document.TableDataRow([ln_type, ln_label, ln_desc]))
        return document.Table(data)

    def generate_logic(
        self, cid: str, lns: component.LogicNodeList
    ) -> document.Document:
        in_lns = component.LogicNodeList()
        out_lns = component.LogicNodeList()
        conn_lns = component.LogicNodeList()
        for ln in lns:
            if (
                ln.type is component.LogicNodeType.BOOL
                or ln.type is component.LogicNodeType.FLOAT
                or ln.type is component.LogicNodeType.COMPOSITE
                or ln.type is component.LogicNodeType.VIDEO
                or ln.type is component.LogicNodeType.AUDIO
            ):
                if ln.mode is component.LogicNodeMode.INPUT:
                    in_lns.append(ln)
                    continue
                if ln.mode is component.LogicNodeMode.OUTPUT:
                    out_lns.append(ln)
                    continue
                typing.assert_never(ln.mode)
            if (
                ln.type is component.LogicNodeType.TORQUE
                or ln.type is component.LogicNodeType.WATER
                or ln.type is component.LogicNodeType.ELECTRIC
                or ln.type is component.LogicNodeType.ROPE
            ):
                conn_lns.append(ln)
                continue
            typing.assert_never(ln.type)

        doc = document.Document()
        if len(in_lns) > 0:
            in_title = self._lang_find_en("logic inputs")
            doc.append(document.Heading(in_title))
            doc.append(self.generate_logic_table(cid, in_lns))
        if len(out_lns) > 0:
            out_title = self._lang_find_en("logic outputs")
            doc.append(document.Heading(out_title))
            doc.append(self.generate_logic_table(cid, out_lns))
        if len(conn_lns) > 0:
            conn_title = self._lang_find_en("connections")
            doc.append(document.Heading(conn_title))
            doc.append(self.generate_logic_table(cid, conn_lns))
        return doc

    def generate_component(self, comp: component.Definition) -> document.Document:
        doc = document.Document()

        comp_name_id = f"def_{comp.cid}_name"
        comp_name = self._lang_find_id(comp_name_id, comp.name)
        doc.append(document.Heading(comp_name))

        if component.Flags.IS_DEPRECATED in comp.flags:
            doc.append(
                document.Callout(
                    self._label_get("DEPRECATED_TEXT"),
                    kind=document.CalloutKind.WARNING,
                )
            )

        comp_s_desc_id = f"def_{comp.cid}_s_desc"
        comp_s_desc = comp.tooltip_properties.short_description
        comp_s_desc = self._lang_find_id(comp_s_desc_id, comp_s_desc)
        comp_s_desc = self._fmt_format(comp_s_desc)
        if comp_s_desc != "":
            doc.append(document.Paragraph(comp_s_desc))

        comp_desc_id = f"def_{comp.cid}_desc"
        comp_desc = comp.tooltip_properties.description
        comp_desc = self._lang_find_id(comp_desc_id, comp_desc)
        comp_desc = self._fmt_format(comp_desc)
        if comp_desc != "":
            doc.append(document.Paragraph(comp_desc))

        prop_doc = self.generate_property(comp)
        prop_doc.shift(1)
        doc.extend(prop_doc)

        logic_doc = self.generate_logic(comp.cid, comp.logic_nodes)
        logic_doc.shift(1)
        doc.extend(logic_doc)

        return doc

    def generate_component_list(
        self, comp_list: collections.abc.Iterable[component.Definition]
    ) -> document.Document:
        doc = document.Document()
        for comp in comp_list:
            comp_doc = self.generate_component(comp)
            doc.extend(comp_doc)
        return doc

    def generate(
        self, comp_list: collections.abc.Iterable[component.Definition]
    ) -> document.Document:
        def sort_key_category(category: component.Category) -> int:
            return category.value

        def sort_key_component(comp: component.Definition) -> tuple[str, str]:
            return comp.name, comp.cid

        category_comp_dict: dict[component.Category, list[component.Definition]] = {}
        for comp in comp_list:
            category_comp_list = category_comp_dict.setdefault(comp.category, [])
            category_comp_list.append(comp)

        category_list: collections.abc.Iterable[component.Category]
        category_list = category_comp_dict.keys()
        category_list = sorted(category_list, key=sort_key_category)

        doc = document.Document()
        for category in category_list:
            category_comp_list = category_comp_dict[category]
            category_comp_list.sort(key=sort_key_component)
            category_comp_list_doc = self.generate_component_list(category_comp_list)
            category_comp_list_doc.shift(1)

            doc.append(document.Heading(str(category)))
            doc.extend(category_comp_list_doc)
        return doc
