from pydantic import BaseModel, Field
import bleach


class ConverterConfig(BaseModel):
    allowed_tags: set[str] = Field(default_factory=lambda: set(bleach.sanitizer.ALLOWED_TAGS) | {
        "p", "pre", "code", "span",
        "h1", "h2", "h3", "h4", "h5", "h6"
    })
    allowed_attributes: dict = Field(default_factory=lambda: {"*": ["class", "id", "style", "title", "href"]})
    allowed_file_extensions: set[str] = Field(default_factory=lambda: {".md", ".html", ".markdown", ".mdown"})
    max_file_size: int = Field(
        default=2 * 1024 * 1024,  # 2 MB
        description="Maximum allowed file size in bytes"
    )


CONFIG = ConverterConfig()
