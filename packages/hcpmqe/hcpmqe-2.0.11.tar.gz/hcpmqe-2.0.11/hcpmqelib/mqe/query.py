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

import sys
import os
import httpx
import ssl
from base64 import b64encode
from hashlib import md5
from time import time, sleep, strptime
from calendar import timegm
from threading import Thread
from copy import deepcopy
from logging import getLogger

from . import qtemplate
from ..db import CsvHandler
from ..db import DbHandler


class HttpError(Exception):
    """
    Class for HTTP connection exceptions.
    """


class MqeQuery(Thread):
    """
    A class that handles queries to the HCP MQE API.
    """

    def __init__(self, window, conf, cancel, clearfile, *args, **kwargs):
        """
        :param window:  the calling pySimpleGui window
        :param conf:    a dict of configuration values
        :param cancel:  an Event object, used to signal a stop request
        :param clearfile:  clear the output file if True
        """
        self.log = getLogger('hcpmqe.' + __name__)

        super().__init__(*args, **kwargs)
        self.window = window
        self.conf = conf
        self.cancel = cancel  # used to cancel the query
        self.clearfile = clearfile
        # exposed variables, can be changed during a run
        self.__pagesize = self.conf['count']
        self.__throttle = int(float(self.conf['throttle']))
        self.__timeout = self.conf['timeout']

        self.qdict = deepcopy(qtemplate)
        self.count = 0

    @property
    def pagesize(self):
        return self.__pagesize

    @pagesize.setter
    def pagesize(self, value):
        self.__pagesize = int(value)

    @property
    def throttle(self):
        return self.__throttle

    @throttle.setter
    def throttle(self, value):
        self.__throttle = int(value)

    @property
    def timeout(self):
        return self.__timeout

    @throttle.setter
    def timeout(self, value):
        self.__timeout = int(value)

    def run(self):
        """
        Run the query.
        """
        if self.conf['dbformat'] == 'sqlite3':
            self.db = DbHandler(self.conf['dbfile'], self.clearfile)
        else:
            self.db = CsvHandler(self.conf['dbfile'], self.clearfile, compression=self.conf['compression'])

        # setup a non-verifying SSL-context
        # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # context = ssl.create_default_context()
        # context.check_hostname = False
        # context.verify_mode = ssl.CERT_NONE

        self.log.debug(f'request timeout is set to {self.__timeout} seconds')
        self.ses = httpx.Client(base_url='https://' + self.conf['url'],
                                # verify=context,
                                verify=False,
                                timeout=self.__timeout,
                                headers={
                                    'Authorization': f'HCP {b64encode(self.conf["user"].encode()).decode()}:'
                                                     f'{md5(self.conf["password"].encode()).hexdigest()}',
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'}
                                )

        if self.conf['lastResult']['urlName'] and self.conf['lastResult']['changeTimeMilliseconds'] and \
                self.conf['lastResult']['version']:
            lastResult = self.conf['lastResult']
        else:
            lastResult = {}
        first = True
        while True:
            if self.cancel.is_set():
                self.db.close()
                self.ses.close()
                try:  # this will cause a runtime error when the thread ends too quickly, thus ignored
                    self.window.write_event_value('-QTHREAD-ERROR-', ('Query was canceled',))
                except:
                    pass
                return

            try:
                count, urlName, changeTimeMilliseconds, version, finished, qduration, dbduration = self.__query(
                    lastResult=lastResult)
            except HttpError as e:
                self.db.close()
                try:  # this will cause a runtime error when the thread ends too quickly, thus ignored
                    self.window.write_event_value('-QTHREAD-ERROR-', (f'{e}',))
                except:
                    pass
                return

            first = first if not first else False

            if not finished:
                # update window with the latest stats...
                self.window.write_event_value('-QTHREAD-', (count, urlName, version, changeTimeMilliseconds, finished))

                lastResult = {'urlName': urlName,
                              'changeTimeMilliseconds': changeTimeMilliseconds,
                              'version': version
                              }
                if self.__throttle:
                    self.window.write_event_value('-QTHREAD-STATUS-', (f'DB insert took {dbduration:.2f} seconds '
                                                                       f'- now throttling for {int(self.__throttle)} seconds...',
                                                                       'db', dbduration))
                    sleep(int(self.__throttle))
                self.window.write_event_value('-QTHREAD-STATUS-', (f'DB insert took {dbduration:.2f} seconds - '
                                                                   f'now continue with query for next page...',
                                                                   'db', dbduration))

            else:
                self.db.close()
                self.ses.close()
                # signal window that we are finished...
                try:  # this will cause a runtime error when the thread ends too quickly, thus ignored
                    self.window.write_event_value('-QTHREAD-', (count, urlName, version, changeTimeMilliseconds, finished))
                except:
                    pass
                return

    def __query(self, lastResult={}):
        """
        Make a query against the MQE API.

        :param lastResults: a dict holding values for the next page
        """
        # self.qdict['operation']['count'] = self.conf['count']
        self.qdict['operation']['count'] = self.__pagesize
        if lastResult:
            self.qdict['operation']['lastResult'] = {'urlName': lastResult['urlName'],
                                                     'changeTimeMilliseconds': lastResult['changeTimeMilliseconds'],
                                                     'version': lastResult['version']}
        self.qdict['operation']['systemMetadata']['changeTime']['start'] = self.conf['starttime'].replace(' ', 'T')
        self.qdict['operation']['systemMetadata']['changeTime']['end'] = self.conf['endtime'].replace(' ', 'T')
        self.qdict['operation']['systemMetadata']['directories']['directory'] = \
            self.conf['directories'].split(',') if self.conf['directories'] else []
        self.qdict['operation']['systemMetadata']['namespaces']['namespace'] = \
            self.conf['namespaces'].split(',') if self.conf['namespaces'] else []
        self.qdict['operation']['systemMetadata']['transactions']['transaction'] = self.conf['transactions']
        self.qdict['operation']['verbose'] = self.conf['verbose']

        qduration = 0
        try:
            self.log.debug('now sending query')
            qduration = time()
            r = self.ses.post('/query', json=self.qdict)
            qduration = time() - qduration
        except Exception as e:
            raise HttpError(f'fatal: query failed ({e})')
        else:
            if r.status_code == 403:
                self.log.debug(f'fatal: {r.status_code} - {r.reason_phrase}')
                raise HttpError(f'fatal: {r.status_code} - {r.reason_phrase}')
            elif r.status_code != 200:
                self.log.debug(f'fatal: {r.status_code} - {r.headers["X-HCP-ErrorMessage"]}')
                raise HttpError(f'fatal: {r.status_code} - {r.headers["X-HCP-ErrorMessage"]}')
            else:
                self.log.debug(f'status_code = {r.status_code}')
                res = r.json()
                # print(res)
                # {'queryResult': {'query': {'end': 1603745726000, 'start': 0},
                #                  'resultSet': [{'accessTime': 1600781077,
                #                                 'accessTimeString': '2020-09-22T15:24:37+0200',
                #                                 'acl': False,
                #                                 'changeTimeMilliseconds': '1600781077330.00',
                #                                 'changeTimeString': '2020-09-22T15:24:37+0200',
                #                                 'customMetadata': False,
                #                                 'customMetadataAnnotation': '',
                #                                 'dpl': 1,
                #                                 'gid': 0,
                #                                 'hash': 'MD5 04CBFB438DE89F42FD8C2B426FF44E40',
                #                                 'hashScheme': 'MD5',
                #                                 'hold': False,
                #                                 'index': True,
                #                                 'ingestTime': 1600781077,
                #                                 'ingestTimeString': '2020-09-22T15:24:37+0200',
                #                                 'namespace': 'p-demo.s3',
                #                                 'objectPath': '/Pictures/x1b1YDoKapI.jpg',
                #                                 'operation': 'CREATED',
                #                                 'owner': 'USER,s3,s3user',
                #                                 'permissions': 555,
                #                                 'replicated': True,
                #                                 'replicationCollision': False,
                #                                 'retention': 0,
                #                                 'retentionClass': '',
                #                                 'retentionString': 'Deletion Allowed',
                #                                 'shred': False,
                #                                 'size': 252473,
                #                                 'type': 'object',
                #                                 'uid': 0,
                #                                 'updateTime': 1600781077,
                #                                 'updateTimeString': '2020-09-22T15:24:37+0200',
                #                                 'urlName': 'https://p-demo.s3.hcp80.archivas.com/rest/Pictures/x1b1YDoKapI.jpg',
                #                                 'utf8Name': 'x1b1YDoKapI.jpg',
                #                                 'version': 102449988933185}],
                #                  'status': {'code': 'INCOMPLETE', 'message': '', 'results': 1}}}

                self.window.write_event_value('-QTHREAD-STATUS-',
                                              (f'query took {qduration:.2f} seconds - now inserting '
                                               f'{res["queryResult"]["status"]["results"]:,} records into database',
                                               'query', qduration))
                dbduration = time()
                try:
                    self.db.writeops(res["queryResult"]["resultSet"])
                except Exception as e:
                    raise HttpError(f'fatal: writing to DB file went wrong - {e}')
                dbduration = time() - dbduration

                self.count += res["queryResult"]["status"]["results"]

        if res['queryResult']['resultSet']:
            return self.count, \
                   res['queryResult']['resultSet'][-1]['urlName'], \
                   res['queryResult']['resultSet'][-1]['changeTimeMilliseconds'], \
                   res['queryResult']['resultSet'][-1]['version'], \
                   True if res["queryResult"]["status"]["code"] == 'COMPLETE' else False, \
                   qduration, dbduration

        return self.count, '', '', '', \
               True if res["queryResult"]["status"]["code"] == 'COMPLETE' else False, qduration, dbduration
