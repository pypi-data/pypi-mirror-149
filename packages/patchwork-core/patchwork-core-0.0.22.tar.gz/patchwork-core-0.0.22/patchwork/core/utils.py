# -*- coding: utf-8 -*-

import asyncio
import collections


class cached_property:
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    A cached property can be made out of an existing method:
    (e.g. ``url = cached_property(get_absolute_url)``).
    """
    name = None

    @staticmethod
    def func(instance):
        raise TypeError(
            'Cannot use cached_property instance without calling '
            '__set_name__() on it.'
        )

    def __init__(self, func, name=None):

        func_name = func.__name__
        name = name or func_name
        if not (isinstance(name, str) and name.isidentifier()):
            raise ValueError(
                "%r can't be used as the name of a cached_property." % name,
            )

        self.name = name
        self.func = func
        self.__doc__ = getattr(func, '__doc__')

    def __set_name__(self, owner, name):
        if name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


class Flag:
    """
    Simple flag implementation, works like Event but allows to pass a value.
    Use wait() to wait for value change.
    """

    def __init__(self, initial_value=None, *, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._waiters = collections.deque()
        self._value = initial_value

    async def wait(self):
        """
        Waits for flag value change and returns new one.
        :return: flag value
        """
        f = self._loop.create_future()
        self._waiters.append(f)
        return await f

    async def wait_for(self, value):
        """
        Wait for given flag value
        :param value:
        :return:
        """
        if self._value == value:
            return

        while True:
            f = self._loop.create_future()
            self._waiters.append(f)
            res = await f
            if res == value:
                return

    def set(self, value):
        """
        Sets new flag value and notifies all waiters.
        :param value:
        :return:
        """
        if value == self._value:
            # setting to the same value is no-op
            return

        self._value = value

        # store current waiters and create new internal queue before resolving futures,
        # so if someone waits for certain value may safely re-append to waiters list
        waiters = self._waiters
        self._waiters = collections.deque()

        for f in waiters:
            if not f.cancelled():
                f.set_result(value)

    @property
    def value(self):
        """
        Gets current flag value
        :return:
        """
        return self._value

    def __repr__(self):
        res = super().__repr__()
        extra = repr(self._value)
        if self._waiters:
            extra = f'{extra}, waiters:{len(self._waiters)}'
        return f'<{res[1:-1]} [{extra}]>'


class AsyncQueue:
    """
    Async queue which works on events to block and await for empty slots or available data.
    These events are exposed so external code may check if there is a possibility to put or
    get data and await on their own.

    This is FIFO queue.

    Custom events exposed:
    - empty: set when queue becomes empty
    - nonempty: negation of empty, set when queue is not empty and has any data
    - full: set when queue becomes full and there is no free slots available
    - nonfull: negation of full, set when full is not empty and has free slots to put more data

    Interface is compatible with standard Python queues.

    """

    def __init__(self, maxsize=None):
        self.maxsize = maxsize

        self._items = collections.deque()
        self._putters = collections.deque()

        self.empty = asyncio.Event()
        self.nonempty = asyncio.Event()

        self.nonfull = asyncio.Event()
        self.full = asyncio.Event()

        self.empty.set()
        self.nonfull.set()

    def get_nowait(self):
        """
        Pops and returns item from the queue. If there is no item to return raises QueueEmpty exception
        like standard asyncio queue.
        :return:
        """
        if not self._items:
            raise asyncio.QueueEmpty()

        item = self._items.popleft()
        self.full.clear()
        self.nonfull.set()

        if not self._items:
            self.empty.set()
            self.nonempty.clear()

        return item

    def task_done(self):
        """
        Marks fetched task done.
        :return:
        """
        pass

    async def get(self, timeout: float = None):
        """
        Pops and returns item from the queue. If there is no items to return awaits for it.
        :return:
        """
        await asyncio.wait_for(self.nonempty.wait(), timeout=timeout)
        return self.get_nowait()

    async def put(self, item, timeout: float = None):
        """
        Put an item to the queue. If there are no free slots available awaits for it.
        :param item:
        :param timeout:
        :return:
        """
        await asyncio.wait_for(self.nonfull.wait(), timeout=timeout)
        return self.put_nowait(item)

    def put_nowait(self, item):
        """
        Put an item to the queue. If there is no free slots available raises QueueFull exception like
        standard asyncio queue.
        :param item:
        :return:
        """
        if len(self._items) == self.maxsize:
            raise asyncio.QueueFull()

        self._items.append(item)
        self.empty.clear()
        self.nonempty.set()

        if len(self._items) == self.maxsize:
            self.full.set()
            self.nonfull.clear()

    def revoke_nowait(self, item):
        self._items.remove(item)
        self.full.clear()
        self.nonfull.set()

        if not self._items:
            self.empty.set()
            self.nonempty.clear()

    def clear(self):
        """
        Clears the queue
        :return:
        """
        self._items.clear()
        self.full.clear()
        self.nonfull.set()
        self.nonempty.clear()
        self.empty.set()
