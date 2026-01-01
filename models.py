from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password_hash: str

class ScanHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    original_text: str
    summary_text: str
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))