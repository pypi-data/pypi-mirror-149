# -*- coding: utf-8 -*-
from typing import Union, Iterable, Mapping


class ClientSession:

    AUTH_ID_FIELD = 'auth_id'

    def __init__(self, initial: Mapping = None):
        self._data = dict(initial or {})

    def is_anonymous(self):
        return self.auth_id is None

    @property
    def auth_id(self):
        try:
            return self[self.AUTH_ID_FIELD]
        except KeyError:
            return None

    @auth_id.setter
    def auth_id(self, value):
        self[self.AUTH_ID_FIELD] = value

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, item):
        return self._data[item]

    def __contains__(self, item):
        return item in self._data

    def update(self, data: Mapping):
        self._data.update(data)


class BaseClient:

    def __init__(self):
        self._court: Union['patchwork.websoccer.court.base.BaseCourt', None] = None
        self.session = ClientSession()

    async def connect(self, court):
        assert self._court is None
        self._court = court

    async def disconnect(self, court):
        self._court = None

    async def subscribe(self, route_id: Iterable[str]):
        await self._court.add_route(route_id, self)

    async def unsubscribe(self, route_id: Iterable[str]):
        await self._court.remove_route(route_id, self)

    async def subscription(self) -> Iterable[str]:
        return self._court.get_routes(self)

    async def listen(self):
        raise NotImplementedError()

    async def send(self, data: bytes):
        raise NotImplementedError()
