from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str = None
    disabled: bool = False

