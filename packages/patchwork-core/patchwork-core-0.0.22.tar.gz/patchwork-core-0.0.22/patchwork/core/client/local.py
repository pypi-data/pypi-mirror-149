# -*- coding: utf-8 -*-

import asyncio
import warnings
from collections import defaultdict, deque
from enum import IntEnum
from typing import List, Dict, Any, AsyncGenerator, Iterable, TypeVar, Generic, Tuple, Mapping

from .base import SynchronousPublisher, SynchronousSubscriber, AsyncPublisher, AsyncSubscriber


class SyncLocalPublisher(SynchronousPublisher):
    """
    Patchwork is asynchronous framework with fully async nodes, so locally async Python must be supported
    to run the worker. Synchronous client make no sense in that case.
    """
    def __init__(self):
        raise NotImplementedError("There is no synchronous local client")


class SyncLocalSubscriber(SynchronousSubscriber):
    """
    Patchwork is asynchronous framework with fully async nodes, so locally async Python must be supported
    to run the worker. Synchronous client make no sense in that case.
    """
    def __init__(self):
        raise NotImplementedError("There is no synchronous local client")


class DummySerializer:

    @classmethod
    def dumps(cls, data):
        return data

    @classmethod
    def loads(cls, data):
        return data


class MissingBehaviour(IntEnum):
    # skip missing queue
    SKIP = 0
    # warn that queue is missing and skip
    WARN = 1
    # create missing queue
    CREATE = 2
    # raise with ValueError exception
    EXCEPTION = 3
    # wait until queue will be created by another code
    WAIT = 4


class DROP:
    pass


T = TypeVar('T')


class Topic(Generic[T]):
    """
    A queue implementation similar to asyncio one, but works with multiple asyncio loops as queue itself
    is not bound to any loop
    """

    def __init__(self, maxsize: int = None):
        self._queue = deque(maxlen=maxsize)
        self._get_waiters = deque()
        self._put_waiters = deque()
        self._unfinished_tasks = 0

    def qsize(self):
        return len(self._queue)

    def get_nowait(self) -> T:
        item = self._queue.popleft()
        self._unfinished_tasks += 1
        if self._put_waiters:
            self._put_waiters.popleft().set()

        return item

    def put_nowait(self, item: T):
        self._queue.append(item)
        if self._get_waiters:
            self._get_waiters.popleft().set()

    async def get(self) -> T:
        if self._queue:
            return self.get_nowait()

        event = asyncio.Event()
        self._get_waiters.append(event)
        try:
            await event.wait()
        except asyncio.CancelledError:
            self._get_waiters.remove(event)
            raise

        return await self.get()

    async def put(self, item: T):
        if len(self._queue) < self._queue.maxlen:
            return self.put_nowait(item)

        event = asyncio.Event()
        self._put_waiters.append(event)
        try:
            await event.wait()
        except asyncio.CancelledError:
            self._put_waiters.remove(event)
            raise

        return await self.put(item)

    def task_done(self):
        if self._unfinished_tasks == 0:
            raise ValueError()
        self._unfinished_tasks -= 1


class AsyncLocalBroker:
    """
    Simple local broker working on asyncio loop for testing and development purposes only.

    !!! danger
        For development purposes only!
    """

    __default = []

    def __init__(
            self,
            initial_queues: Iterable[str] = tuple(),
            publish_missing: MissingBehaviour = MissingBehaviour.CREATE,
            subscribe_missing: MissingBehaviour = MissingBehaviour.WAIT,
            max_queue_size: int = 100
    ):
        self._queues: Dict[str, Topic] = {}
        self._publish_missing = publish_missing
        self._subscribe_missing = subscribe_missing
        self._queue_size = max_queue_size

        self._missing_notif: Dict[str, List[asyncio.Event]] = defaultdict(list)

        for q_name in initial_queues:
            self._create_queue(q_name)

    @classmethod
    def default(cls):
        if not cls.__default:
            cls.__default.append(cls())

        return cls.__default[0]

    def _create_queue(self, name):
        self._queues[name] = Topic(maxsize=self._queue_size)
        if name in self._missing_notif:
            for n in self._missing_notif.pop(name):
                n.set()

    def get_queue(self, name: str) -> Topic:
        return self._queues[name]

    def has_queue(self, name: str) -> bool:
        return name in self._queues

    async def put(self, msg: Any, *, queue_name: str):
        if queue_name not in self._queues:
            if self._publish_missing == MissingBehaviour.SKIP:
                return
            elif self._publish_missing == MissingBehaviour.WARN:
                warnings.warn(
                    f'{self.__class__.__name__}: unable to deliver message to queue {queue_name}: no such queue'
                )
                return
            elif self._publish_missing == MissingBehaviour.CREATE:
                self._create_queue(queue_name)
            elif self._publish_missing == MissingBehaviour.WAIT:
                await self._missing_created(queue_name)
            else:
                raise ValueError(f'{queue_name}: no such queue')

        await self._queues[queue_name].put(msg)

    def _missing_created(self, queue_name):
        event = asyncio.Event()
        self._missing_notif[queue_name].append(event)

        async def notifier():
            await event.wait()
            return DROP
        return notifier()

    async def subscribe(self, queue_names: List[str]) -> AsyncGenerator:
        if not queue_names:
            return

        waiters: Dict[asyncio.Task, str] = {}

        for queue_name in queue_names:
            if queue_name not in self._queues:
                if self._subscribe_missing == MissingBehaviour.SKIP:
                    return
                elif self._subscribe_missing == MissingBehaviour.WARN:
                    warnings.warn(
                        f'{self.__class__.__name__}: unable to subscribe on queue {queue_name}: no such queue')
                    return
                elif self._subscribe_missing == MissingBehaviour.CREATE:
                    self._create_queue(queue_name)
                elif self._subscribe_missing == MissingBehaviour.WAIT:
                    waiters[asyncio.create_task(self._missing_created(queue_name))] = queue_name
                else:
                    raise ValueError(f'{queue_name}: no such queue')
            else:
                waiters[asyncio.create_task(self._queues[queue_name].get())] = queue_name

        while True:
            try:
                done, pending = await asyncio.wait(waiters.keys(), return_when=asyncio.FIRST_COMPLETED)

                for fut in done:
                    # remove resolved future from dict, get associated queue name
                    q_name = waiters.pop(fut)
                    # create new waiter task for this queue name
                    waiters[asyncio.create_task(self._queues[q_name].get())] = q_name
                    # yield fetched value
                    result = fut.result()
                    if result is not DROP:
                        yield result, q_name
                        self._queues[q_name].task_done()
            except asyncio.CancelledError:
                for w in waiters.keys():
                    if not w.done():
                        w.cancel()
                raise
            except GeneratorExit:
                for w in waiters.keys():
                    w.cancel()

                return

    def __str__(self):
        return f'<{self.__class__.__name__}: {", ".join(self._queues.keys())}>'


