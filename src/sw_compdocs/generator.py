import collections.abc
import os
import tomllib
import typing

from . import _types
from . import component
from . import document
from . import language
from . import template
from . import validator


class LabelFileError(Exception):
    @property
    def msg(self) -> str:
        return self._msg

    @property
    def file(self) -> _types.StrOrBytesPath | None:
        return self._file

    @file.setter
    def file(self, value: _types.StrOrBytesPath | None) -> None:
        if value is not None and not validator.is_pathlike(value):
            raise TypeError
        self._file = value

    def __init__(self, msg: str) -> None:
        if type(msg) is not str:
            raise TypeError

        super().__init__(msg)
        self._msg = msg
        self._file = None

    def __str__(self) -> str:
        file = os.fsdecode(self.file) if self.file is not None else "<label.toml>"
        return f"{file}: {self.msg}"


class LabelDictError(Exception):
    @property
    def msg(self) -> str:
        return self._msg

    def __init__(self, msg: str) -> None:
        if type(msg) is not str:
            raise TypeError

        super().__init__(msg)
        self._msg = msg

    def __str__(self) -> str:
        return self.msg

    def with_file(self, file: _types.StrOrBytesPath | None) -> LabelFileError:
        exc = LabelFileError(self.msg)
        exc.file = file
        return exc


class LabelKeyError(KeyError):
    def __init__(self, key: object) -> None:
        super().__init__(key)
        self.key = key

    def __str__(self) -> str:
        return f"missing label text for key {self.key!r}"


class LabelDict(collections.abc.Mapping[str, str]):
    def __init__(self, mapping: object = {}):
        if not isinstance(mapping, collections.abc.Mapping):
            raise LabelDictError(
                f"invalid label mapping type: {type(mapping).__name__}"
            )

        self._d = {}
        for k, v in mapping.items():
            if not isinstance(k, str):
                raise LabelDictError(f"expected string for label key: {k!r}")
            if not isinstance(v, str):
                raise LabelDictError(f"expected string for label text: {v!r}")
            self._d[k] = v

    @classmethod
    def _from_toml(cls, toml: dict[str, object]) -> typing.Self:
        mapping = toml.get("label")
        if mapping is None:
            raise LabelFileError("missing label table")

        try:
            return cls(mapping)
        except LabelDictError as exc:
            raise exc.with_file(None) from exc

    @classmethod
    def from_toml_file(cls, file: _types.StrOrBytesPath) -> typing.Self:
        if not validator.is_pathlike(file):
            raise TypeError

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
    @property
    def label(self) -> LabelDict | None:
        return self._label

    @label.setter
    def label(self, value: LabelDict | None) -> None:
        if value is not None and type(value) is not LabelDict:
            raise TypeError
        self._label = value

    @property
    def lang(self) -> language.Language | None:
        return self._lang

    @lang.setter
    def lang(self, value: language.Language | None) -> None:
        if value is not None and type(value) is not language.Language:
            raise TypeError
        self._lang = value

    @property
    def fmt(self) -> template.TemplateFormatter | None:
        return self._fmt

    @fmt.setter
    def fmt(self, value: template.TemplateFormatter | None) -> None:
        if value is not None and type(value) is not template.TemplateFormatter:
            raise TypeError
        self._fmt = value

    def __init__(
        self,
        *,
        label: LabelDict | None = None,
        lang: language.Language | None = None,
        fmt: template.TemplateFormatter | None = None,
    ):
        self.label = label
        self.lang = lang
        self.fmt = fmt

    def _label_get(self, s: str) -> str:
        if type(s) is not str:
            raise TypeError

        if self.label is not None:
            s = self.label[s]
        return s

    def _lang_find_id(self, lang_id: str, lang_en: str) -> str:
        if type(lang_en) is not str:
            raise TypeError
        if self.lang is None:
            return lang_en
        return self.lang.find_id(lang_id).local

    def _lang_find_en(self, lang_en: str) -> str:
        if type(lang_en) is not str:
            raise TypeError
        if self.lang is None:
            return lang_en
        return self.lang.find_en(lang_en).local

    def _fmt_format(self, s: str) -> str:
        if type(s) is not str:
            raise TypeError

        if self.fmt is not None:
            s = self.fmt.format(s)
        return s

    def generate_property_table(self, comp: component.Definition) -> document.Table:
        if type(comp) is not component.Definition:
            raise TypeError

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
        if type(cid) is not str or type(lns) is not component.LogicNodeList:
            raise TypeError

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
        if type(cid) is not str or type(lns) is not component.LogicNodeList:
            raise TypeError

        in_lns = component.LogicNodeList()
        out_lns = component.LogicNodeList()
        conn_lns = component.LogicNodeList()
        for ln in lns:
            if ln.type in (
                component.LogicNodeType.BOOL,
                component.LogicNodeType.FLOAT,
                component.LogicNodeType.COMPOSITE,
                component.LogicNodeType.VIDEO,
                component.LogicNodeType.AUDIO,
            ):
                if ln.mode is component.LogicNodeMode.INPUT:
                    in_lns.append(ln)
                    continue
                if ln.mode is component.LogicNodeMode.OUTPUT:
                    out_lns.append(ln)
                    continue
                raise Exception
            if ln.type in (
                component.LogicNodeType.TORQUE,
                component.LogicNodeType.WATER,
                component.LogicNodeType.ELECTRIC,
                component.LogicNodeType.ROPE,
            ):
                conn_lns.append(ln)
                continue
            raise Exception

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
        if type(comp) is not component.Definition:
            raise TypeError
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
            if type(comp) is not component.Definition:
                raise TypeError
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
