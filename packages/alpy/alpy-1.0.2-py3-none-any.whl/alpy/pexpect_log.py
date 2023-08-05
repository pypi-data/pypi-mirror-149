# SPDX-License-Identifier: GPL-3.0-or-later

"""This module contains classes for writing logs from
:py:class:`pexpect:pexpect.spawn` - like class via Python
:py:mod:`python:logging` module.
"""


class Splitter:
    """This class splits data stream into chunks.

    Character stream and byte stream is supported.

    The chunks are defined as a sequence of zero or more characters (bytes)
    ending with a separator. Splitter consumes no more than `high` bytes when
    waiting for a separator. If the separator is not found (*overflow*),
    splitter emits shorter chunks of length `low` until a separator is found.

    :param sep: separator
    :type sep: str or bytes
    :param chunk_ready_callback: function to call to emit a chunk
    :type chunk_ready_callback: callable
    :param low: low threshold
    :type low: int
    :param high: high threshold
    :type high: int
    """

    def __init__(self, *, sep, chunk_ready_callback, low, high):
        self._sep = sep
        self._chunk_ready_callback = chunk_ready_callback
        self._empty_buffer = type(
            sep
        )()  # Make an empty string or byte sequence
        self._buf = self._empty_buffer
        self._low = low
        self._high = high
        self._overflow = False

    def write(self, data):
        """Feed some data.

        :param data: zero or more characters or bytes
        :type data: str or bytes
        """
        callback = self._chunk_ready_callback
        self._buf += data

        start = 0
        end = self._find_chunk_end(start)
        while end:
            callback(self._buf[start:end])
            start = end
            end = self._find_chunk_end(start)

        if start:
            self._buf = self._buf[start:]

    def flush(self):
        """Emit the remaining data if present."""
        if self._buf:
            callback = self._chunk_ready_callback
            callback(self._buf)
            self._buf = self._empty_buffer
            self._overflow = False

    def _find_chunk_end(self, start):
        window_size = self._low if self._overflow else self._high
        pos = self._buf.find(self._sep, start, start + window_size)

        if pos != -1:
            self._overflow = False
            return pos + len(self._sep)

        if len(self._buf) - start >= window_size:
            self._overflow = True
            return start + self._low

        return None


def format_bytes_for_logging(data):
    """Present data as a printable string.

    :param data: zero or more characters or bytes
    :type data: str or bytes
    :return: string representation
    :rtype: str
    """
    return repr(data)[1:]


class LogfileRead:
    """This class logs data read from a :py:class:`pexpect:pexpect.spawn` - like
    class via Python :py:mod:`python:logging` module.

    An instance of this class is a :std:term:`python:file object`. It should be
    assigned to the :py:attr:`pexpect:pexpect.spawn.logfile_read` attribute.

    :param logger: logger
    :type logger: :py:class:`python:logging.Logger`
    """

    def __init__(self, logger):
        log_function = lambda line: logger.debug(
            "< " + format_bytes_for_logging(line)
        )
        self._splitter = Splitter(
            sep=b"\n", chunk_ready_callback=log_function, low=20, high=120
        )

    def write(self, data):
        """Accumulate data and write it to the log.

        :param data: zero or more characters or bytes
        :type data: str or bytes
        """
        self._splitter.write(data)

    def flush(self):
        """Do nothing.

        This method is required by :py:class:`pexpect:pexpect.spawn` - like
        classes.
        """

    def log_remaining_text(self):
        """Log remaining text.

        This method should be called "flush", however `flush` is already in use.
        """
        self._splitter.flush()


class LogfileSend:
    """This class logs data sent to a :py:class:`pexpect:pexpect.spawn` - like
    class via Python :py:mod:`python:logging` module.

    An instance of this class is a :std:term:`python:file object`. It should be
    assigned to the :py:attr:`pexpect:pexpect.spawn.logfile_send` attribute.

    :param logger: logger
    :type logger: :py:class:`python:logging.Logger`
    """

    def __init__(self, logger):
        self._logger = logger

    def write(self, data):
        """Accumulate data and write it to the log.

        :param data: zero or more characters or bytes
        :type data: str or bytes
        """
        for line in LogfileSend._split_lines(data):
            self._logger.debug("> " + format_bytes_for_logging(line))

    def flush(self):
        """Do nothing.

        This method is required by :py:class:`pexpect:pexpect.spawn` - like
        classes.
        """

    @staticmethod
    def _split_lines(data):
        sep = b"\n"
        lines = data.split(sep)
        result = [line + sep for line in lines[:-1]]
        last_line = lines[-1]
        # Return at least one line, even if we only have one line and it is
        # empty.
        if len(lines) == 1 or last_line:
            result.append(last_line)
        return result
