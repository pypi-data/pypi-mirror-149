####
Alpy
####

*Test network virtual appliance using Docker containers*

.. contents::
   :backlinks: none

General information
===================

The project
-----------

This project is a Python library for testing network virtual appliances.

Author
------

Alexey Bogdanenko

License
-------

Alpy is licensed under ``SPDX-License-Identifier: GPL-3.0-or-later``. See
``COPYING`` for more details.

Description
-----------

Alpy manages containers via `Docker Python API`__.

__ https://github.com/docker/docker-py

Alpy interacts with QEMU__ using Python API of the `QEMU Monitor Protocol`__
(QMP). QMP is a JSON-based protocol that allows applications to communicate with
a QEMU instance.

__ https://www.qemu.org
__ https://pypi.org/project/qmp/

Alpy gives user Pexpect__ object to interact with a serial console. The Pexpect
object is configured to log console input and output via the standard `logging
module`__.

__ https://pexpect.readthedocs.io
__ https://docs.python.org/3/library/logging.html

Alpy is packaged and deployed to PyPI. The package__ can be installed using
*pip*.

__ https://pypi.org/project/alpy/

There are unit tests (pytest__) and integration tests in GitLab CI pipeline.
Alpy is tested and works on the latest Ubuntu and the latest Ubuntu LTS release.

__ https://docs.pytest.org/en/latest/

Examples
========

The alpy library repository includes scripts and modules to build a simple
appliance called Rabbit. Rabbit is Alpine Linux with a few packages
pre-installed. Having this simple DUT allows to demonstrate the library
features and capabilities. The tests verify a few features of the network
appliance, for example:

- IPv4 routing (see ``rabbit/tests/forward-ipv4/main.py``)
- rate-limiting network traffic (see ``rabbit/tests/rate-limit/main.py``)
- load-balancing HTTP requests (see ``rabbit/tests/load-balancing/main.py``)

The tests are executed automatically in the GitLab CI pipeline.

Example network (test *rate-limit*)::

   +-------------------------------------+
   |                                     |
   |          Device under test          |
   |          rate limit = 1mbps         |
   +-------+--------------------+--------+
           |                    |
           |                    |
           |                    |
   +-------+--------+   +-------+--------+
   |                |   |                |
   | 192.168.1.1/24 |   | 192.168.1.2/24 |
   |                |   |                |
   | node0          |   | node1          |
   | iperf3 client  |   | iperf3 server  |
   +----------------+   +----------------+

Example test output::

   INFO     __main__               Test description: Check that rabbit rate-limits traffic.
   INFO     alpy.node              Create tap interfaces...
   INFO     alpy.node              Create tap interfaces... done
   INFO     alpy.qemu              Initialize QMP monitor...
   INFO     alpy.qemu              Initialize QMP monitor... done
   INFO     alpy.qemu              Start QEMU...
   INFO     alpy.qemu              Start QEMU... done
   INFO     alpy.qemu              Accept connection from QEMU to QMP monitor...
   INFO     alpy.qemu              Accept connection from QEMU to QMP monitor... done
   INFO     alpy.node              Create nodes...
   INFO     alpy.node              Create nodes... done
   INFO     alpy.console           Connect to console...
   INFO     alpy.console           Connect to console... done
   INFO     alpy.utils             Enter test environment
   INFO     __main__               Start iperf3 server on node 1...
   INFO     __main__               Start iperf3 server on node 1... done
   INFO     alpy.qemu              Start virtual CPU...
   INFO     alpy.qemu              Start virtual CPU... done
   INFO     alpine                 Wait for the system to boot...
   INFO     alpine                 Wait for the system to boot... done
   INFO     alpine                 Login to the system...
   INFO     alpine                 Login to the system... done
   INFO     alpy.remote_shell      Type in script configure-rabbit...
   INFO     alpy.remote_shell      Type in script configure-rabbit... done
   INFO     alpy.remote_shell      Run script configure-rabbit...
   INFO     alpy.remote_shell      Run script configure-rabbit... done
   INFO     __main__               Start iperf3 client on node 0...
   INFO     __main__               Measure rate...
   INFO     __main__               Measure rate... done
   INFO     __main__               Parse iperf3 report...
   INFO     __main__               Parse iperf3 report... done
   INFO     __main__               Start iperf3 client on node 0... done
   INFO     alpine                 Initiate system shutdown...
   INFO     alpine                 Initiate system shutdown... done
   INFO     alpy.qemu              Wait until the VM is powered down...
   INFO     alpy.qemu              Wait until the VM is powered down... done
   INFO     alpy.qemu              Wait until the VM is stopped...
   INFO     alpy.qemu              Wait until the VM is stopped... done
   INFO     __main__               Rate received, bits per second: 976321
   INFO     __main__               Check rate...
   INFO     __main__               Check rate... done
   INFO     alpy.utils             Exit test environment with success
   INFO     alpy.console           Close console...
   INFO     alpy.console           Close console... done
   INFO     alpy.qemu              Quit QEMU...
   INFO     alpy.qemu              Quit QEMU... done
   INFO     alpy.utils             Test passed

