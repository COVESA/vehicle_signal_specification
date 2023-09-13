#!/usr/bin/python3
# Copyright (c) 2023 Contributors to COVESA
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License 2.0 which is available at
# https://www.mozilla.org/en-US/MPL/2.0/
#
# SPDX-License-Identifier: MPL-2.0

import os


def string_exists(file_path, search_string) -> bool:
    with open(file_path, 'r') as file:
        content = file.read()
        if search_string in content:
            return True
    return False


if __name__ == '__main__':

    files = os.getenv('files')
    files = files.split(',')
    for file in files:
        file = os.path.abspath(file)
        if os.path.isfile(file):
            ext = os.path.splitext(file)[1]
            if ext in [".vspec", ".py"]:
                if not string_exists(file, "Contributors to COVESA"):
                    print(f"No contribution statement found in {file}")
                    raise Exception("Check the output, some files have not the right contribution statement!")
                if not string_exists(file, "SPDX-License-Identifier: MPL-2.0"):
                    print(f"Incorrect license statement found in {file}")
                    raise Exception("Check the output, some files have not the right SPDX statement!")

                print(f"Check succeeded for {file}")
    raise SystemExit(0)
