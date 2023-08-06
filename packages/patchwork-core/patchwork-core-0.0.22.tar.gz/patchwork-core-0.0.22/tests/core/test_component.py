# -*- coding: utf-8 -*-

import asyncio

import logging
import pytest
from unittest.mock import patch, AsyncMock

from patchwork.core import Component, OrphanedComponent


class Parent:
    pass


@pytest.fixture
def parent():
    return Parent()


def test_parent():

    parent = Parent()
    cmp = Component(parent=parent)
    assert parent == cmp.parent

    del parent
    with pytest.raises(OrphanedComponent):
        _ = cmp.parent


@pytest.mark.asyncio
async def test_start_procedure(parent):
    cmp = Component(parent=parent)

    with patch.object(cmp, '_start', new_callable=AsyncMock) as setup_mock:
        assert await cmp.run()

        setup_mock.assert_called()
        assert cmp.is_running

        setup_mock.reset_mock()
        assert not await cmp.run(), \
            "Starting already running component should return False"

        assert not setup_mock.called, \
            "Start method called on running component should not invoke _start()"


@pytest.mark.asyncio
async def test_stop_procedure(parent):

    cmp = Component(parent=parent)

    # inject running state
    cmp.state.set(True)

    with patch.object(cmp, '_stop', new_callable=AsyncMock) as teardown_mock:
        assert await cmp.terminate()

        teardown_mock.assert_called()
        assert not cmp.is_running

        teardown_mock.reset_mock()
        assert not await cmp.terminate(), \
            "Stopping not running component should return False"

        assert not teardown_mock.called, \
            "Stop method called on not running component should not invoke _stop()"


@pytest.mark.asyncio
async def test_state_flag_changes(parent, event_loop):

    cmp = Component(parent=parent)
    callback_got = None

    async def callback():
        nonlocal callback_got
        state = await cmp.state.wait()
        callback_got = state

    t = event_loop.create_task(callback())
    await asyncio.wait((cmp.run(), t))

    assert callback_got, \
        "Flag wait() should return True which is running component state"
    callback_got = None

    t = event_loop.create_task(callback())
    await asyncio.wait((cmp.terminate(), t))

    assert not callback_got, \
        "Flag wait() should return False which is not running component state"


@pytest.mark.asyncio
async def test_cant_run_disabled(parent, suppress_logging):

    cmp = Component(parent=parent, enabled=False)

    with pytest.raises(RuntimeError), suppress_logging(max_level=logging.ERROR):
        await cmp.run()
