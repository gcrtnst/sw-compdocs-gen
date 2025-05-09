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


class LabelMissingPlaceholderError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key: typing.Final[str] = key

    def __str__(self) -> str:
        return f"missing placeholder in label text for key {self.key!r}"


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
        if "{}" not in text:
            raise LabelMissingPlaceholderError(key)
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


def _bind_format(bind: collections.abc.Mapping[str, str] | None, s: str) -> str:
    if bind is not None:
        s = template.format(s, bind)
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


def generate_document_property_list(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
) -> document.UnorderedList:
    def file_fn(file: _types.StrOrBytesPath | None) -> str:
        if file is None:
            return ""
        file = os.fsdecode(file)
        file = pathlib.PurePath(file)
        return file.name

    ul = document.UnorderedList()

    mass = f"{comp.mass():g}"
    mass = _label_get(label, "DOCUMENT_PROP_MASS", mass)
    mass = document.ListItem(mass)
    if isinstance(comp, component.Multibody):
        mass_parent = f"{comp.defn.mass:g}"
        mass_parent = _label_get(label, "DOCUMENT_PROP_MASS_PARENT", mass_parent)
        mass_parent = document.ListItem(mass_parent)
        mass.l.append(mass_parent)

        mass_child = f"{comp.child.mass:g}"
        mass_child = _label_get(label, "DOCUMENT_PROP_MASS_CHILD", mass_child)
        mass_child = document.ListItem(mass_child)
        mass.l.append(mass_child)
    ul.l.append(mass)

    comp_total_voxel_max = comp.voxel_max()
    comp_total_voxel_min = comp.voxel_min()
    dims_total_w = comp_total_voxel_max.x - comp_total_voxel_min.x + 1
    dims_total_h = comp_total_voxel_max.y - comp_total_voxel_min.y + 1
    dims_total_d = comp_total_voxel_max.z - comp_total_voxel_min.z + 1
    dims = f"{dims_total_w:d}x{dims_total_d:d}x{dims_total_h:d}"
    dims = _label_get(label, "DOCUMENT_PROP_DIMS", dims)
    dims = document.ListItem(dims)
    if isinstance(comp, component.Multibody):
        comp_parent_voxel_max = comp.defn.voxel_max()
        comp_parent_voxel_min = comp.defn.voxel_min()
        dims_parent_w = comp_parent_voxel_max.x - comp_parent_voxel_min.x + 1
        dims_parent_h = comp_parent_voxel_max.y - comp_parent_voxel_min.y + 1
        dims_parent_d = comp_parent_voxel_max.z - comp_parent_voxel_min.z + 1
        dims_parent = f"{dims_parent_w:d}x{dims_parent_d:d}x{dims_parent_h:d}"
        dims_parent = _label_get(label, "DOCUMENT_PROP_DIMS_PARENT", dims_parent)
        dims_parent = document.ListItem(dims_parent)
        dims.l.append(dims_parent)

        comp_child_voxel_max = comp.child.voxel_max()
        comp_child_voxel_min = comp.child.voxel_min()
        dims_child_w = comp_child_voxel_max.x - comp_child_voxel_min.x + 1
        dims_child_h = comp_child_voxel_max.y - comp_child_voxel_min.y + 1
        dims_child_d = comp_child_voxel_max.z - comp_child_voxel_min.z + 1
        dims_child = f"{dims_child_w:d}x{dims_child_d:d}x{dims_child_h:d}"
        dims_child = _label_get(label, "DOCUMENT_PROP_DIMS_CHILD", dims_child)
        dims_child = document.ListItem(dims_child)
        dims.l.append(dims_child)
    ul.l.append(dims)

    cost = f"{comp.value():d}"
    cost = _label_get(label, "DOCUMENT_PROP_COST", cost)
    cost = document.ListItem(cost)
    ul.l.append(cost)

    tags = comp.tags()
    tags = _label_get(label, "DOCUMENT_PROP_TAGS", tags)
    tags = document.ListItem(tags)
    ul.l.append(tags)

    if not isinstance(comp, component.Multibody):
        file = file_fn(comp.defn.file)
        file = _label_get(label, "DOCUMENT_PROP_FILE", file)
        file = document.ListItem(file)
        ul.l.append(file)
    else:
        file_parent = file_fn(comp.defn.file)
        file_parent = _label_get(label, "DOCUMENT_PROP_FILE_PARENT", file_parent)
        file_parent = document.ListItem(file_parent)
        ul.l.append(file_parent)

        file_child = file_fn(comp.child.file)
        file_child = _label_get(label, "DOCUMENT_PROP_FILE_CHILD", file_child)
        file_child = document.ListItem(file_child)
        ul.l.append(file_child)

    return ul


def generate_document_property(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
) -> document.Document:
    return document.Document(
        [
            document.Heading(_lang_find_en(lang, "PROPERTIES")),
            generate_document_property_list(comp, label=label),
        ]
    )


