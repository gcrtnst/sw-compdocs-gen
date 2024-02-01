import collections.abc
import os
import pathlib
import sw_compdocs._types
import sw_compdocs.component
import sw_compdocs.generator
import sw_compdocs.language
import sw_compdocs.template
import tempfile
import typing
import unittest


class TestDocumentGeneratorInit(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", sw_compdocs.generator.LabelDict | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_fmt", sw_compdocs.template.TemplateFormatter | None),
            ],
        )

        for tc in [
            tt(
                input_label=sw_compdocs.generator.LabelDict(),
                input_lang=sw_compdocs.language.Language(),
                input_fmt=sw_compdocs.template.TemplateFormatter({}),
            ),
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(),
                input_fmt=sw_compdocs.template.TemplateFormatter({}),
            ),
            tt(
                input_label=sw_compdocs.generator.LabelDict(),
                input_lang=None,
                input_fmt=sw_compdocs.template.TemplateFormatter({}),
            ),
            tt(
                input_label=sw_compdocs.generator.LabelDict(),
                input_lang=sw_compdocs.language.Language(),
                input_fmt=None,
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(
                    label=tc.input_label, lang=tc.input_lang, fmt=tc.input_fmt
                )
                self.assertIs(gen.label, tc.input_label)
                self.assertIs(gen.lang, tc.input_lang)
                self.assertIs(gen.fmt, tc.input_fmt)


class TestDocumentGeneratorLabelSetter(unittest.TestCase):
    def test_pass(self) -> None:
        for label in [sw_compdocs.generator.LabelDict(), None]:
            gen = sw_compdocs.generator.DocumentGenerator()
            gen.label = label
            self.assertIs(gen.label, label)


class TestDocumentGeneratorLangSetter(unittest.TestCase):
    def test_pass(self) -> None:
        for lang in [sw_compdocs.language.Language(), None]:
            gen = sw_compdocs.generator.DocumentGenerator()
            gen.lang = lang
            self.assertIs(gen.lang, lang)


class TestDocumentGeneratorFmtSetter(unittest.TestCase):
    def test_pass(self) -> None:
        for fmt in [sw_compdocs.template.TemplateFormatter({}), None]:
            gen = sw_compdocs.generator.DocumentGenerator()
            gen.fmt = fmt
            self.assertIs(gen.fmt, fmt)


class TestDocumentGeneratorGenerate(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp_list", list[sw_compdocs.component.Definition]),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_comp_list=[],
                want_doc=sw_compdocs.document.Document(),
            ),
            # single
            tt(
                input_comp_list=[
                    sw_compdocs.component.Definition(
                        name="Blocks_1", category=sw_compdocs.component.Category.BLOCKS
                    ),
                ],
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
            # sort comp_list name
            tt(
                input_comp_list=[
                    sw_compdocs.component.Definition(
                        cid="blocks_1",
                        name="Blocks_3",
                        value=1,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        cid="blocks_2",
                        name="Blocks_2",
                        value=2,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        cid="blocks_3",
                        name="Blocks_1",
                        value=3,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                ],
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "3"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_2", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_3", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
            # sort comp_list cid
            tt(
                input_comp_list=[
                    sw_compdocs.component.Definition(
                        cid="blocks_3",
                        name="Blocks_1",
                        value=3,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        cid="blocks_2",
                        name="Blocks_1",
                        value=2,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                    sw_compdocs.component.Definition(
                        cid="blocks_1",
                        name="Blocks_1",
                        value=1,
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                ],
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Blocks_1", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "3"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
            # sort category
            tt(
                input_comp_list=[
                    sw_compdocs.component.Definition(
                        name="WINDOWS_0",
                        category=sw_compdocs.component.Category.WINDOWS,
                    ),
                    sw_compdocs.component.Definition(
                        name="INDUSTRY_0",
                        category=sw_compdocs.component.Category.INDUSTRY,
                    ),
                    sw_compdocs.component.Definition(
                        name="MODULAR_ENGINES_0",
                        category=sw_compdocs.component.Category.MODULAR_ENGINES,
                    ),
                    sw_compdocs.component.Definition(
                        name="WEAPONS_0",
                        category=sw_compdocs.component.Category.WEAPONS,
                    ),
                    sw_compdocs.component.Definition(
                        name="JET_ENGINES_0",
                        category=sw_compdocs.component.Category.JET_ENGINES,
                    ),
                    sw_compdocs.component.Definition(
                        name="ELECTRIC_0",
                        category=sw_compdocs.component.Category.ELECTRIC,
                    ),
                    sw_compdocs.component.Definition(
                        name="FLUID_0",
                        category=sw_compdocs.component.Category.FLUID,
                    ),
                    sw_compdocs.component.Definition(
                        name="DECORATIVE_0",
                        category=sw_compdocs.component.Category.DECORATIVE,
                    ),
                    sw_compdocs.component.Definition(
                        name="SENSORS_0",
                        category=sw_compdocs.component.Category.SENSORS,
                    ),
                    sw_compdocs.component.Definition(
                        name="DISPLAYS_0",
                        category=sw_compdocs.component.Category.DISPLAYS,
                    ),
                    sw_compdocs.component.Definition(
                        name="LOGIC_0",
                        category=sw_compdocs.component.Category.LOGIC,
                    ),
                    sw_compdocs.component.Definition(
                        name="SPECIALIST_EQUIPMENT_0",
                        category=sw_compdocs.component.Category.SPECIALIST_EQUIPMENT,
                    ),
                    sw_compdocs.component.Definition(
                        name="PROPULSION_0",
                        category=sw_compdocs.component.Category.PROPULSION,
                    ),
                    sw_compdocs.component.Definition(
                        name="MECHANICS_0",
                        category=sw_compdocs.component.Category.MECHANICS,
                    ),
                    sw_compdocs.component.Definition(
                        name="VEHICLE_CONTROL_0",
                        category=sw_compdocs.component.Category.VEHICLE_CONTROL,
                    ),
                    sw_compdocs.component.Definition(
                        name="BLOCKS_0",
                        category=sw_compdocs.component.Category.BLOCKS,
                    ),
                ],
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Blocks", level=1),
                        sw_compdocs.document.Heading("BLOCKS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Vehicle Control", level=1),
                        sw_compdocs.document.Heading("VEHICLE_CONTROL_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Mechanics", level=1),
                        sw_compdocs.document.Heading("MECHANICS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Propulsion", level=1),
                        sw_compdocs.document.Heading("PROPULSION_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Specialist Equipment", level=1),
                        sw_compdocs.document.Heading("SPECIALIST_EQUIPMENT_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Logic", level=1),
                        sw_compdocs.document.Heading("LOGIC_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Displays", level=1),
                        sw_compdocs.document.Heading("DISPLAYS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Sensors", level=1),
                        sw_compdocs.document.Heading("SENSORS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Decorative", level=1),
                        sw_compdocs.document.Heading("DECORATIVE_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Fluid", level=1),
                        sw_compdocs.document.Heading("FLUID_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Electric", level=1),
                        sw_compdocs.document.Heading("ELECTRIC_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Jet Engines", level=1),
                        sw_compdocs.document.Heading("JET_ENGINES_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Weapons", level=1),
                        sw_compdocs.document.Heading("WEAPONS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Modular Engines", level=1),
                        sw_compdocs.document.Heading("MODULAR_ENGINES_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Industry", level=1),
                        sw_compdocs.document.Heading("INDUSTRY_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("Windows", level=1),
                        sw_compdocs.document.Heading("WINDOWS_0", level=2),
                        sw_compdocs.document.Heading("PROPERTIES", level=3),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ],
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator()
                got_doc = gen.generate(tc.input_comp_list)
                self.assertEqual(got_doc, tc.want_doc)


class TestDocumentGeneratorGenerateComponentList(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_comp_list", list[sw_compdocs.component.Definition]),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            tt(
                input_comp_list=[],
                want_doc=sw_compdocs.document.Document(),
            ),
            tt(
                input_comp_list=[
                    sw_compdocs.component.Definition(name="A"),
                    sw_compdocs.component.Definition(name="B"),
                ],
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("A", level=1),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("B", level=1),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator()
                got_doc = gen.generate_component_list(tc.input_comp_list)
                self.assertEqual(got_doc, tc.want_doc)


class TestDocumentGeneratorGenerateComponent(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", sw_compdocs.generator.LabelDict | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_fmt", sw_compdocs.template.TemplateFormatter | None),
                ("input_comp", sw_compdocs.component.Definition),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            tt(  # normal
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_comp=sw_compdocs.component.Definition(
                    cid="clock",
                    name="Clock",
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description="An analogue clock display that outputs a number value representing the time of day.",
                        description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                idx=0,
                                label="Time",
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=1,
                                label="Backlight",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description="Enables the backlight when receiving an on signal.",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=2,
                                label="Electric",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description="Electrical power connection.",
                            ),
                        ]
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Paragraph(
                            "An analogue clock display that outputs a number value representing the time of day."
                        ),
                        sw_compdocs.document.Paragraph(
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display."
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic inputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # deprecated
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_comp=sw_compdocs.component.Definition(
                    cid="clock",
                    name="Clock",
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags.IS_DEPRECATED,
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description="An analogue clock display that outputs a number value representing the time of day.",
                        description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                idx=0,
                                label="Time",
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=1,
                                label="Backlight",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description="Enables the backlight when receiving an on signal.",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=2,
                                label="Electric",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description="Electrical power connection.",
                            ),
                        ]
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Callout(
                            "DEPRECATED_TEXT",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Paragraph(
                            "An analogue clock display that outputs a number value representing the time of day."
                        ),
                        sw_compdocs.document.Paragraph(
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display."
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic inputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # label, lang
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "DEPRECATED_TEXT": "この部品は非推奨です。",
                        "PROP_TABLE_HEAD_LABEL": "ラベル",
                        "PROP_TABLE_HEAD_VALUE": "値",
                        "PROP_TABLE_MASS_LABEL": "重量",
                        "PROP_TABLE_DIMS_LABEL": "サイズ(WxDxH)",
                        "PROP_TABLE_COST_LABEL": "値段",
                        "PROP_TABLE_TAGS_LABEL": "タグ",
                        "LOGIC_TABLE_HEAD_TYPE": "型",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "logic inputs",
                            "ロジック入力",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "logic outputs",
                            "ロジック出力",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "connections",
                            "接続",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "PROPERTIES",
                            "プロパティ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "number",
                            "数値",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_name",
                            "",
                            "Clock",
                            "時計",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_desc",
                            "",
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                            "時計に表示されている青い矢印が12時の方向です.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_s_desc",
                            "",
                            "An analogue clock display that outputs a number value representing the time of day.",
                            "ゲーム内の時刻に対応した数値信号を出力するアナログ時計です.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_0_label",
                            "",
                            "Time",
                            "ゲーム内の時刻",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_0_desc",
                            "",
                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                            "ゲーム内の時刻に対応した数値を0 (0:00) から1 (24:00) の範囲で出力します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_1_label",
                            "",
                            "Backlight",
                            "バックライト",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_1_desc",
                            "",
                            "Enables the backlight when receiving an on signal.",
                            "オン信号を受け取るとバックライトが点灯します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_2_label",
                            "",
                            "Electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_clock_node_2_desc",
                            "",
                            "Electrical power connection.",
                            "電力網から電力を供給します.",
                        ),
                    ]
                ),
                input_fmt=sw_compdocs.template.TemplateFormatter({}),
                input_comp=sw_compdocs.component.Definition(
                    cid="clock",
                    name="Clock",
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags.IS_DEPRECATED,
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description="An analogue clock display that outputs a number value representing the time of day.",
                        description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                idx=0,
                                label="Time",
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=1,
                                label="Backlight",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description="Enables the backlight when receiving an on signal.",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=2,
                                label="Electric",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description="Electrical power connection.",
                            ),
                        ]
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("時計"),
                        sw_compdocs.document.Callout(
                            "この部品は非推奨です。",
                            kind=sw_compdocs.document.CalloutKind.WARNING,
                        ),
                        sw_compdocs.document.Paragraph(
                            "ゲーム内の時刻に対応した数値信号を出力するアナログ時計です."
                        ),
                        sw_compdocs.document.Paragraph("時計に表示されている青い矢印が12時の方向です."),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["ラベル", "値"]),
                                [
                                    sw_compdocs.document.TableDataRow(["重量", "1"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["サイズ(WxDxH)", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["値段", "100"]),
                                    sw_compdocs.document.TableDataRow(["タグ", "basic"]),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック入力", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["型", "ラベル", "説明"]),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "オン/オフ",
                                            "バックライト",
                                            "オン信号を受け取るとバックライトが点灯します.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック出力", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["型", "ラベル", "説明"]),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "数値",
                                            "ゲーム内の時刻",
                                            "ゲーム内の時刻に対応した数値を0 (0:00) から1 (24:00) の範囲で出力します.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("接続", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["型", "ラベル", "説明"]),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "電力",
                                            "電力",
                                            "電力網から電力を供給します.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # label, lang, template
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "PROP_TABLE_HEAD_LABEL": "ラベル",
                        "PROP_TABLE_HEAD_VALUE": "値",
                        "PROP_TABLE_MASS_LABEL": "重量",
                        "PROP_TABLE_DIMS_LABEL": "サイズ(WxDxH)",
                        "PROP_TABLE_COST_LABEL": "値段",
                        "PROP_TABLE_TAGS_LABEL": "タグ",
                        "LOGIC_TABLE_HEAD_TYPE": "型",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "logic inputs",
                            "ロジック入力",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "logic outputs",
                            "ロジック出力",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "connections",
                            "接続",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "PROPERTIES",
                            "プロパティ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_name",
                            "",
                            "Push Button",
                            "押しボタン",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_desc",
                            "",
                            "An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs.",
                            "外部入力でボタンのオン/オフを制御することができ, 複数のボタンを同時に制御できます.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_s_desc",
                            "",
                            "A button that outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal when not interacting.",
                            "[$[action_interact_left]]/[$[action_interact_right]] を押している間のみオン信号を出力するボタンです.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_0_label",
                            "",
                            "Pressed",
                            "オン",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_0_desc",
                            "",
                            "Outputs an on signal when you interact wtih [$[action_interact_left]]/[$[action_interact_right]], and an off signal otherwise.",
                            "[$[action_interact_left]]/[$[action_interact_right]] を押している間のみオン信号を出力します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_1_label",
                            "",
                            "External Input",
                            "外部入力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_1_desc",
                            "",
                            "Allows an external on/off signal to control whether or not the button is pressed.",
                            "外部からのオン/オフ信号の入力でボタンのオン/オフを制御できます.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_2_label",
                            "",
                            "Electric",
                            "電力",
                        ),
                        sw_compdocs.language.Translation(
                            "def_button_push_node_2_desc",
                            "",
                            "Electrical power connection.",
                            "電力網から電力を供給します.",
                        ),
                    ]
                ),
                input_fmt=sw_compdocs.template.TemplateFormatter(
                    {"action_interact_left": "q", "action_interact_right": "e"}
                ),
                input_comp=sw_compdocs.component.Definition(
                    cid="button_push",
                    name="Push Button",
                    category=sw_compdocs.component.Category.MECHANICS,
                    mass=1.0,
                    value=10,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description="A button that outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal when not interacting.",
                        description="An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs.",
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                idx=0,
                                label="Pressed",
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description="Outputs an on signal when you interact wtih [$[action_interact_left]]/[$[action_interact_right]], and an off signal otherwise.",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=1,
                                label="External Input",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description="Allows an external on/off signal to control whether or not the button is pressed.",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=2,
                                label="Electric",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description="Electrical power connection.",
                            ),
                        ]
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("押しボタン"),
                        sw_compdocs.document.Paragraph(
                            "[q]/[e] を押している間のみオン信号を出力するボタンです."
                        ),
                        sw_compdocs.document.Paragraph(
                            "外部入力でボタンのオン/オフを制御することができ, 複数のボタンを同時に制御できます."
                        ),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["ラベル", "値"]),
                                [
                                    sw_compdocs.document.TableDataRow(["重量", "1"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["サイズ(WxDxH)", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["値段", "10"]),
                                    sw_compdocs.document.TableDataRow(["タグ", "basic"]),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック入力", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["型", "ラベル", "説明"]),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "オン/オフ",
                                            "外部入力",
                                            "外部からのオン/オフ信号の入力でボタンのオン/オフを制御できます.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("ロジック出力", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["型", "ラベル", "説明"]),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "オン/オフ",
                                            "オン",
                                            "[q]/[e] を押している間のみオン信号を出力します.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("接続", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["型", "ラベル", "説明"]),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "電力",
                                            "電力",
                                            "電力網から電力を供給します.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # label, lang, template
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "PROP_TABLE_HEAD_LABEL": "ラベル",
                        "PROP_TABLE_HEAD_VALUE": "値",
                        "PROP_TABLE_MASS_LABEL": "重量",
                        "PROP_TABLE_DIMS_LABEL": "サイズ(WxDxH)",
                        "PROP_TABLE_COST_LABEL": "値段",
                        "PROP_TABLE_TAGS_LABEL": "タグ",
                        "LOGIC_TABLE_HEAD_TYPE": "型",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "PROPERTIES",
                            "プロパティ",
                        ),
                        sw_compdocs.language.Translation(
                            "def_handle_name",
                            "",
                            "Handle",
                            "取っ手",
                        ),
                        sw_compdocs.language.Translation(
                            "def_handle_desc",
                            "",
                            "Interacting with [$[action_interact_left]] or [$[action_interact_right]] again will detach that hand. The handle can be used to drag vehicles around. If a vehicle is too heavy to move, you will be detached automatically when you move outside the handle's interaction range.",
                            "取っ手を掴んでいる時に [$[action_interact_left]]/[$[action_interact_right]] を押すと離すことができます. 軽い乗り物は取っ手を掴んでそのまま動かすことができます. プレイヤーが取っ手の範囲外まで移動した場合は自動的に手を離します.",
                        ),
                        sw_compdocs.language.Translation(
                            "def_handle_s_desc",
                            "",
                            "A handle that you can attach to by interacting with [$[action_interact_left]] or [$[action_interact_right]].",
                            "[$[action_interact_left]] や [$[action_interact_right]] を押して掴むことができる取っ手です.",
                        ),
                    ]
                ),
                input_fmt=sw_compdocs.template.TemplateFormatter(
                    {"action_interact_left": "q", "action_interact_right": "e"}
                ),
                input_comp=sw_compdocs.component.Definition(
                    cid="handle",
                    name="Handle",
                    category=sw_compdocs.component.Category.BLOCKS,
                    mass=1.0,
                    value=5,
                    flags=sw_compdocs.component.Flags(0),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description="Interacting with [$[action_interact_left]] or [$[action_interact_right]] again will detach that hand. The handle can be used to drag vehicles around. If a vehicle is too heavy to move, you will be detached automatically when you move outside the handle's interaction range.",
                        description="A handle that you can attach to by interacting with [$[action_interact_left]] or [$[action_interact_right]].",
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("取っ手"),
                        sw_compdocs.document.Paragraph("[q] や [e] を押して掴むことができる取っ手です."),
                        sw_compdocs.document.Paragraph(
                            "取っ手を掴んでいる時に [q]/[e] を押すと離すことができます. 軽い乗り物は取っ手を掴んでそのまま動かすことができます. プレイヤーが取っ手の範囲外まで移動した場合は自動的に手を離します."
                        ),
                        sw_compdocs.document.Heading("プロパティ", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(["ラベル", "値"]),
                                [
                                    sw_compdocs.document.TableDataRow(["重量", "1"]),
                                    sw_compdocs.document.TableDataRow(
                                        ["サイズ(WxDxH)", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(["値段", "5"]),
                                    sw_compdocs.document.TableDataRow(["タグ", "basic"]),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # omit short_description
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_comp=sw_compdocs.component.Definition(
                    cid="clock",
                    name="Clock",
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description="",
                        description="The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.",
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                idx=0,
                                label="Time",
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=1,
                                label="Backlight",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description="Enables the backlight when receiving an on signal.",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=2,
                                label="Electric",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description="Electrical power connection.",
                            ),
                        ]
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Paragraph(
                            "The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display."
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic inputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(  # omit description
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_comp=sw_compdocs.component.Definition(
                    cid="clock",
                    name="Clock",
                    category=sw_compdocs.component.Category.DISPLAYS,
                    mass=1.0,
                    value=100,
                    flags=sw_compdocs.component.Flags(8192),
                    tags="basic",
                    tooltip_properties=sw_compdocs.component.TooltipProperties(
                        short_description="An analogue clock display that outputs a number value representing the time of day.",
                        description="",
                    ),
                    logic_nodes=sw_compdocs.component.LogicNodeList(
                        [
                            sw_compdocs.component.LogicNode(
                                idx=0,
                                label="Time",
                                mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                                type=sw_compdocs.component.LogicNodeType.FLOAT,
                                description="The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=1,
                                label="Backlight",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.BOOL,
                                description="Enables the backlight when receiving an on signal.",
                            ),
                            sw_compdocs.component.LogicNode(
                                idx=2,
                                label="Electric",
                                mode=sw_compdocs.component.LogicNodeMode.INPUT,
                                type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                                description="Electrical power connection.",
                            ),
                        ]
                    ),
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=0, z=0),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=0),
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("Clock"),
                        sw_compdocs.document.Paragraph(
                            "An analogue clock display that outputs a number value representing the time of day."
                        ),
                        sw_compdocs.document.Heading("PROPERTIES", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "100"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", "basic"]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic inputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "on/off",
                                            "Backlight",
                                            "Enables the backlight when receiving an on signal.",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "number",
                                            "Time",
                                            "The time as a factor of a day, from 0 (midnight) to 1 (midnight).",
                                        ]
                                    )
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections", level=2),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        [
                                            "electric",
                                            "Electric",
                                            "Electrical power connection.",
                                        ]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(
                    label=tc.input_label, lang=tc.input_lang, fmt=tc.input_fmt
                )
                got_doc = gen.generate_component(tc.input_comp)
                self.assertEqual(got_doc, tc.want_doc)


class TestDocumentGeneratorGenerateProperty(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", sw_compdocs.generator.LabelDict | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_comp", sw_compdocs.component.Definition),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            tt(
                input_label=None,
                input_lang=None,
                input_comp=sw_compdocs.component.Definition(),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("PROPERTIES"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [sw_compdocs.language.Translation("", "", "PROPERTIES", "プロパティ")]
                ),
                input_comp=sw_compdocs.component.Definition(),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("プロパティ"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_MASS_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_DIMS_LABEL", "1x1x1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_COST_LABEL", "0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["PROP_TABLE_TAGS_LABEL", ""]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(
                    label=tc.input_label, lang=tc.input_lang
                )
                got_doc = gen.generate_property(tc.input_comp)
                self.assertEqual(got_doc, tc.want_doc)


class TestDocumentGeneratorGeneratePropertyTable(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", sw_compdocs.generator.LabelDict | None),
                ("input_comp", sw_compdocs.component.Definition),
                ("want_tbl", sw_compdocs.document.Table),
            ],
        )

        for tc in [
            tt(
                input_label=None,
                input_comp=sw_compdocs.component.Definition(
                    mass=10.0,
                    value=100,
                    tags="tags",
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=-1, z=-2),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=2),
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_MASS_LABEL", "10"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_DIMS_LABEL", "1x5x3"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_COST_LABEL", "100"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_TAGS_LABEL", "tags"]
                            ),
                        ],
                    )
                ),
            ),
            # mass format
            tt(
                input_label=None,
                input_comp=sw_compdocs.component.Definition(
                    mass=0.5,
                    value=100,
                    tags="tags",
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=-1, z=-2),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=2),
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_MASS_LABEL", "0.5"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_DIMS_LABEL", "1x5x3"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_COST_LABEL", "100"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_TAGS_LABEL", "tags"]
                            ),
                        ],
                    )
                ),
            ),
            tt(
                input_label=None,
                input_comp=sw_compdocs.component.Definition(
                    mass=0.25,
                    value=100,
                    tags="tags",
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=-1, z=-2),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=2),
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            ["PROP_TABLE_HEAD_LABEL", "PROP_TABLE_HEAD_VALUE"]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_MASS_LABEL", "0.25"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_DIMS_LABEL", "1x5x3"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_COST_LABEL", "100"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["PROP_TABLE_TAGS_LABEL", "tags"]
                            ),
                        ],
                    )
                ),
            ),
            # label
            tt(
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "PROP_TABLE_HEAD_LABEL": "Label",
                        "PROP_TABLE_HEAD_VALUE": "Value",
                        "PROP_TABLE_MASS_LABEL": "Mass",
                        "PROP_TABLE_DIMS_LABEL": "Dimensions",
                        "PROP_TABLE_COST_LABEL": "Cost",
                        "PROP_TABLE_TAGS_LABEL": "Tags",
                    }
                ),
                input_comp=sw_compdocs.component.Definition(
                    mass=10.0,
                    value=100,
                    tags="tags",
                    voxel_min=sw_compdocs.component.VoxelPos(x=0, y=-1, z=-2),
                    voxel_max=sw_compdocs.component.VoxelPos(x=0, y=1, z=2),
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["Label", "Value"]),
                        [
                            sw_compdocs.document.TableDataRow(["Mass", "10"]),
                            sw_compdocs.document.TableDataRow(["Dimensions", "1x5x3"]),
                            sw_compdocs.document.TableDataRow(["Cost", "100"]),
                            sw_compdocs.document.TableDataRow(["Tags", "tags"]),
                        ],
                    )
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(label=tc.input_label)
                got_tbl = gen.generate_property_table(tc.input_comp)
                self.assertEqual(got_tbl, tc.want_tbl)


