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

import sqlite3
import re
from logging import getLogger
from datetime import datetime, timedelta
from os import access, F_OK
from hashlib import sha256

from hcilib.version import Gvars


class Db:
    """
    Handle the search log database.
    """

    def __init__(self, db):
        """
        :param db:  the database file
        """
        self.log = getLogger('hcisle.' + __name__)
        self.syslog = getLogger('SYSLOG')  # to send records to syslog
        self.db = db
        self.__opendb()
        self.__checkdb()

    def __opendb(self):
        """
        Create (if needed), check and open the database.
        """
        self.log.debug(f'Try to open database {self.db}')
        if access(self.db, F_OK) or self.db == ':memory:':
            try:
                self.con = sqlite3.connect(self.db, detect_types=sqlite3.PARSE_DECLTYPES)
            except sqlite3.DatabaseError as e:
                self.log.error(f'open of database {self.db} failed ({e})')
                raise
            self.con.row_factory = sqlite3.Row
        else:
            self.log.debug('database {} not found'.format(self.db))
            self.con = sqlite3.connect(self.db, detect_types=sqlite3.PARSE_DECLTYPES)
            self.con.row_factory = sqlite3.Row

            self.__createdb()

    def __checkdb(self):
        """
        Check is we have a valid DB.
        """
        self.log.debug(f'checking database {self.db} for being valid')
        cur = self.con.execute("SELECT count(name) FROM sqlite_master "
                               "     WHERE type='table' AND name='admin'")
        rec = cur.fetchone()

        if not rec['count(name)']:
            self.log.error(f'database {self.db} is not a valid hcpinsight database')
            raise sqlite3.DatabaseError('database is not a valid hcpinsight database')

        cur = self.con.execute('SELECT * FROM admin')
        rec = cur.fetchone()
        if rec:
            if not rec['magic'].startswith('hcisle'):
                self.log.error(f'database {self.db} is not a valid hcisle '
                               f'database (invalid magic number)')
                raise sqlite3.DatabaseError(
                    'database is not a valid hcisle database (invalid magic number)')
        else:
            self.log.error(f'database {self.db} is not a valid hcisle database')
            raise sqlite3.DatabaseError('database is not a valid hcisle database')

    def __createdb(self):
        """
        Setup a new database.
        """
        self.log.debug(f'creating new database {self.db}')
        self.con.execute("CREATE TABLE admin (magic TEXT,\n"
                         "                    creationdate timestamp ,\n"
                         "                    clusterid TEXT,\n"
                         "                    nodes TEXT)")
        self.con.commit()

        self.con.execute("INSERT INTO admin (magic, creationdate)"
                         "       VALUES (?, ?)",
                         (f'hcisle {Gvars.s_version}', datetime.now(),))
        self.con.commit()

        self.con.execute("CREATE TABLE searchapp (timestamp TEXT,\n"
                         "                        hash TEXT,\n"
                         "                        timestampstr TEXT,\n"
                         "                        user TEXT,\n"
                         "                        sent TEXT,\n"
                         "                        record TEXT)")
        self.con.execute("CREATE UNIQUE INDEX searchapp_idx ON searchapp(timestamp, hash) ")
        self.con.commit()

        self.con.execute("CREATE TABLE solrquery (timestamp TEXT,\n"
                         "                        hash TEXT,\n"
                         "                        timestampstr TEXT,\n"
                         "                        filter TEXT,\n"
                         "                        query TEXT,\n"
                         "                        sent TEXT,\n"
                         "                        record TEXT)")
        self.con.execute("CREATE UNIQUE INDEX solrquery_idx ON solrquery(timestamp, hash) ")
        self.con.commit()

    def add_searchapp(self, rec):
        """
        Add a record indicating a query to the Search App.

        :param rec:  the record
        """
        _rec = rec.split()
        timestamp = datetime.strptime(f'{_rec[3]} {_rec[4]}', '[%d/%b/%Y:%H:%M:%S %z]').timestamp()

        dbrec = {'timestamp': timestamp,
                 'hash': sha256(rec.encode()).hexdigest(),
                 'timestampstr': datetime.fromtimestamp(timestamp).strftime('%c'),
                 'user': _rec[2],
                 'sent': 'N',
                 'record': rec
                 }

        self.log.debug(f'db insert: {dbrec["timestamp"]}|{dbrec["hash"]}|{dbrec["timestampstr"]}|'
                       f'{dbrec["user"]}|{dbrec["record"]}')

        self.con.execute('INSERT INTO searchapp'
                         '       (timestamp, hash, timestampstr, user, sent, record) VALUES'
                         '       (:timestamp, :hash, :timestampstr, :user, :sent, :record)',
                         dbrec)

        self.con.commit()

    def add_solrquery(self, rec):
        """
        Add a SOLR query record.

        :param rec:  the record
        """
        # get timestamp or skip this record
        _m = re.search('NOW=(?P<timestamp>\d*)', rec)
        if _m and _m.group('timestamp'):
            timestamp = float(_m.group('timestamp'))/1000
        else:
            raise ValueError()  # we're dropping records w/o the NOW tag, as they are not of interest.
        # search for patterns needed
        _filter = re.search('&fq=(?P<filter>[^&]*)&', rec)
        _query = re.search('&q=(?P<query>[^&]*)&', rec)

        _rec = rec.split()
        dbrec = {'timestamp': timestamp,
                 'hash': sha256(rec.encode()).hexdigest(),
                 'timestampstr': datetime.fromtimestamp(timestamp).strftime('%c'),
                 'filter': _filter.group('filter') if _filter else '',
                 'query': _query.group('query') if _query else '',
                 'sent': 'N',
                 'record': rec
                 }

        self.log.debug(f'db insert: {dbrec["timestamp"]}|{dbrec["hash"]}|{dbrec["timestampstr"]}|'
                       f'{dbrec["filter"]}|{dbrec["query"]}|{dbrec["record"]}')

        self.con.execute('INSERT INTO solrquery'
                         '       (timestamp, hash, timestampstr, filter, query, sent, record) VALUES'
                         '       (:timestamp, :hash, :timestampstr, :filter, :query, :sent, :record)',
                         dbrec)

        self.con.commit()
        return dbrec["hash"]

    def logallqueries(self):
        """
        Debug method: scan database for all query strings found since last time records
        were sent to syslog, return a set().
        """
        self.log.debug('fetching all query strings from solrquery')

        qs = set()
        cur = self.con.execute("SELECT query FROM solrquery WHERE sent='N'")
        for rec in cur.fetchall():
            qs.add(rec['query'])

        self.log.debug(f'captured query strings:')
        self.log.debug(f'{qs}')

    def sendsyslog(self):
        """
        Submit records from both 'searchapp' and 'solrquery' table to syslog.
        """
        self.log.debug('now sending records to syslog server')

        cnt = 0  # record counter

        # read the recs from the tables and send them to syslog
        cur = self.con.execute("SELECT timestamp, hash, record, tab" \
                               "  FROM (" \
                               "    SELECT timestamp, hash, record, 'searchapp' as tab FROM searchapp" \
                               "      WHERE sent='N'" \
                               "    UNION ALL" \
                               "    SELECT timestamp, hash, record, 'solrquery' as tab FROM solrquery" \
                               "      WHERE sent='N'" \
                               "    ) t" \
                               "  Order BY t.timestamp ASC")

        while True:
            rec = cur.fetchone()
            if not rec:
                break
            self.syslog.info(f'{rec["record"]}')
            cnt +=1

            # update the 'sent' column
            if rec['tab'] == 'searchapp':
                self.con.execute('UPDATE searchapp SET sent="Y" WHERE timestamp=:timestamp and hash=:hash',
                                 {'timestamp': rec['timestamp'],
                                  'hash': rec['hash']})
            else:
                self.con.execute('UPDATE solrquery SET sent="Y" WHERE timestamp=:timestamp and hash=:hash',
                                 {'timestamp': rec['timestamp'],
                                  'hash': rec['hash']})
            self.con.commit()

        self.log.info(f'records sent to syslog: {cnt}')


    def maintenance(self, days):
        """
        Database maintenance: remove sent records older than <days> and VACUUM the DB.

        :param days:  days to keep in the database
        """
        rmdate = datetime.now() - timedelta(days=days)
        rmtill = rmdate.timestamp()

        self.log.info(f'now removing records sent to syslog prior to {rmdate.ctime()}')

        cur = self.con.execute('DELETE FROM searchapp WHERE sent="Y" and timestamp<:timestamp',
                               {'timestamp': rmtill})
        self.log.info(f'removed {cur.rowcount} records from the searchapp table')
        self.con.commit()

        cur = self.con.execute('DELETE FROM solrquery WHERE sent="Y" and timestamp<:timestamp',
                               {'timestamp': rmtill})
        self.log.info(f'removed {cur.rowcount} records from the solrquery table')
        self.con.commit()

        self.log.info('now running DB VACUUM')
        self.con.execute('VACUUM')
        self.log.info('DB VACUUM done')


    def close(self):
        """
        Close the database.
        """
        self.con.close()

