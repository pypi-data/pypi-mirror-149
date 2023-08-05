# SPDX-License-Identifier: GPL-3.0-or-later

"""In Alpy, containers are managed using the :std:doc:`docker:index`. This
module contains a few extra functions for managing containers. The functions are
helpful when testing a network appliance. The functions do primarily the
following tasks:

- Write container logs via Python :py:mod:`python:logging` module.
- Write container exit code to the log.
- Check container exit code.
- Configure container interface.
"""

import logging
import time

import alpy.utils


def write_logs(container):
    """Write container logs via Python :py:mod:`python:logging` module.

    :param container: container
    :type container: :py:class:`docker:docker.models.containers.Container`
    """

    logger = logging.getLogger(__name__)

    def log_each_line(lines_bytes, prefix):
        if lines_bytes:
            for line in lines_bytes.decode().splitlines():
                logger.debug(prefix + line)

    log_each_line(
        container.logs(stdout=True, stderr=False),
        f"{container.short_id} stdout: ",
    )

    log_each_line(
        container.logs(stdout=False, stderr=True),
        f"{container.short_id} stderr: ",
    )


def get_signal_number_from_exit_code(code):
    """Convert container exit code to signal number.

    :param code: container exit code
    :type code: int
    :return: signal number or None (if *code* does not represent a signal)
    :rtype: int or NoneType
    """
    if code >= 128:
        return code - 128
    return None


def log_exit_code(code, name):
    """Log container exit code via Python :py:mod:`python:logging` module.

    Log message examples:

    - "Container apache exited with code 0"
    - "Container apache was killed by signal SIGKILL"

    :param code: container exit code
    :type code: int
    :param name: container name
    :type name: str
    """
    logger = logging.getLogger(__name__)
    signal_number = get_signal_number_from_exit_code(code)
    if signal_number:
        signal_name = alpy.utils.signal_name(signal_number)
        logger.debug(f"Container {name} was killed by signal {signal_name}")
    else:
        logger.debug(f"Container {name} exited with code {code}")


def check_exit_code(code):
    """Check container exit code.

    :param code: container exit code
    :type code: int
    :raises alpy.utils.NonZeroExitCode: if *code* is not zero
    """
    signal_number = get_signal_number_from_exit_code(code)
    if signal_number:
        raise alpy.utils.NonZeroExitCode(
            "Container process was killed by signal "
            + alpy.utils.signal_name(signal_number)
        )
    if code != 0:
        raise alpy.utils.NonZeroExitCode(
            f"Container process exited with non-zero code {code}"
        )


def stop(container, timeout, signal="SIGTERM"):
    """Kill a container and wait until it stops.

    Write the container logs and exit code via Python :py:mod:`python:logging`
    module.

    :param container: container
    :type container: :py:class:`docker:docker.models.containers.Container`
    :param timeout: maximum number of seconds to wait
    :type timeout: int
    :param signal: signal to send
    :type signal: str
    :return: exit code
    :rtype: int
    """
    try:
        container.kill(signal)
        result = container.wait(timeout=timeout)
    finally:
        write_logs(container)
    exit_code = int(result["StatusCode"])
    log_exit_code(exit_code, container.short_id)
    return exit_code


def close(container, timeout):
    """Wait for a container to stop. If the container does not stop, kill it.

    Check the exit code. Write container logs and the exit code via Python
    :py:mod:`python:logging` module.

    :param container: container
    :type container: :py:class:`docker:docker.models.containers.Container`
    :param timeout: maximum number of seconds to wait
    :type timeout: int
    """
    result = None
    try:
        result = container.wait(timeout=timeout)
    except:
        logger = logging.getLogger(__name__)
        logger.error(
            "Timed out waiting for container "
            + container.short_id
            + " to stop by itself"
        )
        container.kill()
        result = container.wait(timeout=timeout)
        raise
    finally:
        write_logs(container)
        if result:
            exit_code = int(result["StatusCode"])
            log_exit_code(exit_code, container.short_id)
    check_exit_code(exit_code)


class Timeout(Exception):
    """Timeout expired."""


def wait_running(container, timeout):
    """Wait for a container to start.

    :param container: container
    :type container: :py:class:`docker:docker.models.containers.Container`
    :param timeout: maximum number of seconds to wait
    :type timeout: int
    :raises alpy.container.Timeout: if the container does not start before
       timeout expires.
    """

    time_start = time.time()
    while True:
        container.reload()
        if container.status == "running":
            break
        if time.time() > time_start + timeout:
            raise Timeout
        time.sleep(0.5)


def configure_interface(
    container_name, address, gateway=None, *, docker_client, image, timeout
):
    """Configure a network interface of a running container.

    This function spawns a temporary container which shares a network namespace
    with container *container_name*. The temporary container configures the
    interface using *ip* command.

    :param container_name: container ID or name
    :type container_name: str
    :param address: IP address followed by a slash and network prefix length,
       for example, "192.168.1.2/24"
    :type address: str
    :param gateway: the default gateway IP address. If omitted, the default
       route is not configured.
    :type gateway: str
    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param image: ID or name of Docker image containing *ip* executable, for
       example, "busybox:latest"
    :type image: str
    :param timeout: maximum number of seconds to wait. The function waits for
       the temporary container to configure the interface.
    :type timeout: int
    """
    add_ip_address(
        container_name,
        address,
        docker_client=docker_client,
        image=image,
        timeout=timeout,
    )
    if gateway:
        add_default_route(
            container_name,
            gateway,
            docker_client=docker_client,
            image=image,
            timeout=timeout,
        )


def add_ip_address(container_name, address, *, docker_client, image, timeout):
    """Add an ip address to a network interface of a running container.

    This function spawns a temporary container which shares a network namespace
    with container *container_name*. The temporary container configures the
    interface using *ip* command.

    :param container_name: container ID or name
    :type container_name: str
    :param address: IP address followed by a slash and network prefix length,
       for example, "192.168.1.2/24"
    :type address: str
    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param image: ID or name of Docker image containing *ip* executable, for
       example, "busybox:latest"
    :type image: str
    :param timeout: maximum number of seconds to wait. The function waits for
       the temporary container to configure the interface.
    :type timeout: int
    """
    container = docker_client.containers.create(
        image,
        ["ip", "address", "add", address, "dev", "eth0"],
        network_mode="container:" + container_name,
        cap_add=["NET_ADMIN"],
    )
    try:
        container.start()
        close(container, timeout)
    finally:
        container.remove()


def add_default_route(
    container_name, gateway, *, docker_client, image, timeout
):
    """Add the default route in a network namespace of a running container.

    This function spawns a temporary container which shares a network namespace
    with container *container_name*. The temporary container adds the default
    gateway using *ip* command.

    :param container_name: container ID or name
    :type container_name: str
    :param gateway: the default gateway IP address
    :type gateway: str
    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param image: ID or name of Docker image containing *ip* executable, for
       example, "busybox:latest"
    :type image: str
    :param timeout: maximum number of seconds to wait. The function waits for
       the temporary container to stop.
    :type timeout: int
    """
    container = docker_client.containers.create(
        image,
        ["ip", "route", "add", "default", "via", gateway],
        network_mode="container:" + container_name,
        cap_add=["NET_ADMIN"],
    )
    try:
        container.start()
        close(container, timeout)
    finally:
        container.remove()
