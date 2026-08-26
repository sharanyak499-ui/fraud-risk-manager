from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_id: str
    amount: float
    location_changed: bool
    new_device: bool
    failed_attempts: int