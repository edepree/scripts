#connection_tracker.py
#####Python v2.7.3

A tool that pulls the connections from netstat on the local PC. A list of the connections will be displayed to the user along with their age. The tool refreshes every so often updating its connections and the display. Usage information can be found with the following command: `connection_tracker.py --help`.

#####Known Issues

* Loading a file will increment the times by one automatically due to how the thread starts.
* Connection will scroll off the terminal if they overflow.

#cron_tracker.py
#####Python v2.7.5

A tool that pulls cron tabs for all user and tracks how they change over time to the console. Usage information can be found with the following command: `cron_tracker.py --help`. This program needs to be executed with elevated privileges.

#udp_echo.py
#####Python v2.7.5

A simple UDP echo server/client.

* See all options: `python udp_echo.ph -h`
* Launch default server: `python udp_echo.ph server`
* Launch default client: `python udp_echo.ph client`

#dns_lite.py
#####Python v2.7.5

A simple DNS server.

* See all options: `python udp_echo.py --help`

#http_upload_server.py
#####Python v2.7.5

An HTTP server accepting and parsing a POST request for a download from a PowerShell client.

* See all options: `python http_upload_server.py --help`