from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Record(BaseModel):
    """Record"""
    content: str = None


class Message(BaseModel):
    """Message"""
    message: str
    data: Record | list | object | bool = None
    response_time: float = None
