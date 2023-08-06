# -*- coding: utf-8 -*-

import asyncio
import warnings
import weakref
from typing import Literal, Callable, Dict, List

import logging
from pydantic import ValidationError, BaseModel

from patchwork.core.utils import cached_property, Flag


class OrphanedComponent(RuntimeError):
    """
    Component which has parent defined becomes orphaned which means that parent has been destroyed.
    """
    pass


class Component:
    """
    A base class for every Patchwork component.
    """

    class Config(BaseModel):
        """
        Base settings class for all components

        :cvar enabled: determines if component is enabled or not
        """
        enabled: bool = True

    EVENTS = ('startup', 'shutdown')

    settings: Config
    logger_name: str
    state: Flag

    def __init__(self, *, parent=None, **options):
        """
        :param parent:  optional parent component
        :param options: component configuration which must conform `Settings` schema
        """
        if parent is not None:
            self._parent = weakref.ref(parent)

        try:
            self.settings = self.Config(**options)
        except ValidationError as e:
            from patchwork.core.config.base import ImproperlyConfigured
            raise ImproperlyConfigured(f"{self.__class__.__name__}: {e}\nsettings received: {options}") from e

        self.state = Flag(False)

        self._is_stopping: bool = False
        self._is_starting: bool = False

        self._event_handlers: Dict[str, List[Callable]] = {
            event_name: [] for event_name in self.EVENTS
        }

    def __repr__(self):
        state = 'running' if self.is_running else ('starting' if self.is_starting else (
            'stopping' if self.is_stopping else 'stopped'))
        return f"<Component {self.__class__.__name__}[{hex(id(self))}] {state}>"

    async def __aenter__(self):
        await self.run()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.terminate()

    @property
    def parent(self):
        """
        Returns parent instance
        :return:
        """
        if self._parent is None:
            return None

        parent = self._parent()
        if parent is None:
            raise OrphanedComponent("Parent instance gone! This component instance is orphaned and should be destroyed")

        return parent

    @property
    def is_running(self):
        """
        Tells if component is running
        :return: True if component is running, False otherwise
        """
        if not hasattr(self, 'state'):
            return False
        return self.state.value

    @property
    def is_starting(self):
        """
        Tells if component is starting
        :return: True if component is in the middle of starting process, False otherwise
        """
        return self._is_starting

    @property
    def is_stopping(self):
        """
        Tells if component is stopping
        :return: True if component is in the middle of stopping process, False otherwise
        """
        return self._is_stopping

    @cached_property
    def logger(self) -> logging.Logger:
        """
        Returns logger instance for the component
        :return:
        """
        return logging.getLogger(f'patchwork.{getattr(self, "logger_name", self.__class__.__name__.lower())}')

    def _add_event_handler(self, event: str, handler: Callable):
        if event not in self.EVENTS:
            raise ValueError(f'unknown event {event}')
        self._event_handlers[event].append(handler)

    async def _dispatch_event(self, event: str, **kwargs):
        assert event in self.EVENTS, "no such event to dispatch"
        for handler in self._event_handlers[event]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(**kwargs)
                else:
                    handler(**kwargs)
            except Exception as e:
                warnings.warn(f'event handler failed with exception: {e.__class__.__name__}({e})', RuntimeWarning)

    def on_event(self, event: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._add_event_handler(event, func)
            return func

        return decorator

    async def _start(self) -> bool:
        """
        Starts component internals. Implement this method in your component.

        !!! hint
            This method internally should handle all known or expected exceptions, make possible cleanup and
            return False. Raise exceptions from here only if error in unrecoverable (aka fatal)

        :return: True if startup succeed, False otherwise
        """
        # put custom startup code here, return from this method when all related objects are started and running
        # await if needed!
        pass

    async def run(self) -> bool:
        """
        Starts component

        !!! note
            If component is already started this method returns `False`!

        :return: True if has been started, False otherwise
        """
        if self.is_running:
            return False

        if not self.settings.enabled:
            self.logger.error("Can't start disabled component")
            raise RuntimeError("Module disabled")

        self._is_starting = True

        if await self._start() is False:
            self._is_starting = False
            return False

        await self._dispatch_event('startup')

        self.state.set(True)
        self._is_starting = False

        return True

    async def terminate(self) -> bool:
        """
        Stops component

        !!! note
            If the component is already stopped this method returns `False`!

        :return: True if has been stopped, False otherwise
        """
        if not self.is_running:
            return False

        self._is_stopping = True

        await self._dispatch_event('shutdown')

        if await self._stop() is False:
            self._is_stopping = False
            return False

        self.state.set(False)
        self._is_stopping = False
        return True

    async def _stop(self) -> bool:
        """
        Stops component internals. Implement this method in your component.

        !!! hint
            This method internally should handle all known or expected exceptions, make possible cleanup and
            return False. Raise exceptions from here only if error in unrecoverable (aka fatal)

        :return: True if stopping succeed, False otherwise
        """
        # put custom termination code here, return from this method when all related objects are STOPPED
        # await if needed!
        pass

    async def recover(self) -> bool:
        """
        Recover is called by parent component if this components terminates (it states change to False)
        unexpectedly become corrupted.

        If recovering is possible try to do that here, but remember that current state can be really
        *EVERYTHING*. If recovering fail or it's not possible return False.

        Return only when recovery procedure is fully completed or failed. Awaits on internal steps.
        :return:
        """
        return False
