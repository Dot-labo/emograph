# emograph

本リポジトリは、授業用資料の視覚的理解を助けるため、YAMLで定義された絵文字、矢印、テキスト要素を基に画像を自動生成するpythonライブラリを提供します。

## 環境設定

* uvをインストール
  * macOSの場合

    ```bash
    brew install uv
    ```

* ライブラリをインストール

  ```bash
  uv sync
   ```

## 実行方法

  ```bash
  uv run main.py --config=config.yml --output-name=output.png
  ```
