import sw_compdocs._types
import sw_compdocs.wraperr
import typing
import unittest


class TestUnicodeEncodeFileErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.wraperr.UnicodeEncodeFileError(
            "encoding", "object", 52149, 52150, "reason", filename="filename"
        )
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("encoding", "object", 52149, 52150, "reason"))
        self.assertEqual(exc.encoding, "encoding")
        self.assertEqual(exc.object, "object")
        self.assertEqual(exc.start, 52149)
        self.assertEqual(exc.end, 52150)
        self.assertEqual(exc.reason, "reason")
        self.assertEqual(exc.filename, "filename")


class TestUnicodeEncodeFileErrorExtends(unittest.TestCase):
    def test(self) -> None:
        base_exc = UnicodeEncodeError("encoding", "object", 52149, 52150, "reason")
        exc = sw_compdocs.wraperr.UnicodeEncodeFileError.extends(
            base_exc, filename="filename"
        )
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("encoding", "object", 52149, 52150, "reason"))
        self.assertEqual(exc.encoding, "encoding")
        self.assertEqual(exc.object, "object")
        self.assertEqual(exc.start, 52149)
        self.assertEqual(exc.end, 52150)
        self.assertEqual(exc.reason, "reason")
        self.assertEqual(exc.filename, "filename")


class TestUnicodeEncodeFileErrorStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_encoding", str),
                ("input_object", str),
                ("input_start", int),
                ("input_end", int),
                ("input_reason", str),
                ("input_filename", sw_compdocs._types.StrOrBytesPath | None),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_encoding="encoding",
                input_object="object",
                input_start=1,
                input_end=2,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't encode character '\\x62' in position 1: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="object",
                input_start=1,
                input_end=2,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't encode character '\\x62' in file 'filename': reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="あ",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't encode character '\\u3042' in position 0: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="あ",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't encode character '\\u3042' in file 'filename': reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="🀄",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't encode character '\\U0001f004' in position 0: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="🀄",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't encode character '\\U0001f004' in file 'filename': reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="object",
                input_start=1,
                input_end=3,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't encode characters in position 1-2: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="object",
                input_start=1,
                input_end=3,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't encode characters in file 'filename': reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="object",
                input_start=6,
                input_end=7,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't encode characters in position 6-6: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object="object",
                input_start=6,
                input_end=7,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't encode characters in file 'filename': reason",
            ),
        ]:
            with self.subTest(tc=tc):
                exc = sw_compdocs.wraperr.UnicodeEncodeFileError(
                    tc.input_encoding,
                    tc.input_object,
                    tc.input_start,
                    tc.input_end,
                    tc.input_reason,
                    filename=tc.input_filename,
                )
                got_s = str(exc)
                self.assertEqual(got_s, tc.want_s)


class TestUnicodeDecodeFileErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.wraperr.UnicodeDecodeFileError(
            "encoding", b"object", 52149, 52150, "reason", filename="filename"
        )
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("encoding", b"object", 52149, 52150, "reason"))
        self.assertEqual(exc.encoding, "encoding")
        self.assertEqual(exc.object, b"object")
        self.assertEqual(exc.start, 52149)
        self.assertEqual(exc.end, 52150)
        self.assertEqual(exc.reason, "reason")
        self.assertEqual(exc.filename, "filename")


class TestUnicodeDecodeFileErrorExtends(unittest.TestCase):
    def test(self) -> None:
        base_exc = UnicodeDecodeError("encoding", b"object", 52149, 52150, "reason")
        exc = sw_compdocs.wraperr.UnicodeDecodeFileError.extends(
            base_exc, filename="filename"
        )
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("encoding", b"object", 52149, 52150, "reason"))
        self.assertEqual(exc.encoding, "encoding")
        self.assertEqual(exc.object, b"object")
        self.assertEqual(exc.start, 52149)
        self.assertEqual(exc.end, 52150)
        self.assertEqual(exc.reason, "reason")
        self.assertEqual(exc.filename, "filename")


class TestUnicodeDecodeFileErrorStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_encoding", str),
                ("input_object", bytes),
                ("input_start", int),
                ("input_end", int),
                ("input_reason", str),
                ("input_filename", sw_compdocs._types.StrOrBytesPath | None),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_encoding="encoding",
                input_object=b"object",
                input_start=1,
                input_end=2,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't decode byte 0x62 in position 1: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object=b"object",
                input_start=1,
                input_end=2,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't decode byte 0x62 in file 'filename': reason",
            ),
            tt(
                input_encoding="encoding",
                input_object=b"object",
                input_start=1,
                input_end=3,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't decode bytes in position 1-2: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object=b"object",
                input_start=1,
                input_end=3,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't decode bytes in file 'filename': reason",
            ),
            tt(
                input_encoding="encoding",
                input_object=b"object",
                input_start=6,
                input_end=7,
                input_reason="reason",
                input_filename=None,
                want_s="'encoding' codec can't decode bytes in position 6-6: reason",
            ),
            tt(
                input_encoding="encoding",
                input_object=b"object",
                input_start=6,
                input_end=7,
                input_reason="reason",
                input_filename=b"filename",
                want_s="'encoding' codec can't decode bytes in file 'filename': reason",
            ),
        ]:
            with self.subTest(tc=tc):
                exc = sw_compdocs.wraperr.UnicodeDecodeFileError(
                    tc.input_encoding,
                    tc.input_object,
                    tc.input_start,
                    tc.input_end,
                    tc.input_reason,
                    filename=tc.input_filename,
                )
                got_s = str(exc)
                self.assertEqual(got_s, tc.want_s)


class TestUnicodeTranslateFileErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.wraperr.UnicodeTranslateFileError(
            "object", 52149, 52150, "reason", filename="filename"
        )
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("object", 52149, 52150, "reason"))
        self.assertEqual(exc.encoding, None)
        self.assertEqual(exc.object, "object")
        self.assertEqual(exc.start, 52149)
        self.assertEqual(exc.end, 52150)
        self.assertEqual(exc.reason, "reason")
        self.assertEqual(exc.filename, "filename")


class TestUnicodeTranslateFileErrorExtends(unittest.TestCase):
    def test(self) -> None:
        base_exc = UnicodeTranslateError("object", 52149, 52150, "reason")
        exc = sw_compdocs.wraperr.UnicodeTranslateFileError.extends(
            base_exc, filename="filename"
        )
        exc_args: tuple[object, ...] = exc.args
        self.assertEqual(exc_args, ("object", 52149, 52150, "reason"))
        self.assertEqual(exc.encoding, None)
        self.assertEqual(exc.object, "object")
        self.assertEqual(exc.start, 52149)
        self.assertEqual(exc.end, 52150)
        self.assertEqual(exc.reason, "reason")
        self.assertEqual(exc.filename, "filename")


class TestUnicodeTranslateFileErrorStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_object", str),
                ("input_start", int),
                ("input_end", int),
                ("input_reason", str),
                ("input_filename", sw_compdocs._types.StrOrBytesPath | None),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_object="object",
                input_start=1,
                input_end=2,
                input_reason="reason",
                input_filename=None,
                want_s="can't translate character '\\x62' in position 1: reason",
            ),
            tt(
                input_object="object",
                input_start=1,
                input_end=2,
                input_reason="reason",
                input_filename=b"filename",
                want_s="can't translate character '\\x62' in file 'filename': reason",
            ),
            tt(
                input_object="あ",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=None,
                want_s="can't translate character '\\u3042' in position 0: reason",
            ),
            tt(
                input_object="あ",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=b"filename",
                want_s="can't translate character '\\u3042' in file 'filename': reason",
            ),
            tt(
                input_object="🀄",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=None,
                want_s="can't translate character '\\U0001f004' in position 0: reason",
            ),
            tt(
                input_object="🀄",
                input_start=0,
                input_end=1,
                input_reason="reason",
                input_filename=b"filename",
                want_s="can't translate character '\\U0001f004' in file 'filename': reason",
            ),
            tt(
                input_object="object",
                input_start=1,
                input_end=3,
                input_reason="reason",
                input_filename=None,
                want_s="can't translate characters in position 1-2: reason",
            ),
            tt(
                input_object="object",
                input_start=1,
                input_end=3,
                input_reason="reason",
                input_filename=b"filename",
                want_s="can't translate characters in file 'filename': reason",
            ),
            tt(
                input_object="object",
                input_start=6,
                input_end=7,
                input_reason="reason",
                input_filename=None,
                want_s="can't translate characters in position 6-6: reason",
            ),
            tt(
                input_object="object",
                input_start=6,
                input_end=7,
                input_reason="reason",
                input_filename=b"filename",
                want_s="can't translate characters in file 'filename': reason",
            ),
        ]:
            with self.subTest(tc=tc):
                exc = sw_compdocs.wraperr.UnicodeTranslateFileError(
                    tc.input_object,
                    tc.input_start,
                    tc.input_end,
                    tc.input_reason,
                    filename=tc.input_filename,
                )
                got_s = str(exc)
                self.assertEqual(got_s, tc.want_s)


