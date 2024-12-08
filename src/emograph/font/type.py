from pydantic import BaseModel, Field


class FontData(BaseModel):
    path: str = Field(description="フォントファイルのパス")
    size: int = Field(description="フォントサイズ")
