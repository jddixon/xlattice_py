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

## Command Line Utilities

At this time all of these are intended for use in managing the
content-keyed data store.  Conventioally this is in a directory called
`U/` or `uDir/`.  The path to the store is `u_path` and the object used
to manage the store is `u_dir`.

### u_consolidate

    usage: u_consolidate [-h] [-b BASE_DIR] [-i IN_DIR] [-j] [-n MAX_COUNT]
                         [-o OUT_DIR] [-v] [-w] [-z]

    move valid files from input U subdirectory to output subdir

    optional arguments:
      -h, --help            show this help message and exit
      -b BASE_DIR, --base_dir BASE_DIR
                            base directory holding U subdirectories
      -i IN_DIR, --in_dir IN_DIR
                            source U directory
      -j, --just_show       show options and exit
      -n MAX_COUNT, --max_count MAX_COUNT
                            number of files to move; -1 = all of them
      -o OUT_DIR, --out_dir OUT_DIR
                            destination U directory
      -v, --verbose         be chatty
      -w, --writing         overwrite existing files
      -z, --dont_do_it      don't do anything, just say what you would do

### u_preen

    usage: u_preen [-h] [-b B_DIR] [-g GROUP] [-j] [-u USER] [-v]

    regularize permissions in a U directory structure

    optional arguments:
      -h, --help            show this help message and exit
      -b B_DIR, --b_dir B_DIR
                            path to U directory to be preened (default=/var/U)
      -g GROUP, --group GROUP
                            group (default jdd)
      -j, --just_show       show options and exit
      -u USER, --user USER  user (login, default jdd)
      -v, --verbose         be chatty

### u\_re_struc

    usage: u_re_struc [-h] [-j] [-o OUT_PATH] [-s NEW_STRUC_NAME] [-u U_PATH] [-v]

    modify directory structure for uDir; this is a low-level operation which does
    not alter L

    optional arguments:
      -h, --help            show this help message and exit
      -j, --just_show       show options and exit
      -o OUT_PATH, --out_path OUT_PATH
                            optional destination directory
      -s NEW_STRUC_NAME, --new_struc_name NEW_STRUC_NAME
                            new dirStruc (DIR_FLAT, DIR16x16, or DIR256x256
      -u U_PATH, --u_path U_PATH
                            path to uDir (no default)
      -v, --verbose         be chatty

### u_stats

    usage: u_stats [-h] [-j] [-o OUT_PATH] [-u U_PATH] [-v]

    display statistical information on u_path

    optional arguments:
      -h, --help            show this help message and exit
      -j, --just_show       show options and exit
      -o OUT_PATH, --out_path OUT_PATH
                            destination directory
      -u U_PATH, --u_path U_PATH
                            source U directory (default=/var/U)
      -v, --verbose         be chatty

### verify_content

    usage: verify_content_keys [-h] [-j] [-t] [-T] [-V] [-1] [-2] [-3] [-u U_PATH]
                               [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -j, --just_show       show args and exit
      -t, --show_timestamp  show run timestamp
      -T, --testing         test run - write to ./testU
      -V, --show_version    show version number and date
      -1, --using_sha1      using the 160-bit SHA1 hash
      -2, --using_sha2      using the 256-bit SHA2 (SHA256) hash
      -3, --using_sha3      using the 256-bit SHA3 (Keccak-256) hash
      -u U_PATH, --u_path U_PATH
                            path to uDir
      -v, --verbose         be chatty


## Project Status

An incomplete implementation of the Python code necessary to support
[xlreg_py](https://jddixon.github.io/xlreg_py).

xlreg_py is a library enabling applications to easily use an
[xlReg](https://jddixon/github.io/xlReg_go) server
to set up communications between ad-hoc clusters of application servers
incorporating XLattice nodes.

## On-line Documentation

More information on the **xlattice_py** project can be found
[here](https://jddixon.github.io/xlattice_py)
