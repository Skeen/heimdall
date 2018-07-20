#!/usr/bin/env python
# pylint: disable=W9903
"""Tool for checking that mapping.py is in sync with `requirements.txt`."""

# Change to the script dir
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/../")


def check_python():
    # Load in the requirements packages
    status_code = 0

    for filename_ext in os.listdir('requirements'):
        filename = os.path.splitext(filename_ext)[0]
        req_packages = {}

        with open("requirements/" + filename + ".txt", 'r') as file_in:
            for line in file_in:
                if line.startswith("#"):
                    continue
                elif line.startswith("-r"):
                    continue
                    #filepath = line.split(' ')[1].strip()
                    #filename = os.path.basename(filepath)
                    #filedir = os.path.dirname(filepath)
                    #read_packages(folder + "/" + filedir, filename)
                    #continue
                elif line.startswith("git+"):
                    package_name = line.split('.git')[0].rsplit('/', 1)[1]
                    if '/Skeen/' in line:
                        package_version = 'forked'
                    else:
                        package_version = 'upstream'
                else:
                    package_name = line.split("==")[0]
                    package_version = line.split("==")[1].strip()
                req_packages[package_name] = {}
                req_packages[package_name] = package_version

        # Load in the licence packages
        lic_packages = {}
        import ast
        with open("licence/mapping/python/" + filename + ".py", 'r') as file_in:
            licence_map = ast.literal_eval(file_in.read())
            for package_name, dicty in licence_map.items():
                dicty.pop('licence', None)
                dicty.pop('homepage', None)
                package_version = dicty.pop('version', None)
                lic_packages[package_name] = {}
                lic_packages[package_name] = package_version

        # Find the symmetric set difference between the packages
        set_symmetric_difference = (set(lic_packages.items()) ^
                                    set(req_packages.items()))

        # Print differences
        for key in dict(set_symmetric_difference).keys():
            print "Python:" + key + " differs in " + filename

        # Exit 1 if differences was found
        if len(set_symmetric_difference) > 0:
            status_code += 1

    return status_code


if __name__ == "__main__":
    status_code = 0
    status_code += check_python()
    exit(status_code)
