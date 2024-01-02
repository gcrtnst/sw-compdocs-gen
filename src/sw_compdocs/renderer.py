from . import document


def render_markdown(doc):
    if not isinstance(doc, document.Document):
        raise TypeError

    return "\n".join(render_markdown_block(blk) for blk in doc)


def render_markdown_block(blk):
    if not isinstance(blk, document.Block):
        raise TypeError

    if isinstance(blk, document.Heading):
        return render_markdown_heading(blk)
    if isinstance(blk, document.Paragraph):
        return render_markdown_paragraph(blk)
    if isinstance(blk, document.Table):
        return render_markdown_table(blk)
    if isinstance(blk, document.Callout):
        return render_markdown_callout(blk)
    raise Exception


def render_markdown_heading(head):
    if not isinstance(head, document.Heading):
        raise TypeError
    return "#" * head.level + " " + head.text + "\n"


def render_markdown_paragraph(para):
    if not isinstance(para, document.Paragraph):
        raise TypeError
    return para.text + "\n"


def render_markdown_table(tbl):
    if not isinstance(tbl, document.Table):
        raise TypeError

    return render_markdown_table_data(tbl.data)


def render_markdown_table_data(data):
    if not isinstance(data, document.TableData):
        raise TypeError

    return (
        render_markdown_table_data_row(data.head)
        + render_markdown_table_data_delimiter(len(data.head))
        + "".join(render_markdown_table_data_row(row) for row in data)
    )


def render_markdown_table_data_row(row):
    if not isinstance(row, document.TableDataRow):
        raise TypeError

    return "| " + " | ".join(row) + " |\n"


def render_markdown_table_data_delimiter(n):
    if type(n) is not int:
        raise TypeError
    if n <= 0:
        raise ValueError

    return "| " + "--- | " * (n - 1) + "--- |\n"


def render_markdown_callout(callout):
    if not isinstance(callout, document.Callout):
        raise TypeError

    if callout.kind is document.CalloutKind.NOTE:
        kind = "NOTE"
    elif callout.kind is document.CalloutKind.WARNING:
        kind = "WARNING"
    else:
        raise Exception

    l = [f"[!{kind}]"]
    l.extend(callout.text.split("\n"))
    l = ["> " + s for s in l]
    return "\n".join(l) + "\n"
