from pydantic import BaseModel, Field, model_validator


class PasswordRequest(BaseModel):
    length: int = Field(12, ge=6, le=256, description="Password length")
    count: int = Field(1, ge=1, le=100, description="Number of passwords to generate")
    use_lower: bool = Field(True, description="Include lowercase letters")
    use_upper: bool = Field(True, description="Include uppercase letters")
    use_digits: bool = Field(True, description="Include digits")
    use_special: bool = Field(True, description="Include special characters")

    @model_validator(mode="before")
    def check_flags(cls, values):
        if not any(values.get(f) for f in ["use_lower", "use_upper", "use_digits", "use_special"]):
            raise ValueError("At least one character type must be selected.")
        return values
