# SPDX-License-Identifier: GPL-3.0-or-later

"""This module contains functions for generating QEMU command line arguments
and managing QEMU process.
"""


import contextlib
import logging
import shutil
import subprocess
from pathlib import Path

from qmp import QEMUMonitorProtocol

import alpy.config
import alpy.utils

QMP_SOCKET_FILENAME = "qmp.sock"
"""Path to unix domain socket for QMP"""
OVMF_VARS_COPY_FILENAME = "OVMF_VARS.fd"
"""OVMF variables store filename"""


@contextlib.contextmanager
def run(qemu_args, timeout):
    """QEMU process context manager.

    On entering context the manager starts a QMP server and a QEMU process. QEMU
    connects to the QMP server. On exiting the context the `quit` QMP command is
    issued, QEMU process stops.

    :param qemu_args: QEMU command line arguments. The arguments must include
       QMP-related arguments returned by :py:func:`alpy.qemu.get_qmp_args`.
    :type qemu_args: list(str)
    :param timeout: number of seconds to wait for QEMU to stop after issuing
       the `quit` QMP command
    :type timeout: int
    :return: QMP handle
    :rtype: QEMUMonitorProtocol
    """
    logger = logging.getLogger(__name__)
    context_logger = alpy.utils.make_context_logger(logger)
    with context_logger("Initialize QMP monitor"):
        qmp = QEMUMonitorProtocol(QMP_SOCKET_FILENAME, server=True)
    try:
        with context_logger("Start QEMU"):
            logger.debug(f"Starting subprocess: {qemu_args}")
            process = subprocess.Popen(  # pylint: disable=consider-using-with
                qemu_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
        try:
            with context_logger("Accept connection from QEMU to QMP monitor"):
                qmp.accept()
            try:
                yield qmp
            finally:
                with context_logger("Quit QEMU"):
                    qmp.command("quit")
        finally:
            close(process, timeout)
    finally:
        Path(QMP_SOCKET_FILENAME).unlink()


def close(process, timeout):
    """Stop QEMU.

    Wait for QEMU process to stop. If the process does not stop, kill it. Check
    exit code. Log process output and the exit code via Python
    :py:mod:`python:logging` module.

    :param process: QEMU process
    :type process: :py:class:`python:subprocess.Popen`
    :param timeout: maximum number of seconds to wait
    :type timeout: int
    :raises alpy.utils.NonZeroExitCode: if the process exited with non-zero code
       or was killed by a signal
    """
    logger = logging.getLogger(__name__)
    context_logger = alpy.utils.make_context_logger(logger)

    try:
        stdout_data, stderr_data = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.error("QEMU is still running")
        with context_logger("Kill QEMU"):
            process.kill()
            stdout_data, stderr_data = process.communicate()

    for line in stdout_data.splitlines():
        logger.debug("qemu stdout: " + line)

    for line in stderr_data.splitlines():
        logger.debug("qemu stderr: " + line)

    return_code = process.returncode

    if return_code > 0:
        raise alpy.utils.NonZeroExitCode(
            f"QEMU exited with non-zero code {return_code}"
        )
    if return_code < 0:
        signal_number = -1 * return_code
        raise alpy.utils.NonZeroExitCode(
            "QEMU was killed by signal " + alpy.utils.signal_name(signal_number)
        )
    logger.debug("QEMU exited with code 0")


def start_virtual_cpu(qmp):
    """Start virtual CPU.

    :param qmp: QMP handle
    :type qmp: QEMUMonitorProtocol
    """
    logger = logging.getLogger(__name__)
    context_logger = alpy.utils.make_context_logger(logger)
    with context_logger("Start virtual CPU"):
        qmp.command("cont")


def read_events(qmp):
    """Read and log QEMU events.

    :param qmp: QMP handle
    :type qmp: QEMUMonitorProtocol
    """
    logger = logging.getLogger(__name__)
    logger.debug("Read QEMU events")
    while qmp.pull_event():
        pass


def wait_shutdown(qmp):
    """Wait until the VM is powered down and stopped.

    :param qmp: QMP handle
    :type qmp: QEMUMonitorProtocol
    """
    logger = logging.getLogger(__name__)
    context_logger = alpy.utils.make_context_logger(logger)

    with context_logger("Wait until the VM is powered down"):
        while qmp.pull_event(wait=True)["event"] != "SHUTDOWN":
            pass

    with context_logger("Wait until the VM is stopped"):
        while qmp.pull_event(wait=True)["event"] != "STOP":
            pass


def get_qmp_args():
    """Get QMP-related QEMU command line arguments.

    The arguments instruct QEMU to connect to QMP server at startup.

    The connection is made to unix socket. The path is specified by
    :py:data:`alpy.qemu.QMP_SOCKET_FILENAME`.

    :return: list of arguments
    :rtype: list(str)
    """
    return [
        "-chardev",
        "socket,id=id_char_qmp,path=" + QMP_SOCKET_FILENAME,
        "-mon",
        "chardev=id_char_qmp,mode=control",
    ]


def get_network_interface_args(interface_index, interface_name):
    """Get QEMU command line arguments which add network interface.

    The arguments also instruct QEMU to capture packets on the interface. The
    packets are captured to file "link{interface_index}.pcap".

    :param interface_index: unique number for each interface
    :type interface_index: int
    :param interface_name: tap interface name
    :type interface_name: str
    :return: list of arguments
    :rtype: list(str)
    """
    packet_capture_filename = f"link{interface_index}.pcap"
    netdev_id = f"id_net{interface_index}"

    return [
        "-netdev",
        f"tap,id={netdev_id},ifname={interface_name},script=no,downscript=no",
        "-device",
        f"e1000,netdev={netdev_id}",
        "-object",
        f"filter-dump,id=id_dump{interface_index},netdev={netdev_id},file="
        + packet_capture_filename,
    ]


def get_network_interfaces_args(tap_interfaces):
    """Get QEMU command line arguments which add network interfaces.

    The arguments also instruct QEMU to capture packets on the interfaces. The
    packets are captured to files "link0.pcap", "link1.pcap", etc.

    :param tap_interfaces: names of tap interfaces
    :type tap_interfaces: list(str)
    :return: list of arguments
    :rtype: list(str)
    """
    args = []
    for interface_index, interface_name in enumerate(tap_interfaces):
        args.extend(get_network_interface_args(interface_index, interface_name))
    return args


def get_serial_port_args(tcp_port=alpy.config.QEMU_SERIAL_PORT):
    """Get QEMU command line arguments which add serial port.

    QEMU listens on and redirects virtual serial port to 127.0.0.1 port
    *tcp_port*.

    The arguments also instruct QEMU to capture serial port output. The output
    is captured to file "console.log".

    :param tcp_port: TCP port to listen on
    :type tcp_port: int
    :return: list of arguments
    :rtype: list(str)
    """
    return [
        "-chardev",
        f"socket,id=id_char_serial,port={tcp_port},"
        "host=127.0.0.1,ipv4,nodelay,server,nowait,telnet,logfile=console.log",
        "-serial",
        "chardev:id_char_serial",
    ]


@contextlib.contextmanager
def temporary_copy_ovmf_vars():
    """Make a temporary file to store OVMF variables.

    On entering context this context manager makes a file to store OVMF
    variables in. The path is specified by
    :py:data:`alpy.qemu.OVMF_VARS_COPY_FILENAME`. The file is a copy of
    "/usr/share/OVMF/OVMF_VARS.fd". On exiting the context the file is removed.

    See also :py:func:`alpy.qemu.get_uefi_firmware_args`.
    """
    shutil.copy("/usr/share/OVMF/OVMF_VARS.fd", OVMF_VARS_COPY_FILENAME)
    try:
        yield
    finally:
        Path(OVMF_VARS_COPY_FILENAME).unlink()


def get_uefi_firmware_args():
    """Get UEFI-related QEMU command line arguments.

    See also `Open Virtual Machine Firmware (OVMF) Status Report
    <http://www.linux-kvm.org/downloads/lersek/ovmf-whitepaper-c770f8c.txt>`_:

       The 128 KB firmware volume with the variable store, discussed under (1),
       is also built as a separate host-side file, named "OVMF_VARS.fd". The
       "rest" is built into a third file, "OVMF_CODE.fd", which is only 1920 KB
       in size. The variable store is mapped into its usual location, at
       4 GB - 2 MB = 0xFFE0_0000, through the following qemu options:

       .. code:: text

          -drive if=pflash,format=raw,readonly,file=OVMF_CODE.fd
          -drive if=pflash,format=raw,file=fedora.varstore.fd

    See also `#764918 - Please split into OVMF_VARS.fd and OVMF_CODE.fd - Debian
    Bug report logs
    <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=764918>`_.

    :return: list of arguments
    :rtype: list(str)
    """
    args = []

    # firmware executable code
    args.append("-drive")
    args.append(
        "if=pflash,format=raw,unit=0,readonly,file=/usr/share/OVMF/OVMF_CODE.fd"
    )

    # firmware variable store
    args.append("-drive")
    args.append("if=pflash,format=raw,unit=1,file=" + OVMF_VARS_COPY_FILENAME)

    return args
