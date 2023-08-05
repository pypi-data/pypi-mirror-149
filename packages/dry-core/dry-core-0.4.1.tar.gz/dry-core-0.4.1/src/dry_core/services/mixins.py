from typing import Optional, Generic, TypeVar, Type, Union
from uuid import UUID

from dry_core.selectors.generics import BaseSelector

ServiceInstance = TypeVar("ServiceInstance")
BaseInstanceSelector = TypeVar("BaseInstanceSelector", bound=BaseSelector)


class BaseServiceMixin(Generic[ServiceInstance]):
    model: Type[ServiceInstance]

    def __init__(self, *args, **kwargs):
        self.validate_service_model_defined()

    def validate_service_model_defined(self) -> None:
        if self.model is None:
            raise AttributeError(f'Service class {self.__class__.__name__} must setup "model" field')


class ServiceInstanceMixin(BaseServiceMixin[ServiceInstance], Generic[ServiceInstance]):
    def __init__(self, instance: Optional[ServiceInstance] = None, *args, **kwargs):
        super(ServiceInstanceMixin, self).__init__(*args, **kwargs)
        self.validate_service_model_defined()
        # if instance don't set on higher level, like it can be in UUIDServiceMixin, try init it from arguments
        if getattr(self, "instance", None) is None:
            self.instance: Optional[ServiceInstance] = instance

    def validate_instance_filled(self, validate_type: bool = True, raise_exception: bool = True) -> bool:
        if self.instance is None:
            if raise_exception:
                raise ValueError(
                    '{class_name} object field "instance" is None'.format(class_name=self.__class__.__name__)
                )
            return False
        if validate_type:
            if not isinstance(self.instance, self.model):
                if raise_exception:
                    raise TypeError(
                        '{class_name} field "instance" is type {instance_type}, must be {service_instance_model}'.format(
                            class_name=self.__class__.__name__,
                            instance_type=self.instance.__class__.__name__,
                            service_instance_model=self.model.__name__,
                        )
                    )
                return False
        return True


class UUIDServiceInstanceMixin(ServiceInstanceMixin[ServiceInstance], Generic[ServiceInstance]):
    selector: Type[BaseInstanceSelector]
    selector_get_by_uuid_method_name: str = "get_by_uuid"
    selector_get_by_uuid_param_name: str = "uuid"

    def __init__(self, *args, uuid: Optional[Union[UUID, str]] = None, **kwargs):
        if self.selector is None:
            raise AttributeError(f'"selector" class attr must be defined for {self.__class__}')
        if getattr(self.selector, self.selector_get_by_uuid_method_name, None) is None:
            raise AttributeError(f'"selector" class must have method "{self.selector_get_by_uuid_method_name}"')
        if uuid is not None:
            if isinstance(uuid, UUID):
                uuid = str(uuid)
            self.instance: ServiceInstance = getattr(self.selector, self.selector_get_by_uuid_method_name)(
                **{self.selector_get_by_uuid_param_name: uuid}
            )
        super(UUIDServiceInstanceMixin, self).__init__(*args, **kwargs)
