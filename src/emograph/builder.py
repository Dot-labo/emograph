import os
import math
import yaml
from PIL import Image, ImageDraw, ImageFont
import emoji
from .fonts import DEFAULT_FONT_PATH, DEFAULT_EMOJI_FONT_PATH


class Builder:
    def load_yaml(self, file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def draw_emoji(
        self,
        image: Image.Image,
        element: dict,
        emoji_font_path: str,
        text_font_path: str
    ) -> Image.Image:
        # 透明な新規レイヤーを作成
        text_image = Image.new('RGBA', image.size, (255,255,255,0))
        text_draw = ImageDraw.Draw(text_image)
        
        emj = emoji.emojize(element['emoji'])
        x, y = element['position']['x'], element['position']['y']
        font_path = element.get('font_path', emoji_font_path)
        font_size = element.get('size', 1.0)
        rotation = element.get('rotation', 0)

        font = ImageFont.truetype(font_path, font_size)

        # テキスト画像のサイズを計算
        bbox = text_draw.textbbox((0, 0), emj, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if rotation:
            diagonal = math.sqrt(text_width**2 + text_height**2)
            rotated_image = Image.new('RGBA', (int(diagonal), int(diagonal)), (255, 255, 255, 0))
            rotated_draw = ImageDraw.Draw(rotated_image)

            # テキストを中央に配置
            text_x = (diagonal - text_width) / 2
            text_y = (diagonal - text_height) / 2
            rotated_draw.text(
                xy=(text_x, text_y),
                text=emj,
                font=font,
                fill="black",
                embedded_color=True
            )
            rotated_image = rotated_image.rotate(rotation, resample=Image.BICUBIC, expand=True)

            # 回転後の画像を配置
            paste_x = int(x - rotated_image.width / 2)
            paste_y = int(y - rotated_image.height / 2)
            text_image.paste(rotated_image, (paste_x, paste_y), rotated_image)
        else:
            text_draw.text(
                xy=(x, y),
                text=emj,
                font=font,
                fill="black",
                embedded_color=True
            )

        result = Image.alpha_composite(image, text_image)

        # キャプションがあれば追加
        if 'caption' in element:
            result = self._draw_caption(result, element, text_font_path)

        return result

    def draw_shapes(self, image: Image.Image, element: dict, text_font_path: str) -> Image.Image:
        shape_image = Image.new('RGBA', image.size, (255,255,255,0))
        draw = ImageDraw.Draw(shape_image)

        if element['shape'] == 'circle':
            draw.ellipse(
                xy=(
                    element['position']['x'],
                    element['position']['y'],
                    element['position']['x'] + element['size'],
                    element['position']['y'] + element['size']
                ),
                outline=element.get('color', "#000000"),
                width=element.get('thickness', 1)
            )
        elif element['shape'] == 'rectangle':  
            draw.rectangle(
                xy=(
                    element['position']['x'],
                    element['position']['y'],
                    element['position']['x'] + element['size'],
                    element['position']['y'] + element['size']
                ),
                outline=element.get('color', "#000000"),
                width=element.get('thickness', 1)
            )
        elif element['shape'] == 'line':
            draw.line(
                xy=(
                    element['position']['start']['x'],
                    element['position']['start']['y'],
                    element['position']['end']['x'],
                    element['position']['end']['y']
                ),
                fill=element.get('color', "#000000"),
                width=element.get('thickness', 1)
            )
        else:
            print(f"未対応の形状: {element['shape']}")
            return image

        if 'caption' in element:
            shape_image = self._draw_caption(shape_image, element, text_font_path)

        return Image.alpha_composite(image, shape_image)

    def _draw_caption(self, image: Image.Image, element: dict, text_font_path: str) -> Image.Image:
        # 透明な新規レイヤーを作成
        caption_image = Image.new('RGBA', image.size, (255,255,255,0))
        caption_draw = ImageDraw.Draw(caption_image)

        cap = element['caption']
        font_path = element.get('font_path', text_font_path)
        font_size = element.get('font_size', 24)
        cap_font = ImageFont.truetype(font_path, font_size)
        caption_draw.text(
            xy=(cap['position']['x'], cap['position']['y']),
            text=cap['content'],
            font=cap_font,
            fill=cap['color']
        )

        return Image.alpha_composite(image, caption_image)

    def draw_arrow(
        self,
        image: Image.Image,
        element: dict,
        elements_dict: dict
    ) -> Image.Image:
        # 透明な新規レイヤーを作成
        arrow_image = Image.new('RGBA', image.size, (255,255,255,0))
        arrow_draw = ImageDraw.Draw(arrow_image)

        start = elements_dict.get(element['start_id'])
        end = elements_dict.get(element['end_id'])
        if not start or not end:
            print(f"Arrowのstart_idまたはend_idが見つかりません: {element['start_id']}, {element['end_id']}")
            return

        if 'position' in element:
            start_x = element['position']['start']['x'] + 12  # 仮の中心
            start_y = element['position']['start']['y'] + 12
            end_x = element['position']['end']['x'] + 12
            end_y = element['position']['end']['y'] + 12
        else:
            start_x = start['position']['x'] + 12  # 仮の中心
            start_y = start['position']['y'] + 12
            end_x = end['position']['x'] + 12
            end_y = end['position']['y'] + 12
        arrow_draw.line(
            xy=[(start_x, start_y), (end_x, end_y)],
            fill=element.get('color', "#000000"),
            width=element.get('thickness', 1)
        )
        angle = math.atan2(end_y - start_y, end_x - start_x)
        arrow_length, arrow_angle = 10, math.radians(30)
        points = [
            (end_x, end_y),
            (end_x - arrow_length * math.cos(angle - arrow_angle), end_y - arrow_length * math.sin(angle - arrow_angle)),
            (end_x - arrow_length * math.cos(angle + arrow_angle), end_y - arrow_length * math.sin(angle + arrow_angle))
        ]
        arrow_draw.polygon(xy=points, fill=element.get('color', "#000000"))

        return Image.alpha_composite(image, arrow_image)

    def draw_text(
        self,
        image: Image.Image,
        element: dict,
        text_font_path: str
    ) -> Image.Image:
        # 透明な新規レイヤーを作成
        text_image = Image.new('RGBA', image.size, (255,255,255,0))
        text_draw = ImageDraw.Draw(text_image)

        font_path = element.get('font_path', text_font_path)
        font_size = element.get('font_size', 24)
        font = ImageFont.truetype(font_path, font_size)

        text_draw.text(
            xy=(element['position']['x'], element['position']['y']),
            text=element['content'],
            font=font,
            fill=element.get('color', "#000000")
        )

        return Image.alpha_composite(image, text_image)

    def generate_image(self, yaml_data: dict, output_path: str) -> None:
        spec = yaml_data['image']
        image = Image.new('RGBA', (spec['width'], spec['height']), spec.get('background_color', "#FFFFFF"))
        text_font_path = spec.get('text_font_path', DEFAULT_FONT_PATH)
        emoji_font_path = spec.get('emoji_font_path', DEFAULT_EMOJI_FONT_PATH)
        elements_dict = {e['id']: e for e in spec['elements'] if 'id' in e}

        for element in spec['elements']:
            if element['type'] == 'emoji':
                image = self.draw_emoji(image, element, emoji_font_path, text_font_path)
            elif element['type'] == 'shape':
                image = self.draw_shapes(image, element, text_font_path)
            elif element['type'] == 'arrow':
                image = self.draw_arrow(image, element, elements_dict)
            elif element['type'] == 'text':
                image = self.draw_text(image, element, text_font_path)
            else:
                print(f"未対応の要素タイプ: {element['type']}")

        image.convert("RGB").save(output_path, "PNG")