class TestWrapUnicodeError(unittest.TestCase):
    def test_pass(self) -> None:
        b = False
        with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
            b = True
        self.assertTrue(b)

    def test_exc_encode(self) -> None:
        base_exc = UnicodeEncodeError("encoding", "object", 52149, 52150, "reason")
        with self.assertRaises(sw_compdocs.wraperr.UnicodeEncodeFileError) as ctx:
            with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
                raise base_exc
        self.assertIs(ctx.exception.__cause__, base_exc)
        self.assertEqual(ctx.exception.encoding, "encoding")
        self.assertEqual(ctx.exception.object, "object")
        self.assertEqual(ctx.exception.start, 52149)
        self.assertEqual(ctx.exception.end, 52150)
        self.assertEqual(ctx.exception.reason, "reason")
        self.assertEqual(ctx.exception.filename, b"filename")

    def test_exc_decode(self) -> None:
        base_exc = UnicodeDecodeError("encoding", b"object", 52149, 52150, "reason")
        with self.assertRaises(sw_compdocs.wraperr.UnicodeDecodeFileError) as ctx:
            with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
                raise base_exc
        self.assertIs(ctx.exception.__cause__, base_exc)
        self.assertEqual(ctx.exception.encoding, "encoding")
        self.assertEqual(ctx.exception.object, b"object")
        self.assertEqual(ctx.exception.start, 52149)
        self.assertEqual(ctx.exception.end, 52150)
        self.assertEqual(ctx.exception.reason, "reason")
        self.assertEqual(ctx.exception.filename, b"filename")

    def test_exc_translate(self) -> None:
        base_exc = UnicodeTranslateError("object", 52149, 52150, "reason")
        with self.assertRaises(sw_compdocs.wraperr.UnicodeTranslateFileError) as ctx:
            with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
                raise base_exc
        self.assertIs(ctx.exception.__cause__, base_exc)
        self.assertEqual(ctx.exception.object, "object")
        self.assertEqual(ctx.exception.start, 52149)
        self.assertEqual(ctx.exception.end, 52150)
        self.assertEqual(ctx.exception.reason, "reason")
        self.assertEqual(ctx.exception.filename, b"filename")

    def test_exc_encode_file(self) -> None:
        base_exc = sw_compdocs.wraperr.UnicodeEncodeFileError(
            "encoding", "object", 52149, 52150, "reason"
        )
        with self.assertRaises(sw_compdocs.wraperr.UnicodeEncodeFileError) as ctx:
            with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
                raise base_exc
        self.assertIs(ctx.exception, base_exc)
        self.assertEqual(ctx.exception.filename, b"filename")
        self.assertIsNone(ctx.exception.__cause__)

    def test_exc_decode_file(self) -> None:
        base_exc = sw_compdocs.wraperr.UnicodeDecodeFileError(
            "encoding", b"object", 52149, 52150, "reason"
        )
        with self.assertRaises(sw_compdocs.wraperr.UnicodeDecodeFileError) as ctx:
            with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
                raise base_exc
        self.assertIs(ctx.exception, base_exc)
        self.assertEqual(ctx.exception.filename, b"filename")
        self.assertIsNone(ctx.exception.__cause__)

    def test_exc_translate_file(self) -> None:
        base_exc = sw_compdocs.wraperr.UnicodeTranslateFileError(
            "object", 52149, 52150, "reason"
        )
        with self.assertRaises(sw_compdocs.wraperr.UnicodeTranslateFileError) as ctx:
            with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
                raise base_exc
        self.assertIs(ctx.exception, base_exc)
        self.assertEqual(ctx.exception.filename, b"filename")
        self.assertIsNone(ctx.exception.__cause__)

    def test_exc_other(self) -> None:
        exc = Exception()
        with self.assertRaises(Exception) as ctx:
            with sw_compdocs.wraperr.wrap_unicode_error(filename=b"filename"):
                raise exc
        self.assertIs(ctx.exception, exc)
