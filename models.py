from sqlmodel import SQLModel, Field
from typing import Optional

# This is the blueprint of our database table.
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: str 