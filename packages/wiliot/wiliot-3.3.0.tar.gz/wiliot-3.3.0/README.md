# PyWiliot #

PyWiliot is a python library for accessing Wiliot's tools including:
* Wiliot's cloud services from Python
* Wiliot's Gateway control
* Wiliot's tester utilities
In addition, examples and scripts for Wiliot testers are provided

## Public Library

### MAC Installation
#### Getting around SSL issue on Mac with Python 3.7 and later versions

Python version 3.7 on Mac OS has stopped using the OS's version of SSL and started using Python's implementation instead. As a result, the CA
certificates included in the OS are no longer usable. To avoid getting SSL related errors from the code when running under this setup you need
to execute Install Certificates.command Python script. Typically you will find it under
~~~~
/Applications/Python\ 3.7/Install\ Certificates.command
~~~~

#### Python 3 on Mac
The default Python version on mac is 2.x. Since Wiliot package requires Python 3.x you should download Python3 
(e.g.  Python3.7) and make python 3 your default.
There are many ways how to do it such as add python3 to your PATH (one possible solution https://www.educative.io/edpresso/how-to-add-python-to-the-path-variable-in-mac) 

#### Git is not working after Mac update
please check the following solution:
https://stackoverflow.com/questions/52522565/git-is-not-working-after-macos-update-xcrun-error-invalid-active-developer-pa

### Linux Installation
Since some of Wiliot package's dependencies are not fully compatible with Linux, please install first the following:
````commandline
pip install pc-ble-driver-py
pip install libusb1
pip install --no-deps nrfutil 
````


### Installing pyWiliot
````commandline
pip install wiliot
````

### Using pyWiliot
Wiliot package location can be found, by typing in the command line:
````commandline
pip show wiliot
````
please check out our examples including:
* cloud services (under ../wiliot/cloud_apis/management/examples)
* gateway (under ../wiliot/gateway_api/examples)
* testers (under ../wiliot/wiliot_testers)

For more documentation and instructions, please contact us: support@wiliot.com
