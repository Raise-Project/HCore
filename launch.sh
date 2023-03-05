#File: launch.sh
#Created Date: Monday, February 6th 2023, 11:39:35 pm
#Author: Zentetsu
#
#----
#
#Last Modified: Sun Mar 05 2023
#Modified By: Zentetsu
#
#----
#
#Project: HCore
#Copyright (c) 2023 Zentetsu
#
#----
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#----
#
#HISTORY:
#2020-11-07	Zen	Adding startup script
#2021-10-05	Zen Adding logging system
#2023-03-05	Zen	Adding cleaning function


validate=0
HController=0
HMovement=0
Verbose=0
Clean=0

directory="log"
logFile="/Hexapod.log"

if [ ! -d ~/"$directory" ]; then
	mkdir ~/$directory
fi

while [[ $# -gt 0 ]]; do
	key="$1"

	case $key in
		--HController)
		HController=1
		shift # past value
		;;
		--HMovement)
		HMovement=1
		shift # past value
		;;
		--Verbose)
		Verbose=1
		shift # past value
		;;
		--Clean)
		Clean=1
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
	./start.sh "HController" 1
fi

if [[ $HMovement -eq 1 ]]; then
	./start.sh "HMovement" 2
fi

if [[ $Clean -eq 1 ]]; then
	python ./src/Clean.py
fi

if [[ $Clean -eq 0 ]]; then
	python ./src/main.py ~/$directory$logFile
fi

# clear