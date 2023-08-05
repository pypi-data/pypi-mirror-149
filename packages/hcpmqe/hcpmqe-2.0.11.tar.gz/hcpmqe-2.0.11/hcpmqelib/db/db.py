# The MIT License (MIT)
#
# Copyright (c) 2012-2022 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sqlite3
from time import strftime, localtime, time
from logging import getLogger

from ..version import Gvars


# noinspection SqlNoDataSourceInspection
class DbHandler():
    """
    Setup and write a SQLite3 database file.
    """

    def __init__(self, filename, clearfile):
        """
        :param filename:   the name of the sqlite3 database
        :param clearfile:  clear the output file if True
        """
        self.filename = filename
        self.clearfile = clearfile

        self.log = getLogger('hcpmqe.' + __name__)

        # delete database file if existant
        if self.clearfile:
            try:
                os.remove(filename)
                self.log.debug(f'deleted existing db file "{filename}"')
            except (OSError) as e:
                self.log.debug(f'failed to delete db file "{filename}" - {e}')
                pass

        ## setup database
        try:
            self.dbConn = sqlite3.connect(self.filename)
            self.dbConn.isolation_level = None  # use AUTOCOMMIT mode
            self.log.debug(f'connected to DB file "{filename}"')
        except sqlite3.DatabaseError as e:
            self.log.debug(f'failed to connect to DB file "{filename}" - {e}')
            raise (e)

        self.opscreated = False  # signals that the ops table is not yet created
        self.ic = None

    def __init_db(self):
        """
        This initializes the database with the proper tables.
        """
        self.log.debug('initializing the database')
        self.ic = self.dbConn.cursor()

        dbSchema = {"admin": '''CREATE TABLE admin
                                (magic           TEXT,
                                 version         TEXT,
                                 creation        TEXT)'''
                    }

        # initialize the needed database tables
        for k in dbSchema.keys():
            self.ic.execute(dbSchema[k])

        # write admin record
        self.ic.execute('INSERT INTO admin VALUES (?,?,?)', ('hcpmqt', Gvars.Version,
                                                             strftime("%a, %Y/%m/%d, %H:%M:%S",
                                                                      localtime(time()))))

        self.dbConn.commit()

    def __init_ops(self, fullinit, rec):
        """
        Create the ops table, depending on the records received

        :param fullinit:  create the table if True
        :param rec:       the first record to carve the columns from
        """
        if fullinit:
            schema = f'CREATE TABLE ops ({", ".join(sorted(rec.keys())).replace("index", "_index")})'
            self.log.debug(f'Schema -> {schema}')
            self.ic.execute(schema)
            self.dbConn.commit()

        self.insert = f'INSERT INTO ops ({", ".join([x for x in rec.keys()]).replace("index", "_index")}) ' \
                      f'VALUES ({", ".join([f":{x}" for x in rec.keys()])})'
        self.log.debug(f'self.insert -> {self.insert}')

    def writeops(self, resultset):
        """
        Ingest all records in resultset into DB.
        """
        if not self.opscreated:  # in case this is the first record...
            if self.clearfile:   # ...create the ops table based on the first record
                self.__init_db()
            self.opscreated = True
            try:
                self.__init_ops(self.clearfile, resultset[0])
            except IndexError as e:
                self.log.debug(f'resultset was empty - inserted {len(resultset)} records into db')
                return

        if not self.ic:
            self.ic = self.dbConn.cursor()

        # Using a transaction speeds up DB inserts drastically, as it turns off auto-commit
        # of every single INSERT, in exchange for just one commit for the while batch.
        # In addition, it allows for a clean continuation in case the query got stuck due
        # to an error.
        self.ic.execute('BEGIN IMMEDIATE TRANSACTION')
        self.ic.executemany(self.insert, resultset)

        self.dbConn.commit()
        self.log.debug(f'inserted {len(resultset)} records into db')

    def close(self):
        self.dbConn.close()
        self.log.debug('closed db')
