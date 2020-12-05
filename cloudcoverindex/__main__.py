"""
Cloud Cover Index: Determine cloud cover index from jpeg image(s)

This module checks the python version the user is running the program
with to prevent any errors that might occur if it's run with too old a version.
"""

import sys

if __name__ == "__main__":
    # Checking if the user is using the correct version of Python
    # For example:
    # If Python version is 3.6.5
    #              major --^
    #              minor ----^
    #              micro ------^
    major = sys.version_info[0]
    minor = sys.version_info[1]

    python_version = str(major)+"."+str(minor)+"."+str(sys.version_info[2])

    if major != 3 or major == 3 and minor < 6:
        print("Cloud Cover Index requires Python 3.6+\nYou are using Python %s, which is not supported by Cloud Cover Index" % python_version)
        sys.exit(1)

    import cloudcoverindex
    cloudcoverindex.main()
