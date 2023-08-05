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
import csv
import bz2
import gzip
import lzma
from logging import getLogger


# noinspection SqlNoDataSourceInspection
class CsvHandler():
    """
    Setup and write a SQLite3 database file.
    """

    def __init__(self, filename, clearfile, compression='plain'):
        """
        :param filename:     the name of the sqlite3 database
        :param compression:  the compression method
        :param clearfile:    clear the output file if True
        """
        self.filename = filename
        self.clearfile = clearfile

        self.log = getLogger('hcpmqe.' + __name__)

        # delete csv file if existent
        if self.clearfile:
            try:
                os.remove(filename)
                self.log.debug(f'deleted existing csv file "{filename}"')
            except (OSError) as e:
                self.log.debug(f'failed to delete csv file "{filename}" - {e}')

        compression = compression.strip("('").strip("',)")

        ## setup csv writer
        try:
            if compression == 'plain':
                self.filehdl = open(self.filename, 'a', newline='')
            elif compression == 'bz2':
                self.filehdl = bz2.open(self.filename, 'at', newline='', compresslevel=9)  # bzip2 -d -c test.csv.bz2
            elif compression == 'gzip':
                self.filehdl = gzip.open(self.filename, 'at', newline='', compresslevel=9)  # gunzip < test.csv.gzip
            elif compression == 'lzma':
                self.filehdl = lzma.open(self.filename, 'at', newline='')  # zcat < test.csv.lzma
            else:
                self.log.debug(f'unable to create csv file - {compression} compression unavailable')
                raise AttributeError(f'unable to create csv file - {compression} compression unavailable')
            self.log.debug(f'created csv file "{filename}" ({compression})')
        except Exception as e:
            self.log.debug(f'failed to create csv file "{filename}" - {e}')
            raise (e)

        self.opscreated = False  # signals that the header is not yet created

    def init_db(self):
        """
        This initializes the csv file - a dummy method.
        """
        self.log.debug('initializing the csv file')


    def __init_ops(self, rec):
        """
        Create the ops table, depending on the records received
        """
        self.csv = csv.DictWriter(self.filehdl, sorted(rec.keys()))
        self.csv.writeheader()
        self.log.debug(f'wrote csv header -> {list(rec.keys())}')


    def writeops(self, resultset):
        """
        Ingest all records in resultset into DB.
        """
        if not self.opscreated:  # create the ops table based on the first record
            self.__init_ops(resultset[0])
            self.opscreated = True

        self.csv.writerows(resultset)

        self.log.debug(f'wrote {len(resultset)} records into csv file')

    def close(self):
        self.filehdl.close()
        self.log.debug('closed csv file')