class TestDocumentGeneratorGenerateLogic(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", sw_compdocs.generator.LabelDict | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_fmt", sw_compdocs.template.TemplateFormatter | None),
                ("input_cid", str),
                ("input_lns", sw_compdocs.component.LogicNodeList),
                ("want_doc", sw_compdocs.document.Document),
            ],
        )

        for tc in [
            # empty
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(),
                want_doc=sw_compdocs.document.Document(),
            ),
            # logic node type
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic inputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic inputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["number", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("connections"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["power", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.WATER,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("connections"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["fluid", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ELECTRIC,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("connections"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["electric", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.COMPOSITE,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic inputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["composite", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.VIDEO,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic inputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["video", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.AUDIO,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic inputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["audio", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.ROPE,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("connections"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["rope", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # logic node mode
            tt(
                input_label=None,
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic outputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label", "desc"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # lang
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic inputs", "ロジック入力"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "ラベル"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "説明"
                        ),
                    ]
                ),
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック入力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["オン/オフ", "ラベル", "説明"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic outputs", "ロジック出力"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "オン/オフ"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "ラベル"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "説明"
                        ),
                    ]
                ),
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("ロジック出力"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["オン/オフ", "ラベル", "説明"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation("", "", "connections", "接続"),
                        sw_compdocs.language.Translation("", "", "power", "動力"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "ラベル"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "説明"
                        ),
                    ]
                ),
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("接続"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["動力", "ラベル", "説明"]
                                    )
                                ],
                            )
                        ),
                    ]
                ),
            ),
            # logic idx
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "", "", "logic inputs", "logic inputs"
                        ),
                        sw_compdocs.language.Translation(
                            "", "", "logic outputs", "logic outputs"
                        ),
                        sw_compdocs.language.Translation(
                            "", "", "connections", "connections"
                        ),
                        sw_compdocs.language.Translation("", "", "on/off", "on/off"),
                        sw_compdocs.language.Translation("", "", "power", "power"),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label", "", "", "label 0"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc", "", "", "desc 0"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_label", "", "", "label 1"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_desc", "", "", "desc 1"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_2_label", "", "", "label 2"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_2_desc", "", "", "desc 2"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_3_label", "", "", "label 3"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_3_desc", "", "", "desc 3"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_4_label", "", "", "label 4"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_4_desc", "", "", "desc 4"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_label", "", "", "label 5"
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_desc", "", "", "desc 5"
                        ),
                    ]
                ),
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=0,
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=1,
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=2,
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description="desc",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=3,
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=4,
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.OUTPUT,
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=5,
                            label="label",
                            mode=sw_compdocs.component.LogicNodeMode.INPUT,
                            type=sw_compdocs.component.LogicNodeType.TORQUE,
                            description="desc",
                        ),
                    ]
                ),
                want_doc=sw_compdocs.document.Document(
                    [
                        sw_compdocs.document.Heading("logic inputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label 0", "desc 0"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label 3", "desc 3"]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("logic outputs"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label 1", "desc 1"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["on/off", "label 4", "desc 4"]
                                    ),
                                ],
                            )
                        ),
                        sw_compdocs.document.Heading("connections"),
                        sw_compdocs.document.Table(
                            sw_compdocs.document.TableData(
                                sw_compdocs.document.TableDataRow(
                                    [
                                        "LOGIC_TABLE_HEAD_TYPE",
                                        "LOGIC_TABLE_HEAD_LABEL",
                                        "LOGIC_TABLE_HEAD_DESC",
                                    ]
                                ),
                                [
                                    sw_compdocs.document.TableDataRow(
                                        ["power", "label 2", "desc 2"]
                                    ),
                                    sw_compdocs.document.TableDataRow(
                                        ["power", "label 5", "desc 5"]
                                    ),
                                ],
                            )
                        ),
                    ]
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(
                    label=tc.input_label, lang=tc.input_lang, fmt=tc.input_fmt
                )
                got_doc = gen.generate_logic(tc.input_cid, tc.input_lns)
                self.assertEqual(got_doc, tc.want_doc)


