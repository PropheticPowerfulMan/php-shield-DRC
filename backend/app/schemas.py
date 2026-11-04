from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid import UUID

class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("Valid email address required.")
        return value

class CurrentUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: str
    roles: list[str]
