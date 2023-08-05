from typing import Any, Optional


class DryPyException(Exception):
    def __init__(self, *args, additional_data: Optional[dict[str, Any]] = None):
        super(DryPyException, self).__init__(*args)
        self.additional_data: dict[str, Any] = additional_data or {}


class ApplicationError(DryPyException):
    pass


class NotFoundError(DryPyException):
    pass


# Operations Errors
class BaseOperationException(DryPyException):
    pass


class OperationImproperlyConfigured(BaseOperationException):
    pass
