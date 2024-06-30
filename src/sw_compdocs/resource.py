import collections.abc
import os
import re
import tomllib
import typing

from . import _types
from . import wraperr


default_label: typing.Final[collections.abc.Mapping[str, str]] = {
    "DOCUMENT_PROP_MASS": "Mass: {}",
    "DOCUMENT_PROP_MASS_PARENT": "Parent Mass: {}",
    "DOCUMENT_PROP_MASS_CHILD": "Child Mass: {}",
    "DOCUMENT_PROP_DIMS": "Dimensions (WxDxH): {}",
    "DOCUMENT_PROP_DIMS_PARENT": "Parent Dimensions (WxDxH): {}",
    "DOCUMENT_PROP_DIMS_CHILD": "Child Dimensions (WxDxH): {}",
    "DOCUMENT_PROP_COST": "Cost: ${}",
    "DOCUMENT_PROP_TAGS": "Tags: {}",
    "DOCUMENT_PROP_FILE": "File: {}",
    "DOCUMENT_PROP_FILE_PARENT": "Parent File: {}",
    "DOCUMENT_PROP_FILE_CHILD": "Child File: {}",
    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_TYPE": "Type",
    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_LABEL": "Label",
    "DOCUMENT_LOGIC_TABLE_NORMAL_HEAD_DESC": "Description",
    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_BODY": "Body",
    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_TYPE": "Type",
    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_LABEL": "Label",
    "DOCUMENT_LOGIC_TABLE_MULTIBODY_HEAD_DESC": "Description",
    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_PARENT": "Parent",
    "DOCUMENT_LOGIC_TABLE_MULTIBODY_BODY_CHILD": "Child",
    "DOCUMENT_DEPRECATED_TEXT": "This component is deprecated.",
    "DOCUMENT_ORPHANED_TEXT": "This component is orphaned. No parent component found.",
    "SHEET_HEAD_NAME": "Name",
    "SHEET_HEAD_FILE": "File",
    "SHEET_HEAD_CATEGORY": "Category",
    "SHEET_HEAD_TAGS": "Tags",
    "SHEET_HEAD_MULTIBODY": "Multibody",
    "SHEET_HEAD_DEPRECATED": "Deprecated",
    "SHEET_HEAD_ORPHANED": "Orphaned",
    "SHEET_HEAD_COST": "Cost",
    "SHEET_HEAD_MASS": "Mass",
    "SHEET_HEAD_DIMS_WIDTH": "Width",
    "SHEET_HEAD_DIMS_DEPTH": "Depth",
    "SHEET_HEAD_DIMS_HEIGHT": "Height",
    "SHEET_HEAD_SDESC": "Short Description",
    "SHEET_HEAD_DESC": "Description",
}


