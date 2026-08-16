from pydantic import BaseModel, ConfigDict


class ComplaintAddressCreate(BaseModel):
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = "India"
    zipcode: str | None = None


class ComplaintAddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    complaint_id: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = "India"
    zipcode: str | None = None
