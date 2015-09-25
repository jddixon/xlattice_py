# xlattice_py

[XLattice](https://jddixon.github.io/xlattice)
utilty functions for Python.

These are collected in the `xlattice` subdirectory:

* **crypto.py**, functions for PKCS7Padding and deserialization of PEM-encoded RSA public keys
* **helloAndReply.py**, an implementation of XLattice's `helloAndReply` protocol for setting up inter-node AES-based communications
* **lfs.py**, wrapper functions for `mkdir_p` and `touch`
* **ui.py**, simple functions for handle Y/N questions on the command line and assessing password strength
* **u.py**, XLattice system for storing data by content key
* **util.py**, which contains functions for dealing with XLattice `DecimalVersion` and `Timestamp` classes

** Project Status

An incomplete implementation of the Python code necessary to support
[xlReg_py](https://jddixon.github.io/xlReg_py).  xlReg_py is a library
enabling applications to easily use an
[xlReg](https://jddixon/github.io/xlReg_go) server
to set up communications between ad-hoc clusters of application servers
incorporating XLattice nodes.

## On-line Documentation

More information on the **xlattice_py** project can be found
[here](https://jddixon.github.io/xlattice_py)