default_bind: typing.Final[collections.abc.Mapping[str, str]] = {
    "action_axis_ui_navigate_x": "pad 1 axis 1",
    "action_axis_ui_navigate_y": "pad 1 axis 2",
    "action_ui_select": "pad 1 button 1",
    "action_ui_back": "pad 1 button 2",
    "action_ui_context": "pad 1 button 3",
    "action_ui_tab_left": "pad 1 button 5",
    "action_ui_tab_right": "pad 1 button 6",
    "action_axis_move_x": "pad 1 axis 1",
    "action_axis_move_y": "pad 1 axis 2",
    "action_axis_view_x": "pad 1 axis 3",
    "action_axis_view_y": "pad 1 axis 4",
    "action_up": "w",
    "action_down": "s",
    "action_left": "a",
    "action_right": "d",
    "action_crouch": "lctrl",
    "action_jump": "space",
    "action_sprint": "lshift",
    "action_walk": "unassigned",
    "action_interact_left": "q",
    "action_interact_right": "e",
    "action_equipment_use": "lmb",
    "action_equipment_secondary": "r",
    "action_equipment_drop": "backspace",
    "action_equipment_cycle_next": "v",
    "action_equipment_cycle_prev": "c",
    "action_use_seat": "f",
    "action_return_to_workbench": "b",
    "action_axis_1": "pad 1 axis 1",
    "action_axis_2": "pad 1 axis 2",
    "action_axis_3": "pad 1 axis 3",
    "action_axis_4": "pad 1 axis 4",
    "action_axis_5": "pad 1 axis 5",
    "action_axis_6": "pad 1 axis 6",
    "action_axis_7": "pad 1 axis 7",
    "action_axis_8": "pad 1 axis 8",
    "action_throttle_up": "up",
    "action_throttle_down": "down",
    "action_pedal_left": "left",
    "action_pedal_right": "right",
    "action_trim": "lalt",
    "action_hide_seat_ui": "h",
    "action_pad_look_left": "unassigned",
    "action_pad_look_right": "unassigned",
    "action_pad_look_down": "unassigned",
    "action_pad_look_up": "unassigned",
    "action_free_view": "pad 1 button 5",
    "action_trigger": "space",
    "action_hotkey_1": "1",
    "action_hotkey_2": "2",
    "action_hotkey_3": "3",
    "action_hotkey_4": "4",
    "action_hotkey_5": "5",
    "action_hotkey_6": "6",
    "action_hotkey_7": "unassigned",
    "action_hotkey_8": "unassigned",
    "action_hotkey_9": "unassigned",
    "action_hotkey_10": "unassigned",
    "action_hotkey_11": "unassigned",
    "action_hotkey_12": "unassigned",
    "action_hotkey_13": "unassigned",
    "action_hotkey_14": "unassigned",
    "action_hotkey_15": "unassigned",
    "action_hotkey_16": "unassigned",
    "action_hotkey_17": "unassigned",
    "action_hotkey_18": "unassigned",
    "action_hotkey_19": "unassigned",
    "action_hotkey_20": "unassigned",
    "action_hotkey_21": "unassigned",
    "action_hotkey_22": "unassigned",
    "action_hotkey_23": "unassigned",
    "action_hotkey_24": "unassigned",
    "action_hotkey_25": "unassigned",
    "action_hotkey_26": "unassigned",
    "action_hotkey_27": "unassigned",
    "action_hotkey_28": "unassigned",
    "action_hotkey_29": "unassigned",
    "action_hotkey_30": "unassigned",
    "action_hotkey_31": "unassigned",
    "action_hotkey_32": "unassigned",
    "action_hotkey_33": "unassigned",
    "action_hotkey_34": "unassigned",
    "action_hotkey_35": "unassigned",
    "action_hotkey_36": "unassigned",
    "action_hotkey_37": "unassigned",
    "action_hotkey_38": "unassigned",
    "action_hotkey_39": "unassigned",
    "action_hotkey_40": "unassigned",
    "action_hotkey_41": "unassigned",
    "action_hotkey_42": "unassigned",
    "action_hotkey_43": "unassigned",
    "action_hotkey_44": "unassigned",
    "action_hotkey_45": "unassigned",
    "action_hotkey_46": "unassigned",
    "action_hotkey_47": "unassigned",
    "action_hotkey_48": "unassigned",
    "action_camera_mode": "tab",
    "action_zoom": "rmb",
    "action_photo_crane_up": "up",
    "action_photo_crane_down": "down",
    "action_photo_slow": "lctrl",
    "action_photo_fast": "lshift",
    "action_photo_very_fast": "lalt",
    "action_photo_pause": "p",
    "action_photo_hide": "h",
    "action_photo_reset": "r",
    "action_player_list": "`",
    "action_emote_wheel": "unassigned",
    "action_quick_chat": "enter",
    "action_voice_chat": "'",
    "action_pause": "pad 1 button 8",
    "action_map": "m",
    "action_creative_menu": "unassigned",
    "action_photo_mode": "unassigned",
    "action_labels_detailed": "page up",
    "action_noclip": "home",
    "action_editor_camera_forward": "w",
    "action_editor_camera_back": "s",
    "action_editor_camera_left": "a",
    "action_editor_camera_right": "d",
    "action_editor_camera_up": "e",
    "action_editor_camera_down": "q",
    "action_editor_camera_zoom_in": "=",
    "action_editor_camera_zoom_out": "-",
    "action_editor_camera_set_origin": "f",
    "action_editor_rotate_x": "j",
    "action_editor_rotate_y": "k",
    "action_editor_rotate_z": "l",
    "action_editor_flip_x": "u",
    "action_editor_flip_y": "i",
    "action_editor_flip_z": "o",
    "action_editor_show_rotation_ui": "p",
    "action_editor_toggle_eraser": "x",
    "action_editor_show_hide_vehicle": "h",
    "action_editor_spawn_vehicle": "enter",
}


