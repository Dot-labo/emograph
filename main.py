import os
from src.emograph import Builder


def main(yaml_file: str, output_image_name: str, output_dir = "./output"):
    builder = Builder()

    yaml_data = builder.load_yaml(yaml_file)
    output_path = os.path.join(output_dir, output_image_name)
    builder.generate_image(yaml_data, output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YAML定義から画像を生成")
    parser.add_argument(
        '--config',
        required=True,
        help="configを記述したyamlファイル",
    )
    parser.add_argument(
        '--output_name',
        required=False,
        help="出力画像ファイル（例: output.png）",
    )
    args = parser.parse_args()

    main(
        yaml_file=args.config,
        output_image_name=args.output_name
    )
