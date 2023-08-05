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

import json
from logging import getLogger
from os.path import expanduser
from pathlib import PurePath
from time import time, strftime, localtime
from copy import deepcopy


class Configuration():
    """
    Read/Write configuration to disk.

    Configuration file is in ~/.hcpmqe.conf, in json format.
    """

    def __init__(self):
        self.log = getLogger('hcpmqe.' + __name__)

    def emptyconfig(self):
        """
        Create an empty configuration structure.
        """
        self.conf = {'url': '',
                     'user': '',
                     'password': '',
                     'count': 2500,
                     'throttle': 0,
                     'timeout': 60,
                     'namespaces': [],
                     'directories': [],
                     'transactions': ['CREATE'],
                     'starttime': strftime('%Y-%m-%d %H:%M:%S%z', localtime(0)),
                     'endtime': strftime('%Y-%m-%d %H:%M:%S%z', localtime()),
                     'verbose': False,
                     'dbformat': 'sqlite3',
                     'compression': 'plain',
                     'dbfile': '',
                     'lastResult': {
                         'urlName': '',
                         'changeTimeMilliseconds': '',
                         'version': ''
                     },
                     }

    def readconfig(self, file=None) -> dict:
        """
        Read the configuration file from a side file.

        :param file:  the name of the data file chosen by the user
        :return:      the configuration dict
        """
        readfromdisk = False
        try:
            with open(file, 'r') as rhdl:
                self.conf = json.load(rhdl)
                readfromdisk = True
                self.log.debug(f'read configuration from {file}')
        except Exception as e:
            self.log.debug(f'unable to read configuration from {file} ({e}) - '
                             f'using default values')
            self.emptyconfig()

        return self.conf, readfromdisk

    def updateconf(self, values):
        """
        Update the conf dict with the windows content.

        :param values:  the pysimpleguy values object
        """
        self.conf['url'] = values['-URL-']
        self.conf['user'] = values['-USER-']
        self.conf['password'] = values['-PASSWORD-']
        self.conf['count'] = int(values['-COUNT-'])
        self.conf['throttle'] = values['-THROTTLE-']
        self.conf['timeout'] = values['-TIMEOUT-']
        self.conf['namespaces'] = values['-NAMESPACES-']
        self.conf['directories'] = values['-DIRECTORIES-']
        self.conf['transactions'] = [x[4:-1] for x in values.keys() if str(x).startswith('-TP-') and values[x]]
        self.conf['starttime'] = values['-STARTTIME-']
        self.conf['endtime'] = values['-ENDTIME-']
        self.conf['verbose'] = values['-VERBOSE-']
        self.conf['dbformat'] = 'csv' if values['-CSV-'] else 'sqlite3'
        self.conf['compression'] = values['-COMPRESSION-'].strip("('").strip("',)")
        self.conf['dbfile'] = values['-FILE-']
        if '-LAST-URL-' in values and '-LAST-VERSION-' in values and '-LAST-CHGTIMEMS-' in values:
            self.conf['lastResult'] = {'urlName': values['-LAST-URL-'],
                                       'changeTimeMilliseconds': values['-LAST-CHGTIMEMS-'],
                                       'version': values['-LAST-VERSION-']
                                       }
        else:
            self.conf['lastResult'] = {}

        self.log.debug('updated conf from window entries')

    def writeconfig(self, file) -> bool:
        """
        Write the configuration to a file.

        :param file:  the name of the file chosen by the user
        :returns:    True if successfull, else False
        """
        c = deepcopy(self.conf)
        del c['password']  # we don't want a password to be stored to disk, right?
        try:
            with open(file, 'w') as whdl:
                json.dump(c, whdl, indent=2)
                self.log.debug(f'wrote config to file {file}')
                return True
        except Exception as e:
            self.log.debug(f'unable to write configuration to file {file} ({e}) - skipping')
            return False

