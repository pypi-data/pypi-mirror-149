from typing import Optional, Union, Iterable

import pytest
from _pytest.config import ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.runner import CallInfo

from pytest_message.listeners.listiner import Listener


def notify(listeners: Iterable[Listener]):
    return pytest.mark.notifiable(listeners=listeners)


class NotifyPlugin(object):
    def __init__(self):
        self._test_items = {}
        self._listeners = set()

    def pytest_runtest_protocol(self, item: Item, nextitem: Optional[Item]):
        marker = self.notifiable_marker(item)
        if item.originalname not in self._test_items and marker:
            [self._listeners.add(x) for x in marker.kwargs['listeners']]
            self._test_items[item.originalname] = (marker.kwargs['listeners'], [])

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item: Item, call: CallInfo[None]):
        result = (yield).get_result()
        if self._test_items.get(item.originalname):
            if result.outcome == 'skipped':
                self.add_report(item.originalname, result)
            if call.when == 'call':
                self.add_report(item.originalname, result)

    # Todo: Extract to DTO
    def add_report(self, func_name: str, result):
        self._test_items.get(func_name)[1].append(result)

    @staticmethod
    def notifiable_marker(item: Item):
        for marker in item.own_markers:
            if marker.name == 'notifiable':
                return marker

    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]):

        for func_name, notify_data in self._test_items.items():
            listeners, report_data = notify_data
            for listener in listeners:
                listener.update((func_name, report_data))

        for item in self._listeners:
            item.finish()
