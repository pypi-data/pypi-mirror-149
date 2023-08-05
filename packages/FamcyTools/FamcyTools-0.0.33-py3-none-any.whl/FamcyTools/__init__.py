import os
import sys
import pwd
import FamcyTools

def get_username():
    return pwd.getpwuid(os.getuid())[0]

def get_version():
	major = sys.version_info.major
	minor = sys.version_info.minor
	return str(major)+"."+str(minor)

USERNAME = get_username()
# TODO: in the future, this needs to be more modular
HOME_DIR = os.path.expanduser('~')
FAMCY_DIR = HOME_DIR+"/.local/share/famcy/%s/venv/lib/python"+get_version()+"/site-packages/Famcy"
FAMCYTOOLS_DIR = os.path.dirname(FamcyTools.__file__)
