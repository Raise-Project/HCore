'''
File: main.py
Created Date: Thursday, October 4th 2020, 12:31:07 am
Author: Zentetsu

----

Last Modified: Sun Mar 05 2023
Modified By: Zentetsu

----

Project: HCore
Copyright (c) 2020 Zentetsu

----

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

----

HISTORY:
2020-11-06	Zen	Test for SM and Module
2021-10-05  Zen Adding logging system
'''


from CorState import StateMachine
import curses
import signal

from SharedMemory import SharedMemory
import time

from IRONbark import Module
import logging
import sys
import os

if __name__ == "__main__":
	logging.basicConfig(filename=sys.argv[1], format='%(asctime)s - HCore - %(levelname)s - %(message)s', level=logging.DEBUG)

	f = open(os.devnull, 'w')
	sys.stdout = f

	logging.info('Init SM')
	state_machine = StateMachine("Hcore")

	logging.info('Loading SM')
	state_machine.loadJSON("./data/HCore_SM.json")

	logging.info('Starting SM')
	state_machine.start()
	logging.info('Stoping SM')

	#########################################################

	# m = Module(file="./data/HCore_Modules.json")

	# print(m, m["HController"])

	# while True:
	#     print(m["HController"])
	#     if not m["HController"].getAvailability()[1]:
	#         m.restartModule("HController")
	#     time.sleep(0.1)

	#     try:
	#         if m["HController"]["Keyboard"]["esc"]:
	#             break
	#     except:
	#         pass


	# m.stopModule()

	#########################################################

	# s = Server("test")
	# while True:
	#     print(s)
	#     if not s.getAvailability()[1]:
	#         s.reconnect()
	#     time.sleep(0.1)