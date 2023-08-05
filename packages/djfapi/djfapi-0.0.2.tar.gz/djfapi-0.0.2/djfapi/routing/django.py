from functools import partial
from typing import List, Optional, Type, TypeVar
from collections import OrderedDict
import forge
from django.db import models
from pydantic import validate_arguments
from fastapi import APIRouter, Depends, Request, Security, Path, Body
from fastapi.security.base import SecurityBase
from ..schemas import Access
from ..utils.fastapi import Pagination, depends_pagination
from . import BaseRouter, RouterSchema


def _partial_with_description(func, /, *args, **kwargs):
    wrapped = partial(func, *args, **kwargs)
    wrapped.__doc__ = func.__doc__
    return wrapped


TDjangoModel = TypeVar('TDjangoModel', bound=models.Model)


class DjangoRouterSchema(RouterSchema):
    __router = None

    model: Type[TDjangoModel]

    def objects_filter(self, access: Optional[Access] = None) -> models.Q:
        return models.Q()

    def objects_get_filtered(self, access: Optional[Access] = None) -> List[TDjangoModel]:
        return list(self.model.objects.filter(self.objects_filter(access)))

    def objects_get_by_id(self, id: str, access: Optional[Access] = None) -> TDjangoModel:
        return self.model.objects.filter(self.objects_filter(access)).get(id=id)

    def _security_signature(self, method):
        if not self.security:
            return []

        return [
            forge.kwarg('access', type=Access, default=Security(self.security)),
        ]


    def endpoint_list(self, access: Optional[Access] = None):
            return self.list(items=[self.get.from_orm(obj) for obj in self.objects_get_filtered()])

    def _create_endpoint_list(self):
        return forge.sign(*[
            *self._security_signature('list'),
        ])(self.endpoint_list)


    def endpoint_post(self, *, data, access: Optional[Access] = None, **kwargs):
            obj = self.object_create(data)
            return self.get.from_orm(obj)

    def _create_endpoint_post(self):
        return forge.sign(*[
            forge.kwarg('data', type=self.create, default=Body(...)),
            *self._security_signature('post'),
        ])(self.endpoint_post)


    def endpoint_get(self, *, id: str = Path(...), access: Optional[Access] = None, **kwargs):
            obj = self.objects_get_by_id(id, access)
            return self.get.from_orm(obj)

    def _create_endpoint_get(self):
        return forge.sign(*[
            forge.kwarg('id', type=str, default=Path(..., min_length=self.model.id.field.max_length, max_length=self.model.id.field.max_length)),
            *self._security_signature('get'),
        ])(self.endpoint_get)


    def endpoint_patch(self, *, id: str = Path(...), data, access: Optional[Access] = None, **kwargs):
            obj = self.objects_get_by_id(id, access)
            return self.get.from_orm(obj)

    def _create_endpoint_patch(self):
        return forge.sign(*[
            forge.kwarg('id', type=str, default=Path(..., min_length=self.model.id.field.max_length, max_length=self.model.id.field.max_length)),
            forge.kwarg('data', type=self.update, default=Body(...)),
            *self._security_signature('patch'),
        ])(self.endpoint_patch)


    def endpoint_put(self, *, id: str = Path(...), data, access: Optional[Access] = None, **kwargs):
        obj = self.objects_get_by_id(id, access)
        return self.get.from_orm(obj)

    def _create_endpoint_put(self):
        return forge.sign(*[
            forge.kwarg('id', type=str, default=Path(..., min_length=self.model.id.field.max_length, max_length=self.model.id.field.max_length)),
            forge.kwarg('data', type=self.update, default=Body(...)),
            *self._security_signature('put'),
        ])(self.endpoint_put)

    def endpoint_delete(self, *, id: str = Path(...), access: Optional[Access] = None, **kwargs):
        obj = self.objects_get_by_id(id, access)

    def _create_endpoint_delete(self):
        return forge.sign(*[
            forge.kwarg('id', type=str, default=Path(..., min_length=self.model.id.field.max_length, max_length=self.model.id.field.max_length)),
            *self._security_signature('delete'),
        ])(self.endpoint_delete)

    def _create_route_list(self):
        self.__router.add_api_route('', methods=['GET'], endpoint=self._create_endpoint_list(), response_model=self.list)

    def _create_route_post(self):
        self.__router.add_api_route('', methods=['POST'], endpoint=self._create_endpoint_post(), response_model=self.get)

    def _create_route_get(self):
        self.__router.add_api_route('/{id}', methods=['GET'], endpoint=self._create_endpoint_get(), response_model=self.get)

    def _create_route_patch(self):
        self.__router.add_api_route('/{id}', methods=['PATCH'], endpoint=self._create_endpoint_patch(), response_model=self.get)

    def _create_route_put(self):
        self.__router.add_api_route('/{id}', methods=['PUT'], endpoint=self._create_endpoint_put(), response_model=self.get)

    def _create_route_delete(self):
        self.__router.add_api_route('/{id}', methods=['DELETE'], endpoint=self._create_endpoint_delete(), status_code=204)

    def _create_router(self):
        self.__router = APIRouter(prefix=f'/{self.name}')

        if self.list and self.list is not ...:
            self._create_route_list()

        if self.create and self.create is not ...:
            self._create_route_post()

        if self.get and self.get is not ...:
            self._create_route_get()

        if self.update and self.update is not ...:
            self._create_route_patch()
            self._create_route_put()

        if self.delete:
            self._create_route_delete()

    @property
    def router(self) -> APIRouter:
        if not self.__router:
            self._create_router()

        return self.__router


class ModelRouter(BaseRouter):
    __model: models.Model
    __router: APIRouter
    __schema: RouterSchema
    __security: Optional[SecurityBase]

    def __init_subclass__(cls, model: models.Model, router: APIRouter, schema: RouterSchema, security: Optional[SecurityBase] = None) -> None:
        cls.__model = model
        cls.__router = router
        cls.__schema = schema
        cls.__security = security

        super().__init_subclass__()

        cls.init_routes()

    @classmethod
    def _add_api_route(cls, path, func, method='GET', response_model=None):
        cls.__router.add_api_route(
            path,
            endpoint=_partial_with_description(func, cls),
            response_model=response_model,
            methods=[method],
            **getattr(func, 'route_options', {}),
        )

    @classmethod
    def init_routes(cls):
        pass
