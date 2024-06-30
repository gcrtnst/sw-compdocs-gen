English / [日本語](./README-ja.md)

# sw-compdocs-gen
sw-compdocs-gen is a tool for automatically generating Markdown documents from Stormworks component definition files.

## Installation
1. Install the latest stable version of [Python](https://www.python.org/).
2. `pip install git+https://github.com/gcrtnst/sw-compdocs-gen.git`

For isolated virtual environment installation, you can use `pipx` instead of `pip`. For more information, see the [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/).

## Usage
Generate component documentation using the following command:
```
sw_compdocs output_dir/
```

In most cases, the tool can automatically locate the Stormworks component definition directory. If automatic detection fails, use the `-d` option to provide the path manually. The directory is typically located at `rom/data/definitions` within your Stormworks installation directory.
```
sw_compdocs -d path/to/definitions/ output_dir/
```

### Command-Line Options
#### Positional Arguments
- `output`
  - Specifies the output path.
  - In document mode (default), provide the output directory path.
  - In sheet mode (`-m sheet`), specify the path for the output CSV file.

#### Options
- `-d DEFINITIONS`, `--definitions DEFINITIONS`
  - Manually sets the Stormworks component definition directory path.
  - Only required if automatic detection fails.
- `--show-deprecated`, `--hide-deprecated`
  - Controls whether to include deprecated components in the output.
  - Displayed by default.
- `--show-orphan`, `--hide-orphan`
  - Controls whether to include orphaned components in the output.
  - Orphaned components are multibody child components without a corresponding parent component.
  - Hidden by default.
- `-s LABEL`, `--label LABEL`
  - Specifies the label file.
  - For details, see [How to Translate Tool-Specific Text](#How-to-Translate-Tool-Specific-Text).
  - English is used by default.
- `-l LANGUAGE, --language LANGUAGE`
  - Specifies the Stormworks language file.
  - For details, see [How to Translate Stormworks-Derived Text](#How-to-Translate-Stormworks-Derived-Text).
  - English is used by default.
- `-k KEYBINDINGS, --keybindings KEYBINDINGS`
  - Specifies the key bindings file.
  - For details, see [Customizing Key Display](#Customizing-Key-Display).
  - By default, the tool's built-in key bindings are used.
- `-m {document,sheet}`, `--mode {document,sheet}`
  - Selects the output mode:
    - `document`: Generates Markdown documents (default).
    - `sheet`: Generates a CSV file listing components.
- `-e ENCODING`, `--encoding ENCODING`
  - Specifies the character encoding for the output file.
  - For a list of supported encodings, see the [Python documentation](https://docs.python.org/3/library/codecs.html#standard-encodings).
  - The default is `utf-8`.
- `-n {CR,LF,CRLF}`, `--newline {CR,LF,CRLF}`
  - Specifies the newline character for the output file.
  - In document mode, the default is LF.
  - In sheet mode, the default is CRLF.

### Multilingual Support
By default, the tool generates documentation in English, but it can also be used to generate documents in other languages with additional translation files.

#### How to Translate Stormworks-Derived Text
The tool can read translation data used in Stormworks. Specify the TSV file path using the `-l LANG` option to generate translated documents.

#### How to Translate Tool-Specific Text
To translate tool-specific text that is not included in Stormworks translation data, you'll need to create a separate translation file.

To create translation data, follow these steps:
1. Copy the [res/sw_compdocs_label.toml](./res/sw_compdocs_label.toml) file from this repository.
2. Rewrite the text in the copied file to the language you want to translate.
3. Specify the rewritten file with the `-s LABEL` option.

Keep the `{}` placeholders intact, as they are used for inserting actual values.

### Customizing Key Display
Some component descriptions include the keys used for operation. By default, the tool uses the default key bindings from Stormworks. However, you can customize this display to match a different key bindings.

To change the key display, follow these steps:
1. Copy the [res/sw_compdocs_keybindings.toml](./res/sw_compdocs_keybindings.toml) file from this repository.
2. Rewrite the keys you want to change in the copied file.
3. Specify the rewritten file with the `-k KEYBINDINGS` option.

## Development
You can set up a development environment by following these steps:
1. Clone this repository using `git clone`.
2. Create and activate a venv.
3. Run `pip install -e . [dev]` in the root directory of this repository.

You can find the scripts used for development in the root directory of this repository.
- `run_test.py`: Executes all test commands collectively.
- `run_update.py`: Automatically generates files in the `res` directory.
- `run_all.py`: Runs both `run_test.py` and `run_update.py` sequentially.

## License
Please refer to the [LICENSE](./LICENSE) file in the root directory of this repository.
