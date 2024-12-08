import os
import math
import yaml
from PIL import Image, ImageDraw, ImageFont
import emoji


class Builder:
    def __init__(self):
        pass

    def load_yaml(self, file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def get_font(self, font_path: str | None = None, size: int = 24) -> ImageFont.FreeTypeFont:
        try:
            return ImageFont.truetype(font_path, size) if font_path else ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

    def draw_emoji(self, image: Image.Image, element: dict, fonts: dict) -> Image.Image:
        draw = ImageDraw.Draw(image)
        emj = emoji.emojize(element['emoji'])
        x, y = element['position']['x'], element['position']['y']
        size = element.get('size', 1.0)
        rotation = element.get('rotation', 0)
        #font = self.get_font(size=int(fonts['emoji'].size * size))
        font_path = "./fonts/Noto-COLRv1-emojicompat.ttf"
        font = ImageFont.truetype(font_path, 109, encoding='unic')

        # テキスト画像のサイズを計算
        bbox = draw.textbbox((0, 0), emj, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 回転を考慮したサイズの text_image を作成
        if rotation:
            diagonal = math.sqrt(text_width**2 + text_height**2)
            text_image = Image.new('RGBA', (int(diagonal), int(diagonal)), (255,255,255,0))
            text_draw = ImageDraw.Draw(text_image)
            # テキストを中央に配置
            text_x = (diagonal - text_width) / 2
            text_y = (diagonal - text_height) / 2
            text_draw.text((text_x, text_y), emj, font=font, fill="black", embedded_color=True)
            text_image = text_image.rotate(rotation, resample=Image.BICUBIC, expand=True)
            # 回転後の画像を元のサイズの画像に貼り付け
            final_image = Image.new('RGBA', image.size, (255,255,255,0))
            paste_x = int(x - text_image.width/2)
            paste_y = int(y - text_image.height/2)
            final_image.paste(text_image, (paste_x, paste_y), text_image)
            text_image = final_image
        else:
            text_image = Image.new('RGBA', image.size, (255,255,255,0))
            text_draw = ImageDraw.Draw(text_image)
            text_draw.text((x, y), emj, font=font, fill="black", embedded_color=True)

        image = Image.alpha_composite(image, text_image)
        
        if 'caption' in element:
            cap = element['caption']
            cap_font = self.get_font(cap.get('font_path'), cap.get('font_size', 16))
            draw.text((cap['position']['x'], cap['position']['y']), cap['content'], font=cap_font, fill=cap['color'])

        return image

    def draw_arrow(self, draw: ImageDraw.ImageDraw, element: dict, elements_dict: dict) -> None:
        start = elements_dict.get(element['start_id'])
        end = elements_dict.get(element['end_id'])
        if not start or not end:
            print(f"Arrowのstart_idまたはend_idが見つかりません: {element['start_id']}, {element['end_id']}")
            return
        start_x = start['position']['x'] + 12  # 仮の中心
        start_y = start['position']['y'] + 12
        end_x = end['position']['x'] + 12
        end_y = end['position']['y'] + 12
        draw.line([(start_x, start_y), (end_x, end_y)], fill=element.get('color', "#000000"), width=element.get('thickness',1))
        angle = math.atan2(end_y - start_y, end_x - start_x)
        arrow_length, arrow_angle = 10, math.radians(30)
        points = [
            (end_x, end_y),
            (end_x - arrow_length * math.cos(angle - arrow_angle), end_y - arrow_length * math.sin(angle - arrow_angle)),
            (end_x - arrow_length * math.cos(angle + arrow_angle), end_y - arrow_length * math.sin(angle + arrow_angle))
        ]
        draw.polygon(points, fill=element.get('color', "#000000"))

    def draw_text(self, draw: ImageDraw.ImageDraw, element: dict) -> None:
        font = self.get_font(element.get('font_path'), element.get('font_size',24))
        draw.text((element['position']['x'], element['position']['y']), element['content'], font=font, fill=element.get('color', "#000000"))

    def generate_image(self, yaml_data: dict, output_path: str) -> None:
        spec = yaml_data['image']
        image = Image.new('RGBA', (spec['width'], spec['height']), spec.get('background_color', "#FFFFFF"))
        draw = ImageDraw.Draw(image)
        elements_dict = {e['id']: e for e in spec['elements'] if 'id' in e}
        for element in spec['elements']:
            if element['type'] == 'emoji':
                image = self.draw_emoji(image, element, fonts={'emoji': self.get_font(size=24)})
            elif element['type'] == 'arrow':
                self.draw_arrow(draw, element, elements_dict)
            elif element['type'] == 'text':
                self.draw_text(draw, element)
            else:
                print(f"未対応の要素タイプ: {element['type']}")
        image.convert("RGB").save(output_path, "PNG")
