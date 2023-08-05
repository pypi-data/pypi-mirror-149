This contains packaging tools and example notebooks for the Python
interface to [lifelib](https://gitlab.com/apgoucher/lifelib). Comprehensive
[documentation](https://gitlab.com/apgoucher/lifelib/blob/master/README.md)
is available from the main repository.

Quick start
-----------

Make sure your machine has the correct system requirements before commencing.
This essentially boils down to you having an **x86-64 processor** (likely to
be the case unless you're using a smartphone, tablet, or Raspberry Pi). Then
getting started with `lifelib` is straightforward.

 - Install Python with the `numpy` and `jupyter` packages and the 'pip'
   package manager. The [Anaconda](https://www.anaconda.com/download)
   distribution contains those packages and many more, and is available
   on Windows, Mac OS X, and Linux. You can use either Python 2 or 3.

 - If on Mac OS X, make sure you have the **command-line developer tools**
   installed. You can test this by opening a terminal and running the
   command `g++ --version`.

 - Download and run the [installation script][1] to install or upgrade
   `lifelib`. Internally, this uses the pip package manager and installs
   `lifelib` into a user-local directory.

 - Clone this repository:

        git clone https://gitlab.com/apgoucher/python-lifelib.git

 - Spin up a notebook server and explore the example notebooks:

        cd python-lifelib/notebooks
        jupyter notebook

[1]: https://gitlab.com/apgoucher/python-lifelib/blob/master/install/install.py
