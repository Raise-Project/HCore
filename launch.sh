#!/bin/bash

# File: launch.sh
# Created Date: Saturday, November 6th 2020, 11:16:56 am
# Author: Zentetsu
#
# ----
#
# Last Modified: Sat Nov 07 2020
# Modified By: Zentetsu
#
# ----
#
# Project: HCore
# Copyright (c) 2020 Zentetsu
#
# ----
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ----
#
# HISTORY:
# 2020-11-07	Zen	Adding startup script


validate=0
HController=0

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --HController)
        HController=1
        shift # past value
        ;;
        --default)
        shift # past argument
        ;;
        *)    # unknown option
        validate=-1
        break
        shift # past argument
        ;;
    esac
done

if [[ $validate -eq -1 ]]; then
    echo "ERROR: wrong arguments."
    exit 1
fi

if [[ $HController -eq 1 ]]; then
    cd ./modules/HController
    python ./src/main.py &
    cd ../..
fi

python ./src/main.py