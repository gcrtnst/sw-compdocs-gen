import argparse
import collections.abc
import lxml.etree
import os
import pathlib
import sys
import typing

from . import _types
from . import component
from . import generator
from . import language
from . import renderer
from . import resource
from . import steamfind
from . import template
from . import wraperr


def format_os_error(exc: OSError) -> str:
    exc_filename: object = exc.filename
    exc_filename2: object = exc.filename2
    if exc_filename is None and exc_filename2 is not None:
        exc_filename, exc_filename2 = exc_filename2, exc_filename

    if (
        isinstance(exc_filename, str)
        or isinstance(exc_filename, bytes)
        or isinstance(exc_filename, os.PathLike)
    ):
        exc_filename = os.fsdecode(exc_filename)
    if (
        isinstance(exc_filename2, str)
        or isinstance(exc_filename2, bytes)
        or isinstance(exc_filename2, os.PathLike)
    ):
        exc_filename2 = os.fsdecode(exc_filename2)

    if exc.strerror is None:
        return str(exc)
    if exc_filename is None:
        return exc.strerror
    if exc_filename2 is None:
        return f"{exc.strerror} (file: {exc_filename!r})"
    return f"{exc.strerror} (file: {exc_filename!r}, {exc_filename2!r})"


def format_parse_error(exc: lxml.etree.ParseError) -> str:
    if exc.filename is not None:
        exc_filename = os.fsdecode(exc.filename)
        return f"{exc.msg} (in file '{exc_filename}')"
    return str(exc.msg)


def run(
    *,
    doc_file: _types.StrOrBytesPath,
    comp_dir: _types.StrOrBytesPath,
    label_file: _types.StrOrBytesPath | None = None,
    lang_file: _types.StrOrBytesPath | None = None,
    template_file: _types.StrOrBytesPath | None = None,
    doc_encoding: str = "utf-8",
    doc_newline: str = "\n",
) -> None:
    label = None
    if label_file is not None:
        label_tbl = resource.load_toml_table(label_file, "label")
        label = generator.LabelDict(label_tbl)

    lang = None
    if lang_file is not None:
        lang = language.Language.from_file(lang_file)

    fmt = None
    if template_file is not None:
        template_tbl = resource.load_toml_table(template_file, "template")
        fmt = template.TemplateFormatter(template_tbl)

    comp_list = []
    comp_dir = pathlib.Path(os.fsdecode(comp_dir))
    for comp_file in comp_dir.iterdir():
        if not comp_file.is_file():
            continue
        comp = component.parse_xml_file(comp_file)
        comp_list.append(comp)

    gen = generator.DocumentGenerator(label=label, lang=lang, fmt=fmt)
    doc = gen.generate(comp_list)
    md = renderer.render_markdown(doc)
    with open(
        doc_file, mode="w", encoding=doc_encoding, errors="replace", newline=doc_newline
    ) as fp:
        fp.write(md)


def main(
    *,
    prog: str | None = "sw_compdocs",
    args: collections.abc.Sequence[str] | None = None,
) -> None:
    argp_definitions_default = None
    argp_definitions_required = True
    argp_definitions_help = "stormworks definitions directory"
    argp_definitions_default_path = steamfind.find_definitions()
    if argp_definitions_default_path is not None:
        argp_definitions_default = os.fsdecode(argp_definitions_default_path)
        argp_definitions_required = False
        argp_definitions_help += f" (default: {argp_definitions_default!r})"

    argp = argparse.ArgumentParser(prog=prog)
    argp.add_argument(
        "-d",
        "--definitions",
        default=argp_definitions_default,
        required=argp_definitions_required,
        help=argp_definitions_help,
    )
    argp.add_argument(
        "-s",
        "--label",
        help="toml file containing label table",
    )
    argp.add_argument(
        "-l",
        "--language",
        help="stormworks language tsv file",
    )
    argp.add_argument(
        "-t",
        "--template",
        help="toml file containing template table",
    )
    argp.add_argument(
        "-e",
        "--encoding",
        default="utf-8",
        help="output encoding (default: %(default)s)",
    )
    argp.add_argument(
        "-n",
        "--newline",
        default="LF",
        choices=("CR", "LF", "CRLF"),
        help="output newline (default: %(default)s)",
    )
    argp.add_argument(
        "output",
        help="output file",
    )
    argv = argp.parse_args(args=args)

    argv_definitions: object = argv.definitions
    if not isinstance(argv_definitions, str):
        raise Exception

    argv_label: object = argv.label
    if argv_label is not None and not isinstance(argv_label, str):
        raise Exception

    argv_language: object = argv.language
    if argv_language is not None and not isinstance(argv_language, str):
        raise Exception

    argv_template: object = argv.template
    if argv_template is not None and not isinstance(argv_template, str):
        raise Exception

    argv_encoding: object = argv.encoding
    if not isinstance(argv_encoding, str):
        raise Exception

    argv_newline: object = argv.newline
    match argv_newline:
        case "CR":
            argv_newline = "\r"
        case "LF":
            argv_newline = "\n"
        case "CRLF":
            argv_newline = "\r\n"
        case _:
            raise Exception

    argv_output: object = argv.output
    if not isinstance(argv_output, str):
        raise Exception

    def error(msg: object) -> typing.NoReturn:
        print(f"{argp.prog}: error: {msg}", file=sys.stderr)
        sys.exit(1)

    try:
        run(
            doc_file=argv_output,
            comp_dir=argv_definitions,
            label_file=argv_label,
            lang_file=argv_language,
            template_file=argv_template,
            doc_encoding=argv_encoding,
            doc_newline=argv_newline,
        )
    except component.ComponentXMLError as exc:
        error(exc)
    except generator.LabelKeyError as exc:
        error(exc)
    except language.LanguageTSVError as exc:
        error(exc)
    except language.LanguageFindError as exc:
        error(exc)
    except resource.ResourceFileError as exc:
        error(exc)
    except resource.TOMLFileDecodeError as exc:
        error(exc)
    except template.TemplateKeyError as exc:
        error(exc)
    except wraperr.UnicodeEncodeFileError as exc:
        error(exc)
    except wraperr.UnicodeDecodeFileError as exc:
        error(exc)
    except wraperr.UnicodeTranslateFileError as exc:
        error(exc)
    except lxml.etree.ParseError as exc:
        exc_msg = format_parse_error(exc)
        error(exc_msg)
    except OSError as exc:
        exc_msg = format_os_error(exc)
        error(exc_msg)
