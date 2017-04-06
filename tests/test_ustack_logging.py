import base64
import logging
import unittest

from kubernetes.client import V1Secret, V1Pod, V1ObjectMeta

try:
    from unittest import mock
except ImportError:
    import mock

from ustack_logging.logging_configuration import configure_logging


class TestLogging(unittest.TestCase):
    @mock.patch("socket.gethostname")
    @mock.patch("kubernetes.config.load_incluster_config")
    @mock.patch("kubernetes.client.CoreV1Api")
    @mock.patch("ustack_logging.logging_configuration.log_error_events", autospec=True)
    @mock.patch("datadog.initialize", autospec=True)
    @mock.patch("logging.basicConfig", autospec=True)
    def test_configures_logging_format_and_logs_errors_to_datadog(
            self, mock_log_config, mock_dd_init, mock_log_errors, mock_k8s_api_class,
            mock_k8s_config, mock_gethostname):

        mock_k8s_api = mock_k8s_api_class.return_value

        mock_gethostname.return_value = "podname.domain"

        mock_k8s_api.read_namespaced_secret.return_value = V1Secret(
            data={
                "environment": base64.b64encode("dev".encode("utf8")),
                "datadog-api-key": base64.b64encode("dd-api-key".encode("utf8")),
            })
        mock_k8s_api.read_namespaced_pod.return_value = V1Pod(
            metadata=V1ObjectMeta(labels={
                "role": "my-role"
            }))

        with mock.patch(
                "ustack_logging.logging_configuration.open",
                mock.mock_open(read_data="my-app"),
                create=True) as mock_open:
            configure_logging()

        mock_log_config.assert_called_once_with(
            format="%(asctime)s %(levelname)s:%(module)s:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.INFO)

        mock_k8s_config.assert_called_once_with()

        mock_k8s_api.read_namespaced_secret.assert_called_once_with(
            "environment-info", "ustudio-system")

        mock_dd_init.assert_called_once_with(api_key="dd-api-key")

        mock_open.assert_called_once_with("/var/run/secrets/kubernetes.io/serviceaccount/namespace")

        mock_gethostname.assert_called_once_with()

        mock_k8s_api.read_namespaced_pod.assert_called_once_with("podname", "my-app")

        mock_log_errors.assert_called_once_with(
            tags=["environment:dev", "service:my-app", "role:my-role"])

    @mock.patch("kubernetes.config.load_incluster_config")
    @mock.patch("logging.basicConfig", autospec=True)
    def test_ignores_errors_from_datadog_initialization(self, mock_log_config, mock_k8s_config):

        mock_k8s_config.side_effect = RuntimeError

        configure_logging()

        mock_log_config.assert_called_once_with(
            format="%(asctime)s %(levelname)s:%(module)s:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.INFO)
