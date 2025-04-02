from typing import TypeVar, Generic, Optional
from pydantic.generics import GenericModel

T = TypeVar('T')

class APIResponse(GenericModel, Generic[T]):
    """Standard API response wrapper"""
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def success_response(cls, data: T, message: str = None) -> 'APIResponse[T]':
        return cls(success=True, data=data, message=message)

    @classmethod
    def error_response(cls, error: str, message: str = None) -> 'APIResponse[T]':
        return cls(success=False, error=error, message=message)