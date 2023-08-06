# Introduction 
This is a tool class for use cases to find exception information in logcat in real time

#Usage

## 1. Import
```
from logcat_monitor.logcat_monitor import LogcatMonitor
```

## 2. Start 
```
logcat_monitor = LogcatMonitor(serial_number, parent_folder, key_dict, rows)
logcat_monitor.start_monitor()
```
#### LogcatMonitor parameters:
##### serial_number: Serial number of the device, If only one device is connected, it can be set to None
##### parent_folder: The directory where the file is stored. In this directory, a directory named "logcats" will be created
##### key_dict: Keyword dictionary to find. 
```
{"ANR in ": "Anr",
 "FATAL EXCEPTION:": "Fatal",
 "signal 6": "Signal6",
 "signal 7": "Signal7",
 "signal 11": "Signal11",
 "CRASH: ": "Crash",
 "Force Closed": "ForceClose"}
```
###### In dictionary, "Key" is keyword to find. "Value" must conform to Python's variable naming rules.
###### After finding the corresponding problem, a file named "Value_%Y%m%d%H%M%S%f.txt" will be generated.

##### rows:  After finding the problem, intercept the number of lines of logcat. Default is 100.

## 3. Stop
```
logcat_monitor.stop_monitor()
```
#### After stopping monitoring, a file named "statistics.txt" will be generated.
    

# Example
```
if __name__ == '__main__':
    ...
    # Monitor logcat in real time
    logcat_monitor = LogcatMonitor(main_device.serial_number, parent_folder, key_dict={"E/ActivityManager": "Test"}, rows=50)
    logcat_monitor.start_monitor()

    ...
    
    logcat_monitor.stop_monitor()
```

```
if __name__ == '__main__':
    ...
    # Filter existing logcat files
    logcat_monitor = LogcatMonitor()
    logcat_monitor.filter_file("logcat.txt")
    
```