#!../venv/bin/python3
import os
import sys

# Notes: 'ensure shebang has suitable path', 'echo $PATH' , 'ls -l',
# 'chmod +x filename'  or 'chmod 744 filename' then run './filename.py'
# or   'configure python launcher as default application for finder etc'
# The commonly used path to env does not exist on my mac, so we cannot use

# __file__ can sometimes only be the name, not the full path, hence abspath.
strFile = os.path.abspath(__file__)
strDirectory = os.path.dirname(strFile)
# Get parent directory
strParentDirectory = os.path.join(strDirectory, '..')
strParentDirectory = os.path.abspath(strParentDirectory)
# Insert the parent directory into the path.
sys.path.insert(0, strParentDirectory)

# Import Packages in Parent Directory Here.   Disable pylint error message.
import analytics  # pylint: disable=E0401

if __name__ == "__main__":
    print(sys.path)
