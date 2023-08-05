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

import logging
import os


def logger(logtarget='console', level='INFO'):
    """
    Setup loggging, either to journald or to file.

    :param logtarget:  where to log: console, logfile or journald
    :param level:      the log level (INFO or DEBUG)
    """
    logtarget = logtarget.upper()
    level = level.upper()

    if logtarget not in ['CONSOLE', 'LOGFILE']:
        raise AttributeError(f'unable to log to "{logtarget}"')
    if level not in ['INFO', 'DEBUG']:
        raise AttributeError(f'log level "{level}" is not supported')

    log = logging.getLogger('hcpmqe')
    log.setLevel(logging.DEBUG if level=='DEBUG' else logging.INFO)

    if logtarget == 'CONSOLE':
        th = logging.StreamHandler()
        if level == 'DEBUG':
            fm = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s  %(lineno)s : %(message)s')
        else:
            fm = logging.Formatter('[%(levelname)s] : %(message)s')
    else:  # LOGFILE
        logfile = f'hcpmqe.{os.getpid()}.log'

        # delete logfile if existent
        try:
            os.remove(logfile)
        except (OSError) as e:
            pass

        th = logging.FileHandler(logfile)
        if level == 'DEBUG':
            fm = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s : %(message)s')
        else:
            fm = logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s')

    log.addHandler(th)
    th.setFormatter(fm)

    return log