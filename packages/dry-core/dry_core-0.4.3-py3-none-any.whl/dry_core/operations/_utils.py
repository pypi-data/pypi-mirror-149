import inspect
from typing import Callable

from ._models import FunctionInformation, FunctionArgInfo


def parse_function_information(
    function: Callable,
) -> FunctionInformation:
    return FunctionInformation(
        function_object=function,
        args=parse_function_parameters(function),
    )


def parse_function_parameters(
    function: Callable,
) -> dict[str, FunctionArgInfo]:
    return {
        parameter.name: FunctionArgInfo(
            name=parameter.name,
            type=parameter.annotation if parameter.annotation is not inspect.Parameter.empty else None,
            default_value=parameter.default if parameter.default is not inspect.Parameter.empty else ...,
        )
        for _, parameter in inspect.signature(function).parameters.items()
    }
