# SPDX-License-Identifier: GPL-3.0-or-later

"""This module contains functions for uploading and executing scripts on a
remote system. The remote system must have a shell.

The functions of this module accept :py:class:`pexpect:pexpect.spawn` - like
objects as arguments and require established connection to the remote system.
"""


import logging
import random
from pathlib import Path

import alpy.utils


def _random_delimiter():
    return f"eof{random.randrange(1000000):06}"


def upload_text_file(console, prompt, source_filename, destination_filename):
    """Upload text file via a shell connection.

    :param console: console object
    :type console: :py:class:`pexpect:pexpect.spawn` - like class
    :param prompt: shell prompt
    :type prompt: str
    :param source_filename: name of the file to upload
    :type source_filename: str
    :param destination_filename: where upload the file to
    :type destination_filename: str
    """
    delimiter = _random_delimiter()
    console.expect_exact(prompt)
    # Interactive shell line wrapping can cut the delimiter if the destination
    # filename is long enough. To mitigate this, we type the name on
    # one line and then type the delimiter on a new line.
    console.sendline(f"cat > {destination_filename} \\")
    console.expect_exact("\n")
    # Delimiter is quoted in order to disable parameter expansion etc. in the
    # here-document.
    console.sendline(f"<<'{delimiter}'")
    console.expect_exact(delimiter)
    console.send(Path(source_filename).read_bytes())
    console.sendline(delimiter)
    console.expect_exact(delimiter)
    console.expect_exact("\n")


def execute_program(console, prompt, program, timeout):
    """Execute a program remotely via a shell connection.

    :param console: console object
    :type console: :py:class:`pexpect:pexpect.spawn` - like class
    :param prompt: shell prompt
    :type prompt: str
    :param program: name of program to run
    :type program: str
    :param timeout: timeout for program execution in seconds
    :type timeout: int
    :return: program exit code
    :rtype: int
    """
    console.expect_exact(prompt)
    # Interactive shell line wrapping can cut a pattern if the program filename
    # is long enough. To mitigate this, we type the filename on a separate line.
    console.sendline(program + " \\")
    console.expect_exact("\n")
    command_part_2 = "; echo Exit code: $?."
    console.sendline(command_part_2)
    console.expect_exact(command_part_2)
    console.expect_exact("\n")
    console.expect(r"Exit code: (\d+).", timeout=timeout)
    exit_code_bytes = console.match.group(1)
    console.expect_exact("\n")
    return int(exit_code_bytes.decode())


def check_execute_program(console, prompt, program, timeout):
    """Execute a program remotely via a shell connection. Check exit code.

    :param console: console object
    :type console: :py:class:`pexpect:pexpect.spawn` - like class
    :param prompt: shell prompt
    :type prompt: str
    :param program: name of program to run
    :type program: str
    :param timeout: timeout for program execution in seconds
    :type timeout: int
    :raises alpy.utils.NonZeroExitCode: if the program exited with non-zero code
    """
    exit_code = execute_program(console, prompt, program, timeout)

    if exit_code != 0:
        raise alpy.utils.NonZeroExitCode(
            f"Program {program} exited with non-zero code {exit_code}"
        )


def upload_and_execute_script(console, prompt, filename, timeout):
    """Upload and execute a script via a shell connection. Check exit code.

    :param console: console object
    :type console: :py:class:`pexpect:pexpect.spawn` - like class
    :param prompt: shell prompt
    :type prompt: str
    :param filename: script filename
    :type filename: str
    :param timeout: timeout for program execution in seconds
    :type timeout: int
    :raises alpy.utils.NonZeroExitCode: if the script exited with non-zero code
    """
    logger = logging.getLogger(__name__)
    context_logger = alpy.utils.make_context_logger(logger)

    with context_logger("Type in script " + filename):
        upload_text_file(console, prompt, filename, filename)
        console.expect_exact(prompt)
        command = "chmod +x " + filename
        console.sendline(command)
        console.expect_exact(f"{command}\r\n")

    with context_logger("Run script " + filename):
        if timeout != console.timeout:
            logger.info(f"Timeout, seconds: {timeout}")
        check_execute_program(console, prompt, "./" + filename, timeout)
