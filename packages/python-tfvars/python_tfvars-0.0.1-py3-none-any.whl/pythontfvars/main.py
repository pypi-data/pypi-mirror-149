#!/usr/bin/env python

"""read secrets from terraform tfvars files"""

import pkg_resources
from stringcolor import cs, bold, underline


def main():
    """read secrets from terraform tfvars files"""
#    version = pkg_resources.require("python-tfvars")[0].version
    version = "infancy"
    print(version)
    return

if __name__ == "__main__":
    main()
