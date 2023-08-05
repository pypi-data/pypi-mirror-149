import functools
import inspect
from typing import Callable, Type, Iterable, TYPE_CHECKING, Optional

from ._models import FunctionInformation
from ._utils import parse_function_information


class _BaseOperationAdditionalFunctionDecorator:  # noqa
    """
    Base decorator class, that contain all common logic for
    store and work with decorated functions of services classes
    """

    def __init__(self):
        self._operations_additional_funcs_store: dict[Type, dict[str, list[FunctionInformation]]] = {}

    def __getattr__(self, operation_name):
        """
        Use getattr to dynamic registration of any operation additions
        """

        class _BaseOperationAdditionalFunctionDecoratorWrapper:
            def __init__(self, method=None, *, priority: int = -1, rollback: Optional[Callable] = None):
                self.method = method
                self.priority = priority
                self.rollback = rollback

                if method is not None:
                    functools.update_wrapper(self, method)

            def __set_name__(local_self, owner, name):
                nonlocal self

                self._register_operation_func(
                    operation_name=operation_name,
                    original_function_owner=owner,
                    original_function=local_self.method,
                    priority=local_self.priority,
                    rollback=local_self.rollback,
                )

                setattr(owner, name, local_self.method)

            def __call__(self, method):
                return _BaseOperationAdditionalFunctionDecoratorWrapper(
                    method, priority=self.priority, rollback=self.rollback
                )

        return _BaseOperationAdditionalFunctionDecoratorWrapper

    def _get_class_funcs(self, class_obj) -> dict[str, list[FunctionInformation]]:
        """
        Used in local cases and can be used only for add/edit class funcs,
        but can't handle MRO recursive funcs handling
        """
        if (res := self._operations_additional_funcs_store.get(class_obj, None)) is None:
            res = self._operations_additional_funcs_store[class_obj] = {}
        return res

    def _register_operation_func(
        self,
        operation_name: str,
        original_function_owner: Type,
        original_function: Callable,
        priority: int,
        rollback: Optional[Callable] = None,
    ):
        operation_name = operation_name.lower()
        funcs_store = self._get_class_funcs(original_function_owner)
        if operation_name not in funcs_store:
            funcs_store[operation_name] = []
        funcs_list = funcs_store[operation_name]

        func_info = parse_function_information(original_function)
        func_info.priority = priority
        func_info.rollback = rollback
        funcs_list.append(func_info)

    def get_additional_operation_funcs(self, operation_owner_class, operation_name: str) -> list[FunctionInformation]:
        classes: Iterable[Type] = reversed(inspect.getmro(operation_owner_class))
        result: list[FunctionInformation] = []
        for obj in classes:
            result.extend(self._get_class_funcs(obj).get(operation_name, []))
        return result


# Decorators collection for automatic running pre-operation functions
pre = _BaseOperationAdditionalFunctionDecorator()

# Decorators collection for automatic running post-operation functions
post = _BaseOperationAdditionalFunctionDecorator()


if TYPE_CHECKING:
    # defined here to help IDEs and static type checkers only
    def operation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

else:

    class operation:
        def __init__(
            self,
            method=None,
            *,
            exception_handlers_mapping: Optional[dict[Type, Callable]] = None,
            as_transaction: bool = False,
            rollback: Optional[Callable] = None,
        ):
            self.method = method
            self.operation = None

            self.exception_handlers_mapping = exception_handlers_mapping
            self.as_transaction = as_transaction
            self.rollback = rollback

        def __set_name__(self, owner, name):
            from .operations import Operation, _AsyncOperation

            if inspect.iscoroutinefunction(self.method):
                self.operation = _AsyncOperation(
                    method=self.method,
                    method_class=owner,
                    exception_handlers_mapping=self.exception_handlers_mapping,
                    as_transaction=self.as_transaction,
                    rollback=self.rollback,
                )
            else:
                self.operation = Operation(
                    method=self.method,
                    method_class=owner,
                    exception_handlers_mapping=self.exception_handlers_mapping,
                    as_transaction=self.as_transaction,
                    rollback=self.rollback,
                )

            @functools.wraps(self.method)
            def wrapper(*args, **kwargs):
                return self.operation(*args, **kwargs)

            setattr(owner, name, wrapper)

        def __call__(self, func):
            return operation(
                func,
                exception_handlers_mapping=self.exception_handlers_mapping,
                as_transaction=self.as_transaction,
                rollback=self.rollback,
            )
