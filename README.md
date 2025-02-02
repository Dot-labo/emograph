# emograph

本リポジトリは、授業用資料の視覚的理解を助けるため、YAMLで定義された絵文字、矢印、テキスト要素を基に画像を自動生成するpythonライブラリを提供します。

## 利用方法

  ```bash
  poetry add git+https://github.com/Dot-labo/emograph.git
  ```

## 開発環境設定

* poetry(2.0以上)をインストール

* ライブラリをインストール

  ```bash
  poetry env use python3
  poetry install
  ```

## デコード例の実行方法

  ```bash
  cd example
  poetry run python main.py --config=config_example.yml --output-name=output.png
  ```
