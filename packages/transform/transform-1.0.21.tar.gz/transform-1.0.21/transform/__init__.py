# To solve some issues with clashing dependencies we are going to vendor gql 3.0 into this repo for a short time
# And for this, I apologize
import os
import sys

vendor_file_path = os.path.abspath(__file__)
root_dir = vendor_file_path.replace("/__init__.py", "")
sys.path.append(f"{root_dir}/vendor")

from .mql import MQLClient  # noqa: E402

__version__ = "1.0.21"
PACKAGE_NAME = "transform"

# mql gets imported if user is already authenticated
mql = None
try:
    mql = MQLClient()
except Exception as e:  # noqa: D
    pass
