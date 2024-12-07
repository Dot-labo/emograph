from src.emograph import Builder


def main(yaml_file: str, output_image: str):
    builder = Builder()

    yaml_data = builder.load_yaml(yaml_file)
    builder.generate_image(yaml_data, output_image)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YAML定義から画像を生成")
    parser.add_argument('-Y', '--yaml', required=True, help="入力YAMLファイル")
    parser.add_argument('-O', '--output', required=True, help="出力画像ファイル（例: output.png）")
    args = parser.parse_args()

    main(yaml_file=args.yaml, output_image=args.output)
