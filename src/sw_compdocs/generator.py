import collections.abc
import os
import pathlib
import typing

from . import component
from . import document
from . import language
from . import template


class LabelKeyError(KeyError):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key: typing.Final[str] = key

    def __str__(self) -> str:
        return f"missing label text for key {self.key!r}"


def _label_get(label: collections.abc.Mapping[str, str] | None, key: str) -> str:
    if label is not None:
        try:
            key = label[key]
        except KeyError as exc:
            raise LabelKeyError(key) from exc
    return key


def _lang_find_en(lang: language.Language | None, lang_en: str) -> str:
    if lang is None:
        return lang_en
    return lang.find_en(lang_en).local


def _lang_translate(lang: language.Language | None, text: language.Text) -> str:
    if lang is None:
        return text.en
    return lang.translate(text)


def _ctx_format(ctx: collections.abc.Mapping[str, str] | None, s: str) -> str:
    if ctx is not None:
        s = template.format(s, ctx)
    return s


def generate_document_property_table(
    defn: component.Definition,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    head = document.TableDataRow(
        [
            _label_get(label, "DOCUMENT_PROP_TABLE_HEAD_LABEL"),
            _label_get(label, "DOCUMENT_PROP_TABLE_HEAD_VALUE"),
        ]
    )
    data = document.TableData(head)

    mass_label = _label_get(label, "DOCUMENT_PROP_TABLE_MASS_LABEL")
    mass_value = f"{defn.mass:g}"
    data.append(document.TableDataRow([mass_label, mass_value]))

    dims_w = defn.voxel_max.x - defn.voxel_min.x + 1
    dims_h = defn.voxel_max.y - defn.voxel_min.y + 1
    dims_d = defn.voxel_max.z - defn.voxel_min.z + 1
    dims_label = _label_get(label, "DOCUMENT_PROP_TABLE_DIMS_LABEL")
    dims_value = f"{dims_w:d}x{dims_d:d}x{dims_h:d}"
    data.append(document.TableDataRow([dims_label, dims_value]))

    cost_label = _label_get(label, "DOCUMENT_PROP_TABLE_COST_LABEL")
    cost_value = f"{defn.value:d}"
    data.append(document.TableDataRow([cost_label, cost_value]))

    tags_label = _label_get(label, "DOCUMENT_PROP_TABLE_TAGS_LABEL")
    data.append(document.TableDataRow([tags_label, defn.tags]))

    file_label = _label_get(label, "DOCUMENT_PROP_TABLE_FILE_LABEL")
    file_value = ""
    if defn.file is not None:
        file_value = os.fsdecode(defn.file)
        file_value = pathlib.PurePath(file_value).name
    data.append(document.TableDataRow([file_label, file_value]))

    return document.Table(data)


def generate_document_property(
    defn: component.Definition,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
) -> document.Document:
    return document.Document(
        [
            document.Heading(_lang_find_en(lang, "PROPERTIES")),
            generate_document_property_table(defn, label=label),
        ]
    )


def generate_document_logic_table(
    ln_list: collections.abc.Iterable[component.LogicNode],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    head = document.TableDataRow(
        [
            _label_get(label, "DOCUMENT_LOGIC_TABLE_HEAD_TYPE"),
            _label_get(label, "DOCUMENT_LOGIC_TABLE_HEAD_LABEL"),
            _label_get(label, "DOCUMENT_LOGIC_TABLE_HEAD_DESC"),
        ]
    )
    data = document.TableData(head)
    for ln in ln_list:
        ln_type = _lang_find_en(lang, str(ln.type))
        ln_label = _lang_translate(lang, ln.label)
        ln_label = _ctx_format(ctx, ln_label)
        ln_desc = _lang_translate(lang, ln.description)
        ln_desc = _ctx_format(ctx, ln_desc)
        data.append(document.TableDataRow([ln_type, ln_label, ln_desc]))
    return document.Table(data)


def generate_document_logic(
    lns: component.LogicNodeList,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    in_list = []
    out_list = []
    conn_list = []
    for ln in lns:
        if (
            ln.type is component.LogicNodeType.BOOL
            or ln.type is component.LogicNodeType.FLOAT
            or ln.type is component.LogicNodeType.COMPOSITE
            or ln.type is component.LogicNodeType.VIDEO
            or ln.type is component.LogicNodeType.AUDIO
        ):
            if ln.mode is component.LogicNodeMode.INPUT:
                in_list.append(ln)
                continue
            if ln.mode is component.LogicNodeMode.OUTPUT:
                out_list.append(ln)
                continue
            typing.assert_never(ln.mode)
        if (
            ln.type is component.LogicNodeType.TORQUE
            or ln.type is component.LogicNodeType.WATER
            or ln.type is component.LogicNodeType.ELECTRIC
            or ln.type is component.LogicNodeType.ROPE
        ):
            conn_list.append(ln)
            continue
        typing.assert_never(ln.type)

    doc = document.Document()
    if len(in_list) > 0:
        in_head = document.Heading(_lang_find_en(lang, "logic inputs"))
        in_tbl = generate_document_logic_table(in_list, label=label, lang=lang, ctx=ctx)
        doc.append(in_head)
        doc.append(in_tbl)
    if len(out_list) > 0:
        out_head = document.Heading(_lang_find_en(lang, "logic outputs"))
        out_tbl = generate_document_logic_table(
            out_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(out_head)
        doc.append(out_tbl)
    if len(conn_list) > 0:
        conn_head = document.Heading(_lang_find_en(lang, "connections"))
        conn_tbl = generate_document_logic_table(
            conn_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(conn_head)
        doc.append(conn_tbl)
    return doc


def generate_document_component(
    defn: component.Definition,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    doc = document.Document()

    defn_name = _lang_translate(lang, defn.name)
    doc.append(document.Heading(defn_name))

    if component.Flags.IS_DEPRECATED in defn.flags:
        doc.append(
            document.Callout(
                _label_get(label, "DOCUMENT_DEPRECATED_TEXT"),
                kind=document.CalloutKind.WARNING,
            )
        )

    defn_s_desc_text = defn.tooltip_properties.short_description
    defn_s_desc = _lang_translate(lang, defn_s_desc_text)
    defn_s_desc = _ctx_format(ctx, defn_s_desc)
    if defn_s_desc != "":
        doc.append(document.Paragraph(defn_s_desc))

    defn_desc_text = defn.tooltip_properties.description
    defn_desc = _lang_translate(lang, defn_desc_text)
    defn_desc = _ctx_format(ctx, defn_desc)
    if defn_desc != "":
        doc.append(document.Paragraph(defn_desc))

    prop_doc = generate_document_property(defn, label=label, lang=lang)
    prop_doc.shift(1)
    doc.extend(prop_doc)

    logic_doc = generate_document_logic(
        defn.logic_nodes, label=label, lang=lang, ctx=ctx
    )
    logic_doc.shift(1)
    doc.extend(logic_doc)

    return doc


def generate_document_component_list(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    doc = document.Document()
    for comp in comp_list:
        comp_doc = generate_document_component(
            comp.defn, label=label, lang=lang, ctx=ctx
        )
        doc.extend(comp_doc)
    return doc


def generate_document(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    def sort_key_category(category: component.Category) -> int:
        return category.value

    def sort_key_component(comp: component.Component) -> tuple[str, bool, str]:
        return comp.name().en, comp.defn.key is None, comp.defn.key or ""

    category_comp_dict: dict[component.Category, list[component.Component]] = {}
    for comp in comp_list:
        category_comp_list = category_comp_dict.setdefault(comp.category(), [])
        category_comp_list.append(comp)

    category_list: collections.abc.Iterable[component.Category]
    category_list = category_comp_dict.keys()
    category_list = sorted(category_list, key=sort_key_category)

    doc = document.Document()
    for category in category_list:
        category_comp_list = category_comp_dict[category]
        category_comp_list.sort(key=sort_key_component)
        category_comp_list_doc = generate_document_component_list(
            category_comp_list, label=label, lang=lang, ctx=ctx
        )
        category_comp_list_doc.shift(1)

        doc.append(document.Heading(str(category)))
        doc.extend(category_comp_list_doc)
    return doc


def generate_sheet_component(
    comp: component.Component,
    *,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> list[str]:
    comp_voxel_min = comp.voxel_min()
    comp_voxel_max = comp.voxel_max()
    dims_w = comp_voxel_max.x - comp_voxel_min.x + 1
    dims_h = comp_voxel_max.y - comp_voxel_min.y + 1
    dims_d = comp_voxel_max.z - comp_voxel_min.z + 1

    comp_name = _lang_translate(lang, comp.name())

    comp_file = ""
    if comp.defn.file is not None:
        comp_file = os.fsdecode(comp.defn.file)
        comp_file = pathlib.PurePath(comp_file).name

    comp_s_desc_text = comp.short_description()
    comp_s_desc = _lang_translate(lang, comp_s_desc_text)
    comp_s_desc = _ctx_format(ctx, comp_s_desc)

    comp_desc_text = comp.description()
    comp_desc = _lang_translate(lang, comp_desc_text)
    comp_desc = _ctx_format(ctx, comp_desc)

    return [
        comp_name,
        comp_file,
        str(comp.category()),
        comp.tags(),
        "TRUE" if component.Flags.IS_DEPRECATED in comp.defn.flags else "FALSE",
        f"{comp.mass():g}",
        f"{comp.value():d}",
        f"{dims_w:d}",
        f"{dims_d:d}",
        f"{dims_h:d}",
        comp_s_desc,
        comp_desc,
    ]


def generate_sheet_component_list(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> list[list[str]]:
    record_list = []
    for comp in comp_list:
        record = generate_sheet_component(comp, lang=lang, ctx=ctx)
        record_list.append(record)
    return record_list


def generate_sheet(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> list[list[str]]:
    def sort_key(comp: component.Component) -> tuple[int, str, bool, str]:
        return (
            comp.category().value,
            comp.name().en,
            comp.defn.key is None,
            comp.defn.key or "",
        )

    comp_list = list(comp_list)
    comp_list.sort(key=sort_key)

    header = [
        _label_get(label, "SHEET_HEAD_NAME"),
        _label_get(label, "SHEET_HEAD_FILE"),
        _label_get(label, "SHEET_HEAD_CATEGORY"),
        _label_get(label, "SHEET_HEAD_TAGS"),
        _label_get(label, "SHEET_HEAD_DEPRECATED"),
        _label_get(label, "SHEET_HEAD_MASS"),
        _label_get(label, "SHEET_HEAD_COST"),
        _label_get(label, "SHEET_HEAD_WIDTH"),
        _label_get(label, "SHEET_HEAD_DEPTH"),
        _label_get(label, "SHEET_HEAD_HEIGHT"),
        _label_get(label, "SHEET_HEAD_SDESC"),
        _label_get(label, "SHEET_HEAD_DESC"),
    ]
    record_list = [header]
    record_list.extend(generate_sheet_component_list(comp_list, lang=lang, ctx=ctx))
    return record_list
