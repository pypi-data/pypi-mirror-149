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

import time
from os import getcwd
from textwrap import fill
import PySimpleGUI as sg


def buildlayout(conf: dict, readfromdisk: bool = False) -> list:
    """
    Build the GUI layout.

    :param conf:          the configuration dict
    :param readfromdisk:  True if config was successfully read from disk
    :returns:             a list holding the layout
    """
    sg.theme('SystemDefault1')

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Load configuration...',
                           '&Save configuration as...',
                           '---',
                           '&Clear configuration',
                           '---',
                           'E&xit']],
                ['&Help', ['&About...',
                           '&Open help in browser...']]
                ]

    # ------ left column ------ #
    HCPacc_l = [[sg.Text('HCP FQDN:'),
                 sg.InputText(conf['url'], key='-URL-', size=(49, 1),
                              tooltip=fill('Enter the full FQDN, either starting with "admin" or a '
                                           'Tenant\'s name', width=50))],
                [sg.Text('Namespace(s):'),
                 sg.InputText(conf['namespaces'] if conf['namespaces'] else '', key='-NAMESPACES-',
                              size=(49,1),
                              tooltip=fill('Enter zero, one or multiple Namespaces in the form of "Namespace.Tenant", '
                                           'separated by commas.', width=50))],
                [sg.Text('Directories:'),
                 sg.InputText(conf['directories'] if conf['directories'] else '', key='-DIRECTORIES-',
                              size=(49,1),
                              tooltip=fill('Enter zero, one or multiple directories, each starting with a "/"; '
                                           'separate by commas.', width=50))],
                [sg.Text('User:'),
                 sg.InputText(conf['user'], key='-USER-', size=(49,1),
                              tooltip=fill('Enter a system or Tenant user name that has the search permision.'
                                           , width=50))],
                [sg.Text('Password:'),
                 sg.InputText(password_char='*', key='-PASSWORD-', size=(49,1))],
                ]

    HCPload_ll = [[sg.Text('Records per page:'),
                  sg.Spin([1,10,100,200,300,400]+[i for i in range(500, 10001, 500)],
                          initial_value=int(conf['count']),
                          key='-COUNT-',
                          size=(10, 15),
                          tooltip=fill('The number of records that are asked for in a single request. '
                                       'Can be changed while a query is running.', width=50)),],
                 [sg.Text('Throttle (seconds between pages):'),
                  sg.Spin([i for i in range(0, 61)],
                          initial_value=int(conf['throttle']),
                          key='-THROTTLE-',
                          size=(10, 15),
                          tooltip=fill('The wait time in seconds between two requests. Can be changed while '
                                       'a query is running.', width=50)),],
                 [sg.Text('Request timeout (seconds):'),
                  sg.Spin([i for i in range(30, 7201, 30)],
                          initial_value=int(conf['timeout']),
                          key='-TIMEOUT-',
                          size=(10, 15),
                          tooltip=fill('The HTTP timeout to use. Cannot be changed once a query has been '
                                       'started.', width=50)),]
                 ]
    HCPload_lr = [[sg.Button('Set', key='-SET-PAGE-', disabled=True),]
                  ]

    HCPload_l = [[sg.Frame('', layout=HCPload_ll, border_width=0, element_justification='right'),
                  sg.Frame('', layout=HCPload_lr, border_width=0, vertical_alignment='middle', element_justification='right')]]

    Output_l = [[sg.Text('Output type:'),
                 sg.Radio('csv', 'R-1', key='-CSV-',
                          default=True if conf['dbformat']=='csv' else False),
                 sg.Spin(['plain','bz2','gzip','lzma'], initial_value=[conf['compression']],
                            size=(6,1), key='-COMPRESSION-',
                         tooltip=fill('A CSV can be stored compressed, right away.', width=50)),
                 sg.VerticalSeparator(color='dark grey'),
                 sg.Radio('sqlite3', 'R-1', key='-SQLITE3-',
                          default=True if conf['dbformat']=='sqlite3' else False),
                 sg.VerticalSeparator(color='dark grey'),
                 sg.FileSaveAs('Browse', key='-SAVEAS-', target='-FILE-', initial_folder=getcwd())],
                 # sg.FileBrowse('Browse', key='-SAVEAS-', target='-FILE-', initial_folder=getcwd())],
                [sg.Text('Output file:'),
                 sg.InputText(conf['dbfile'] if conf['dbfile'] else '', key='-FILE-', enable_events=True, disabled=True),
                 sg.Checkbox('verbose', key='-VERBOSE-', default=conf['verbose'],
                              tooltip=fill('When checked, all system metadata is collected.', width=50))],
                ]

    leftupper_l = [[sg.Frame('HCP access parameters:', layout=HCPacc_l, element_justification='right')],
                   [sg.Frame('HCP load parameters:', layout=HCPload_l, element_justification='right')],
                   [sg.Frame('Output parameters:', layout=Output_l, element_justification='right')]
                   ]

    # ------ right column ------ #
    qParams_l = [[sg.Checkbox('create', default=True if 'CREATE' in conf['transactions'] else False,
                              key='-TP-CREATE-',
                              tooltip=fill('Object creation', width=50))],
                 [sg.Checkbox('delete', default=True if 'DELETE' in conf['transactions'] else False,
                              key='-TP-DELETE-',
                              tooltip=fill('Object deletion', width=50))],
                 [sg.Checkbox('dispose', default=True if 'DISPOSE' in conf['transactions'] else False,
                              key='-TP-DISPOSE-',
                              tooltip=fill('Object deletion by the Disposition Service', width=50))],
                 [sg.Checkbox('prune', default=True if 'PRUNE' in conf['transactions'] else False,
                              key='-TP-PRUNE-',
                              tooltip=fill('Object version deletion by pruning (version\'s life time ended)', width=50))],
                 [sg.Checkbox('purge', default=True if 'PURGE' in conf['transactions'] else False,
                              key='-TP-PURGE-',
                              tooltip=fill('Object deleted by purging (object including versions was '
                                           'deleted)', width=50))],
                 ]

    timeRange_l = [[sg.Text('Start time:'),
                    sg.InputText(conf['starttime'], key='-STARTTIME-', size=(23,1),
                                 tooltip=fill('The point in time the query\'s time range shall start with '
                                              '(format: YYYY-MM-DD HH:MM:SS[+-]ZZZZ, where ZZZZ is the '
                                              'deviation from UTC in HHMM)', width=50)),
                    sg.Button('Reset', key='-RESET-START-')],
                   [sg.Text('End time:'),
                    sg.InputText(conf['endtime'], key='-ENDTIME-', size=(23,1),
                                 tooltip=fill('The point in time the query\'s time range shall end with '
                                              '(format: YYYY-MM-DD HH:MM:SS[+-]ZZZZ, where ZZZZ is the '
                                              'deviation from UTC in HHMM)', width=50)),
                    sg.Button('Reset', key='-RESET-END-')],
                   ]

    rightupper_l = [[sg.Frame('Transaction types:', layout=qParams_l)],
                    [sg.Frame('Time range:', layout=timeRange_l, element_justification='right')],
                    ]

    baseframe_t = [[sg.Text('Status:'),
                    sg.Text('settings were successfully read from history file' if readfromdisk else
                            'no settings read from history file', key='-STATUS-', size=(100,1))],
                   [sg.Text('Records found:'),
                    sg.Text('', key='-RECS-FOUND-', size=(100,1))]]

    baseframe_b = [
                   # [sg.Text('Last record:', justification='top'),
                   #  sg.Text('', size=(100, 1), justification='left')],
                   [sg.Text('Url:', justification='top'),
                    sg.InputText(conf['lastResult']['urlName'] if 'urlName' in conf['lastResult'] else '',
                                 key='-LAST-URL-', size=(110, 1), justification='left')],
                   [sg.Text('Version:', justification='top'),
                    sg.InputText(conf['lastResult']['version'] if 'version' in conf['lastResult'] else '',
                                 key='-LAST-VERSION-', size=(110, 1), justification='left')],
                   [sg.Text('ChgTimeSec:', justification='top'),
                    sg.InputText(conf['lastResult']['changeTimeMilliseconds'] if 'changeTimeMilliseconds' in conf['lastResult'] else '',
                                 key='-LAST-CHGTIMEMS-', size=(110, 1), justification='left')]]

    layout = [[sg.Menu(menu_def)],
              [sg.Frame('', layout=leftupper_l, border_width=0, element_justification='left'),
               sg.VerticalSeparator(color='dark grey'),
               sg.Frame('Query parameters', layout=rightupper_l, vertical_alignment='top', border_width=0)],
              [sg.Frame('', layout=baseframe_t, border_width=0, element_justification='right', vertical_alignment='top')],
              [sg.Frame('Last record', layout=baseframe_b, border_width=1, element_justification='right', vertical_alignment='top')],
              [sg.Frame('',
                        [[sg.Submit('Run query', key='-RUN-QUERY-', bind_return_key=False),
                          sg.Cancel('Quit', key='-QUIT-'),
                          sg.HorizontalSeparator(),
                          sg.Text('',size=(100,1),key='-TIMESTAMP-')]],
                        vertical_alignment='right', element_justification='right', border_width=0)]]

    return layout

