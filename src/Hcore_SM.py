'''
File: Hcore_SM.py
Created Date: Thursday, October 4th 2020, 11:26:33 pm
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

import IRONbark
import curses
import signal
import time

global original_signal, out, screen

original_signal = None
screen = None
out = False

global time_launch, modules, init_ended, HCore_Modules

init_ended = False
time_launch = 0
modules = None
HCore_Modules = None

def a_initUI():
	global screen, init_ended, modules, time_launch, HCore_Modules

	initSignal()
	screen = curses.initscr()
	screen.clear()
	screen.refresh()

	initColors()
	modules = getModules(time_launch)

	HCore_Modules = IRONbark.Module(file="./data/HCore_Modules.json")

	init_ended = True

def a_Main():
	global screen, modules

	screen.clear()
	height, width = screen.getmaxyx()

	updateModules(modules, height, width)
	displayModules(modules, screen)

	screen.refresh()

def a_CheckState():
	time.sleep(0.1)

def t_init():
	return True

def t_exit():
	global screen, out

	screen.clear()

	return out

def t_endCS():
	return True

def t_beginCS():
	return not out

def t_startMain():
	global init_ended

	return init_ended

#----------------------------------------------------------------------#
def initSignal():
	original_sigint = signal.getsignal(signal.SIGINT)
	signal.signal(signal.SIGINT, stopSM)

def stopSM(signum, frame):
	global out

	out = True

def initColors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

def getTime(start):
    time_elapsed = ""
    seconds = time.time() - start

    hours = int(seconds / 3600)
    minutes = int(seconds % 3600 / 60)
    seconds = int(seconds % 60)

    if hours < 10:
        time_elapsed += "0"+str(hours)
    else:
        time_elapsed += str(hours)

    if minutes < 10:
        time_elapsed += ":0"+str(minutes)
    else:
        time_elapsed += ":"+str(minutes)

    if seconds < 10:
        time_elapsed += ":0"+str(seconds)
    else:
        time_elapsed += ":"+str(seconds)

    return time_elapsed

def getModules(time_launch):
	modules = {}

	modules["HCore Manager"] = ["HCore Manager", "", [0, 0], [0, 0]]
	modules["Module name"] = ["Module name    ", "Status", [0, 0], [0, 0]]
	modules["HController"] = ["HController       ", "OFF", [0, 0], [0, 0]]
	modules["HPhysicsEngine"] = ["HPhysicsEngine    ", "OFF", [0, 0], [0, 0]]
	# modules["HMovement"] = [" *HMovement       ", "OFF", [0, 0], [0, 0]]
	modules["HPathPlaner"] = ["HPathPlaner       ", "OFF", [0, 0], [0, 0]]
	modules["HBatteryMonitoring"] = ["HBatteryMonitoring", "OFF", [0, 0], [0, 0]]
	modules["StatusBar"] = ["TIME " + getTime(time_launch) + " | STATUS BAR | LOG: ", "NORMAL", [0, 0], [0, 0], time_launch]

	return modules

def updateModules(moduless, height, width):
	global modules, HCore_Modules

	for name in modules:
		if name == "HCore Manager":
			modules[name][2][0] = int((width / 2) - (len(modules[name][0]) / 2))
			modules[name][2][1] = modules[name][3][1] = int((height / 2) - 4)
			continue

		if name == "StatusBar":
			modules[name][0] = "TIME " + getTime(modules[name][4]) + " | STATUS BAR | LOG: "
			modules[name][1] = "NORMAL"
			modules[name][2][0] = 0
			modules[name][2][1] = modules[name][3][1] = height - 1

			modules[name][0] = " " * int((width - len(modules[name][0] + modules[name][1]) - 1)/2) + "TIME " + getTime(modules[name][4]) + " | STATUS BAR | LOG: "
			modules[name][1] = "NORMAL" + " " * int((width - len(modules[name][0] + modules[name][1]) - 1))
			modules[name][3][0] = len(modules[name][0])
			continue

		modules[name][2][0] = int((width/2) - ((len(modules[name][0]) + 13) / 2))
		modules[name][3][0] = modules[name][2][0] + len(modules[name][0]) + 10
		modules[name][2][1] = modules[name][3][1] = int((height / 2) - 4)

		if name != "Module name" and name != "HCore Manager":
			if HCore_Modules[name][0] is None:
				modules[name][1] = "OFF "
			elif  "ON" in HCore_Modules[name][0]["status"]:
				modules[name][1] = HCore_Modules[name][0]["status"] + " "
			else:
				modules[name][1] = HCore_Modules[name][0]["status"]

def displayModules(modules, screen):
	step = 0
	color = 1

	for name in modules:
		if "OFF" in modules[name][1]:
			color = 1
		elif "ON" in modules[name][1]:
			color = 2
		elif "WAIT" in modules[name][1]:
			color = 3
		else:
			color = 0

		if name == "StatusBar":
			step = 0
			screen.attron(curses.color_pair(4))
			screen.addstr(modules[name][2][1], modules[name][2][0], modules[name][0])
			screen.addstr(modules[name][3][1], modules[name][3][0], modules[name][1])
			screen.attroff(curses.color_pair(4))
			continue

		screen.addstr(modules[name][2][1] + step, modules[name][2][0], modules[name][0])

		screen.attron(curses.color_pair(color))
		screen.addstr(modules[name][3][1] + step, modules[name][3][0], modules[name][1])
		screen.attroff(curses.color_pair(color))

		if name == "HCore Manager":
			step += 2
		else:
			step += 1