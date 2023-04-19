from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Error(BaseModel):
    error_key: str = Field(..., title="Error Key")
    error_message: str = Field(..., title="Error Message")
    error_loc: Optional[Any] = None


class NotFoundError(BaseModel):
    error_key: str = Field(..., title="model_not_found")
    error_message: str = Field(..., title="Model <model_name> not found")
    error_loc: Optional[List[str]] = Field(None, title="Error Location")

    class Config:
        schema_extra = {
            "example": {
                "error_key": "model_not_found",
                "error_message": "Model <model_name> not found",
                "error_loc": "",
            }
        }


class ValidationError(BaseModel):
    error_key: str = Field(..., title="Error Key")
    error_message: str = Field(..., title="Error Message")
    error_loc: Optional[List[str]] = Field(None, title="Error Location")


class RecoResponse(BaseModel):
    user_id: int = Field(..., title="User Id")
    items: List[int] = Field(..., title="Items")

    class Config:
        schema_extra = {
            "example": {
                "user_id": 4456,
                "items": [12, 13, 123, 124, 24, 35, 67, 56, 89, 23],
            }
        }


class HealthResponse(BaseModel):
    health: str = Field(..., title="Health")

    class Config:
        schema_extra = {"example": {"health": "I am alive. Everything is OK!"}}


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title="Validation Error")
