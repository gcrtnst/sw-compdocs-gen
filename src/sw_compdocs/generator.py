import collections.abc
import os
import pathlib
import typing

from . import _types
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


def _label_get(
    label: collections.abc.Mapping[str, str] | None,
    key: str,
    repl: str | None = None,
) -> str:
    if label is None:
        return key
    try:
        text = label[key]
    except KeyError as exc:
        raise LabelKeyError(key) from exc
    if repl is not None:
        text = text.replace("{}", repl)
    return text


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


def _classify_logic(
    lns: component.LogicNodeList,
) -> tuple[
    list[component.LogicNode], list[component.LogicNode], list[component.LogicNode]
]:
    in_list: list[component.LogicNode] = []
    out_list: list[component.LogicNode] = []
    conn_list: list[component.LogicNode] = []
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
    return in_list, out_list, conn_list


def generate_document_property_table_normal(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    head = document.TableDataRow(
        [
            _label_get(label, "DOCUMENT_PROP_TABLE_NORMAL_HEAD_LABEL"),
            _label_get(label, "DOCUMENT_PROP_TABLE_NORMAL_HEAD_VALUE"),
        ]
    )
    data = document.TableData(head)

    mass_label = _label_get(label, "DOCUMENT_PROP_TABLE_NORMAL_MASS_LABEL")
    mass_value = f"{comp.mass():g}"
    data.append(document.TableDataRow([mass_label, mass_value]))

    voxel_min = comp.voxel_min()
    voxel_max = comp.voxel_max()
    dims_w = voxel_max.x - voxel_min.x + 1
    dims_h = voxel_max.y - voxel_min.y + 1
    dims_d = voxel_max.z - voxel_min.z + 1
    dims_label = _label_get(label, "DOCUMENT_PROP_TABLE_NORMAL_DIMS_LABEL")
    dims_value = f"{dims_w:d}x{dims_d:d}x{dims_h:d}"
    data.append(document.TableDataRow([dims_label, dims_value]))

    cost_label = _label_get(label, "DOCUMENT_PROP_TABLE_NORMAL_COST_LABEL")
    cost_value = f"{comp.value():d}"
    data.append(document.TableDataRow([cost_label, cost_value]))

    tags_label = _label_get(label, "DOCUMENT_PROP_TABLE_NORMAL_TAGS_LABEL")
    data.append(document.TableDataRow([tags_label, comp.tags()]))

    file_label = _label_get(label, "DOCUMENT_PROP_TABLE_NORMAL_FILE_LABEL")
    file_value = ""
    if comp.defn.file is not None:
        file_value = os.fsdecode(comp.defn.file)
        file_value = pathlib.PurePath(file_value).name
    data.append(document.TableDataRow([file_label, file_value]))

    return document.Table(data)


def generate_document_property_table_multibody(
    comp: component.Multibody,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    def file_fn(file: _types.StrOrBytesPath | None) -> str:
        if file is None:
            return ""
        file = os.fsdecode(file)
        file = pathlib.PurePath(file)
        return file.name

    data = document.TableData(
        document.TableDataRow(
            [
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_HEAD_LABEL"),
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_HEAD_PARENT"),
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_HEAD_CHILD"),
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_HEAD_TOTAL"),
            ]
        )
    )

    data.append(
        document.TableDataRow(
            [
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_MASS_LABEL"),
                f"{comp.defn.mass:g}",
                f"{comp.child.mass:g}",
                f"{comp.mass():g}",
            ]
        )
    )

    comp_total_voxel_max = comp.voxel_max()
    comp_total_voxel_min = comp.voxel_min()
    dims_parent_w = comp.defn.voxel_max.x - comp.defn.voxel_min.x + 1
    dims_parent_h = comp.defn.voxel_max.y - comp.defn.voxel_min.y + 1
    dims_parent_d = comp.defn.voxel_max.z - comp.defn.voxel_min.z + 1
    dims_child_w = comp.child.voxel_max.x - comp.child.voxel_min.x + 1
    dims_child_h = comp.child.voxel_max.y - comp.child.voxel_min.y + 1
    dims_child_d = comp.child.voxel_max.z - comp.child.voxel_min.z + 1
    dims_total_w = comp_total_voxel_max.x - comp_total_voxel_min.x + 1
    dims_total_h = comp_total_voxel_max.y - comp_total_voxel_min.y + 1
    dims_total_d = comp_total_voxel_max.z - comp_total_voxel_min.z + 1
    data.append(
        document.TableDataRow(
            [
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_DIMS_LABEL"),
                f"{dims_parent_w:d}x{dims_parent_d:d}x{dims_parent_h:d}",
                f"{dims_child_w:d}x{dims_child_d:d}x{dims_child_h:d}",
                f"{dims_total_w:d}x{dims_total_d:d}x{dims_total_h:d}",
            ]
        )
    )

    data.append(
        document.TableDataRow(
            [
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_COST_LABEL"),
                f"{comp.defn.value:d}",
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_COST_CHILD"),
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_COST_TOTAL"),
            ]
        )
    )

    data.append(
        document.TableDataRow(
            [
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_TAGS_LABEL"),
                comp.defn.tags,
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_TAGS_CHILD"),
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_TAGS_TOTAL"),
            ]
        )
    )

    data.append(
        document.TableDataRow(
            [
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_FILE_LABEL"),
                file_fn(comp.defn.file),
                file_fn(comp.child.file),
                _label_get(label, "DOCUMENT_PROP_TABLE_MULTIBODY_FILE_TOTAL"),
            ]
        )
    )

    return document.Table(data)


def generate_document_property_table(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    if isinstance(comp, component.Multibody):
        return generate_document_property_table_multibody(comp, label=label)
    return generate_document_property_table_normal(comp, label=label)


def generate_document_property(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
) -> document.Document:
    return document.Document(
        [
            document.Heading(_lang_find_en(lang, "PROPERTIES")),
            generate_document_property_table(comp, label=label),
        ]
    )


def generate_document_logic_table_normal(
    ln_list: collections.abc.Iterable[component.LogicNode],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    head = document.TableDataRow(
        [
            _label_get(label, "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE"),
            _label_get(label, "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL"),
            _label_get(label, "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC"),
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


def generate_document_logic_normal(
    lns: component.LogicNodeList,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    in_list, out_list, conn_list = _classify_logic(lns)
    doc = document.Document()
    if len(in_list) > 0:
        in_head = document.Heading(_lang_find_en(lang, "logic inputs"))
        in_tbl = generate_document_logic_table_normal(
            in_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(in_head)
        doc.append(in_tbl)
    if len(out_list) > 0:
        out_head = document.Heading(_lang_find_en(lang, "logic outputs"))
        out_tbl = generate_document_logic_table_normal(
            out_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(out_head)
        doc.append(out_tbl)
    if len(conn_list) > 0:
        conn_head = document.Heading(_lang_find_en(lang, "connections"))
        conn_tbl = generate_document_logic_table_normal(
            conn_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(conn_head)
        doc.append(conn_tbl)
    return doc


def generate_document_logic_table_multibody(
    parent_ln_list: collections.abc.Iterable[component.LogicNode],
    child_ln_list: collections.abc.Iterable[component.LogicNode],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    def generate_row(
        body: str, ln_list: collections.abc.Iterable[component.LogicNode]
    ) -> collections.abc.Iterable[document.TableDataRow]:
        for ln in ln_list:
            ln_type = _lang_find_en(lang, str(ln.type))
            ln_label = _lang_translate(lang, ln.label)
            ln_label = _ctx_format(ctx, ln_label)
            ln_desc = _lang_translate(lang, ln.description)
            ln_desc = _ctx_format(ctx, ln_desc)
            yield document.TableDataRow([body, ln_type, ln_label, ln_desc])

    head = document.TableDataRow(
        [
            _label_get(label, "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY"),
            _label_get(label, "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE"),
            _label_get(label, "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL"),
            _label_get(label, "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC"),
        ]
    )
    data = document.TableData(head)

    parent_label = _label_get(label, "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT")
    child_label = _label_get(label, "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD")
    data.extend(generate_row(parent_label, parent_ln_list))
    data.extend(generate_row(child_label, child_ln_list))
    return document.Table(data)


def generate_document_logic_multibody(
    parent_lns: component.LogicNodeList,
    child_lns: component.LogicNodeList,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    parent_ln_list_tuple = _classify_logic(parent_lns)
    parent_in_ln_list, parent_out_ln_list, parent_conn_ln_list = parent_ln_list_tuple
    child_ln_list_tuple = _classify_logic(child_lns)
    child_in_ln_list, child_out_ln_list, child_conn_ln_list = child_ln_list_tuple

    doc = document.Document()
    if len(parent_in_ln_list) > 0 or len(child_in_ln_list) > 0:
        in_head = document.Heading(_lang_find_en(lang, "logic inputs"))
        in_tbl = generate_document_logic_table_multibody(
            parent_in_ln_list, child_in_ln_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(in_head)
        doc.append(in_tbl)
    if len(parent_out_ln_list) > 0 or len(child_out_ln_list) > 0:
        out_head = document.Heading(_lang_find_en(lang, "logic outputs"))
        out_tbl = generate_document_logic_table_multibody(
            parent_out_ln_list, child_out_ln_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(out_head)
        doc.append(out_tbl)
    if len(parent_conn_ln_list) > 0 or len(child_conn_ln_list) > 0:
        conn_head = document.Heading(_lang_find_en(lang, "connections"))
        conn_tbl = generate_document_logic_table_multibody(
            parent_conn_ln_list, child_conn_ln_list, label=label, lang=lang, ctx=ctx
        )
        doc.append(conn_head)
        doc.append(conn_tbl)
    return doc


def generate_document_logic(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    if isinstance(comp, component.Multibody):
        return generate_document_logic_multibody(
            comp.defn.logic_nodes,
            comp.child.logic_nodes,
            label=label,
            lang=lang,
            ctx=ctx,
        )
    return generate_document_logic_normal(
        comp.defn.logic_nodes,
        label=label,
        lang=lang,
        ctx=ctx,
    )


def generate_document_component(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    doc = document.Document()

    comp_name = _lang_translate(lang, comp.name())
    doc.append(document.Heading(comp_name))

    if component.Flags.IS_DEPRECATED in comp.defn.flags:
        doc.append(
            document.Callout(
                _label_get(label, "DOCUMENT_DEPRECATED_TEXT"),
                kind=document.CalloutKind.WARNING,
            )
        )

    if component.Flags.MULTIBODY_CHILD in comp.defn.flags:
        doc.append(
            document.Callout(
                _label_get(label, "DOCUMENT_ORPHAN_TEXT"),
                kind=document.CalloutKind.WARNING,
            )
        )

    comp_s_desc_text = comp.short_description()
    comp_s_desc = _lang_translate(lang, comp_s_desc_text)
    comp_s_desc = _ctx_format(ctx, comp_s_desc)
    if comp_s_desc != "":
        doc.append(document.Paragraph(comp_s_desc))

    comp_desc_text = comp.description()
    comp_desc = _lang_translate(lang, comp_desc_text)
    comp_desc = _ctx_format(ctx, comp_desc)
    if comp_desc != "":
        doc.append(document.Paragraph(comp_desc))

    prop_doc = generate_document_property(comp, label=label, lang=lang)
    prop_doc.shift(1)
    doc.extend(prop_doc)

    logic_doc = generate_document_logic(comp, label=label, lang=lang, ctx=ctx)
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
        comp_doc = generate_document_component(comp, label=label, lang=lang, ctx=ctx)
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

    dims_total_w = comp_voxel_max.x - comp_voxel_min.x + 1
    dims_total_h = comp_voxel_max.y - comp_voxel_min.y + 1
    dims_total_d = comp_voxel_max.z - comp_voxel_min.z + 1
    dims_parent_w = comp.defn.voxel_max.x - comp.defn.voxel_min.x + 1
    dims_parent_h = comp.defn.voxel_max.y - comp.defn.voxel_min.y + 1
    dims_parent_d = comp.defn.voxel_max.z - comp.defn.voxel_min.z + 1
    dims_child_w = None
    dims_child_h = None
    dims_child_d = None
    if isinstance(comp, component.Multibody):
        dims_child_w = comp.child.voxel_max.x - comp.child.voxel_min.x + 1
        dims_child_h = comp.child.voxel_max.y - comp.child.voxel_min.y + 1
        dims_child_d = comp.child.voxel_max.z - comp.child.voxel_min.z + 1

    comp_name = _lang_translate(lang, comp.name())

    comp_file_parent = ""
    if comp.defn.file is not None:
        comp_file_parent = os.fsdecode(comp.defn.file)
        comp_file_parent = pathlib.PurePath(comp_file_parent).name

    comp_file_child = ""
    if isinstance(comp, component.Multibody) and comp.child.file is not None:
        comp_file_child = os.fsdecode(comp.child.file)
        comp_file_child = pathlib.PurePath(comp_file_child).name

    comp_s_desc_text = comp.short_description()
    comp_s_desc = _lang_translate(lang, comp_s_desc_text)
    comp_s_desc = _ctx_format(ctx, comp_s_desc)

    comp_desc_text = comp.description()
    comp_desc = _lang_translate(lang, comp_desc_text)
    comp_desc = _ctx_format(ctx, comp_desc)

    return [
        comp_name,
        comp_file_parent,
        comp_file_child,
        str(comp.category()),
        comp.tags(),
        "TRUE" if component.Flags.IS_DEPRECATED in comp.defn.flags else "FALSE",
        "TRUE" if component.Flags.MULTIBODY_CHILD in comp.defn.flags else "FALSE",
        f"{comp.value():d}",
        f"{comp.mass():g}",
        f"{comp.defn.mass:g}",
        f"{comp.child.mass:g}" if isinstance(comp, component.Multibody) else "",
        f"{dims_total_w:d}",
        f"{dims_total_d:d}",
        f"{dims_total_h:d}",
        f"{dims_parent_w:d}",
        f"{dims_parent_d:d}",
        f"{dims_parent_h:d}",
        f"{dims_child_w:d}" if dims_child_w is not None else "",
        f"{dims_child_d:d}" if dims_child_d is not None else "",
        f"{dims_child_h:d}" if dims_child_h is not None else "",
        comp_s_desc,
        comp_desc,
    ]


def generate_sheet_component_list(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    lang: language.Language | None = None,
    ctx: collections.abc.Mapping[str, str] | None = None,
) -> list[list[str]]:
    record_list: list[list[str]] = []
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
        _label_get(label, "SHEET_HEAD_FILE_PARENT"),
        _label_get(label, "SHEET_HEAD_FILE_CHILD"),
        _label_get(label, "SHEET_HEAD_CATEGORY"),
        _label_get(label, "SHEET_HEAD_TAGS"),
        _label_get(label, "SHEET_HEAD_DEPRECATED"),
        _label_get(label, "SHEET_HEAD_ORPHAN"),
        _label_get(label, "SHEET_HEAD_COST"),
        _label_get(label, "SHEET_HEAD_MASS_TOTAL"),
        _label_get(label, "SHEET_HEAD_MASS_PARENT"),
        _label_get(label, "SHEET_HEAD_MASS_CHILD"),
        _label_get(label, "SHEET_HEAD_DIMS_TOTAL_WIDTH"),
        _label_get(label, "SHEET_HEAD_DIMS_TOTAL_DEPTH"),
        _label_get(label, "SHEET_HEAD_DIMS_TOTAL_HEIGHT"),
        _label_get(label, "SHEET_HEAD_DIMS_PARENT_WIDTH"),
        _label_get(label, "SHEET_HEAD_DIMS_PARENT_DEPTH"),
        _label_get(label, "SHEET_HEAD_DIMS_PARENT_HEIGHT"),
        _label_get(label, "SHEET_HEAD_DIMS_CHILD_WIDTH"),
        _label_get(label, "SHEET_HEAD_DIMS_CHILD_DEPTH"),
        _label_get(label, "SHEET_HEAD_DIMS_CHILD_HEIGHT"),
        _label_get(label, "SHEET_HEAD_SDESC"),
        _label_get(label, "SHEET_HEAD_DESC"),
    ]
    record_list = [header]
    record_list.extend(generate_sheet_component_list(comp_list, lang=lang, ctx=ctx))
    return record_list