The tests for the Rabbit device share a lot of code so the code is organized as
a library. The library is called *carrot*.

Features
========

The simplest docker to QEMU networking connection
-------------------------------------------------

Nothing in the middle. No bridges, no veth pairs, no NAT etc.

Each layer 2 frame emitted is delivered unmodified, reliably.

Reliable packet capture
-----------------------

Each frame is captured reliably thanks to the QEMU *filter-dump* feature.

First-class Docker container support
------------------------------------

Alpy follows and encourages single process per container design.

Logging
-------

Test logs are easy to configure and customize. Alpy consistently uses Python
*logging* module.

Alpy collects serial console log in binary as well as text (escaped) form.

No trash left behind
--------------------

Alpy cleans up after itself:

- processes stopped with error codes and logs collected,
- files, directories unmounted,
- temporary files removed,
- sockets closed,
- interfaces removed...

... reliably.

No root required
----------------

Run as a regular user.

API documentation
=================

The documentation is published on GitLab Pages of your GitLab project (if GitLab
Pages is enabled on your GitLab instance). For example, upstream project
documentation lives at https://abogdanenko.gitlab.io/alpy.

Alpy API documentation is generated using Sphinx__. To generate HTML API
documentation locally, install `Sphinx package`__ and run the following
command::

   PYTHONPATH=. sphinx-build docs public

To view the generated documentation, open ``public/index.html`` in a browser.

__ https://www.sphinx-doc.org/
__ https://pypi.org/project/Sphinx/

Network design
==============

The appliance being tested is referred to as a *device under test* or *DUT*.

The DUT communicates with containers attached to each of its network links.

Guest network adapters are connected to the host via tap devices (Figure 1)::

   +-----QEMU hypervisor------+
   |                          |   +-------------+
   | +-----Guest OS-----+     |   |             |
   | |                  |     |   |  docker     |
   | | +--------------+ |     |   |  container  |
   | | |              | |     |   |  network    |
   | | |  NIC driver  | |     |   |  namespace  |
   | | |              | |     |   |             |
   | +------------------+     |   |   +-----+   |
   |   |              |       |   |   |     |   |
   |   | NIC hardware +---+-----------+ tap |   |
   |   |              |   |   |   |   |     |   |
   |   +--------------+   |   |   |   +-----+   |
   |                      |   |   |             |
   +--------------------------+   +-------------+
                          |
                          |
                          v
                    +-----------+
                    |           |
                    | pcap file |
                    |           |
                    +-----------+

*Figure 1. Network link between QEMU guest and a docker container.*

Each tap device lives in its network namespace. This namespace belongs to a
dedicated container - a *node*. The node's purpose is to keep the namespace
alive during the lifetime of a test.

For an application to be able to communicate with the DUT the application is
containerized. The application container must be created in a special way: it
must share network namespace with one of the nodes.

Figure 2 shows an example where application containers *app0* and *app1* share
network namespace with node container *node0*. Application container *app2*
shares another network namespace with *node2*.

This sharing is supported by Docker. All we have to do is to create the
application container with the ``--network=container:NODE_NAME`` Docker option.
For example, if we want to send traffic to the DUT via its first link, we create
a traffic generator container with Docker option ``--network=container:node0``.

