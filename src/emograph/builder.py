import math
import yaml
from PIL import Image, ImageDraw, ImageFont
import emoji
from emograph.utils.color_utils import hex_to_tuple


class Builder:
    def load_yaml(self, file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def draw_emoji(
        self,
        canvas_image: Image.Image,
        element: dict,
        emoji_font_path: str,
        text_font_path: str
    ) -> Image.Image:
        # 透明な新規レイヤーを作成
        #text_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
        #text_draw = ImageDraw.Draw(text_image)

        emj = emoji.emojize(element['emoji'])
        x, y = element['position']['x'], element['position']['y']
        font_path = element.get('font_path', emoji_font_path)
        font_size = element.get('size', 1.0)
        rotation = element.get('rotation', 0)
        font = ImageFont.truetype(font_path, font_size)

        # フォントサイズに合わせた透明な新規レイヤーを作成
        emoji_image = Image.new('RGBA', (font_size, font_size), (0, 0, 0, 0))
        emoji_draw = ImageDraw.Draw(emoji_image)

        # テキスト画像のサイズを計算
        bbox = emoji_draw.textbbox((0, 0), emj, font=font)
        emoji_width = bbox[2] - bbox[0]
        emoji_height = bbox[3] - bbox[1]

        if rotation:
            diagonal = math.sqrt(emoji_width**2 + emoji_height**2)
            rotated_image = Image.new('RGBA', (int(diagonal), int(diagonal)), (0, 0, 0, 0))
            rotated_draw = ImageDraw.Draw(rotated_image)

            # テキストを中央に配置
            emoji_x = (diagonal - emoji_width) / 2
            emoji_y = (diagonal - emoji_height) / 2
            rotated_draw.text(
                xy=(emoji_x, emoji_y),
                text=emj,
                font=font,
                fill="black",
                embedded_color=True
            )
            rotated_image = rotated_image.rotate(rotation, resample=Image.BICUBIC, expand=True)

            # 回転後の画像を配置
            paste_x = int(x - rotated_image.width / 2)
            paste_y = int(y - rotated_image.height / 2)
            emoji_image.paste(rotated_image, (paste_x, paste_y), rotated_image)
        else:
            diagonal = math.sqrt(emoji_width**2 + emoji_height**2)
            emoji_x = (diagonal - emoji_width) / 2
            emoji_y = (diagonal - emoji_height) / 2
            emoji_draw.text(
                xy=(x, y),
                text=emj,
                font=font,
                fill="black",
                embedded_color=True
            )

        emoji_image.save('emoji_image.png', 'PNG')

        # emoji_imageをcanvas_imageに貼り付け
        canvas_image.paste(emoji_image, (x, y), emoji_image)

        # キャプションがあれば追加
        if 'caption' in element:
            # 透明な新規レイヤーを作成
            caption_image = Image.new('RGBA', canvas_image.size, (0, 0, 0, 0))
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
            result = Image.alpha_composite(canvas_image, caption_image)

        return result

    def draw_arrow(
        self,
        image: Image.Image,
        element: dict,
        elements_dict: dict
    ) -> Image.Image:
        # 透明な新規レイヤーを作成
        arrow_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
        arrow_draw = ImageDraw.Draw(arrow_image)

        start = elements_dict.get(element['start_id'])
        end = elements_dict.get(element['end_id'])
        if not start or not end:
            return image

        start = elements_dict.get(element['start_id'])
        end = elements_dict.get(element['end_id'])
        if not start or not end:
            print(f"Arrowのstart_idまたはend_idが見つかりません: {element['start_id']}, {element['end_id']}")
            return

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
        text_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
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
        background_color = spec.get('background_color', "#FFFFFF")
        background_color_tuple = hex_to_tuple(background_color)
        background_alpha = spec.get('background_alpha', 0)
        background_alpha_color_tuple = background_color_tuple + (background_alpha,)
        image = Image.new('RGBA', (spec['width'], spec['height']), background_alpha_color_tuple)
        text_font_path = spec.get('text_font_path', 'arial')
        emoji_font_path = spec.get('emoji_font_path', 'NotoColorEmoji')
        elements_dict = {e['id']: e for e in spec['elements'] if 'id' in e}

        for element in spec['elements']:
            if element['type'] == 'emoji':
                image = self.draw_emoji(image, element, emoji_font_path, text_font_path)
            elif element['type'] == 'arrow':
                image = self.draw_arrow(image, element, elements_dict)
            elif element['type'] == 'text':
                image = self.draw_text(image, element, text_font_path)
            else:
                print(f"未対応の要素タイプ: {element['type']}")

        image.convert("RGB").save(output_path, "PNG")
