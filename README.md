# emograph

本リポジトリは、授業用資料の視覚的理解を助けるため、YAMLで定義された絵文字、矢印、テキスト要素を基に画像を自動生成するpythonライブラリを提供します。

## 利用方法

  ```bash
  pip install git+https://github.com/Dot-labo/emograph.git
  ```

## 開発環境設定

* uvをインストール
  * macOSの場合

    ```bash
    brew install uv
    ```

* ライブラリをインストール

  ```bash
  uv sync
   ```

## デコード例の実行方法

  ```bash
  cd example
  uv run main.py --config=config_example.yml --output-name=output.png
  ```