class ResourceFileError(Exception):
    def __init__(self, msg: str, *, file: _types.StrOrBytesPath | None = None) -> None:
        super().__init__(msg)
        self.msg: typing.Final[str] = msg
        self.file: _types.StrOrBytesPath | None = file

    def __str__(self) -> str:
        msg = self.msg
        if self.file is not None:
            file = os.fsdecode(self.file)
            msg = f"{self.msg} (in file '{file}')"
        return msg


class TOMLFileDecodeError(tomllib.TOMLDecodeError):
    def __init__(
        self, *args: object, file: _types.StrOrBytesPath | None = None
    ) -> None:
        super().__init__(*args)
        self.file: _types.StrOrBytesPath | None = file

    def __str__(self) -> str:
        msg_list: list[str] = []

        msg = super().__str__()
        if msg != "":
            msg_list.append(msg)

        if self.file is not None:
            file = os.fsdecode(self.file)
            msg_list.append(f"(in file '{file}')")

        msg_full = " ".join(msg_list)
        return msg_full


def format_toml_string(s: str) -> str:
    esc_set = frozenset(chr(i) for i in range(0x00, 0x20)) | {'"', "\\", "\x7f"}
    esc_dict = {
        "\b": r"\b",
        "\t": r"\t",
        "\n": r"\n",
        "\f": r"\f",
        "\r": r"\r",
        '"': r"\"",
        "\\": r"\\",
    }

    l: list[str] = []
    for c in s:
        if c not in esc_set:
            l.append(c)
            continue
        if c in esc_dict:
            l.append(esc_dict[c])
            continue

        u = ord(c)
        if u <= 0xFFFF:
            l.append(f"\\u{u:04X}")
            continue
        l.append(f"\\U{u:08X}")
    return '"' + "".join(l) + '"'


def format_toml_key(key: str) -> str:
    if re.search(r"\A[A-Za-z0-9_\-]+\Z", key) is not None:
        return key
    return format_toml_string(key)


def load_toml_table(file: _types.StrOrBytesPath, table_key: str) -> dict[str, str]:
    try:
        with wraperr.wrap_unicode_error(file):
            with open(file, mode="rb") as fp:
                toml: dict[str, object] = tomllib.load(fp)
    except tomllib.TOMLDecodeError as exc:
        exc_args: tuple[object, ...] = exc.args
        raise TOMLFileDecodeError(*exc_args, file=file) from exc

    obj = toml.get(table_key)
    if obj is None:
        exc_table_key = format_toml_key(table_key)
        exc_msg = f"table {exc_table_key!r} does not exist"
        raise ResourceFileError(exc_msg, file=file)
    if not isinstance(obj, dict):
        exc_table_key = format_toml_key(table_key)
        exc_obj_type = type(obj).__name__
        exc_msg = f"expected table for {exc_table_key!r}, but found {exc_obj_type}"
        raise ResourceFileError(exc_msg, file=file)

    # dict[typing.Any, typing.Any] -> dict[object, object]
    obj = typing.cast(dict[object, object], obj)

    table: dict[str, str] = {}
    for key, val in obj.items():
        if not isinstance(key, str):
            # In TOML, keys are always strings.
            # If a non-string key is given, it is a bug in tomllib.
            raise Exception
        if not isinstance(val, str):
            exc_key_1 = format_toml_key(table_key)
            exc_key_2 = format_toml_key(key)
            exc_key = exc_key_1 + "." + exc_key_2
            exc_val_type = type(val).__name__
            exc_msg = f"expected string value for {exc_key!r}, but found {exc_val_type}"
            raise ResourceFileError(exc_msg, file=file)
        table[key] = val
    return table


def load_label(file: _types.StrOrBytesPath | None = None) -> dict[str, str]:
    if file is None:
        return dict(default_label)
    return load_toml_table(file, "label")


def load_keybindings(file: _types.StrOrBytesPath | None = None) -> dict[str, str]:
    if file is None:
        return dict(default_bind)
    return load_toml_table(file, "keybindings")
