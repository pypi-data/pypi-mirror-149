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

qtemplate = {'operation': {'count': 'num-recs-requested',
                           # commented out, as it is not needed in the 1st request
                           # 'lastResult': {'urlName': 'object-url',
                           #                'changeTimeMilliseconds': 'change-time-in-milliseconds.index',
                           #                'version': 'version-id'
                           #                },
                           # 'objectProperties': 'comma-separated-list-of-properties',
                           'systemMetadata': {'changeTime': {'start': 'start-time-in-milliseconds',
                                                             'end': 'end-time-in-milliseconds'
                                                             },
                                              'directories': {'directory': ['directory-path', '...']
                                                              },
                                              # 'indexable': 'bool',
                                              'namespaces': {'namespace': ['namespace-name.tenant-name', '...']
                                                             },
                                              # 'replicationCollision': 'bool',
                                              'transactions': {
                                                  'transaction': ['operation-type', '...']
                                              }
                                              },
                           'verbose': 'bool'
                           }
             }

