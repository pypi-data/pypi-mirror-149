# -*- coding: utf-8 -*-
import logging

from secrets import token_urlsafe
from typing import Protocol, Union

from patchwork.websoccer.client.base import BaseClient


logger = logging.getLogger('patchwork.websoccer.client')


class WebsockProtocol(Protocol):

    async def receive_bytes(self) -> bytes:
        pass

    async def send_bytes(self, data: bytes):
        pass

    async def receive_text(self) -> str:
        pass

    async def send_text(self, data: str):
        pass

    async def close(self, code: int):
        pass


class WebsockClient(BaseClient):

    def __init__(self, sock: WebsockProtocol, binary: bool):
        super().__init__()
        self._id = token_urlsafe(16)
        self._binary = binary
        self._sock = sock

    @property
    def session_id(self):
        return self._id

    async def get(self) -> Union[bytes, str]:
        if self._binary:
            return await self._sock.receive_bytes()
        else:
            return await self._sock.receive_text()

    async def listen(self):
        while True:
            try:
                data = await self.get()
            except EOFError:
                logger.debug(f"{self}: connection closed, get returned EOF")
                break

            try:
                await self.handle(data)
            except PermissionError:
                logger.info(f"{self}: connection closed, operation not permitted")
                await self._sock.close(code=1008)
                break
            except ValueError as e:
                logger.info(f"{self}: unprocessable request: {e}")
                await self._sock.close(code=1007)
                break
            except Exception as e:
                logger.warning(f"{self}: request handler failed: {e.__class__.__name__}({e})")
                await self._sock.close(code=1011)
                break

    async def send(self, data: Union[bytes, str]):
        if self._binary:
            if isinstance(data, str):
                raise ValueError('Unable to send text data over binary socket')
            await self._sock.send_bytes(data)
        else:
            if isinstance(data, bytes):
                raise ValueError('Unable to send binary data over text socket')
            await self._sock.send_text(data)

    async def handle(self, data: Union[bytes, str]):
        raise NotImplementedError()
