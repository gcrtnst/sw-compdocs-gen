import os
import sw_compdocs.steamfind
import unittest


class TestFindSteam(unittest.TestCase):
    def test_windows(self) -> None:
        if os.name != "nt":
            self.skipTest("Not Windows")

        # Test only that no exception is thrown,
        # since the return value depends on whether Steam is installed.
        sw_compdocs.steamfind.find_steam()

    def test_nonwindows(self) -> None:
        if os.name == "nt":
            self.skipTest("Windows")

        steam_dir = sw_compdocs.steamfind.find_steam()
        self.assertIsNone(steam_dir)


class TestFindStormworks(unittest.TestCase):
    def test_steam_installed(self) -> None:
        steam_dir = sw_compdocs.steamfind.find_steam()
        if steam_dir is None:
            self.skipTest("Steam is not installed")

        # Test only that no exception is thrown,
        # since the return value depends on whether Stormworks is installed.
        sw_compdocs.steamfind.find_stormworks()

    def test_steam_missing(self) -> None:
        steam_dir = sw_compdocs.steamfind.find_steam()
        if steam_dir is not None:
            self.skipTest("Steam is installed")

        stormworks_dir = sw_compdocs.steamfind.find_stormworks()
        self.assertIsNone(stormworks_dir)


class TestFindDefinitions(unittest.TestCase):
    def test_stormworks_installed(self) -> None:
        stormworks_dir = sw_compdocs.steamfind.find_stormworks()
        if stormworks_dir is None:
            self.skipTest("Stormworks is not installed")

        # Test only that no exception is thrown,
        # since the return value depends on whether Stormworks is installed.
        sw_compdocs.steamfind.find_definitions()

    def test_stormworks_missing(self) -> None:
        stormworks_dir = sw_compdocs.steamfind.find_stormworks()
        if stormworks_dir is not None:
            self.skipTest("Stormworks is installed")

        definitions_dir = sw_compdocs.steamfind.find_definitions()
        self.assertIsNone(definitions_dir)
