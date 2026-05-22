from pydantic import BaseModel


class DecompiledFunction(BaseModel):
    name: str
    address: str
    code: str
