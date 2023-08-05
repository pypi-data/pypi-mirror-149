from typing import Any, Type, Optional, Callable
from pydantic import BaseModel


class FunctionArgInfo(BaseModel):
    name: str
    type: Optional[Type] = None
    default_value: Optional[Any] = None


class FunctionInformation(BaseModel):
    function_object: Callable
    priority: int = -1
    args: dict[str, FunctionArgInfo] = {}
    rollback: Optional[Callable] = None

    @property
    def name(self) -> str:
        return self.function_object.__name__

    @property
    def receives_all_kwargs(self) -> bool:
        return "kwargs" in self.args.keys()


class OperationExecutionInfo(BaseModel):
    exc: Optional[Exception] = None
    on_func: Optional[FunctionInformation] = None
    func_args: Optional[dict[str, Any]] = None

    class Config:
        arbitrary_types_allowed = (Exception,)
