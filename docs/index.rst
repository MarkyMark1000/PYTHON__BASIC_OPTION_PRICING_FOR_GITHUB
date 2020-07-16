====================
BASIC OPTION PRICING
====================

Overview
========

Tutorial
--------

Within this project, I wanted to explore the use of numpy, pandas, scipy and matplotlib for analysing
options.   This is a basic calculation which only considers European Options and Monte Carlo Simulations
for European Options.   There is no rate curve, borrow curve, vol surface etc.

A set of tests have been created to ensure the obtained price and greeks are reasonably accurate.

Originally, this was written using Anaconda, however I decided to analyse this data using a local
virtual environment and a requirements file, but found that a relatively up to date version of python
was required such as 3.7.

The Gamma calculation has a discontinuity at the strike price (imagine differentiating the intrinsic
value of an option twice).   This makes the Gamma results a bit unstable, which you will see in the
graphs.   See the following discussion for more information:

https://quant.stackexchange.com/questions/18208/greeks-why-does-my-monte-carlo-give-correct-delta-but-incorrect-gamma#%20greeks-why-does-my-monte-carlo-give-correct-delta-but-incorrect-gamma

Becuase the number of simulations, as an input, is unlimited it is possible that large amounts of memory
could be allocated, which may cause memory problems.   If this is the case, you will need to either
i) Reduce the number of simulations which may require adjustments to the tests, ii) Adjust or use
another computer or iii) Modify the code so that the calculation is processed in smaller chunks.

I have also created some docker files for running the tests.

Installation Guide
==================

Manual Installation
-------------------

- If it exists, remove the venv virtual environment directory using the following:
    - ``rm -rf venv      (mac)``
    - ``rmdir venv /s    (windows)``
- Recreate the virtual environment directory using the following:
    - Mac:
        - ``python3.7 -m venv venv``
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``pip install -r requirements.txt``
    - Windows:
        - ``vipython3.7 -m venv venv``
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ``pip install -r requirements.txt``
- Note, you may need to install the app manually using:
    - ``pip install -e .``
- If necessary, the html document in the docs directory can be rebuilt using:
    - Mac:
        - ``rm -rf ./docs/*.html``
        - ``rst2html ./docs/index.rst ./docs/index.html``
    - Windows:
        - ``del .\docs\*.html``
        - ``rst2html.py .\docs\index.rst .\docs\index.html``


MakeFile Installation (Mac, Linux or Unix)
------------------------------------------   
This project was written and tested on a mac and it has not been tested on Linux.

- To get help:
    - Run 'make' or 'make help' to get help on this project.
- It is sensible to reset the virtual environment so that it reflects the current requirements.txt file:
    - Run 'make venv' to build the virtual environment from requirements.txt.
- ``pip install -e .`` should be run automatically
- There isn't much supporting documentation, but it can be rebuilt using the following:
    - Run 'make venv-docs' to build /docs/index.html

    
Running the Application
=======================

Manual
------

- To run the app using the normal environment:
    - Mac:
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``python3.7 ./run/run_0_BlackScholesvsIntrinsic.py``
        - etc .....
    - Windows:
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ````python3.7 ./run/run_0_BlackScholesvsIntrinsic.py``
        - etc .....

MakeFile
--------

- To run in a normal environemnt:
    - Run 'make run-bs-int'
    - Run 'run-bs-monte'
    - Run 'make run-th-graphs'
    - Run 'run-thread'


Testing the Application
=======================

Manual
------

- Depending upon if new packages have been installed and if you wish to keep them in the project, it may be worth rebuilding the virtual environment and requirements.txt file to ensure they are consistent:

- To run a basic test:
    - Mac:
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``python3.7 -m unittest``
    - Windows:
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ``python3.7 -m unittest``

- To run a test showing the coverage of the test in a report:
    - Mac:
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``coverage run -m unittest discover``
        - ``coverage report``
    - Windows:
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ``coverage run -m unittest discover``
        - ``coverage report``

- To run a test showing the coverage of the test in an html based report:
    - Mac:
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``coverage run -m unittest discover``
        - ``coverage html``
    - Windows:
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ``coverage run -m unittest discover``
        - ``coverage html``

MakeFile
--------

- Depending upon if new packages have been installed and if you wish to keep them in the project, it may be worth rebuilding the virtual environment and requirements.txt file to ensure they are consistent:
    - To throw away any new packages and recreate the venv virtual environment from the requirements.txt file:
        - Run 'make venv' to build a new venv environment from existing requirements.txt file.
    - To recreate the requirements.txt file from the current venv virtual environment:
        - Run 'make venv-build-req' to build a new requirements.txt file from existing venv environment.

- To run a basic test:
    - Run 'make venv-test' to run test in venv virtual environment.

- To run a test showing the coverage of the test in a report:
    - Run 'make venv-cov-report' to run test in venv virtual environment and display report.

- To run a test showing the coverage of the test in an html based report:
    - Run 'make venv-cov-html' to run test in venv virtual environment.

Test Coding Standards
=====================

Manual
------

- Test the code within the analytics directory:
    - Mac:
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``pycodestyle --statistics ./analytics/*.py``
    - Windows:
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ``pycodestyle --statistics filename.py``
- Test the code within the run directory:
    - Mac:
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``ppycodestyle --statistics ./run/*.py``
    - Windows:
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ``pycodestyle --statistics filename.py``
- Test the code within the test directory:
    - Mac:
        - ``deactivate or source deactivate``
        - ``source venv/bin/activate``
        - ``ppycodestyle --statistics ./test/*.py``
    - Windows:
        - ``deactivate or source deactivate``
        - ``.\venv\Scripts\activate``
        - ``pycodestyle --statistics filename.py``

MakeFile
--------

- Test the code within the analytics, run and test directory:
    - Run 'make pystat'

Additional Commands
-------------------

A number of additional makefile commands exist to help clean up and manage the environment:

- To clean files such as __pycache__ etc:
    - Run 'make venv-clean'

- If you wish to remove the venv virtual environment directory:
    - Run 'make clean-venv'

- If you wish to rebuild the requirements file:
    - Run 'venv-build-req'