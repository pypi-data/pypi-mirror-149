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

import logging
import sqlite3
from time import sleep
from os import unlink

from hcilib.base.tools import parseargs
from hcilib.version import Gvars
from hcilib.loghandler import logger
from hcilib.db import Db
from hcilib.collect import collect
from hcilib.ziphandler import LogReader


def main():
    opts = parseargs()

    # set up logging
    try:
        logger(level=opts.loglevel.upper(),
               syslog_ip=opts.syslog_ip, syslog_port=opts.syslog_port,
               syslog_prot=opts.syslog_prot, syslog_facility=opts.syslog_facility)
        log = logging.getLogger('hcisle')
    except Exception as e:
        exit(f'Fatal: error when setting up logging:\n{e}')

    log.info(f'{Gvars.Executable} {Gvars.Version}')
    log.debug(f'args: {str(opts)}')

    # setup logging to syslog
    if not opts.syslog_ip:
        log.info('forwarding to syslog server is disabled')
    
    # 1. Open the database
    try:
        db = Db(opts.db)  # check and open the database
    except Exception as e:
        log.error(f'Fatal: open database {opts.db} failed ({e})')
        import traceback
        traceback.print_exc()
        exit(code=1)

    # 2. Collect the logs
    if not opts.logpackage:
        log.info('collecting logs')
        logpkg = collect(opts.installdir, opts.logdir)
        # logpkg = '/opt/hci/logs_1634240828405.zip'
    else:
        log.info(f'NOT collecting logs - using {opts.logpackage} instead')
        logpkg = opts.logpackage
    log.info(f'log package: {logpkg}')

    # 3. unpack the logs (LogReader)
    try:
        lr = LogReader(logpkg, db)
        # this will give us a dict with the node IDs and their IP addresses
        clusterid = lr.clusterid
        nodes = lr.nodes.keys()
        # db.updateHcp(hcpname, nodes, snodes)
        log.info('working on HCI: {}'.format(clusterid))
        log.info('log package covering {} to {}'.format(lr.log_starts, lr.log_ends))
        log.info(f'nodes in the log package: {", ".join(nodes)}')
        if lr.failednodes:
            log.error(f'nodes where the log generation in {clusterid} failed: {", ".join(lr.failednodes)}')
            sleep(1)

        lr.extract()
    except sqlite3.DatabaseError as e:
        log.error('Fatal: {}'.format(e))
        exit(1)
    except KeyboardInterrupt:
        log.error('Fatal: execution aborted by user')
        exit(2)
    except Exception as e:
        import traceback
        traceback.print_exc()
        log.error('Fatal: extracting logs failed\nhint: {}'.format(e))
        exit(1)
    else:
        log.info(f'log records found: {lr.stats["fnd"]["searchapp"]} (searchapp),'
                 f' {lr.stats["fnd"]["solrquery"]} (solrquery)')
        log.info(f'thereof ignored (duplicate) log records: {lr.stats["dup"]["searchapp"]} (searchapp),'
                 f' {lr.stats["dup"]["solrquery"]} (solrquery)')
        db.logallqueries()

    lr.close()  # close zipreader

    # 4. Send the collected records to a syslog server
    if opts.syslog_ip:
        db.sendsyslog()

    # 5. DB maintenance
    db.maintenance(opts.vacuumdb)

    db.close()  # close the database

    # remove the log package
    if not opts.logpackage:
        try:
            unlink(logpkg)
        except OSError as e:
            log.error(f'deleting log package {logpkg} failed ({e})')
        else:
            log.info(f'cleaned up log package {logpkg}')
    else:
        log.info(f'leaving log package {opts.logpackage} untouched')
