# SPDX-License-Identifier: GPL-3.0-or-later

"""This module contains high-level functions for connecting QEMU process with
a network skeleton.
"""

import contextlib

import alpy.qemu


@contextlib.contextmanager
def qemu_with_skeleton(*, qemu_args, skeleton, timeout):
    """Context manager for QEMU and network skeleton.

    On entering context the manager creates tap interfaces and starts QEMU. QEMU
    connects to tap interfaces. Then network nodes are created and the
    interfaces are moved to the node namespaces. On exiting the context QEMU
    process is stopped and network skeleton is destroyed.

    :param qemu_args: QEMU command line arguments. The arguments must include
       arguments returned by :py:func:`alpy.qemu.get_qmp_args` and by
       :py:func:`alpy.qemu.get_network_interfaces_args`.

       .. note::

          Tap interfaces names in QEMU args must match network skeleton tap
          interfaces names.

    :type qemu_args: list(str)
    :param skeleton: network skeleton
    :type skeleton: :py:class:`alpy.node.Skeleton`
    :param timeout: number of seconds to wait for QEMU to stop after issuing
       the `quit` QMP command
    :type timeout: int
    :return: QMP handle
    :rtype: QEMUMonitorProtocol
    """
    try:
        skeleton.create_tap_interfaces()
        with alpy.qemu.run(qemu_args, timeout) as qmp:
            skeleton.create()
            alpy.qemu.read_events(qmp)
            yield qmp
    finally:
        skeleton.close()
