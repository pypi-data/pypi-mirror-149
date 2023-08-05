from typing import Generic, TypeVar

from . import mixins

ServiceInstance = TypeVar("ServiceInstance")


class Service(mixins.ServiceInstanceMixin[ServiceInstance], Generic[ServiceInstance]):
    pass


class UUIDService(mixins.UUIDServiceInstanceMixin[ServiceInstance], Service[ServiceInstance], Generic[ServiceInstance]):
    pass