class TestDocumentGeneratorGenerateLogicTable(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", sw_compdocs.generator.LabelDict | None),
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_fmt", sw_compdocs.template.TemplateFormatter | None),
                ("input_cid", str),
                ("input_lns", sw_compdocs.component.LogicNodeList),
                ("want_tbl", sw_compdocs.document.Table),
            ],
        )

        for tc in [
            tt(
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "LOGIC_TABLE_HEAD_TYPE": "種別",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=None,
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList([]),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [],
                    )
                ),
            ),
            tt(
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "LOGIC_TABLE_HEAD_TYPE": "種別",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "number",
                            "数値",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label",
                            "",
                            "label 0 $[label_0]",
                            "ラベル 0 $[label_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc",
                            "",
                            "desc 0 $[desc_0]",
                            "説明 0 $[desc_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_label",
                            "",
                            "label 1 $[label_1]",
                            "ラベル 1 $[label_1]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_desc",
                            "",
                            "desc 1 $[desc_1]",
                            "説明 1 $[desc_1]",
                        ),
                    ]
                ),
                input_fmt=sw_compdocs.template.TemplateFormatter(
                    {
                        "label_0": "label_0_fmt",
                        "desc_0": "desc_0_fmt",
                        "label_1": "label_1_fmt",
                        "desc_1": "desc_1_fmt",
                    }
                ),
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=0,
                            label="label 0 $[label_0]",
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc 0 $[desc_0]",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=1,
                            label="label 1 $[label_1]",
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="desc 1 $[desc_1]",
                        ),
                    ]
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["オン/オフ", "ラベル 0 label_0_fmt", "説明 0 desc_0_fmt"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["数値", "ラベル 1 label_1_fmt", "説明 1 desc_1_fmt"]
                            ),
                        ],
                    )
                ),
            ),
            tt(
                input_label=None,
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "number",
                            "数値",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label",
                            "",
                            "label 0 $[label_0]",
                            "ラベル 0 $[label_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc",
                            "",
                            "desc 0 $[desc_0]",
                            "説明 0 $[desc_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_label",
                            "",
                            "label 1 $[label_1]",
                            "ラベル 1 $[label_1]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_desc",
                            "",
                            "desc 1 $[desc_1]",
                            "説明 1 $[desc_1]",
                        ),
                    ]
                ),
                input_fmt=sw_compdocs.template.TemplateFormatter(
                    {
                        "label_0": "label_0_fmt",
                        "desc_0": "desc_0_fmt",
                        "label_1": "label_1_fmt",
                        "desc_1": "desc_1_fmt",
                    }
                ),
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=0,
                            label="label 0 $[label_0]",
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc 0 $[desc_0]",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=1,
                            label="label 1 $[label_1]",
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="desc 1 $[desc_1]",
                        ),
                    ]
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(
                            [
                                "LOGIC_TABLE_HEAD_TYPE",
                                "LOGIC_TABLE_HEAD_LABEL",
                                "LOGIC_TABLE_HEAD_DESC",
                            ]
                        ),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["オン/オフ", "ラベル 0 label_0_fmt", "説明 0 desc_0_fmt"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["数値", "ラベル 1 label_1_fmt", "説明 1 desc_1_fmt"]
                            ),
                        ],
                    )
                ),
            ),
            tt(
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "LOGIC_TABLE_HEAD_TYPE": "種別",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=None,
                input_fmt=sw_compdocs.template.TemplateFormatter(
                    {
                        "label_0": "label_0_fmt",
                        "desc_0": "desc_0_fmt",
                        "label_1": "label_1_fmt",
                        "desc_1": "desc_1_fmt",
                    }
                ),
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=0,
                            label="label 0 $[label_0]",
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc 0 $[desc_0]",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=1,
                            label="label 1 $[label_1]",
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="desc 1 $[desc_1]",
                        ),
                    ]
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["on/off", "label 0 label_0_fmt", "desc 0 desc_0_fmt"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["number", "label 1 label_1_fmt", "desc 1 desc_1_fmt"]
                            ),
                        ],
                    )
                ),
            ),
            tt(
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "LOGIC_TABLE_HEAD_TYPE": "種別",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "number",
                            "数値",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_label",
                            "",
                            "label 0 $[label_0]",
                            "ラベル 0 $[label_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_0_desc",
                            "",
                            "desc 0 $[desc_0]",
                            "説明 0 $[desc_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_label",
                            "",
                            "label 1 $[label_1]",
                            "ラベル 1 $[label_1]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_1_desc",
                            "",
                            "desc 1 $[desc_1]",
                            "説明 1 $[desc_1]",
                        ),
                    ]
                ),
                input_fmt=None,
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=0,
                            label="label 0 $[label_0]",
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc 0 $[desc_0]",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=1,
                            label="label 1 $[label_1]",
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="desc 1 $[desc_1]",
                        ),
                    ]
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["オン/オフ", "ラベル 0 $[label_0]", "説明 0 $[desc_0]"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["数値", "ラベル 1 $[label_1]", "説明 1 $[desc_1]"]
                            ),
                        ],
                    )
                ),
            ),
            tt(
                input_label=sw_compdocs.generator.LabelDict(
                    {
                        "LOGIC_TABLE_HEAD_TYPE": "種別",
                        "LOGIC_TABLE_HEAD_LABEL": "ラベル",
                        "LOGIC_TABLE_HEAD_DESC": "説明",
                    }
                ),
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "on/off",
                            "オン/オフ",
                        ),
                        sw_compdocs.language.Translation(
                            "",
                            "",
                            "number",
                            "数値",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_3_label",
                            "",
                            "label 0 $[label_0]",
                            "ラベル 0 $[label_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_3_desc",
                            "",
                            "desc 0 $[desc_0]",
                            "説明 0 $[desc_0]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_label",
                            "",
                            "label 1 $[label_1]",
                            "ラベル 1 $[label_1]",
                        ),
                        sw_compdocs.language.Translation(
                            "def_test_node_5_desc",
                            "",
                            "desc 1 $[desc_1]",
                            "説明 1 $[desc_1]",
                        ),
                    ]
                ),
                input_fmt=sw_compdocs.template.TemplateFormatter(
                    {
                        "label_0": "label_0_fmt",
                        "desc_0": "desc_0_fmt",
                        "label_1": "label_1_fmt",
                        "desc_1": "desc_1_fmt",
                    }
                ),
                input_cid="test",
                input_lns=sw_compdocs.component.LogicNodeList(
                    [
                        sw_compdocs.component.LogicNode(
                            idx=3,
                            label="label 0 $[label_0]",
                            type=sw_compdocs.component.LogicNodeType.BOOL,
                            description="desc 0 $[desc_0]",
                        ),
                        sw_compdocs.component.LogicNode(
                            idx=5,
                            label="label 1 $[label_1]",
                            type=sw_compdocs.component.LogicNodeType.FLOAT,
                            description="desc 1 $[desc_1]",
                        ),
                    ]
                ),
                want_tbl=sw_compdocs.document.Table(
                    sw_compdocs.document.TableData(
                        sw_compdocs.document.TableDataRow(["種別", "ラベル", "説明"]),
                        [
                            sw_compdocs.document.TableDataRow(
                                ["オン/オフ", "ラベル 0 label_0_fmt", "説明 0 desc_0_fmt"]
                            ),
                            sw_compdocs.document.TableDataRow(
                                ["数値", "ラベル 1 label_1_fmt", "説明 1 desc_1_fmt"]
                            ),
                        ],
                    )
                ),
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(
                    label=tc.input_label, lang=tc.input_lang, fmt=tc.input_fmt
                )
                got_tbl = gen.generate_logic_table(tc.input_cid, tc.input_lns)
                self.assertEqual(got_tbl, tc.want_tbl)


