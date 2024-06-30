[English](./README.md) / 日本語

# sw-compdocs-gen
Stormworks 部品定義ファイルから Markdown ドキュメントを自動生成するツールです。

## インストール
1. [Python](https://www.python.org/) の最新安定版をインストール
2. `pip install git+https://github.com/gcrtnst/sw-compdocs-gen.git`

pip の代わりに pipx を利用することで、環境を汚染せずにツールをインストールできます。詳細は [Python Packaging User Guide](https://packaging.python.org/ja/latest/guides/installing-stand-alone-command-line-tools/) を参照ください。

## 使い方
以下のコマンドでドキュメントを生成できます。
```
sw_compdocs output_dir/
```

Stormworks の部品定義ディレクトリを自動検出できない場合があります。この場合は、`-d` オプションを使用して手動で場所を指定してください。部品定義ディレクトリは、Stormworks インストールディレクトリ内の `rom/data/definitions` にあります。
```
sw_compdocs -d path/to/definitions/ output_dir/
```

### コマンドラインオプション
#### 位置引数
- `output`
  - 出力先のパスを指定します。
  - ドキュメントモード(`-m document` 指定時、デフォルト)では、出力先ディレクトリのパスを指定してください。
  - シートモード(`-m sheet` 指定時)では、出力先 CSV ファイルのパスを指定してください。

#### オプション
- `-d DEFINITIONS`, `--definitions DEFINITIONS`
  - Stormworks の部品定義ディレクトリを指定します。
  - デフォルトでは自動検出されます。自動検出に失敗した場合、このオプションは指定必須となります。
- `--show-deprecated`, `--hide-deprecated`
  - 非推奨の部品を表示するかどうかを制御します。
  - デフォルトでは表示となります。
- `--show-orphan`, `--hide-orphan`
  - 孤児の部品を表示するかどうかを制御します。
  - 孤児の部品とは、対応するマルチボディ親部品が存在しないマルチボディ子部品のことです。
  - デフォルトでは非表示となります。
- `-s LABEL`, `--label LABEL`
  - ラベルファイルを指定します。
  - 詳細は [本ツール独自のテキストの翻訳方法](#本ツール独自のテキストの翻訳方法) を参照ください。
  - デフォルトでは、英語のテキストを表示します。
- `-l LANGUAGE, --language LANGUAGE`
  - Stormworks の言語ファイルを指定します。
  - 詳細は [Stormworks 由来のテキストの翻訳方法](#Stormworks-由来のテキストの翻訳方法) を参照ください。
  - デフォルトでは、英語のテキストを表示します。
- `-k KEYBINDINGS, --keybindings KEYBINDINGS`
  - キーバインドファイルを指定します。
  - 詳細は [キー表示のカスタマイズ](#キー表示のカスタマイズ) を参照ください。
  - デフォルトでは、本ツールに埋め込まれているキーバインドを使用します。
- `-m {document,sheet}`, `--mode {document,sheet}`
  - モードを選択します：
    - `document`: Markdown ドキュメントを出力します（デフォルト）。
    - `sheet`: 部品一覧の CSV を出力します。
- `-e ENCODING`, `--encoding ENCODING`
  - 出力ファイルのエンコーディングを指定します。
  - 指定できるエンコーディングの一覧は [Python のドキュメント](https://docs.python.org/ja/3/library/codecs.html#standard-encodings) を参照ください。
  - デフォルトは `utf-8` です。
- `-n {CR,LF,CRLF}`, `--newline {CR,LF,CRLF}`
  - 出力ファイルの改行コードを指定します。
  - ドキュメントモードでは、デフォルトは LF です。
  - シートモードでは、デフォルトは CRLF です。

### 多言語対応
本ツールは、デフォルトでは英語のドキュメントを生成しますが、追加で翻訳データを用意することで、多言語でのドキュメント生成にも対応できます。

#### Stormworks 由来のテキストの翻訳方法
本ツールは Stormworks で使用されている翻訳データをそのまま読み込むことができます。`-l LANG` オプションで TSV ファイルを指定すると、翻訳されたテキストを出力します。

#### 本ツール独自のテキストの翻訳方法
Stormworks の翻訳データに含まれていない、本ツール独自のテキストについては、別途翻訳する必要があります。

翻訳データの作成方法は以下の通りです。
1. 本リポジトリの [res/sw_compdocs_label.toml](./res/sw_compdocs_label.toml) ファイルをコピーします。
2. コピーしたファイル内のテキストを、翻訳したい言語に書き換えます。
3. 書き換えたファイルを `-s LABEL` オプションで指定します。

なお、一部のテキストには `{}` 形式のプレースホルダが含まれていますが、これはツール実行時に実際の値に置き換えられる為、削除しないでください。

### キー表示のカスタマイズ
一部の部品説明文には、操作に使用するキーが記載されています。デフォルトでは、Stormworks 本体のデフォルトキーバインドが表示されますが、この表示を別のキーに変更することもできます。

キー表示は以下の手順で変更できます。
1. 本リポジトリの [res/sw_compdocs_keybindings.toml](./res/sw_compdocs_keybindings.toml) ファイルをコピーします。
2. コピーしたファイル内で、変更したいキーを書き換えます。
3. 書き換えたファイルを `-k KEYBINDINGS` オプションで指定します。

## 開発
以下の手順で開発環境を構築できます。
1. git clone で本リポジトリをクローンします。
2. 仮想環境(venv)を作成して、有効化します。
3. 本リポジトリのルートディレクトリに移動して、`pip install -e .[dev]` を実行します。

本リポジトリのルートディレクトリには、開発に使用するスクリプトが格納されています。
- `run_test.py`: テストコマンドをまとめて実行します。
- `run_update.py`: `res` ディレクトリ内のファイルを自動生成します。
- `run_all.py`: `run_test.py` と `run_update.py` をまとめて実行します。

## ライセンス
本リポジトリのルートディレクトリにある [LICENSE](./LICENSE) ファイルを参照ください。