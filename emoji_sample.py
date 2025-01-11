from PIL import Image, ImageDraw, ImageFont
import os


def emoji_to_png(emoji: str, size: int, output_path: str) -> None:
    """
    絵文字を指定されたサイズの透過PNG画像として保存する関数
    
    Args:
        emoji (str): 変換したい絵文字文字列
        size (int): 出力画像の幅と高さ（ピクセル）
        output_path (str): 出力ファイルのパス（.pngで終わること）
    """
    # 透明な背景の画像を作成
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    try:
        # システムにインストールされているフォントから絵文字対応フォントを探す
        # Macの場合
        font_paths = [
            '/System/Library/Fonts/Apple Color Emoji.ttc',  # macOS
            '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',  # Linux
            'C:\\Windows\\Fonts\\seguiemj.ttf'  # Windows
        ]
        
        font_path = None
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                break
                
        if font_path is None:
            raise Exception("絵文字対応フォントが見つかりません")
            
        # フォントサイズを画像サイズに合わせて調整
        # 実際の絵文字は画像サイズの約80%のサイズにする
        font_size = int(size * 0.8)
        font = ImageFont.truetype(font_path, font_size)
        
        # 絵文字を画像の中央に配置
        # テキストのバウンディングボックスを取得
        bbox = draw.textbbox((0, 0), emoji, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 中央配置の座標を計算
        x = (size - text_width) / 2
        y = (size - text_height) / 2
        
        # 絵文字を描画
        draw.text((x, y), emoji, font=font, embedded_color=True)
        
        # PNG形式で保存
        image.save(output_path, 'PNG')
        print(f"画像を保存しました: {output_path}")
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise


# 使用例
if __name__ == "__main__":
    # 様々なサイズで絵文字を画像化する例
    emoji_list = ["😊"]
    sizes = [256]

    for emoji in emoji_list:
        for size in sizes:
            output_path = f"emoji_{ord(emoji)}_{size}px.png"
            emoji_to_png(emoji, size, output_path)