def updatelayout(window, conf):
    """
    Update the GUI with values from the config.

    :param window:        the window object
    :param conf:          the configuration dict
    :param readfromdisk:  True if config was successfully read from disk
    """
    window['-URL-'].update(conf['url'])
    window['-USER-'].update(conf['user'])
    window['-PASSWORD-'].update('')
    window['-COUNT-'].update(conf['count'])
    window['-THROTTLE-'].update(conf['throttle'])
    window['-NAMESPACES-'].update(conf['namespaces'] if conf['namespaces'] else '')
    window['-DIRECTORIES-'].update(conf['directories'] if conf['directories'] else '')

    window['-TP-CREATE-'].update(value=True if 'CREATE' in conf['transactions'] else False)
    window['-TP-DELETE-'].update(value=True if 'DELETE' in conf['transactions'] else False)
    window['-TP-DISPOSE-'].update(value=True if 'DISPOSE' in conf['transactions'] else False)
    window['-TP-PRUNE-'].update(value=True if 'PRUNE' in conf['transactions'] else False)
    window['-TP-PURGE-'].update(value=True if 'PURGE' in conf['transactions'] else False)

    window['-STARTTIME-'].update(conf['starttime'])
    window['-ENDTIME-'].update(conf['endtime'])
    window['-VERBOSE-'].update(conf['verbose'])
    window['-CSV-'].update(True if conf['dbformat']=='csv' else False)
    window['-SQLITE3-'].update(True if conf['dbformat']=='sqlite3' else False)
    window['-COMPRESSION-'].update(conf['compression'])
    window['-FILE-'].update(conf['dbfile'])

    if conf['lastResult'] and conf['lastResult']['urlName'] and conf['lastResult']['changeTimeMilliseconds'] and conf['lastResult']['version']:
        window['-LAST-URL-'].update(conf['lastResult']['urlName'])
        window['-LAST-CHGTIMEMS-'].update(conf['lastResult']['changeTimeMilliseconds'])
        window['-LAST-VERSION-'].update(conf['lastResult']['version'])
    else:
        window['-LAST-URL-'].update('')
        window['-LAST-CHGTIMEMS-'].update('')
        window['-LAST-VERSION-'].update('')
