#File: start.sh
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
#2023-02-06	Zen	Adding script to start module

directory="log"
logFile="/Hexapod.log"

cd ./modules/$1
sleep $2 && python ./src/main.py ~/$directory$logFile &
cd ../..