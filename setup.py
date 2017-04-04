try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


install_requires = [
    "datadog-logger",
    "datadog",
    "kubernetes"
]

setup(name="ustack-logging",
      version="0.2.0",
      description="Default logging configuration for uStack style Python applications.",
      url="https://github.com/ustudio/ustack-logging",
      packages=["ustack_logging"],
      install_requires=install_requires)
