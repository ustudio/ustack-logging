from collections.abc import Mapping
from typing import AnyStr


class V1Secret:
    data: Mapping[str, str]

    def __init__(self, data: Mapping[str, AnyStr]) -> None:
        ...


class V1ObjectMeta:
    labels: Mapping[str, str]

    def __init__(self, labels: Mapping[str, str]) -> None:
        ...


class V1Pod:
    metadata: V1ObjectMeta

    def __init__(self, metadata: V1ObjectMeta) -> None:
        ...


class CoreV1Api:
    def __init__(self) -> None:
        ...

    def read_namespaced_secret(self, secretName: str, namespaceName: str) -> V1Secret:
        ...

    def read_namespaced_pod(self, podName: str, namespaceName: str) -> V1Pod:
        ...
