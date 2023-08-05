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

from os import getcwd
from time import localtime, strftime, strptime, time
from threading import Event
from logging import getLogger
from pathlib import PurePath
import PySimpleGUI as sg

from ..conf.config import Configuration
from .layout import buildlayout, updatelayout
from ..mqe import MqeQuery
from ..version import Gvars


def loop():
    log = getLogger('hcpmqe.' + __name__)

    # read the configuration file and build the layout
    conf = Configuration()
    c, r = conf.readconfig()
    layout = buildlayout(c, r)
    title = f'HCP Metadata Query Tool v{Gvars.s_version}'
    sg.theme('SystemDefault1')

    window = sg.Window(title, layout,
                       default_element_size=(40, 1),
                       grab_anywhere=False)

    configpath = getcwd()
    configfile = None
    t_run = t_query = t_db = 0  # used to record the seconds consumed
    mq = None  # placeholder for the query class

    while True:
        event, values = window.read()
        # update the bottom status line while a query thread is running
        if t_run:
            tstxt = f'run time: {hms(time()-t_run)}, ' \
                    f'overall query time: {hms(t_query)}, ' \
                    f'overall DB insert time: {hms(t_db)}'
            window['-TIMESTAMP-'].update(f'{tstxt:>130}')

        # ----- USER ACTIVITY ----- #
        # handle the user closing the window (hard program abort)
        if not event:
            log.debug("user closed the window (abort)")
            break

        # handle the user ending the program cleanly
        elif event == '-QUIT-' or event == 'Exit':
            log.debug("user selected the [Quit] button or [Exit] from menu")
            if configfile:
                conf.updateconf(values)
                if conf.writeconfig(configfile):
                    log.debug(f'auto-updated configuration file {configfile}')
                else:
                    log.debug(f'fatal: failed to auto-update configuration file {configfile}')

            break

        # handle menu:file/load...
        elif event == 'Load configuration...':
            log.debug(f'user selected "{event}" from the menu')
            configfile = sg.popup_get_file('Load configuration file',
                                           title='Load configuration file...',
                                           default_path=configfile or '',
                                           default_extension='.mqe',
                                           initial_folder=configpath,
                                           save_as=False)
            _c, _r = conf.readconfig(configfile)
            if _r:
                updatelayout(window, _c)
                window['-STATUS-'].update(f'loaded configuration file {configfile}')
                window.set_title(f'{title} - {PurePath(configfile).name}')
            else:
                configfile = None

        # handle menu:file/save...
        elif event == 'Save configuration as...':
            log.debug(f'user selected "{event}" from the menu')
            configfile = sg.popup_get_file('Save configuration file',
                                           title='Save configuration file as...',
                                           default_path=configfile or '',
                                           default_extension='.mqe',
                                           initial_folder=configpath,
                                           save_as=True)
            if configfile:
                conf.updateconf(values)
                if conf.writeconfig(configfile):
                    window['-STATUS-'].update(f'configuration written to file {configfile}')
                    window.set_title(f'{title} - {PurePath(configfile).name}')
                else:
                    window['-STATUS-'].update(f'fatal: failed to write configuration to file {configfile}')
                    configfile = None

        # handle menu:file/clear
        elif event == 'Clear configuration':
            log.debug(f'user selected "{event}" from the menu')
            if sg.popup_yes_no('Do you really want to clear the configuration?') == 'Yes':
                log.debug(f'user decided to clear the configuration')
                configfile = None
                _c, _r = conf.readconfig(configfile)
                updatelayout(window, _c)
                window['-STATUS-'].update(f'configuration cleared')
                window.set_title(title)
            else:
                og.debug(f'user decided NOT to clear the configuration')

        # handle menu:help/about...
        elif event == 'About...':
            sg.popup_ok(f'{Gvars.s_description}\n'
                        f'{Gvars.Version}\n\n'
                        f'Operational queries towards HCP MQE API\n\n'
                        f'{Gvars.Author}\n'
                        f'{Gvars.AuthorMail}',
                        background_color='khaki')

        # handle menu:help/Open help in browser...
        elif event == 'Open help in browser...':
            log.debug("user selected [Help] in menu")
            import webbrowser
            webbrowser.open_new_tab(Gvars.AppURL)

        # handle the user changing the HCP load parameters
        elif event == '-SET-PAGE-':
            # Due to the spin boxes behavior, where an user could just delete the value,
            # which would crash the code later due to a conversion to int.
            # That's why we set default values in this case.
            try:
                __dummy = int(values['-COUNT-'])
            except ValueError:
                values['-COUNT-'] = 2500
                window['-COUNT-'].update(2500)
            try:
                __dummy = int(values['-THROTTLE-'])
            except ValueError:
                values['-THROTTLE-'] = 0
                window['-THROTTLE-'].update(0)

            mq.pagesize = values['-COUNT-']
            mq.throttle = values['-THROTTLE-']
            log.debug(f"user selected the [SET] button (recs/page: {mq.pagesize} / throttle: {mq.throttle})")

        # handle the user resetting the start time
        elif event == '-RESET-START-':
            log.debug("user selected the [Reset] start time button")
            window['-STARTTIME-'].update(strftime('%Y-%m-%d %H:%M:%S%z', localtime(0)))

        # handle the user resetting the end time
        elif event == '-RESET-END-':
            log.debug("user selected the [Reset] end time button")
            window['-ENDTIME-'].update(strftime('%Y-%m-%d %H:%M:%S%z', localtime()))

        # handle the user starting or canceling the query
        elif event == '-RUN-QUERY-':
            if window['-RUN-QUERY-'].GetText() == 'Run query':  # start query
                log.debug("user selected the [Run query] button")
                if not configfile:
                    log.debug("unable to run a query, as no config file was available")
                    sg.popup_error('Please save the configuration before running a query...')
                    continue

                if not values["-FILE-"]:
                    log.debug("unable to run a query, as no output file was selected")
                    sg.popup_error('No output file selected...')
                elif not checkdatestr(values['-STARTTIME-']):
                    log.debug("unable to run a query, as the start time is incorrect.")
                    sg.popup_error('"Start Time" is incorrect.')
                elif not checkdatestr(values['-ENDTIME-']):
                    log.debug("unable to run a query, as the end time is incorrect.")
                    sg.popup_error('"End Time" is incorrect.')
                else:
                    if values['-LAST-URL-'] and values['-LAST-VERSION-'] and values['-LAST-CHGTIMEMS-']:
                        continuequery = sg.popup_yes_no('Do you want to continue the query from the position '
                                                        'shown as last record?\n\nWARNING: this will lead to false '
                                                        'results in case ANY parameter (other than the End time) have '
                                                        'been changed!!!',
                                                        title='Warning!',
                                                        background_color='sienna1',
                                                        text_color='black',
                                                        line_width=100, keep_on_top=True)
                        if continuequery == 'No':
                            log.debug("user selected to start with a new query")
                        else:
                            log.debug("user selected to continue from the values in last record")

                    if not values['-LAST-URL-'] or continuequery == 'No':
                        if sg.popup_yes_no(f'Running the query will overwrite the file\n'
                                         f'{values["-FILE-"]}\n'
                                         f'Do you really want to do that?',
                                         text_color='red3',
                                         line_width=100,
                                         keep_on_top=True) == 'Yes':
                            values['-LAST-URL-'] = ''
                            values['-LAST-VERSION-'] = ''
                            values['-LAST-CHGTIMEMS-'] = ''
                            window['-LAST-URL-'].update('')
                            window['-LAST-VERSION-'].update('')
                            window['-LAST-CHGTIMEMS-'].update('')
                            log.debug("user selected to overwrite the db file")
                        else:
                            log.debug("user selected not to run the query")
                            continue

                    togglequery(window, values, True)
                    window['-STATUS-'].update('Query started...')
                    window['-RECS-FOUND-'].update('')
                    window['-TIMESTAMP-'].update('')
                    if configfile:
                        conf.updateconf(values)
                        if conf.writeconfig(configfile):
                            log.debug(f'auto-updated configuration file {configfile} (query start)')
                        else:
                            log.debug(f'fatal: failed to auto-update configuration file {configfile} (query start)')

                    cancel = Event()  # used to cancel a running query
                    mq = MqeQuery(window, conf.conf, cancel, False if values['-LAST-URL-'] else True,
                                  daemon=True, name='*query*')
                    t_run = time()
                    t_query = t_db = 0
                    mq.start()
            else:  # cancel query
                log.debug("user selected the [Cancel query] button")
                if sg.popup_yes_no('Do you really want to cancel the running query?', text_color='red2',
                                   # background_color='khaki'
                                   ) == 'Yes':
                    log.debug("user chose to cancel the query")
                    cancel.set()
                    window['-RUN-QUERY-'].update(disabled=True)
                    window['-STATUS-'].update('Query is being canceled - please wait for finishing')
                    window.Finalize()
                else:
                    log.debug("user chose NOT to cancel the query")

        # ----- QUERY THREAD ACTIVITY ----- #
        # handle messages from the query thread
        elif event == '-QTHREAD-' and len(values['-QTHREAD-']) > 1:  # the query didn't fail
            if values['-QTHREAD-'][4]:  # finished
                log.debug("Query thread signaled query has finished successfully")
                #mq.join()
                mq = None
                if values['-QTHREAD-'][0]:
                    window['-RECS-FOUND-'].update(values['-QTHREAD-'][0])
                    window['-LAST-URL-'].update(values["-QTHREAD-"][1]),
                    window['-LAST-VERSION-'].update(values["-QTHREAD-"][2]),
                    window['-LAST-CHGTIMEMS-'].update(values["-QTHREAD-"][3]),
                    window['-STATUS-'].update('finished')
                else:
                    pass # we didn't get new records, so we don't reset the values!
                togglequery(window, values, False)
            else:  # not finished, ongoing...
                log.debug("Query thread signaled query information update")
                window['-RECS-FOUND-'].update(values['-QTHREAD-'][0])
                window['-LAST-URL-'].update(values["-QTHREAD-"][1]),
                window['-LAST-VERSION-'].update(values["-QTHREAD-"][2]),
                window['-LAST-CHGTIMEMS-'].update(values["-QTHREAD-"][3]),
                window['-STATUS-'].update(values["-QTHREAD-"][0])

            # need to tweak the machinery here, to get these values updated
            values['-LAST-URL-'] = values["-QTHREAD-"][1]
            values['-LAST-VERSION-'] = values["-QTHREAD-"][2]
            values['-LAST-CHGTIMEMS-'] = values["-QTHREAD-"][3]
            conf.updateconf(values)
            if conf.writeconfig(configfile):
                log.debug(f'auto-updated configuration file {configfile} (status update)')
            else:
                log.debug(f'fatal: failed to auto-update configuration file {configfile} (status update)')


        # handle status updated submitted by the query thread
        elif event == '-QTHREAD-STATUS-':
            log.debug(f'Query thread signaled status update ({values["-QTHREAD-STATUS-"][0]})')
            window['-STATUS-'].update(values['-QTHREAD-STATUS-'][0])
            if values["-QTHREAD-STATUS-"][1] == 'db':
                t_db += float(values["-QTHREAD-STATUS-"][2])
            elif values["-QTHREAD-STATUS-"][1] == 'query':
                t_query += float(values["-QTHREAD-STATUS-"][2])

        # handle the query thread signalling an error that causes the query to end
        elif event == '-QTHREAD-ERROR-':  # the query failed/canceled
            log.debug(f'Query thread signaled status update ({values["-QTHREAD-ERROR-"][0]})')
            window['-STATUS-'].update(values['-QTHREAD-ERROR-'][0])
            togglequery(window, values, False)
            # mq.join()  # there is no sense in joining this thread, as everything will be shut down before
            #              reaching this piece of code.
            mq = None

            if values['-QTHREAD-ERROR-'][0].find('403 -') >= 0:
                conf.updateconf(values)
                if conf.writeconfig(configfile):
                    log.debug(f'auto-updated configuration file {configfile} (query cancel/fail)')
                else:
                    log.debug(f'fatal: failed to auto-update configuration file {configfile} (query cancel/fail)')
            else:
                log.debug(f'NOT auto-updating the configuration file {configfile} (due to error 403)')

    window.close()
    log.debug('program ended')


