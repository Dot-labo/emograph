# emograph

本リポジトリは、授業用資料の視覚的理解を助けるため、YAMLで定義された絵文字、矢印、テキスト要素を基に画像を自動生成する Python ライブラリを提供します。

## 外部パッケージからの利用方法

プロジェクトに `emograph` を追加するには、以下のコマンドを実行してください。

```bash
poetry add git+https://github.com/Dot-labo/emograph.git
```

## 開発環境設定

1. **Poetry (2.0以上) をインストール**
2. **依存関係をインストール**
   ```bash
   poetry install
   ```

## デコード例の実行方法

以下の手順で `example` ディレクトリ内のサンプルを実行できます。

```bash
cd example
poetry run python main.py --config=config_example.yml --output-name=output.png
```

または、仮想環境を手動で有効化してから実行することもできます。

```bash
cd example
source $(poetry env info --path)/bin/activate  # 仮想環境を有効化 (必要なら)
python main.py --config=config_example.yml --output-name=output.png
```