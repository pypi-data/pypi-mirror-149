from typing import Any, Callable, Optional, Union, Dict

from pydantic import BaseModel


class Argument(BaseModel):
    default_value: Any
    from_name: Optional[str] = None
    from_initial_args: bool = False
    validators: Optional[list[Callable]] = None

    def __init__(self, _default_value, **kwargs):
        kwargs["default_value"] = _default_value
        super(Argument, self).__init__(**kwargs)


class ArgumentsStore:
    def __init__(self, operation_args_dict: dict[str, Any], *, immutable: bool = False):
        self._operation_args_dict = operation_args_dict.copy()
        self._immutable = immutable

    @property
    def immutable(self) -> bool:
        return self._immutable

    # Store dict-like interface definition

    def _validate_immutability(self) -> None:
        if self._immutable:
            raise ValueError("Store is immutable")

    def get_with_default(self, key, default):
        return self._operation_args_dict.get(key, default)

    def copy(self):
        return self._operation_args_dict.copy()

    def clear(self):
        self._validate_immutability()
        return self._operation_args_dict.clear()

    def has_arg(self, arg_name):
        return arg_name in self._operation_args_dict

    def keys(self):
        return self._operation_args_dict.keys()

    def items(self):
        return self._operation_args_dict.items()

    def dict(self) -> dict[str, Any]:
        return self._operation_args_dict.copy()

    def update(self, **kwargs):
        self._validate_immutability()
        self._operation_args_dict.update(**kwargs)

    def __getitem__(self, arg_name):
        return self._operation_args_dict[arg_name]

    def __setitem__(self, arg_name, value):
        self._validate_immutability()
        self._operation_args_dict[arg_name] = value
        return self._operation_args_dict[arg_name]

    def __delitem__(self, key):
        self._validate_immutability()
        del self._operation_args_dict[key]

    def __repr__(self):
        return repr(self._operation_args_dict)

    def __len__(self):
        return len(self._operation_args_dict)

    def __eq__(self, other_store: Union["ArgumentsStore", Dict[str, Any]]):
        return set(self.items()) == set(other_store.items())

    def __contains__(self, item):
        return item in self._operation_args_dict

    def __iter__(self):
        return iter(self._operation_args_dict)