def togglequery(window, values, run: bool):
    """
    Toggle the query status in the GUI.

    :param window:  the window
    :param values:  the values dict()
    :param run:     True if we toggle to run query mode
    """
    # groups of elements to be toggled when running a query / query finished or canceled
    t1 = ['-URL-', '-NAMESPACES-', '-DIRECTORIES-', '-USER-', '-PASSWORD-', '-TIMEOUT-',
          '-CSV-', '-COMPRESSION-', '-SQLITE3-', '-SAVEAS-',  '-FILE-', '-VERBOSE-',
          '-TP-CREATE-', '-TP-DELETE-', '-TP-DISPOSE-', '-TP-PRUNE-', '-TP-PURGE-',
          '-STARTTIME-', '-RESET-START-',  '-ENDTIME-', '-RESET-END-', '-QUIT-']
    t2 = ['-SET-PAGE-']

    if run:
        for el in t1:
            window[el].update(disabled=True)
        for el in t2:
            window[el].update(disabled=False)
        window['-RUN-QUERY-'].update(text='Cancel query')
    else:
        for el in t1:
            window[el].update(disabled=False)
        for el in t2:
            window[el].update(disabled=True)
        window['-RUN-QUERY-'].update(text='Run query', disabled=False)

def checkdatestr(datestr):
    """
    Check a date string for proper format.

    An ISO 8601 datetime value in this format: yyyy-MM-ddThh:mm:ssZ
    Z represents the offset from UTC, in this format: (+|-)hhmm
    For example, 2011-11-16T14:27:20-0500 represents the start of the
    20th second into 2:27 PM, November 16, 2011, EST.

    :param datestr:  the datestr from the gui
    :return:         nothing if datestr is ok, otherwise raise
    """
    log = getLogger('hcpmqe.' + __name__)

    try:
        t = strptime(datestr, '%Y-%m-%d %H:%M:%S%z')
    except ValueError as e:
        log.debug(f'start/end time "{datestr}" invalid - {e}')
        return False
    else:
        return True

def hms(t):
    """
    Return a sting of HH:MM:SS from an integer
    """
    h = int(t/3600)
    m = int((t-h*3600)/60)
    s = int(t-h*3600-m*60)

    return f'{h:02}:{m:02}:{s:02}'