::

   +----QEMU---+   +------shared network namespace-----+
   |           |   |                                   |
   |           |   |    eth0                           |
   |   +---+   |   |   +---+   +-----+ +----+ +----+   |
   |   |NIC+-----------+tap|   |node0| |app0| |app1|   |
   |   +---+   |   |   +---+   +-----+ +----+ +----+   |
   |           |   |                                   |
   |           |   +-----------------------------------+
   |           |
   |           |
   |           |
   |           |   +------shared network namespace-----+
   |           |   |                                   |
   |           |   |    eth0                           |
   |   +---+   |   |   +---+   +-----+                 |
   |   |NIC+-----------+tap|   |node1|                 |
   |   +---+   |   |   +---+   +-----+                 |
   |           |   |                                   |
   |           |   +-----------------------------------+
   |           |
   |           |
   |           |
   |           |   +------shared network namespace-----+
   |           |   |                                   |
   |           |   |    eth0                           |
   |   +---+   |   |   +---+   +-----+ +----+          |
   |   |NIC+-----------+tap|   |node2| |app2|          |
   |   +---+   |   |   +---+   +-----+ +----+          |
   |           |   |                                   |
   +-----------+   +-----------------------------------+

*Figure 2. Application containers attached to the DUT links.*

Building a network of nodes
===========================

Network configuration operations are performed by temporary one-off Docker
containers by calling *ip* commands inside the containers.

A distinction is made between a simplified version of the *ip* binary and the
full version. The simplified version is a busybox__ applet. The full version is
shipped in the iproute2__ package.

__ https://busybox.net/
__ https://wiki.linuxfoundation.org/networking/iproute2

Here is a list of features which alpy requires but which are missing from the
simplified version:

1. Move a network interface to a different namespace ("ip link set netns ...")

2. Create a tap interface ("ip tuntap add mode tap ...")

The image which contains the simplified version is called `busybox_image` while
the full image is called `iproute2_image`.

The images must be provided by the caller and must be present on the system. For
example, set::

   busybox_image = "busybox:latest"
   iproute2_image = "registry.gitlab.com/abogdanenko/alpy/iproute2:latest"


FAQ
===

How do I watch serial console?
------------------------------

Use *tail*::

   tail --follow name --retry console.log

The same command, but shorter::

   tail -F console.log

How do I watch traffic on an interface?
---------------------------------------

Use tcpdump::

   tail --bytes +0 --follow name --retry link0.pcap | tcpdump -n -r -

The same command, but shorter::

   tail -Fc +0 link0.pcap | tcpdump -nr-

Can I use Wireshark to watch traffic on an interface?
-----------------------------------------------------

Yes, you can::

   tail --bytes +0 --follow name --retry link0.pcap | wireshark -k -i -

The same command, but shorter::

   tail -Fc +0 link0.pcap | wireshark -ki-

How do I debug my program?
--------------------------

Use `The Python Debugger <https://docs.python.org/3/library/pdb.html>`_.

How do I enter node network namespace?
--------------------------------------

#. Get node pid::

      docker inspect --format '{{.State.Pid}}' node0

#. Jump into node namespace using that pid::

      nsenter --net --target "$pid"

One-liner::

   nsenter --net --target "$(docker inspect --format '{{.State.Pid}}' node0)"

A note about GitLab Container Registry
======================================

Many CI jobs use one of the custom images built on the "build-docker-images"
stage. The images are stored in the GitLab Container Registry.

The images are pulled from locations specified by GitLab variables. By default,
the variables point to the registry of the current GitLab project.

If you forked this project and GitLab Container Registry is disabled in your
project, override the variables on a project level so that the images are pulled
from some other registry.

For example, set
``IMAGE_UBUNTU_LTS=registry.gitlab.com/abogdanenko/alpy/ubuntu-lts:latest``.

Related projects
================

- `Containernet <https://containernet.github.io/>`_

- `Kathara <http://www.kathara.org/>`_

- `Netkit <http://wiki.netkit.org/index.php/Main_Page>`_

- `GNS3 <https://www.gns3.com/>`_

- `Virtual Networks over linuX (VNX)
  <http://web.dit.upm.es/vnxwiki/index.php/Main_Page>`_

- `Pipework: Software-Defined Networking for Linux Containers
  <https://github.com/jpetazzo/pipework>`_

- `Eve-NG <https://www.eve-ng.net/>`_
