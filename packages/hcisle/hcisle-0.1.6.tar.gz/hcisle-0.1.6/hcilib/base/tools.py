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

import argparse
import sys
from os.path import isdir

from hcilib.version import Gvars


def parseargs():
    """
    args - build the argument parser, parse the command line.
    """
    mp = argparse.ArgumentParser()
    mp.add_argument('--version', action='version',
                    version="%(prog)s: {0}\n"
                    .format(Gvars.Version))
    mp.add_argument('--logpackage', dest='logpackage', required=False,
                    default='',
                    help='Optional HCI log package (instead of collecting logs from HCI)')
    mp.add_argument('--vacuumdb', dest='vacuumdb', required=False, type=int,
                    default=31, metavar='DAYS',
                    help='DB maintenance: remove sent records older than DAYS from the database '
                         'and VACUUM it afterwards (default: 31 days)')
    mp.add_argument('-i', dest='installdir', required=False,
                    default='/opt/hci',
                    help='HCI installation folder (default: /opt/hci)')
    mp.add_argument('-d', dest='logdir', required=False,
                    default='/opt/hcisle',
                    help='Folder for collected logs (default: /opt/hcisle)')
    mp.add_argument('-D', dest='db', required=False,
                    default='/opt/hcisle/log.db',
                    help='Database to store the logs (default: /opt/hcisle/log.db)')
    mp.add_argument('-L', dest='loglevel', required=False, choices=['info', 'debug'],
                    default='info',
                    help='Logging level (default: info)')
    mp.add_argument('--syslog-ip', dest='syslog_ip', required=False,
                    metavar='IP', default='',
                    help='Syslog server IP address')
    mp.add_argument('--syslog-port', dest='syslog_port', required=False,
                    metavar='PORT', default='514', type=int,
                    help='Syslog server port (default: 514)')
    mp.add_argument('--syslog-prot', dest='syslog_prot', required=False,
                    choices=['UDP', 'TCP'], default='UDP',
                    help='Syslog server protocol (default: UDP)')
    mp.add_argument('--syslog-facility', dest='syslog_facility', required=False,
                    metavar='FACILITY', default='local0',
                    help='Syslog facility (default: local0)')

    result = mp.parse_args()

    # check for paths to be available
    if not result.logpackage:
        if not isdir(result.installdir):
            sys.exit(f"Fatal: install path {result.installdir} doesn't exist")
        if not isdir(result.logdir):
            sys.exit(f"Fatal: install path {result.logdir}' doesn't exist")

    return result
