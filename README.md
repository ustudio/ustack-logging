# ustack-logging

Default logging configuration for uStack style Python applications.

## Installation ##

```
pip install ustack-logging
```

## Usage ##

```python
import os
from ustack_logging.logging_configuration import configure_logging


def main():
    configure_logging(os.environ)

    # Run your application


if __name__ == "__main__":
    main()
```

## Intent ##

This library is intended to codify the standard way uStudio Python
applications log and report errors when running inside Kubernetes. It
takes no configuration because its intent is to enforce a
configuration.

However, it is built on separate libraries that *are* configurable:
[datadog-logger](https://github.com/ustudio/datadog-logger) and
[kubernetes-downward-api](https://github.com/ustudio/kubernetes-downward-api). If
you need a different configuration, it should be trivial to implement
it using those libraries.

## Configuration ##

The library configures the following things:

It sets up the logging library to log the time, log level, module name
and log message for every message, and it sets the current log level
to `INFO`.

It connects to Datadog using the environment variables
`DATADOG_API_KEY` and `DATADOG_APP_KEY`, and parses the Kubernetes
namespace and labels out of a Kubernetes Downward API VolumeMount at
`/etc/podinfo`.

If the environment variables are not set (or are incorrect) or the
Downward API VolumeMount isn't available it logs a warning and does
not error.

It configures the `datadog-logger` library to send `ERROR` and above
log messages to Datadog as events, with the following tag mapping:

* K8s Namespace -> Datadog tag `environment`
* K8s Pod Label `app` -> Datadog tag `service`
* K8s Pod Label `role` -> Datadog tag `role`
