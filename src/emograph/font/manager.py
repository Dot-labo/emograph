import platform
from PIL import ImageFont
from .type import FontData


LOCAL_FONTS_DATA = {
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
    },
    "seguiemj": {
        "path": "./fonts/seguiemj.ttf",
        "size": 109
    },
}


class Manager:
    def get_font_info(self, font_name: str) -> FontData:
        # ローカルフォント情報を取得
        font_info = self._fetch_local_font_info(font_name)
        if font_info is not None:
            return font_info

        # もしローカルにフォントがなければ、プラットフォームのフォント情報を取得
        font_info = self._fetch_platform_font_info(font_name)
        if font_info is not None:
            return font_info

        # フォントが見つからない場合はエラー
        raise ValueError(f"Unsupported font: {font_name}")

    def _fetch_platform_font_info(self, font_name: str) -> FontData | None:
        platform_name = platform.system()
        #TODO: Not implemented yet
        return None

    def _fetch_local_font_info(self, font_name: str) -> FontData:
        try:
            return FontData(**LOCAL_FONTS_DATA[font_name])
        except KeyError:
            print(f"Font not found in local: {font_name}")
            return None

    def get_font(
        self,
        font_name: str = "arial",
        size: int | None = None,
        encoding: str = "",
        layout_engine: str | None = None
    ) -> ImageFont.FreeTypeFont:
        font_info = self.get_font_info(font_name)
        font_path = font_info.path
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
