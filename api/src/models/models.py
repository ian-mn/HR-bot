from pydantic import BaseModel

class BoolResponse(BaseModel):
    result: bool

class PhoneReponse(BaseModel):
    result: str | None