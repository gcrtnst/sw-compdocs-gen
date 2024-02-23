import pathlib
import sys


def find_steam() -> pathlib.Path | None:
    if sys.platform != "win32":
        return None

    import winreg

    try:
        with winreg.OpenKeyEx(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Valve\Steam",
            access=winreg.KEY_QUERY_VALUE | winreg.KEY_WOW64_32KEY,
        ) as reg_key:
            reg_query: tuple[object, int] = winreg.QueryValueEx(reg_key, "InstallPath")
    except FileNotFoundError:
        return None

    reg_val, reg_typ = reg_query
    if not isinstance(reg_val, str) or reg_typ != winreg.REG_SZ:
        return None

    steam_dir = pathlib.Path(reg_val)
    return steam_dir if steam_dir.is_dir() else None


def find_stormworks() -> pathlib.Path | None:
    steam_dir = find_steam()
    if steam_dir is None:
        return None

    # The correct way to get the game's installation folder is described on the
    # following page:
    # https://stackoverflow.com/questions/34090258/find-steam-games-folder
    #
    # However, that method requires parsing Valve Data Format, which can be cumbersome.
    # Therefore, this time we will skip parsing and assume the game's installation
    # folder is as follows:
    stormworks_dir = pathlib.Path(steam_dir, "steamapps/common/Stormworks")

    return stormworks_dir if stormworks_dir.is_dir() else None


def find_definitions() -> pathlib.Path | None:
    stormworks_dir = find_stormworks()
    if stormworks_dir is None:
        return None

    definitions_dir = pathlib.Path(stormworks_dir, "rom/data/definitions")
    return definitions_dir if definitions_dir.is_dir() else None
