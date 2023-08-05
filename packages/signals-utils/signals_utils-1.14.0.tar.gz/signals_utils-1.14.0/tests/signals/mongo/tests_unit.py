from unittest.case import TestCase

from mock.mock import patch
from mongoengine import signals

from signals_utils.commons import exceptions
from signals_utils.signals.mongo import connector
from signals_utils.signals.mongo import decorator


class TestConnectorConnect(TestCase):
    @patch.object(signals.post_save, "connect")
    def test_connect_raises_signals_error_if_bad_connection(self, mock_connect):
        # Arrange
        mock_connect.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(exceptions.SignalsError):
            connector.connect(object, signals.post_save, self)

    @patch.object(signals.post_save, "connect")
    def test_decorator_raises_signals_error_if_bad_connection(self, mock_connect):
        # Arrange
        mock_connect.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(exceptions.SignalsError):
            decorated_func = decorator.receiver(signals.post_save, self)
            decorated_func(object)