class TestDocumentGenerateLabelGet(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_label", sw_compdocs.generator.LabelDict | None),
                ("input_s", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_label=None,
                input_s="LABEL",
                want_s="LABEL",
            ),
            tt(
                input_label=sw_compdocs.generator.LabelDict({"LABEL": "text"}),
                input_s="LABEL",
                want_s="text",
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(label=tc.input_label)
                got_s = gen._label_get(tc.input_s)
                self.assertEqual(got_s, tc.want_s)


class TestDocumentGeneratorLangFindID(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_lang_id", str),
                ("input_lang_en", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_lang=None,
                input_lang_id="id",
                input_lang_en="en",
                want_s="en",
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id", "description", "en", "local"
                        )
                    ]
                ),
                input_lang_id="id",
                input_lang_en="en",
                want_s="local",
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(lang=tc.input_lang)
                got_s = gen._lang_find_id(tc.input_lang_id, tc.input_lang_en)
                self.assertEqual(got_s, tc.want_s)


class TestDocumentGeneratorLangFindEn(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_lang", sw_compdocs.language.Language | None),
                ("input_lang_en", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_lang=None,
                input_lang_en="en",
                want_s="en",
            ),
            tt(
                input_lang=sw_compdocs.language.Language(
                    [
                        sw_compdocs.language.Translation(
                            "id", "description", "en", "local"
                        )
                    ]
                ),
                input_lang_en="en",
                want_s="local",
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(lang=tc.input_lang)
                got_s = gen._lang_find_en(tc.input_lang_en)
                self.assertEqual(got_s, tc.want_s)


class TestDocumentGeneratorFmtFormat(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_fmt", sw_compdocs.template.TemplateFormatter | None),
                ("input_s", str),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_fmt=None,
                input_s="$[var]",
                want_s="$[var]",
            ),
            tt(
                input_fmt=sw_compdocs.template.TemplateFormatter({"var": "text"}),
                input_s="$[var]",
                want_s="text",
            ),
        ]:
            with self.subTest(tc=tc):
                gen = sw_compdocs.generator.DocumentGenerator(fmt=tc.input_fmt)
                got_s = gen._fmt_format(tc.input_s)
                self.assertEqual(got_s, tc.want_s)


class TestLabelDictInit(unittest.TestCase):
    def test_pass(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_mapping", collections.abc.Mapping[str, str]),
                ("want_label_d", dict[str, str]),
            ],
        )

        for tc in [
            tt(
                input_mapping={},
                want_label_d={},
            ),
            tt(
                input_mapping={"key_1": "value_1", "key_2": "value_2"},
                want_label_d={"key_1": "value_1", "key_2": "value_2"},
            ),
            tt(
                input_mapping=sw_compdocs.generator.LabelDict(
                    {"key_1": "value_1", "key_2": "value_2"}
                ),
                want_label_d={"key_1": "value_1", "key_2": "value_2"},
            ),
        ]:
            with self.subTest(tc=tc):
                got_label = sw_compdocs.generator.LabelDict(tc.input_mapping)
                self.assertEqual(got_label._d, tc.want_label_d)
                self.assertIsNot(got_label._d, tc.input_mapping)


class TestLabelDictFromTOMLFile(unittest.TestCase):
    def test_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = pathlib.Path(tmp_dir, "label.toml")
            with open(tmp_file, mode="xt", encoding="utf-8", newline="\n") as fd:
                fd.write(
                    """\
[label]
key_1 = "value_1"
key_2 = "value_2"
"""
                )

            file_list: list[sw_compdocs._types.StrOrBytesPath] = [
                os.fsdecode(tmp_file),
                os.fsencode(tmp_file),
                tmp_file,
            ]
            for file in file_list:
                label = sw_compdocs.generator.LabelDict.from_toml_file(file)
                want_d = {"key_1": "value_1", "key_2": "value_2"}
                self.assertEqual(label._d, want_d)

    def test_exc_label(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_s", str),
                ("want_exc_msg", str),
            ],
        )

        for tc in [
            tt(
                input_s="""\
[label_]
key_1 = "value_1"
key_2 = "value_2"
""",
                want_exc_msg="missing label table",
            ),
            tt(
                input_s="""\
[label]
key_1 = "value_1"
key_2 = 2
""",
                want_exc_msg="expected string for label text: 2",
            ),
        ]:
            with self.subTest(tc=tc):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_file = pathlib.Path(tmp_dir, "label.toml")
                    with open(
                        tmp_file, mode="xt", encoding="utf-8", newline="\n"
                    ) as fp:
                        fp.write(tc.input_s)

                    file_list: list[sw_compdocs._types.StrOrBytesPath] = [
                        os.fsdecode(tmp_file),
                        os.fsencode(tmp_file),
                        tmp_file,
                    ]
                    for file in file_list:
                        with self.assertRaises(
                            sw_compdocs.generator.LabelFileError
                        ) as ctx:
                            sw_compdocs.generator.LabelDict.from_toml_file(file)
                        self.assertEqual(ctx.exception.msg, tc.want_exc_msg)
                        self.assertEqual(ctx.exception.file, file)