def generate_document_logic_table_normal(
    ln_list: collections.abc.Iterable[component.LogicNode],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
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
        ln_label = _bind_format(bind, ln_label)
        ln_desc = _lang_translate(lang, ln.description)
        ln_desc = _bind_format(bind, ln_desc)
        data.append(document.TableDataRow([ln_type, ln_label, ln_desc]))
    return document.Table(data)


def generate_document_logic_normal(
    lns: component.LogicNodeList,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    in_list, out_list, conn_list = _classify_logic(lns)
    doc = document.Document()
    if len(in_list) > 0:
        in_head = document.Heading(_lang_find_en(lang, "logic inputs"))
        in_tbl = generate_document_logic_table_normal(
            in_list, label=label, lang=lang, bind=bind
        )
        doc.append(in_head)
        doc.append(in_tbl)
    if len(out_list) > 0:
        out_head = document.Heading(_lang_find_en(lang, "logic outputs"))
        out_tbl = generate_document_logic_table_normal(
            out_list, label=label, lang=lang, bind=bind
        )
        doc.append(out_head)
        doc.append(out_tbl)
    if len(conn_list) > 0:
        conn_head = document.Heading(_lang_find_en(lang, "connections"))
        conn_tbl = generate_document_logic_table_normal(
            conn_list, label=label, lang=lang, bind=bind
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
    bind: collections.abc.Mapping[str, str] | None = None,
) -> document.Table:
    def generate_row(
        body: str, ln_list: collections.abc.Iterable[component.LogicNode]
    ) -> collections.abc.Iterable[document.TableDataRow]:
        for ln in ln_list:
            ln_type = _lang_find_en(lang, str(ln.type))
            ln_label = _lang_translate(lang, ln.label)
            ln_label = _bind_format(bind, ln_label)
            ln_desc = _lang_translate(lang, ln.description)
            ln_desc = _bind_format(bind, ln_desc)
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
    bind: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    parent_ln_list_tuple = _classify_logic(parent_lns)
    parent_in_ln_list, parent_out_ln_list, parent_conn_ln_list = parent_ln_list_tuple
    child_ln_list_tuple = _classify_logic(child_lns)
    child_in_ln_list, child_out_ln_list, child_conn_ln_list = child_ln_list_tuple

    doc = document.Document()
    if len(parent_in_ln_list) > 0 or len(child_in_ln_list) > 0:
        in_head = document.Heading(_lang_find_en(lang, "logic inputs"))
        in_tbl = generate_document_logic_table_multibody(
            parent_in_ln_list, child_in_ln_list, label=label, lang=lang, bind=bind
        )
        doc.append(in_head)
        doc.append(in_tbl)
    if len(parent_out_ln_list) > 0 or len(child_out_ln_list) > 0:
        out_head = document.Heading(_lang_find_en(lang, "logic outputs"))
        out_tbl = generate_document_logic_table_multibody(
            parent_out_ln_list, child_out_ln_list, label=label, lang=lang, bind=bind
        )
        doc.append(out_head)
        doc.append(out_tbl)
    if len(parent_conn_ln_list) > 0 or len(child_conn_ln_list) > 0:
        conn_head = document.Heading(_lang_find_en(lang, "connections"))
        conn_tbl = generate_document_logic_table_multibody(
            parent_conn_ln_list, child_conn_ln_list, label=label, lang=lang, bind=bind
        )
        doc.append(conn_head)
        doc.append(conn_tbl)
    return doc


def generate_document_logic(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    if isinstance(comp, component.Multibody):
        return generate_document_logic_multibody(
            comp.defn.logic_nodes,
            comp.child.logic_nodes,
            label=label,
            lang=lang,
            bind=bind,
        )
    return generate_document_logic_normal(
        comp.defn.logic_nodes,
        label=label,
        lang=lang,
        bind=bind,
    )


def generate_document_component(
    comp: component.Component,
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    doc = document.Document()

    comp_name = _lang_translate(lang, comp.name())
    if component.Flags.IS_DEPRECATED in comp.defn.flags:
        comp_name += " (Deprecated)"
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
                _label_get(label, "DOCUMENT_ORPHANED_TEXT"),
                kind=document.CalloutKind.WARNING,
            )
        )

    comp_s_desc_text = comp.short_description()
    comp_s_desc = _lang_translate(lang, comp_s_desc_text)
    comp_s_desc = _bind_format(bind, comp_s_desc)
    if comp_s_desc != "":
        doc.append(document.Paragraph(comp_s_desc))

    comp_desc_text = comp.description()
    comp_desc = _lang_translate(lang, comp_desc_text)
    comp_desc = _bind_format(bind, comp_desc)
    if comp_desc != "":
        doc.append(document.Paragraph(comp_desc))

    prop_doc = generate_document_property(comp, label=label, lang=lang)
    prop_doc.shift(1)
    doc.extend(prop_doc)

    logic_doc = generate_document_logic(comp, label=label, lang=lang, bind=bind)
    logic_doc.shift(1)
    doc.extend(logic_doc)

    return doc


def generate_document_component_list(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    doc = document.Document()
    for comp in comp_list:
        comp_doc = generate_document_component(comp, label=label, lang=lang, bind=bind)
        doc.extend(comp_doc)
    return doc


def generate_document_category(
    category: component.Category,
    comp_list: collections.abc.Iterable[component.Component],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> document.Document:
    def sort_key_component(
        comp: component.Component,
    ) -> tuple[bool, bool, str, bool, str]:
        return (
            component.Flags.MULTIBODY_CHILD in comp.defn.flags,
            component.Flags.IS_DEPRECATED in comp.defn.flags,
            comp.name().en.upper(),
            comp.defn.key is None,
            comp.defn.key or "",
        )

    comp_list = list(comp_list)
    for comp in comp_list:
        if comp.category() is not category:
            raise ValueError
    comp_list.sort(key=sort_key_component)

    comp_list_doc = generate_document_component_list(
        comp_list,
        label=label,
        lang=lang,
        bind=bind,
    )
    comp_list_doc.shift(1)

    doc = document.Document()
    doc.append(document.Heading(str(category)))
    doc.extend(comp_list_doc)
    return doc


def generate_document(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> dict[str, document.Document]:
    def sort_key_category(category: component.Category) -> int:
        return category.value

    category_comp_dict: dict[component.Category, list[component.Component]] = {}
    for comp in comp_list:
        category_comp_list = category_comp_dict.setdefault(comp.category(), [])
        category_comp_list.append(comp)

    category_list: collections.abc.Iterable[component.Category]
    category_list = category_comp_dict.keys()
    category_list = sorted(category_list, key=sort_key_category)

    doc_dict: dict[str, document.Document] = {}
    for category in category_list:
        category_comp_list = category_comp_dict[category]

        doc_name = f"{category.value:02d}_{category.name}"
        doc = generate_document_category(
            category,
            category_comp_list,
            label=label,
            lang=lang,
            bind=bind,
        )
        doc_dict[doc_name] = doc
    return doc_dict


def generate_sheet_component(
    comp: component.Component,
    *,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> list[str]:
    comp_name = _lang_translate(lang, comp.name())
    if component.Flags.IS_DEPRECATED in comp.defn.flags:
        comp_name += " (Deprecated)"

    comp_file = ""
    if comp.defn.file is not None:
        comp_file = os.fsdecode(comp.defn.file)
        comp_file = pathlib.PurePath(comp_file).name

    comp_voxel_min = comp.voxel_min()
    comp_voxel_max = comp.voxel_max()
    comp_dims_w = comp_voxel_max.x - comp_voxel_min.x + 1
    comp_dims_h = comp_voxel_max.y - comp_voxel_min.y + 1
    comp_dims_d = comp_voxel_max.z - comp_voxel_min.z + 1

    comp_s_desc_text = comp.short_description()
    comp_s_desc = _lang_translate(lang, comp_s_desc_text)
    comp_s_desc = _bind_format(bind, comp_s_desc)

    comp_desc_text = comp.description()
    comp_desc = _lang_translate(lang, comp_desc_text)
    comp_desc = _bind_format(bind, comp_desc)

    return [
        comp_name,
        comp_file,
        str(comp.category()),
        comp.tags(),
        "TRUE" if isinstance(comp, component.Multibody) else "FALSE",
        "TRUE" if component.Flags.IS_DEPRECATED in comp.defn.flags else "FALSE",
        "TRUE" if component.Flags.MULTIBODY_CHILD in comp.defn.flags else "FALSE",
        f"{comp.value():d}",
        f"{comp.mass():g}",
        f"{comp_dims_w:d}",
        f"{comp_dims_d:d}",
        f"{comp_dims_h:d}",
        comp_s_desc,
        comp_desc,
    ]


def generate_sheet_component_list(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> list[list[str]]:
    record_list: list[list[str]] = []
    for comp in comp_list:
        record = generate_sheet_component(comp, lang=lang, bind=bind)
        record_list.append(record)
    return record_list


def generate_sheet(
    comp_list: collections.abc.Iterable[component.Component],
    *,
    label: collections.abc.Mapping[str, str] | None = None,
    lang: language.Language | None = None,
    bind: collections.abc.Mapping[str, str] | None = None,
) -> list[list[str]]:
    def sort_key(comp: component.Component) -> tuple[int, bool, bool, str, bool, str]:
        return (
            comp.category().value,
            component.Flags.MULTIBODY_CHILD in comp.defn.flags,
            component.Flags.IS_DEPRECATED in comp.defn.flags,
            comp.name().en.upper(),
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
        _label_get(label, "SHEET_HEAD_MULTIBODY"),
        _label_get(label, "SHEET_HEAD_DEPRECATED"),
        _label_get(label, "SHEET_HEAD_ORPHANED"),
        _label_get(label, "SHEET_HEAD_COST"),
        _label_get(label, "SHEET_HEAD_MASS"),
        _label_get(label, "SHEET_HEAD_DIMS_WIDTH"),
        _label_get(label, "SHEET_HEAD_DIMS_DEPTH"),
        _label_get(label, "SHEET_HEAD_DIMS_HEIGHT"),
        _label_get(label, "SHEET_HEAD_SDESC"),
        _label_get(label, "SHEET_HEAD_DESC"),
    ]
    record_list = [header]
    record_list.extend(generate_sheet_component_list(comp_list, lang=lang, bind=bind))
    return record_list
