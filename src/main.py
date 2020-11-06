'''
File: main.py
Created Date: Thursday, October 4th 2020, 12:31:07 am
Author: Zentetsu

----

Last Modified: Fri Nov 06 2020
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
'''


from CorState import StateMachine
import curses
import signal

from SharedMemory import Server
import time

from IRONbark import Module

if __name__ == "__main__":
    state_machine = StateMachine("Hcore")
    state_machine.loadJSON("./data/HCore_SM.json")

    state_machine.start()

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