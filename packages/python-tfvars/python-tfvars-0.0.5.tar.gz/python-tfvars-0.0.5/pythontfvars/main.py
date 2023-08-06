#!/usr/bin/env python

"""read secrets from terraform tfvars files"""

import glob
import os
import re
import pkg_resources

from addict import Dict


def remove_quotes(value):
    value = value.replace("\"", "")
    value = value.replace("\'", "")
    return value


class TFVars:
    def __init__(self, tfvars_file=None, is_module=False):
        self.tfvars_file = self.find_and_verify_tfvars(tfvars_file, is_module)
        self.tflines = self.load_tflines()
        self.tfvars = Dict()
        self.load_dict()
    
    def find_and_verify_tfvars(self, fav_tfvars, is_module):
        """
        find and check the format of the tfvars file
        """
        current_dir = os.getcwd()
        if fav_tfvars is None:
            if is_module:
                raise ValueError("python-tfvars does not currently support usage inside a module.")
            glob_path = f"{current_dir}{os.path.sep}*.tfvars"
            if len(glob.glob(glob_path)) > 1:
                raise TypeError("more than one tfvars. please specify a tfvars file.")
            if not glob.glob(glob_path):
                raise TypeError("no tfvars found.")
            fav_tfvars = glob.glob(glob_path)[0]
        else:
            if not os.path.isabs(fav_tfvars):
                fav_tfvars = os.path.abspath(fav_tfvars)
            if not os.path.exists(fav_tfvars):
                raise ValueError("tfvars file specified does not exist")
        with open(fav_tfvars) as f:
            lines = f.read().splitlines()
        bigstr = "<()>".join(lines)
        matches = re.findall(r'(\w+(?:\(\d+\))?)\s*=\s*(.*?)(?=(!|$|\w+(\(\d+\))?\s*=))', bigstr)
        if not matches:
            raise TypeError("tfvars is not in the right format.")
        return fav_tfvars

    def is_comment(self, line):
        if line.startswith("#"):
            return True
        if line.startswith("//"):
            return True
        return False

    def remove_multiline_and_newline(self, tflines):
        chop = False
        last = False
        newlines = []
        for line in tflines:
            if line.startswith("/*"):
                chop = True
            if line.startswith("*/"):
                last = True
            if not chop:
                if line.strip() != "" and not self.is_comment(line):
                    newlines.append(line)
            if last is True:
                chop = False
            last = False
        return newlines

    def load_tflines(self):
        """
        load a terraform tfvars file and return a list of lines without comments
        """
        with open(self.tfvars_file) as f:
            lf_tflines = f.read().splitlines()
        lf_tflines = self.remove_multiline_and_newline(lf_tflines)
        return lf_tflines

    def read_maps(self):
        """read maps out of file"""
        found = False
        positions = []
        key = ""
        for index, line in enumerate(self.tflines):
            if found:
                positions.append(index)
                if "}" in line:
                    found = False
                    key = ""
                else:
                    kv = line.split("=")
                    name = remove_quotes(kv[0].strip())
                    value = remove_quotes(kv[0].strip())
                    self.tfvars[key].append({kv[0].strip():value})
            if "{" in line:
                found = True
                positions.append(index)
                key = line.split("=")[0].strip()
                self.tfvars[key] = []
        # clean up
        for pos in reversed(positions):
            self.tflines.pop(pos)
            
    def txt_to_list(self, flines):
        txt = "".join(flines)
        kv = txt.split("=")
        key = kv[0].strip()
        vlist = kv[1].strip()
        vlist = vlist.replace("]", "").replace("[", "")
        value = vlist.split(",")
        value = [remove_quotes(x.strip()) for x in value]
        self.tfvars[key] = value

    def read_lists(self):
        """read maps out of file"""
        found = False
        positions = []
        flines = []
        for index, line in enumerate(self.tflines):
            if "[" in line:
                found = True
            if found:
                positions.append(index)
                flines.append(line.strip())
            if "]" in line:
                found = False
                if line not in flines:
                    positions.append(index)
                    flines.append(line.strip())
                self.txt_to_list(flines)
                flines = []
        # clean up
        for pos in reversed(positions):
            self.tflines.pop(pos)

    def load_dict(self):
        """this is the business"""
        self.read_maps()
        self.read_lists()
        positions = []
        for index, line in enumerate(self.tflines):
            kv = line.split("=")
            key = kv[0].strip()
            value = kv[1].strip()
            value = remove_quotes(value)
            self.tfvars[key] = value
            positions.append(index)
        # clean up
        for pos in reversed(positions):
            self.tflines.pop(pos)


def main():
    """
    read secrets from terraform tfvars files
    """
#    future home for any cli tools
#    version = pkg_resources.require("python-tfvars")[0].version
    return

if __name__ == "__main__":
    main()
    tfvars = TFVars("../dev.auto.tfvars")
    import pdb; pdb.set_trace()
