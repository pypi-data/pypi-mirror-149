Release History
===============

**2.0.11 - 2022-05-03**

    *   Added tool tips to most of the form fields

**2.0.10 - 2022-04-28**

    *   Warning box title corrected
    *   some documentation corrections

**2.0.9 - 2022-04-28**

    *   replaced the sliders in the UI with pre-seeded spin boxes
    *   simplified the HCP load parameters to a single [Set] button
    *   added the database schema to the documentation
    *   fixed a bug where the last record values were removed from the configuration file in
        case a repeated query did not return new records

**2.0.8 - 2022-04-26**

    *   made the request timeout configurable from the UI

**2.0.7 - 2021-12-22**

    *   copyright note fixed
    *   added _recipies folder, w/ a script to count objects per folder from a hcpmqe database

**2.0.6 - 2021-10-20**

    *   fixed a bug that causes SSL handshake errors when used with Python 3.10

**2.0.5 - 2020-11-23**

    *   start and end time are now in ISO 8601 format, added field verification

**2.0.4 - 2020-11-17**

    *   db/csv columns are now sorted by name, to make sure they are uniform across multiple runs
    *   fixed a bug where columns in sqlite3 databases were incorrectly named, occasionally
    *   fixed the start- / end-times (needs to be converted to milliseconds to be accurate)

**2.0.3 - 2020-11-11**

    *   preparation for publishing
    *   corrected the URL for help/documentation

**2.0.2 - 2020-11-10**

    *   configuration file now saved/loaded via menu entries
    *   configuration file is auto-updated when changes happen
    *   logging to file now into hcpmqe.<pid>.log

**2.0.1 - 2020-11-08**

    *   automatically adopts to whatever metadata fields the HCP MQE API
        delivers

    *   allows to restart a canceled or interrupted query

**2.0.0 - 2020-11-03**

    *   complete re-write using tkinter through pySimpleGUI

    *   runs on all major platforms (Linux, Windows, macOS)

**1.0.x releases**

*   1.0.11 - 2014-08-21

    [..]

*   1.0.1 - 2012-09-06

    initial release for Windows only
