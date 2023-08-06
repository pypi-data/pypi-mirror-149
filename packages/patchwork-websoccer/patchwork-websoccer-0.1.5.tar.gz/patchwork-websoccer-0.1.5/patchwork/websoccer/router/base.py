# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import Iterable, Union, Set, Dict

from patchwork.core import Task
from patchwork.websoccer.client.base import BaseClient


class BaseRouter:

    def __init__(self):
        self._routes: Dict[str, Set[BaseClient]] = defaultdict(set)
        self._client_map: Dict[BaseClient, Set[str]] = defaultdict(set)

    def add(self, route_id: str, client: BaseClient) -> Iterable[str]:
        """
        Adds route tied to given client.
        :param route_id:
        :param client:
        :return: list of queues which should be listen on to handle this route
        """
        created = route_id not in self._routes
        self._routes[route_id].add(client)
        self._client_map[client].add(route_id)

        if created:
            return self._get_route_queues(route_id)
        else:
            return []

    def remove(self, route_id: str, client: BaseClient) -> Iterable[str]:
        """
        Removes route tied to given client
        :param route_id:
        :param client:
        :return:
        """
        if route_id in self._routes and client in self._routes[route_id]:
            self._routes[route_id].remove(client)
            if route_id in self._client_map[client]:
                self._client_map[client].remove(route_id)

        if not self._client_map[client]:
            self._client_map.pop(client)

        if not self._routes[route_id]:
            # last client unsubscribed
            self._routes.pop(route_id)
            return self._get_route_queues(route_id)
        else:
            return []

    def get(self, client: BaseClient) -> Iterable[str]:
        return self._client_map.get(client, set())

    def route_task(self, task: Task) -> Union[Iterable[BaseClient], None]:
        raise NotImplementedError()

    def _get_route_queues(self, route_id: str) -> Iterable[str]:
        """
        Returns queues which should be listen on to handle the route
        :param route_id:
        :return:
        """
        raise NotImplementedError()


class TaskQueueRouter(BaseRouter):
    """
    Routes tasks to clients basing on task origin queue name.
    This router forwards tasks from Patchwork queues directly to external clients.
    """

    def __init__(self, name_format: str = '{}'):
        """
        Name format where {} will be replaced by client_id
        :param name_format:
        """
        super().__init__()
        self._fmt = name_format
        self._placeholder_pos = self._fmt.find('{}')
        assert self._placeholder_pos > -1, "missing client_id placeholder in queue name format"

    def _extract_route_id_from_queue(self, queue_name: str) -> str:
        return queue_name[self._placeholder_pos:-self._placeholder_pos-2]

    def _get_route_queues(self, route_id: str) -> Iterable[str]:
        return [self._fmt.format(route_id)]

    def route_task(self, task: Task) -> Union[Iterable[BaseClient], None]:
        queue_name = task.meta.queue_name
        if not queue_name:
            return None

        client_id = self._extract_route_id_from_queue(queue_name)
        if not client_id:
            return None

        clients = self._routes.get(client_id)
        if not clients:
            return None

        return clients