class AsyncLocalPublisher(AsyncPublisher):
    """
    Simple patchwork client working on local event loop using given local broker

    !!! danger
        For development purposes only!
    """

    def __init__(self, parent=None, broker: AsyncLocalBroker = None, **options):
        """
        :param queue:   asyncio queue to bind to
        """
        super().__init__(parent=parent, **options)
        if broker is None:
            broker = AsyncLocalBroker.default()

        self._broker = broker

    def __repr__(self):
        res = super().__repr__()
        return f"<{res[1:-1]}, broker={self._broker}]>"

    @property
    def broker(self):
        return self._broker

    async def _start(self):
        self.logger.debug(f"Publisher attached to broker {self._broker}")

    async def _stop(self):
        self.logger.debug(f"Publisher left broker {self._broker}")

    async def _send(self, payload, task, timeout: float = None):
        assert task.meta.queue_name, "missing task queue name"
        try:
            if timeout == 0:
                await self._broker.put(payload, queue_name=task.meta.queue_name)
            else:
                await asyncio.wait_for(self._broker.put(payload, queue_name=task.meta.queue_name), timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"send operation timeout, can't deliver in {timeout}s")


class AsyncLocalSubscriber(AsyncSubscriber):

    class Config(AsyncSubscriber.Config):
        queue_names: List[str] = []

    def __init__(self, parent=None, broker: AsyncLocalBroker = None, **options):
        """
        :param queue:   asyncio queue to bind to
        """
        if broker is None:
            broker = AsyncLocalBroker.default()

        self._broker = broker
        super().__init__(parent=parent, **options)
        self.uncommitted = set()
        self._fetcher: AsyncGenerator

    def __repr__(self):
        res = super().__repr__()
        return f"<{res[1:-1]}, broker={self._broker}]>"

    @property
    def broker(self):
        return self._broker

    async def _start(self):
        self.logger.debug(f"Subscriber attached to broker {self._broker}")
        if not self.settings.queue_names:
            warnings.warn(f'{self.__class__.__name__}: no queues to listen on')
        self._fetcher = self._broker.subscribe(self.settings.queue_names)

    async def _stop(self):
        await self._fetcher.aclose()
        self.logger.debug(f"Subscriber left broker {self._broker}")

    async def _fetch_one(self, timeout: float = None) -> Tuple[bytes, Mapping]:
        try:
            data, q_name = await asyncio.wait_for(self._fetcher.__anext__(), timeout=timeout)
            return data, {'queue_name': q_name}
        except AttributeError:
            if not hasattr(self, '_fetcher'):
                raise RuntimeError(
                    "Can't fetch task: subscriber seems to be not started. "
                    "Did you forgot to call run() method and await?"
                )
            raise
        except asyncio.TimeoutError:
            raise TimeoutError(f"fetch operation timeout, no messages in {timeout}s")

    async def commit(self, task, *, timeout: float = None):
        self.uncommitted.remove(task.uuid)

    async def rollback(self, task, *, timeout: float = None):
        pass

    async def get(self, *, timeout: float = None):
        task = await super().get(timeout=timeout)
        self.uncommitted.add(task.uuid)
        return task

    async def subscribe(self, queue_name: Iterable[str]):
        raise NotImplementedError('changing subscription on local client is not supported')

    async def unsubscribe(self, queue_name: Iterable[str]):
        raise NotImplementedError('changing subscription on local client is not supported')

    def subscription(self) -> Iterable[str]:
        return self.settings.queue_names
