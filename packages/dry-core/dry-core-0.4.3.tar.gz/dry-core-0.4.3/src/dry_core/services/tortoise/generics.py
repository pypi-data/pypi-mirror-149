from typing import TypeVar, Generic

from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel

from dry_core.services import Service
from dry_core.operations import operation


BaseModel = TypeVar("BaseModel", bound=Model)
PydanticBaseModel = TypeVar("PydanticBaseModel", bound=PydanticModel)


class TortoiseService(Service[BaseModel], Generic[BaseModel]):
    @classmethod
    def _model_fields(cls) -> set[str]:
        return cls.model._meta.fields

    @operation
    async def create(self, **kwargs) -> BaseModel:
        self.instance = await self.model.create(**kwargs)
        return self.instance

    @operation
    async def update(self, **kwargs) -> BaseModel:
        self.validate_instance_filled()
        for attr, value in kwargs:
            if attr in self._model_fields():
                setattr(self.instance, attr, value)
        await self.instance.save()
        return self.instance

    @operation
    async def delete(self) -> BaseModel:
        self.validate_instance_filled()
        deleted_instance = self.instance
        await self.instance.delete()
        return deleted_instance
