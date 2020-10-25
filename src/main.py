'''
File: main.py
Created Date: Thursday, October 4th 2020, 12:31:07 am
Author: Zentetsu

----

Last Modified: Sun Oct 25 2020
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
'''


from CorState import StateMachine
import curses
import signal


if __name__ == "__main__":
    state_machine = StateMachine("Hcore")
    state_machine.loadJSON("./data/HCore_SM.json")

    state_machine.start()