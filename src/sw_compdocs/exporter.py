import collections.abc
import os
import pathlib
import typing

from . import _types
from . import document
from . import wraperr


def render_markdown_heading(head: document.Heading) -> str:
    if head.level < 1 or 6 < head.level:
        raise ValueError
    return "#" * head.level + " " + head.text + "\n"


def render_markdown_paragraph(para: document.Paragraph) -> str:
    return para.text + "\n"


def render_markdown_list_unordered(ul: document.UnorderedList) -> str:
    def fn(
        l: collections.abc.Iterable[document.ListItem],
    ) -> collections.abc.Iterable[str]:
        for li in l:
            yield "- " + li.s + "\n"
            for s in fn(li.l):
                yield "  " + s

    return "".join(fn(ul.l))


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
    if isinstance(blk, document.UnorderedList):
        return render_markdown_list_unordered(blk)
    if isinstance(blk, document.Table):
        return render_markdown_table(blk)
    if isinstance(blk, document.Callout):
        return render_markdown_callout(blk)
    raise Exception


def render_markdown(doc: document.Document) -> str:
    return "\n".join(render_markdown_block(blk) for blk in doc)


def export_markdown(
    doc: document.Document,
    file: _types.StrOrBytesPath,
    *,
    mode: typing.Literal["w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"] = "w",
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> None:
    md = render_markdown(doc)

    with wraperr.wrap_unicode_error(file):
        with open(
            file,
            mode=mode,
            encoding=encoding,
            errors=errors,
            newline=newline,
        ) as fp:
            fp.write(md)


def export_markdown_dict(
    doc_dict: collections.abc.Mapping[str, document.Document],
    dir: _types.StrOrBytesPath,
    *,
    mode: typing.Literal["w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"] = "w",
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> None:
    dir = os.fsdecode(dir)
    for name, doc in doc_dict.items():
        file = pathlib.Path(dir, name + ".md")
        export_markdown(
            doc,
            file,
            mode=mode,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )
