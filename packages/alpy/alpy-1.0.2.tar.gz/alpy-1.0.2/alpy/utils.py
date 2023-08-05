# SPDX-License-Identifier: GPL-3.0-or-later

"""This module contains miscellaneous functions which do not fit into other
modules."""

import contextlib
import logging
import signal


def configure_logging(stderr_level=logging.INFO):
    """Configure logging.

    Write messages of :ref:`severity <python:levels>` *stderr_level* or higher
    to stderr. Write all messages to file "debug.log".

    :param stderr_level: severity for handler that writes to stderr
    :type stderr_level: int
    """
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(
        fmt="{levelname:8} {name:22} {message}", style="{"
    )
    stream_handler.setLevel(stderr_level)
    stream_handler.setFormatter(stream_formatter)

    file_handler = logging.FileHandler("debug.log", mode="w")
    file_formatter = logging.Formatter(
        fmt="{relativeCreated:7.0f} {levelname:8} {name:22} {message}",
        style="{",
    )
    file_handler.setFormatter(file_formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)


@contextlib.contextmanager
def context_logger(logger, description):
    # pylint: disable=missing-yield-doc,missing-yield-type-doc
    """Log context enter and exit events.

    On entering the context the manager writes *description* plus "..." using
    the given *logger*.

    On exiting the context the manager logs success if there was no exeption
    and failure if there was an exception.

    Example::

       logger = logging.getLogger("cooking")

       with context_logger(logger, "Add water"):
           print("Adding two cups of water")

       with context_logger(logger, "Add rice"):
           print("Adding a cup of rice")
           raise RuntimeError("Not enough rice")

    Example logs:

    .. code:: text

       INFO:cooking:Add water...
       Adding two cups of water
       INFO:cooking:Add water... done
       INFO:cooking:Add rice...
       Adding a cup of rice
       ERROR:cooking:Add rice... failed

    :param logger: logger
    :type logger: :py:class:`python:logging.Logger`
    :param description: short description of the next block
    :type description: str
    """

    logger.info(description + "...")
    try:
        yield
    except:
        logger.error(description + "... failed")
        raise
    logger.info(description + "... done")


def make_context_logger(logger):
    """Make context manager for logging context enter and exit events.

    See :py:func:`alpy.utils.context_logger`.

    :param logger: logger
    :type logger: :py:class:`python:logging.Logger`
    :return: function which makes context manager for logging context enter
        and exit events. The function accepts one parameter - *description*
        (:py:class:`python:str`).
    :rtype: :std:term:`python:function`
    """
    return lambda description: context_logger(logger, description)


class NonZeroExitCode(Exception):
    """Process exited with non-zero exit code."""


def signal_name(signal_number):
    """Get signal name.

    Example::

       signal_name(9) == "SIGKILL"

    :param signal_number: signal number
    :type signal_number: int
    :return: signal name
    :rtype: str
    """
    # See "false-positive on non-private Enum module members. Issue #2804.
    # PyCQA/pylint. GitHub. https://github.com/PyCQA/pylint/issues/2804
    return signal.Signals(signal_number).name  # pylint: disable=no-member


@contextlib.contextmanager
def print_test_result():
    """On exiting the context this context manager logs test success if there
    was no exeption in this context and logs test failure if there was an
    exception.

    Example::

       with print_test_result():
           print("Adding two cups of water")

       with print_test_result():
           print("Adding a cup of rice")
           raise RuntimeError("Not enough rice")

    Example logs:

    .. code:: text

       Adding two cups of water
       INFO:alpy.utils:Test passed
       Adding a cup of rice
       ERROR:alpy.utils:Test failed
    """
    logger = logging.getLogger(__name__)
    try:
        yield
    except:
        logger.error("Test failed")
        raise
    logger.info("Test passed")


@contextlib.contextmanager
def trace_test_environment():
    """On exiting the context this context manager logs success if there was no
    exeption in this context and logs failure if there was an exception.

    Example::

       with trace_test_environment():
           print("Adding two cups of water")

       with trace_test_environment():
           print("Adding a cup of rice")
           raise RuntimeError("Not enough rice")

    Example logs:

    .. code:: text

       INFO:alpy.utils:Enter test environment
       Adding two cups of water
       INFO:alpy.utils:Exit test environment with success
       INFO:alpy.utils:Enter test environment
       Adding a cup of rice
       ERROR:alpy.utils:Exit test environment with failure
    """
    logger = logging.getLogger(__name__)
    logger.info("Enter test environment")
    try:
        yield
    except:
        logger.error("Exit test environment with failure")
        raise
    logger.info("Exit test environment with success")
