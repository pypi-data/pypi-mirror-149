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

import sys
import zipfile
import tarfile
import re
import sqlite3
from logging import getLogger
from time import strptime, mktime
from datetime import date


class LogReader:
    """
    Handle reading the contents of an HCI Log Package.
    """

    def __init__(self, pkg, db):
        """
        :param pkg:         the name of the HCI log package zip file
        :param db:          a DB() object w/ an open database
        """
        self.log = getLogger('hcisle.' + __name__)

        self.pkg = pkg
        self.db = db

        self.stats = {'fnd': {'searchapp': 0,  # to count records found in the logs
                              'solrquery': 0},
                      'dup': {'searchapp': 0,  # to count records already in database
                              'solrquery': 0},
                      'new': {'searchapp': 0,  # to count new records in database
                              'solrquery': 0}
                      }

        try:
            self.zf = zipfile.ZipFile(self.pkg, mode='r',
                                      compression=zipfile.ZIP_STORED,
                                      allowZip64=True)
        except Exception as e:
            sys.exit('fatal: can\'t read {}\n\thint: {}'.format(self.pkg, e))

        self.log.debug(f'Namelist: {self.zf.namelist()}')

        # read HCPs cluster name and the nodes from the manifest file
        self.clusterid = ''
        self.nodes = {}
        self.snodes = {}
        self.failednodes = []  # lists nodes that are mentioned as not SUCCESSFUL or COMPLETE in the manifest
        self.log_starts = self.log_ends = ''

        self.clusterid, self.nodes, self.log_starts, self.log_ends = self._manifest(
            self.zf, f'manifest.csv')

        self.log.debug(f'Manifest results: {self.clusterid}|{self.nodes}|{self.log_starts}|{self.log_ends}')


    def _manifest(self, zf, file):
        """
        Read the manifest from a given ZIP file (or a handle to it).

        :param zf:    the ZipFile object
        :param file:  the file to read or a handle to a file
        :return:      a 4-tupe of (str(clusterid), dict(nodes),
                      str(log_starts), str(log_ends))
        """

        try:
            first = True
            act = False
            clusterid = ''
            log_ends = log_starts = None

            nodes = {}

            for line in zf.read(file).decode().replace('"', '').split('\n'):
                self.log.debug(f'manifest line: {line}')
                if first:
                    r = line.split(',')
                    try:
                        if r[0].lower() == 'cluster id':
                            clusterid = r[1].lower()
                    except Exception as e:
                        sys.exit(f'unable to read the cluster id from the '
                                 f'manifest file'
                                 f'\n\thint: {e}')
                    first = False
                    continue

                # grab the log start timestamp
                # Start time,Thu Oct 14 18:57:08 UTC 2021
                if line.startswith('Start time'):
                    _d = line.split(',')[1].split()
                    log_starts = date.fromtimestamp(mktime(
                        strptime(' '.join(_d[:3] + [_d[-1]]),
                                 '%a %b %d %Y')))
                # grab the log end timestamp
                # End time,Thu Oct 14 18:57:18 UTC 2021
                if line.startswith('End time'):
                    _d = line.split(',')[1].split()
                    log_ends = date.fromtimestamp(mktime(
                        strptime(' '.join(_d[:3] + [_d[-1]]),
                                 '%a %b %d %Y')))

                # find the line before the list of nodes:
                # ==> "Node IP","Log File Path in Archive","Size","Status"
                if not act:
                    if line.startswith('Node IP'):
                        act = True
                else:
                    line = line.strip()
                    # end if an empty line is found:
                    if not line:
                        break

                    # line == '192.168.0.120,log_192_168_0_120_.tar.gz,237930,SUCCESSFUL'
                    line = line.split(',')

                    # node type decision
                    if '.tar.' in line[1]:  # G-node (or equivalent)
                        # node collection and failed log generation test
                        if line[3].lower().startswith('success'):
                            nodes[line[0]] = line[1]
                        else:
                            self.failednodes.append(line[0])
        except Exception as e:
            sys.exit(f'Fatal: unable to read the manifest file\n\thint: {e}')

        return clusterid, nodes, str(log_starts), str(log_ends)

    def extract(self):
        """
        Pre-handler, used to handle HCP-S Log packages within HCP Log packages
        """
        for node in self.nodes:
            self.log.info(f'processing node {node}')
            self._extract(self.zf, node, self.nodes[node])

    def _extract(self, zf, node, path):
        """
        Extract files from a specific nodes subpackage and send them to their
        respective handlers for further processing.

        :param zf:      the ZipFile object to read from
        :param node:    the node to work with
        :param path:    the path within the archive
        """
        self.log.debug(f'Extracting data of node: {node} ')

        with zf.open(path, mode='r') as hdl:
            t = tarfile.open(fileobj=hdl, mode='r|*')
            while True:
                n = t.next()
                if not n:
                    _msg = ''
                    self.log.debug('done {} {}'.format('-' if _msg else '', _msg))
                    break
                self.log.debug(f'file found: {n.name}')

                # Search App logfiles
                if re.match('.*com.hds.ensemble.plugins.service.searchApp', n.name) \
                        and n.name.split('/')[-1].startswith('default_access_log'):
                    with t.extractfile(n) as f:
                        for line in f.readlines():
                            line = line.decode().strip()
                            if re.match('.*/api/search/query/federated', line) or \
                                    re.match('.*/api/workflow/indexes/[a-f\d-]*/rawQuery', line):
                                try:
                                    self.stats['fnd']['searchapp'] += 1
                                    self.db.add_searchapp(line)
                                except sqlite3.IntegrityError as e:
                                    self.stats['dup']['searchapp'] += 1
                                else:
                                    self.stats['new']['searchapp'] += 1
                    continue

                # solr.log* and/or solr.service* files
                if re.match('.*/com.hds.ensemble.plugins.service.solr/', n.name) \
                        and (n.name.split('/')[-1].startswith('solr.log')
                             or n.name.split('/')[-1].startswith('solr-service')):
                    self.log.debug(f'extracting: {n.name}')
                    with t.extractfile(n) as f:
                        for line in f.readlines():
                            line = line.decode().strip()
                            if re.match('.*&q=', line):
                                if not re.match('.*&q=HCI_autocomplete', line) \
                                        and not re.match('.*&q=\\*', line):
                                    self.log.debug(f'rec={line}')
                                    try:
                                        self.stats['fnd']['solrquery'] += 1
                                        self.db.add_solrquery(line)
                                    except ValueError:
                                        self.stats['fnd']['solrquery'] -= 1
                                    except sqlite3.IntegrityError as e:
                                        self.stats['dup']['solrquery'] += 1
                                    else:
                                        self.stats['new']['solrquery'] += 1
                    continue

    def close(self):
        """
        Close the ZIPFILE.
        """
        self.zf.close()
