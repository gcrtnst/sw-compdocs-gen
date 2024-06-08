import argparse
import collections.abc
import csv
import lxml.etree
import os
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


class ShowHideAction(argparse.Action):
    def __init__(
        self,
        option_strings: collections.abc.Sequence[str],
        dest: str,
        default: object = None,
        required: bool = False,
        help: str | None = None,
    ) -> None:
        if len(option_strings) <= 0:
            raise ValueError

        _option_strings: list[str] = []
        for option_string in option_strings:
            if not option_string.startswith("--show-"):
                raise ValueError
            _option_strings.append(option_string)
            _option_strings.append("--hide-" + option_string[7:])

        super().__init__(
            option_strings=_option_strings,
            dest=dest,
            nargs=0,
            default=default,
            required=required,
            help=help,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: object,
        values: object,
        option_string: str | None = None,
    ) -> None:
        if option_string is not None and option_string in self.option_strings:
            setattr(namespace, self.dest, option_string.startswith("--show-"))

    def format_usage(self) -> str:
        return " | ".join(self.option_strings)


def generate_document(
    *,
    out_file: _types.StrOrBytesPath,
    comp_list: collections.abc.Iterable[component.Component],
    label: collections.abc.Mapping[str, str] | None,
    lang: language.Language | None,
    ctx: collections.abc.Mapping[str, str] | None,
    out_encoding: str | None = None,
    out_newline: typing.Literal["\r", "\n", "\r\n"] | None = None,
) -> None:
    if out_encoding is None:
        out_encoding = "utf-8"
    if out_newline is None:
        out_newline = "\n"

    doc = generator.generate_document(comp_list, label=label, lang=lang, ctx=ctx)
    md = renderer.render_markdown(doc)

    with wraperr.wrap_unicode_error(out_file):
        with open(
            out_file,
            mode="w",
            encoding=out_encoding,
            errors="strict",
            newline=out_newline,
        ) as fp:
            fp.write(md)


def generate_sheet(
    *,
    out_file: _types.StrOrBytesPath,
    comp_list: collections.abc.Iterable[component.Component],
    label: collections.abc.Mapping[str, str] | None,
    lang: language.Language | None,
    ctx: collections.abc.Mapping[str, str] | None,
    out_encoding: str | None = None,
    out_newline: typing.Literal["\r", "\n", "\r\n"] | None = None,
) -> None:
    if out_encoding is None:
        out_encoding = "utf-8"
    if out_newline is None:
        out_newline = "\r\n"

    record_list = generator.generate_sheet(comp_list, label=label, lang=lang, ctx=ctx)
    with wraperr.wrap_unicode_error(out_file):
        with open(
            out_file, mode="w", encoding=out_encoding, errors="strict", newline=""
        ) as fp:
            writer = csv.writer(fp, dialect="excel", lineterminator=out_newline)
            writer.writerows(record_list)


def run(
    *,
    out_file: _types.StrOrBytesPath,
    defn_dir: _types.StrOrBytesPath,
    show_deprecated: bool = True,
    show_orphan: bool = False,
    label_file: _types.StrOrBytesPath | None = None,
    lang_file: _types.StrOrBytesPath | None = None,
    template_file: _types.StrOrBytesPath | None = None,
    out_mode: typing.Literal["document", "sheet"] = "document",
    out_encoding: str | None = None,
    out_newline: typing.Literal["\r", "\n", "\r\n"] | None = None,
) -> None:
    label = None
    if label_file is not None:
        label = resource.load_toml_table(label_file, "label")

    lang = None
    if lang_file is not None:
        lang = language.Language.from_file(lang_file, errors="strict")

    ctx = None
    if template_file is not None:
        ctx = resource.load_toml_table(template_file, "template")

    comp_list = component.load_comp_list(defn_dir)
    comp_list = [
        comp
        for comp in comp_list
        if (
            (show_deprecated or component.Flags.IS_DEPRECATED not in comp.defn.flags)
            and (show_orphan or component.Flags.MULTIBODY_CHILD not in comp.defn.flags)
        )
    ]

    if out_mode == "document":
        generate_document(
            out_file=out_file,
            comp_list=comp_list,
            label=label,
            lang=lang,
            ctx=ctx,
            out_encoding=out_encoding,
            out_newline=out_newline,
        )
        return
    if out_mode == "sheet":
        generate_sheet(
            out_file=out_file,
            comp_list=comp_list,
            label=label,
            lang=lang,
            ctx=ctx,
            out_encoding=out_encoding,
            out_newline=out_newline,
        )
        return
    typing.assert_never(out_mode)


