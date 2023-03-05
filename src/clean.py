'''
File: clean.py
Created Date: Wednesday, March 1st 2023, 6:40:53 pm
Author: Zentetsu

----

Last Modified: Sun Mar 05 2023
Modified By: Zentetsu

----

Project: src
Copyright (c) 2023 Zentetsu

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
2023-03-05	Zen	Creating cleaning script
'''


import posix_ipc

elements = ["HController", "Hcore", "HMovement"]

for e in elements:
    try:
        posix_ipc.unlink_shared_memory("/psm_" + e)
        semaphore.unlink()
        print("psm ", e)
    except:
        pass
        print("Already clean ", e)
    try:
        posix_ipc.unlink_shared_memory("/psm_" + e + "_usr")
        print("psm_usr ", e)
    except:
        pass
        print("Already clean ", e)
    try:
        semaphore = posix_ipc.Semaphore("/sem_" + e)
        semaphore.unlink()
        print("sem", e)
    except:
        pass
        print("Already clean ", e)