from PIL import ImageFont
from .type import FontData


FONTS_DATA = {
    "arial": {
        "path": "arial.ttf",
        "size": 24
    },
    "NotoColorEmoji": {
        "path": "./fonts/NotoColorEmoji.ttf",
        "size": 109
    },
    "Noto-COLRv1": {
        "path": "./fonts/Noto-COLRv1.ttf",
        "size": 109
    }
}


class Manager:
    def get_font_info(self, font_name: str) -> FontData:
        try:
            return FontData(**FONTS_DATA[font_name])
        except KeyError:
            raise ValueError(f"Font '{font_name}' not found in the list of available fonts.")

    def get_font(
        self,
        font_name: str = "arial",
        size: int | None = None,
        encoding: str = "",
        layout_engine: str | None = None
    ) -> ImageFont.FreeTypeFont:
        font_info = self.get_font_info(font_name)
        font_path = font_info.path #"C:\\Windows\\Fonts\\seguiemj.ttf"
        fontsize = font_info.size if size is None else size
        try:
            return ImageFont.truetype(
                font_path,
                size=fontsize,
                encoding=encoding,
                layout_engine=layout_engine
            )
        except:
            return ImageFont.load_default()
