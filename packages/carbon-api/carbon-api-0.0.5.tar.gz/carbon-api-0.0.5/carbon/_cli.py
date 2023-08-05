# Carbon - Create beautiful carbon code images using python or terminal
# Copyright (C) 2022 Stark Bots <https://github.com/StarkBotsIndustries>
#
# This file is part of Carbon.
#
# Carbon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Carbon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Carbon. If not, see <https://www.gnu.org/licenses/>.


import os
import sys
import time
import asyncio
import argparse
from termcolor import colored
from carbon._main import Carbon
from carbon._utils import random_file_name
from carbon._constants import __description__, __version__


def main():
    client = Carbon()
    parser = argparse.ArgumentParser(
        prog='carbon-app',
        description=__description__,
        usage='%(prog)s [options]',
        epilog='Enjoy the program :)',
        allow_abbrev=False,
        add_help=True
    )
    cwd = os.getcwd()
    parser.add_argument('-v', '--version', help='Check the current version installed', action='store_true')
    parser.add_argument('-f', '--file', help='Pass file path to read code from', action='store')
    parser.add_argument('-c', '--code', help='Pass some code to make carbon', action='store')
    parser.add_argument('-n', '--name', help='Specify a name for the image, otherwise a random name will be used', action='store')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if args.version:
        print(f'v{__version__}')
        return
    if args.file:
        path = cwd + "/" + args.file
        with open(path, "r") as f:
            text = f.read()
    elif args.carbon:
        text = args.carbon
    else:
        return
    if args.name:
        name = args.name + ".png" if "." not in args.name else args.name
    else:
        name = random_file_name()
    pref = colored(">", "yellow")
    print(pref, "Creating Carbon...")
    image = asyncio.run(client.create(text, file=name))
    print(pref, "Saved as :", end=" ")
    time.sleep(0.25)
    print(colored(image.rsplit("/", 1)[-1], "green"))
