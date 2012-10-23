old-monitor
===========

## Old Monitor v3 (replaced by monitor-sqlite)

Uses the Google Charts API v1 to stitch together (via CSS placement) a set of 7 charts for ease of viewing of a week's worth of pertinent data, in this case monitoring the vitals of a Linux Server.

1. Top.py & wc.py are called via Cron every few minutes (5min is good)
    to collect, parse, and insert the data into a MySQL database

2. Monitor3.py is called via the web browser
    data is retrieved from the database and processed for reformatting into the Google structure
    a custom Y axis is created for the combined range of display on the 7 charts to ensure that the data is visible (not smooshed down because of excess range)
