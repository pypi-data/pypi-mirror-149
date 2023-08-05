import dataclasses
import datetime
import logging
from typing import Any, List

from _pytest.reports import TestReport
from slack_sdk import WebClient, errors

from pytest_message.listeners.listiner import Listener


__all__ = ['SlackListener']


@dataclasses.dataclass
class Status:
    total: int
    passed: int
    failed: int
    skipped: int


DIVIDER = {
    "type": "divider"
}

MAX_TEXT_ERROR_SIZE = 1000


class SlackListener(Listener):
    def __init__(self, token: str, chat: str):
        self.state = []
        self._client = self.configure(token)
        self._chat = chat

    @staticmethod
    def configure(token: str) -> WebClient:
        return WebClient(token=token)

    def update(self, data: Any) -> None:
        self.state.append(data)

    def finish(self) -> None:
        title = f'Test report result - {datetime.datetime.now().ctime()}'
        blocks = [self._get_heading_block(title)]
        for func_name, report in self.state:
            blocks.extend(self._prepare_test_report_block(func_name, report))
            blocks.append(DIVIDER)

        try:
            self._client.chat_postMessage(channel=self._chat, text=title, blocks=blocks)
        except errors.SlackApiError as e:
            logging.warning(str(e))

    @staticmethod
    def _get_heading_block(heading: str) -> dict:
        return {
                   "type": "header",
                   "text": {
                       "type": "plain_text",
                       "text": heading
                   }
               }

    def _prepare_test_report_block(self, func_name: str, reports: List[TestReport]) -> List[dict]:
        status, errors = self._get_test_info(reports)

        out = [self._create_testfunc_header_block(status, func_name)]
        out.extend(self._create_testfunc_report_blocks(errors))

        return out

    @staticmethod
    def _get_test_info(reports: List[TestReport]):
        total = len(reports)
        passed = 0
        failed = 0
        skipped = 0
        errors = []

        for report in reports:
            if report.outcome == 'skipped':
                skipped += 1
            elif report.outcome == 'passed':
                passed += 1
            elif report.outcome == 'failed':
                failed += 1
                errors.append(report.longrepr.reprcrash.message)

        return Status(total, passed, failed, skipped), errors

    def _create_testfunc_header_block(self, status: Status, header) -> dict:

        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*{header}*"
                },
                {
                    "type": "mrkdwn",
                    "text": self._create_testfunc_status_msg(status)
                }
            ]
        }

    def _create_testfunc_status_msg(self, status: Status) -> str:
        if status.total == 1:
            if status.failed:
                return ":red_circle: *Failed*"
            if status.passed:
                return ':large_green_circle: *Passed*'
            if status.skipped:
                return ':white_circle: *Skipped*'
        return self._format_parametrized_report(status)

    @staticmethod
    def _format_parametrized_report(status):
        msg = []
        if status.passed:
            msg.append(f':large_green_circle: *Passed*: {status.passed}')
        if status.failed:
            msg.append(f':red_circle: *Failed*: {status.failed}')
        if status.skipped:
            msg.append(f':white_circle: *Skipped*: {status.skipped}')
        return '\n'.join(msg)

    @staticmethod
    def _create_testfunc_report_blocks(errors: List[str]) -> List[dict]:
        """Creates blocks list for error messages"""
        out = []
        for error in errors:
            if len(error) > MAX_TEXT_ERROR_SIZE:
                error = error[:MAX_TEXT_ERROR_SIZE] + "...."

            out.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'```{error}```'
                }
            })
        return out
