from pydantic import BaseModel, Field


class SlugRequest(BaseModel):
    text: str = Field(
        ...,
        title="Input Text",
        description="The text to be converted into a URL-friendly slug."
    )
    max_length: int | None = Field(
        None,
        title="Maximum Length",
        description="Optional maximum length of the generated slug."
    )
    lowercase: bool = Field(
        True,
        title="Lowercase",
        description="Whether to convert the slug to lowercase."
    )
    separator: str = Field(
        "-",
        title="Separator",
        description="Character used to separate words in the slug."
    )
    language: str | None = Field(
        None,
        title="Language Code",
        description="Optional language code for transliteration (e.g., 'ru', 'zh', 'ar')."
    )
    allow_unicode: bool = Field(
        False,
        title="Allow Unicode",
        description="If True, Unicode characters are preserved without transliteration."
    )

class SlugResponse(BaseModel):
    slug: str = Field(
        ...,
        title="Generated Slug",
        description="The resulting URL-friendly slug generated from the input text."
    )
