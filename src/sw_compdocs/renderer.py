import typing

from . import document


def render_markdown_heading(head: document.Heading) -> str:
    if head.level < 1 or 6 < head.level:
        raise ValueError
    return "#" * head.level + " " + head.text + "\n"


def render_markdown_paragraph(para: document.Paragraph) -> str:
    return para.text + "\n"


def render_markdown_table_data_delimiter(n: int) -> str:
    if n <= 0:
        raise ValueError

    return "| " + "--- | " * (n - 1) + "--- |\n"


def render_markdown_table_data_row(row: document.TableDataRow) -> str:
    return "| " + " | ".join(row) + " |\n"


def render_markdown_table_data(data: document.TableData) -> str:
    return (
        render_markdown_table_data_row(data.head)
        + render_markdown_table_data_delimiter(len(data.head))
        + "".join(render_markdown_table_data_row(row) for row in data)
    )


def render_markdown_table(tbl: document.Table) -> str:
    return render_markdown_table_data(tbl.data)


def render_markdown_callout(callout: document.Callout) -> str:
    if callout.kind is document.CalloutKind.NOTE:
        kind = "NOTE"
    elif callout.kind is document.CalloutKind.WARNING:
        kind = "WARNING"
    else:
        typing.assert_never(callout.kind)

    l = [f"[!{kind}]"]
    l.extend(callout.text.split("\n"))
    l = ["> " + s for s in l]
    return "\n".join(l) + "\n"


def render_markdown_block(blk: document.Block) -> str:
    if isinstance(blk, document.Heading):
        return render_markdown_heading(blk)
    if isinstance(blk, document.Paragraph):
        return render_markdown_paragraph(blk)
    if isinstance(blk, document.Table):
        return render_markdown_table(blk)
    if isinstance(blk, document.Callout):
        return render_markdown_callout(blk)
    raise Exception


def render_markdown(doc: document.Document) -> str:
    return "\n".join(render_markdown_block(blk) for blk in doc)
