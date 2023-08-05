# The MIT License (MIT)
#
# Copyright (c) 2021-2022 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Sos of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyrighftware without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copiet notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import socket
import logging
from logging.handlers import SysLogHandler

from hcilib.base.exceptions import ConfigError


def logger(level='INFO', syslog_ip=None, syslog_port=None,
           syslog_prot=None, syslog_facility=None):
    """
    Setup logging, either to journald or to console.

    :param level:            the log level (INFO or DEBUG)
    :param syslog_ip:        the syslog servers IP address
    :param syslog_port:      the syslog servers listening port
    :param syslog_prot:      either 'UDP' or 'TCP'
    :param syslog_facility:  the target facility
    """
    level = level.upper()

    if level not in ['INFO', 'DEBUG']:
        raise ConfigError(f'log level "{level}" is not supported')

    log = logging.getLogger()
    log.setLevel(logging.DEBUG if level == 'DEBUG' else logging.INFO)

    th = logging.StreamHandler()

    if level == 'DEBUG':
        th.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s  %(lineno)s : %(message)s'))
    else:
        th.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))

    log.addHandler(th)
    th.addFilter(logging.Filter('hcisle'))

    # adding a handler for syslog messages if requested
    if syslog_ip:
        sh = SysLogHandler((syslog_ip, syslog_port), syslog_facility,
                           socket.SOCK_DGRAM if syslog_prot == 'UDP' else socket.SOCK_STREAM)
        sh.setFormatter(logging.Formatter('%(message)s'))
        sh.addFilter(logging.Filter('SYSLOG'))
        log.addHandler(sh)
