# SPDX-License-Identifier: GPL-3.0-or-later

r"""This module contains functions for connecting to and communicating with a
QEMU virtual machine guest via a serial port.

How to talk to the guest using the module:

#. Connect to the guest by entering :py:func:`alpy.console.connect` context
   manager. The manager yields a :py:class:`pexpect:pexpect.fdpexpect.fdspawn`
   object. The object is configured to log console input and output via Python
   :py:mod:`python:logging` module.

#. Talk to the guest using the fdspawn object.

#. Exit the context.

#. The console connection is closed automatically.

Example::

   with alpy.console.connect(timeout=10) as console:
       console.sendline("python3 -c 'print(2 + 2)'")
       console.expect_exact("4")
       console.expect_exact("\n")

The example produces the following logs:

.. code:: text

   DEBUG    alpy.console    > "python3 -c 'print(2 + 2)'\n"
   DEBUG    alpy.console    < "$ python3 -c 'print(2 + 2)'\r\n"
   DEBUG    alpy.console    < '4\r\n'

For logging implementation details see module :py:mod:`alpy.pexpect_log`.

If the default behaviour (the :py:func:`alpy.console.connect` function) does not
suit your needs, use the lower level API functions:

#. :py:func:`alpy.console.create_socket`
#. :py:func:`alpy.console.connect_socket`
#. :py:func:`alpy.console.create`
#. :py:func:`alpy.console.close`
"""

import contextlib
import logging
import socket
import threading

import pexpect
import pexpect.fdpexpect

import alpy.config
import alpy.pexpect_log
import alpy.utils


def create_socket():
    """Create a TCP :ref:`socket object <python:socket-objects>`."""
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_socket(sock, host="127.0.0.1", port=alpy.config.QEMU_SERIAL_PORT):
    """Establish connection to a host.

    :param sock: socket
    :type sock: :ref:`socket object <python:socket-objects>`
    :param host: host
    :type host: str
    :param port: port
    :type port: int
    """
    logger = logging.getLogger(__name__)
    context_logger = alpy.utils.make_context_logger(logger)
    with context_logger("Connect to console"):
        sock.connect((host, port))


def create(connected_socket, timeout):
    """Create a connected console instance.

    The console logs input and output via Python :py:mod:`python:logging`
    module.

    :param connected_socket: socket of an established connection
    :type connected_socket: :ref:`socket object <python:socket-objects>`
    :param timeout: timeout for ``expect()`` calls
    :type timeout: int or None
    :return: connected console
    :rtype: :py:class:`pexpect:pexpect.fdpexpect.fdspawn`
    """
    logger = logging.getLogger(__name__)
    console = pexpect.fdpexpect.fdspawn(connected_socket, timeout=timeout)
    console.logfile_read = alpy.pexpect_log.LogfileRead(logger)
    console.logfile_send = alpy.pexpect_log.LogfileSend(logger)
    return console


def flush_log(console):
    """Flush console output log buffer.

    Console output is written to the log when end of line is reached. Call this
    function when you want to log the latest console output but the end of the
    last line has not been reached yet.

    .. note::

       In order to support this operation the
       :py:attr:`pexpect:pexpect.spawn.logfile_read` console attribute must be
       set to :py:class:`alpy.pexpect_log.LogfileRead` instance. The console
       objects returned by :py:func:`alpy.console.create` and
       :py:func:`alpy.console.connect` functions are configured in this way.

    :param console: console object
    :type console: :py:class:`pexpect:pexpect.spawn` - like class
    """
    console.logfile_read.log_remaining_text()


def close(console):
    """Close console connection and flush console output to the log.

    .. note::

       The console object must support :py:func:`~alpy.console.flush_log`
       operation. See the note in the :py:func:`alpy.console.flush_log`
       documentation.

    :param console: console object
    :type console: :py:class:`pexpect:pexpect.spawn` - like class
    """
    logger = logging.getLogger(__name__)
    context_logger = alpy.utils.make_context_logger(logger)
    with context_logger("Close console"):
        console.expect_exact([pexpect.EOF, pexpect.TIMEOUT], timeout=1)
        console.close()
        flush_log(console)


@contextlib.contextmanager
def connect(*, host="127.0.0.1", port=alpy.config.QEMU_SERIAL_PORT, timeout):
    """Console connection context manager.

    On entering context the manager establishes connection to the host and
    yields console object. On exiting the context the connection is closed.

    :param host: host
    :type host: str
    :param port: port
    :type port: int
    :param timeout: timeout for ``expect()`` calls
    :type timeout: int or None
    :return: connected console
    :rtype: :py:class:`pexpect:pexpect.fdpexpect.fdspawn`
    """
    sock = create_socket()
    connect_socket(sock, host, port)
    console = create(sock, timeout)
    try:
        yield console
    finally:
        if not console.closed:
            close(console)


@contextlib.contextmanager
def read_in_background(console):
    # pylint: disable=missing-yield-doc,missing-yield-type-doc
    """Background reading context manager.

    On entering context the manager starts reading from the console. On exiting
    the context the manager stops reading. The reading is done in a background
    thread.

    Usage example::

       with alpy.console.read_in_background(console):
           long_operation()

    Console output is being read and logged while ``long_operation()`` is
    executing.

    :param console: console object
    :type console: :py:class:`pexpect:pexpect.spawn` - like class
    """
    stop_reading = threading.Event()

    def read_until_stopped_or_eof():
        while not stop_reading.is_set() and console.expect_exact(
            [pexpect.EOF, pexpect.TIMEOUT], timeout=0.5
        ):
            pass

    thread = threading.Thread(target=read_until_stopped_or_eof)
    thread.start()
    try:
        yield
    finally:
        stop_reading.set()
        thread.join()
