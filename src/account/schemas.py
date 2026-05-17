from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class UserLoginSchema(BaseModel):
    username: str = Field(...,max_length=250, description="User's username")
    password: str = Field(..., description="User's password")

class UserRegisterSchema(BaseModel):
    username: str = Field(..., max_length=250, description="User's username")
    password: str = Field(...,description="User's password")
    password_confirm: str = Field(..., description="User's password confirm")

    @field_validator("password_confirm")
    def check_password_correct(cls, password_confirm, validation):
        if not (password_confirm == validation.data.get("password")):
            raise ValueError("Password does not match")
        return password_confirm
