# -*- coding: utf-8 -*-
import logging
from typing import Callable, Mapping, Union, Coroutine, Any

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from patchwork.websoccer.client.base import BaseClient
from patchwork.websoccer.client.websock import WebsockClient
from patchwork.websoccer.court.base import BaseCourt

logger = logging.getLogger('patchwork.websoccer.fastapi')


def noop_authorizer():
    return None


DataHandler = Callable[[Union[str, bytes], BaseClient], Coroutine[Any, Any, Union[str, bytes, None]]]


class StarletteWebsockClient(WebsockClient):

    _sock: WebSocket

    def __init__(self, handler: DataHandler, **kwargs):
        super().__init__(**kwargs)
        self._handler = handler

    async def get(self) -> Union[bytes, str]:
        try:
            return await super().get()
        except WebSocketDisconnect:
            raise EOFError()

    async def handle(self, data: Union[bytes, str]):
        response = await self._handler(data, self)
        if response is None:
            return

        await self.send(response)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self._sock.client.host}:{self._sock.client.port}>"


def bind_fastapi(
        court: BaseCourt,
        handler: DataHandler,
        authorizer: Callable = None,
        binary_mode: bool = False
):
    """
    Binds court instance to the FastAPI, by returning a router which can be easily included
    at desired path.
    Optional authorizer is a FastAPI dependency which is called to determine if incoming connection
    is authorized. For unauthorized users it must raise exception.

    :param court:
    :param authorizer:
    :param handler:
    :param binary_mode:
    :return:
    """
    router = APIRouter()

    if authorizer is None:
        authorizer = noop_authorizer

    @router.get('')
    async def describe():
        """
        Returns available transports with their locations
        :return:
        """
        return {
            'endpoints': {
                'websocket': '/ws'
            }
        }

    @router.websocket('/ws')
    async def websocket(websocket: WebSocket, auth: Mapping = Depends(authorizer)):
        await websocket.accept()
        logger.info(f"{websocket.client}: websocket client accepted")
        client = StarletteWebsockClient(handler=handler, sock=websocket, binary=binary_mode)

        if auth is not None:
            client.session.update(auth)

        await court.client(client)

        logger.info(f"{websocket.client}: connection closed")

    # TODO: add SSE endpoint
    # TODO: add HTTP poll endpoint

    @router.on_event('startup')
    async def run_websoccer():
        await court.run()

    @router.on_event('shutdown')
    async def stop_websoccer():
        await court.terminate()

    logger.info("Websoccer court initialized for FastAPI")

    # include router to your FastAPI application
    return router
