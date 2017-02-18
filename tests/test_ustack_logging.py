import logging
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from ustack_logging.logging_configuration import configure_logging


class TestLogging(unittest.TestCase):
    @mock.patch("ustack_logging.logging_configuration.log_error_events", autospec=True)
    @mock.patch("kubernetes_downward_api.parse", autospec=True)
    @mock.patch("datadog.initialize", autospec=True)
    @mock.patch("logging.basicConfig", autospec=True)
    def test_configures_logging_format_and_logs_errors_to_datadog(
            self, mock_log_config, mock_dd_init, mock_k8s_parse, mock_log_errors):
        mock_k8s_parse.return_value = {
            "namespace": "dev",
            "labels": {
                "app": "my_app",
                "role": "app"
            }
        }

        configure_logging({
            "DATADOG_API_KEY": "dd-api-key",
            "DATADOG_APP_KEY": "dd-app-key"
        })

        mock_log_config.assert_called_once_with(
            format="%(asctime)s %(levelname)s:%(module)s:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.INFO)

        mock_dd_init.assert_called_once_with(api_key="dd-api-key", app_key="dd-app-key")

        mock_k8s_parse.assert_called_once_with(["/etc/podinfo"])
        mock_log_errors.assert_called_once_with(
            tags=["environment:dev", "service:my_app", "role:app"])

    @mock.patch("ustack_logging.logging_configuration.log_error_events", autospec=True)
    @mock.patch("kubernetes_downward_api.parse", autospec=True)
    @mock.patch("datadog.initialize", autospec=True)
    @mock.patch("logging.basicConfig", autospec=True)
    def test_ignores_errors_from_datadog_initialization(
            self, mock_log_config, mock_dd_init, mock_k8s_parse, mock_log_errors):
        mock_k8s_parse.return_value = {
            "namespace": "dev",
            "labels": {
                "app": "my_app",
                "role": "app"
            }
        }

        mock_dd_init.side_effect = RuntimeError

        configure_logging({
            "DATADOG_API_KEY": "dd-api-key",
            "DATADOG_APP_KEY": "dd-app-key"
        })

        mock_log_config.assert_called_once_with(
            format="%(asctime)s %(levelname)s:%(module)s:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.INFO)