class TestLabelDictFromTOMLStr(unittest.TestCase):
    def test_pass(self) -> None:
        label = sw_compdocs.generator.LabelDict.from_toml_str(
            """\
[label]
key_1 = "value_1"
key_2 = "value_2"
"""
        )
        want_d = {"key_1": "value_1", "key_2": "value_2"}
        self.assertEqual(label._d, want_d)

    def test_exc_label(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_s", str),
                ("want_exc_msg", str),
            ],
        )

        for tc in [
            tt(
                input_s="""\
[label_]
key_1 = "value_1"
key_2 = "value_2"
""",
                want_exc_msg="missing label table",
            ),
            tt(
                input_s="""\
[label]
key_1 = "value_1"
key_2 = 2
""",
                want_exc_msg="expected string for label text: 2",
            ),
        ]:
            with self.subTest(tc=tc):
                with self.assertRaises(sw_compdocs.generator.LabelFileError) as ctx:
                    sw_compdocs.generator.LabelDict.from_toml_str(tc.input_s)
                self.assertEqual(ctx.exception.msg, tc.want_exc_msg)
                self.assertEqual(ctx.exception.file, None)


class TestLabelDictGetItem(unittest.TestCase):
    def test_pass(self) -> None:
        label = sw_compdocs.generator.LabelDict(
            {"key_1": "value_1", "key_2": "value_2"}
        )
        self.assertEqual(label["key_1"], "value_1")
        self.assertEqual(label["key_2"], "value_2")

    def test_exc_key(self) -> None:
        label = sw_compdocs.generator.LabelDict({"key_1": "value_1"})
        with self.assertRaises(sw_compdocs.generator.LabelKeyError) as ctx:
            label["key_2"]
        self.assertEqual(ctx.exception.key, "key_2")


