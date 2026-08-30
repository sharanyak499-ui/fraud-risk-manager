from pydantic import BaseModel, Field


class Transaction(BaseModel):

    transaction_id: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    user_id: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    amount: float = Field(
        ...,
        gt=0,
        le=10_000_000
    )

    location_changed: bool

    new_device: bool

    failed_attempts: int = Field(
        ...,
        ge=0,
        le=20
    )