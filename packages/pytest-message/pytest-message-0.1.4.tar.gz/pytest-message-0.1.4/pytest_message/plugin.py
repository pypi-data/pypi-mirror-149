from _pytest.config import Config

from pytest_message.notifier import NotifyPlugin


def pytest_addoption(parser):
    group = parser.getgroup('notifying')
    group.addoption(
        '--notify',
        action='store_true',
        dest='notify_enabled',
        default=False,
        help='Enable Notifier plugin'
    )


def pytest_configure(config: Config):
    if config.option.notify_enabled:
        config.notification_service = NotifyPlugin()
        if hasattr(config, 'notification_service'):
            config.pluginmanager.register(config.notification_service)
