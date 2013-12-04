# Connection Tracker
##### Python v2.7.3

A tool that pulls the connections from netstat on the local PC. A list of the connections will be displayed to the user along with their age. The tool refreshes every so often updating its connections and the display. Usage information can be found with the following command: `ConnectionTracker.py --help`.

##### Known Issues

* Loading a file will increment the times by one automatically due to how the thread starts.
* Connection will scroll off the terminal if they overflow.