def format_os_error(exc: OSError) -> str:
    exc_strerror = typing.cast(object, exc.strerror)
    exc_filename: object = exc.filename
    exc_filename2: object = exc.filename2
    if exc_filename is None and exc_filename2 is not None:
        exc_filename, exc_filename2 = exc_filename2, exc_filename

    if _types.is_pathlike(exc_filename):
        exc_filename = os.fsdecode(exc_filename)
    if _types.is_pathlike(exc_filename2):
        exc_filename2 = os.fsdecode(exc_filename2)

    if exc_strerror is None:
        return str(exc)
    if exc_filename is None:
        return exc.strerror
    if exc_filename2 is None:
        return f"{exc.strerror} (file: '{exc_filename}')"
    return f"{exc.strerror} (file: '{exc_filename}', '{exc_filename2}')"


def format_parse_error(exc: lxml.etree.ParseError) -> str:
    if exc.filename is not None:
        exc_filename = os.fsdecode(exc.filename)
        return f"{exc.msg} (in file '{exc_filename}')"
    return str(exc.msg)


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
        argp_definitions_help += f" (default: '{argp_definitions_default}')"

    argp = argparse.ArgumentParser(prog=prog, allow_abbrev=False)
    argp.add_argument(
        "-d",
        "--definitions",
        default=argp_definitions_default,
        required=argp_definitions_required,
        help=argp_definitions_help,
    )
    argp.add_argument(
        "--show-deprecated",
        action=ShowHideAction,
        default=True,
        help="show deprecated components (default: show)",
    )
    argp.add_argument(
        "--show-orphan",
        action=ShowHideAction,
        default=False,
        help="show orphan components (default: hide)",
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
        "-m",
        "--mode",
        default="document",
        choices=("document", "sheet"),
        help="output mode (default: %(default)s)",
    )
    argp.add_argument(
        "-e",
        "--encoding",
        help="output encoding (default varies by output format)",
    )
    argp.add_argument(
        "-n",
        "--newline",
        choices=("CR", "LF", "CRLF"),
        help="output newline (default varies by output format)",
    )
    argp.add_argument(
        "output",
        help="output file",
    )
    argv = argp.parse_args(args=args)

    argv_definitions: object = argv.definitions
    if not isinstance(argv_definitions, str):
        raise Exception

    argv_show_deprecated: object = argv.show_deprecated
    if not isinstance(argv_show_deprecated, bool):
        raise Exception

    argv_show_orphan: object = argv.show_orphan
    if not isinstance(argv_show_orphan, bool):
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

    argv_mode: typing.Literal["document", "sheet"] = argv.mode
    if argv_mode != "document" and argv_mode != "sheet":
        raise Exception

    argv_encoding: object = argv.encoding
    if argv_encoding is not None and not isinstance(argv_encoding, str):
        raise Exception

    argv_newline: object = argv.newline
    match argv_newline:
        case "CR":
            argv_newline = "\r"
        case "LF":
            argv_newline = "\n"
        case "CRLF":
            argv_newline = "\r\n"
        case None:
            pass
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
            out_file=argv_output,
            defn_dir=argv_definitions,
            show_deprecated=argv_show_deprecated,
            show_orphan=argv_show_orphan,
            label_file=argv_label,
            lang_file=argv_language,
            template_file=argv_template,
            out_mode=argv_mode,
            out_encoding=argv_encoding,
            out_newline=argv_newline,
        )
    except component.DefinitionXMLError as exc:
        error(exc)
    except component.MultibodyLinkError as exc:
        error(exc)
    except generator.LabelKeyError as exc:
        error(exc)
    except generator.LabelMissingPlaceholderError as exc:
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