class TestLabelDictIter(unittest.TestCase):
    def test(self) -> None:
        label = sw_compdocs.generator.LabelDict(
            {"key_1": "value_1", "key_2": "value_2"}
        )
        self.assertEqual(list[str](label), list[str](["key_1", "key_2"]))


class TestLabelDictLen(unittest.TestCase):
    def test(self) -> None:
        label = sw_compdocs.generator.LabelDict(
            {"key_1": "value_1", "key_2": "value_2"}
        )
        self.assertEqual(len(label), 2)


class TestLabelDictErrorInit(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.generator.LabelDictError("msg")
        self.assertEqual(exc.msg, "msg")


class TestLabelDictErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.generator.LabelDictError("msg")
        self.assertEqual(str(exc), "msg")


class TestLabelDictErrorWithFile(unittest.TestCase):
    def test(self) -> None:
        dict_exc = sw_compdocs.generator.LabelDictError("msg")
        file_exc = dict_exc.with_file("file")
        self.assertEqual(file_exc.msg, "msg")
        self.assertEqual(file_exc.file, "file")


class TestLabelFileErrorInit(unittest.TestCase):
    def test_pass(self) -> None:
        exc = sw_compdocs.generator.LabelFileError("msg")
        exc_args: tuple[object] = exc.args
        self.assertEqual(exc_args, ("msg",))
        self.assertEqual(exc.msg, "msg")
        self.assertEqual(exc.file, None)


class TestLabelFileErrorFileSetter(unittest.TestCase):
    def test_pass(self) -> None:
        for file in [None, "file", b"file", pathlib.PurePath("file")]:
            with self.subTest(file=file):
                exc = sw_compdocs.generator.LabelFileError("msg")
                exc.file = file
                self.assertIs(exc.file, file)


class TestLabelFileErrorStr(unittest.TestCase):
    def test(self) -> None:
        tt = typing.NamedTuple(
            "tt",
            [
                ("input_msg", str),
                ("input_file", sw_compdocs._types.StrOrBytesPath | None),
                ("want_s", str),
            ],
        )

        for tc in [
            tt(
                input_msg="msg",
                input_file=None,
                want_s="<label.toml>: msg",
            ),
            tt(
                input_msg="msg",
                input_file="pathlike",
                want_s="pathlike: msg",
            ),
            tt(
                input_msg="msg",
                input_file=b"pathlike",
                want_s="pathlike: msg",
            ),
            tt(
                input_msg="msg",
                input_file=pathlib.PurePath("pathlike"),
                want_s="pathlike: msg",
            ),
        ]:
            with self.subTest(tc=tc):
                input_exc = sw_compdocs.generator.LabelFileError(tc.input_msg)
                input_exc.file = tc.input_file
                got_s = str(input_exc)
                self.assertEqual(got_s, tc.want_s)


class TestLabelKeyErrorInit(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.generator.LabelKeyError("key")
        exc_args: tuple[object] = exc.args
        self.assertEqual(exc_args, ("key",))
        self.assertEqual(exc.key, "key")


class TestLabelKeyErrorStr(unittest.TestCase):
    def test(self) -> None:
        exc = sw_compdocs.generator.LabelKeyError("key")
        self.assertEqual(str(exc), "missing label text for key 'key'")
