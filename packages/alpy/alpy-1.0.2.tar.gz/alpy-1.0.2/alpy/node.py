# SPDX-License-Identifier: GPL-3.0-or-later

"""This module contains classes and functions for creating and destroying
network nodes and a network skeleton.
"""

import logging

import alpy.container
import alpy.utils


class NodeTap:
    """This class manages tap interface which is used for communication with a
    node container.

    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param node_container_name: ID or name of the node container
    :type node_container_name: str
    :param interface_name: name of interface to create in host namespace
    :type interface_name: str
    :param timeout: timeout for container operations
    :type timeout: int
    :param busybox_image: ID or name of Docker image containing *ip* executable
    :type busybox_image: str
    :param iproute2_image: ID or name of Docker image containing *ip*
       executable (iproute2 version)
    :type iproute2_image: str

    For explanation of `busybox_image` and `iproute2_image` parameters see
    "Building a network of nodes" README section.
    """

    def __init__(
        self,
        *,
        docker_client,
        node_container_name,
        interface_name,
        timeout,
        busybox_image,
        iproute2_image,
    ):
        self._docker_client = docker_client
        self._join_node_ns = "container:" + node_container_name
        self._interface_name = interface_name
        self._timeout = timeout
        self._busybox_image = busybox_image
        self._iproute2_image = iproute2_image
        self._interface_in_host_namespace = False

    def create_tap_interface(self):
        """Create tap interface in host namespace."""
        self._create_interface()
        self._interface_in_host_namespace = True

    def setup_tap_interface(self):
        """Setup tap interface.

        1. Move the interface to node container.
        2. Rename the interface to "eth0".
        3. Raise the interface.
        """
        self._move_interface_to_node_container()
        self._interface_in_host_namespace = False
        self._rename_interface()
        self._raise_interface()

    def close(self):
        """Delete the tap interface.

        If the interface has been moved to the node container then this method
        does nothing: the interface is destroyed automatically when the
        container namespace is destroyed.
        """
        if self._interface_in_host_namespace:
            self._remove_interface()

    def _run_in_container(self, image, command, **kwargs):
        container = self._docker_client.containers.create(
            image, command, **kwargs
        )
        try:
            container.start()
            alpy.container.close(container, self._timeout)
        finally:
            container.remove()

    def _create_interface(self):

        self._run_in_container(
            self._iproute2_image,
            ["ip", "tuntap", "add", "mode", "tap", "dev", self._interface_name],
            network_mode="host",
            cap_add=["NET_ADMIN"],
            devices=["/dev/net/tun"],
        )

    def _move_interface_to_node_container(self):

        self._run_in_container(
            self._iproute2_image,
            ["ip", "link", "set", "netns", "1", "dev", self._interface_name],
            network_mode="host",
            pid_mode=self._join_node_ns,
            cap_add=["NET_ADMIN"],
        )

    def _rename_interface(self):

        self._run_in_container(
            self._busybox_image,
            ["ip", "link", "set", "name", "eth0", "dev", self._interface_name],
            network_mode=self._join_node_ns,
            cap_add=["NET_ADMIN"],
        )

    def _raise_interface(self):

        self._run_in_container(
            self._busybox_image,
            ["ip", "link", "set", "up", "dev", "eth0"],
            network_mode=self._join_node_ns,
            cap_add=["NET_ADMIN"],
        )

    def _remove_interface(self):

        self._run_in_container(
            self._busybox_image,
            ["ip", "link", "delete", "dev", self._interface_name],
            network_mode="host",
            cap_add=["NET_ADMIN"],
        )


class NodeContainer:
    """This class manages a node container.

    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param name: name to give to the container
    :type name: str
    :param timeout: timeout for container operations
    :type timeout: int
    :param image: ID or name of Docker image containing *cat* executable
    :type image: str
    """

    def __init__(self, *, docker_client, name, timeout, image):
        self._docker_client = docker_client
        self._name = name
        self._timeout = timeout
        self._image = image
        self._container = None
        self._started = False

    def run(self):
        """Create and start the container."""

        self._container = self._docker_client.containers.create(
            self._image,
            ["cat"],
            name=self._name,
            network_mode="none",
            stdin_open=True,
        )

        self._container.start()
        alpy.container.wait_running(self._container, self._timeout)
        self._started = True

    def close(self):
        """Stop and remove the container."""

        if self._container:
            if self._started:
                self._container.kill()
                self._container.wait(timeout=self._timeout)
            alpy.container.write_logs(self._container)
            self._container.remove()


