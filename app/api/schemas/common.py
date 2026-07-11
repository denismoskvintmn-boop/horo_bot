from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Schema for health check response."""

    status: str = Field(..., description="Service status")


class ErrorResponse(BaseModel):
    """Schema for error response."""

    detail: str = Field(..., description="Error details")