class Node:
    """This class manages a node.

    :param node_container: node container object
    :type node_container: :py:class:`alpy.node.NodeContainer`
    :param node_tap: node tap object
    :type node_tap: :py:class:`alpy.node.NodeTap`
    """

    def __init__(self, node_container, node_tap):
        self._container = node_container
        self._tap = node_tap

    def create_tap_interface(self):
        """Create tap interface in host namespace."""
        self._tap.create_tap_interface()

    def create(self):
        """Create a node."""
        self._container.run()
        self._tap.setup_tap_interface()

    def close(self):
        """Remove a node."""
        self._container.close()
        self._tap.close()


def make_node(
    *,
    busybox_image,
    docker_client,
    interface_name,
    iproute2_image,
    name,
    timeout,
):
    """Make a node.

    :param busybox_image: ID or name of Docker image containing *cat* and *ip*
       executables
    :type busybox_image: str
    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param interface_name: name of interface to create in host namespace
    :type interface_name: str
    :param iproute2_image: ID or name of Docker image containing *ip*
       executable (iproute2 version)
    :type iproute2_image: str
    :param name: name to give to the node container
    :type name: str
    :param timeout: timeout for container operations
    :type timeout: int
    :return: a node
    :rtype: :py:class:`alpy.node.Node`

    For explanation of `busybox_image` and `iproute2_image` parameters see
    "Building a network of nodes" README section.
    """
    node_container = NodeContainer(
        docker_client=docker_client,
        name=name,
        timeout=timeout,
        image=busybox_image,
    )
    node_tap = NodeTap(
        docker_client=docker_client,
        node_container_name=name,
        interface_name=interface_name,
        timeout=timeout,
        busybox_image=busybox_image,
        iproute2_image=iproute2_image,
    )
    return Node(node_container, node_tap)


def make_numbered_nodes(
    *, busybox_image, docker_client, iproute2_image, tap_interfaces, timeout
):
    """Make a list of nodes named "node0", "node1", etc.

    :param busybox_image: ID or name of Docker image containing *cat* and *ip*
       executables
    :type busybox_image: str
    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param iproute2_image: ID or name of Docker image containing *ip*
       executable (iproute2 version)
    :type iproute2_image: str
    :param tap_interfaces: list of interface names
    :type tap_interfaces: list(str)
    :param timeout: timeout for container operations
    :type timeout: int
    :return: list of node objects
    :rtype: list of :py:class:`alpy.node.Node`

    For explanation of `busybox_image` and `iproute2_image` parameters see
    "Building a network of nodes" README section.
    """
    nodes = []
    for node_index, interface_name in enumerate(tap_interfaces):
        node = make_node(
            busybox_image=busybox_image,
            docker_client=docker_client,
            interface_name=interface_name,
            iproute2_image=iproute2_image,
            name=f"node{node_index}",
            timeout=timeout,
        )
        nodes.append(node)
    return nodes


class Skeleton:
    """A network skeleton. This class manages a collection of nodes.

    :param nodes: a list of node objects
    :type nodes: list of :py:class:`alpy.node.Node`
    """

    def __init__(self, nodes):
        self._nodes = nodes

    def create_tap_interfaces(self):
        """Create tap interfaces in host namespace."""
        logger = logging.getLogger(__name__)
        context_logger = alpy.utils.make_context_logger(logger)
        with context_logger("Create tap interfaces"):
            for node in self._nodes:
                node.create_tap_interface()

    def create(self):
        """Create nodes."""
        logger = logging.getLogger(__name__)
        context_logger = alpy.utils.make_context_logger(logger)
        with context_logger("Create nodes"):
            for node in self._nodes:
                node.create()

    def close(self):
        """Remove nodes."""
        for node in self._nodes:
            node.close()


def make_skeleton(
    *, busybox_image, docker_client, iproute2_image, tap_interfaces, timeout
):
    """Make a network skeleton.

    :param busybox_image: ID or name of Docker image containing *cat* and *ip*
       executables
    :type busybox_image: str
    :param docker_client: Docker client
    :type docker_client: :py:class:`docker:docker.client.DockerClient`
    :param iproute2_image: ID or name of Docker image containing *ip*
       executable (iproute2 version)
    :type iproute2_image: str
    :param tap_interfaces: list of interface names
    :type tap_interfaces: list(str)
    :param timeout: timeout for container operations
    :type timeout: int
    :return: network skeleton
    :rtype: :py:class:`alpy.node.Skeleton`

    For explanation of `busybox_image` and `iproute2_image` parameters see
    "Building a network of nodes" README section.
    """
    return Skeleton(
        make_numbered_nodes(
            busybox_image=busybox_image,
            docker_client=docker_client,
            iproute2_image=iproute2_image,
            tap_interfaces=tap_interfaces,
            timeout=timeout,
        )
    )
