'''
File: Hcore_SM.py
Created Date: Thursday, October 4th 2020, 11:26:33 pm
Author: Zentetsu

----

Last Modified: Sun Nov 18 2020
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
2020-11-18	Zen	Updating interaction with others modules
2020-11-06	Zen	Updating UpdateModules Method
'''

import IRONbark
import logging
import curses
import signal
import time

global original_signal, out, screen

original_signal = None
screen = None
out = False

global time_launch, modules, init_ended, HCore_Modules, active, running

init_ended = False
time_launch = time.time()
modules = None
HCore_Modules = None
active = False
running = False
HController_running = False

def a_initUI():
	# print("a_initUI")
	global screen, init_ended, modules, time_launch, HCore_Modules

	logging.debug("Init UI")

	initSignal()
	screen = curses.initscr()
	screen.clear()
	screen.refresh()

	initColors()
	modules = getModules(time_launch)

	HCore_Modules = IRONbark.Module(file="./data/HCore_Modules.json")

	init_ended = True

def a_Main():
	# print("a_Main")
	global screen, modules

	logging.debug("Main")

	screen.clear()
	height, width = screen.getmaxyx()

	updateModules(modules, height, width)
	displayModules(modules, screen)

	screen.refresh()

def a_CheckState():
	# print("a_CheckState")

	logging.debug("CheckState")

	time.sleep(0.1)

def a_stopModulesAction():
	# print("a_stopModulesAction")
	global active, running, screen, modules

	logging.debug("stopModulesAction")

	screen.clear()
	height, width = screen.getmaxyx()

	active = False
	running = False

	updateModules(modules, height, width, True)
	displayModules(modules, screen)

	screen.refresh()

	time.sleep(0.1)

def a_stopMain():
	# print("a_stopMain")
	global screen, HCore_Modules

	logging.debug("stopMain")

	screen.clear()

	HCore_Modules.stopModule()

def t_init():
	# print("t_init")
	return True

def t_exit():
	# print("t_exit")
	return True

def t_endCS():
	# print("t_endCS")
	return True

def t_beginCS():
	# print("t_beginCS")
	global out

	return not out

def t_startMain():
	# print("t_startMain")
	global init_ended

	return init_ended

def t_stopModules():
	# print("t_stopModules")
	global out

	return out

def t_waitStopAction():
	# print("t_waitStopAction")
	global active, running

	return active or running

def t_stopMain():
	# print("t_stopMain")
	global active, running

	return not active and not running

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
	modules["HMovement"] = ["HMovement         ", "OFF", [0, 0], [0, 0]]
	modules["HPathPlaner"] = ["HPathPlaner       ", "OFF", [0, 0], [0, 0]]
	modules["HBatteryMonitoring"] = ["HBatteryMonitoring", "OFF", [0, 0], [0, 0]]
	modules["StatusBar"] = ["TIME " + getTime(time_launch) + " | STATUS BAR | LOG: ", "NORMAL", [0, 0], [0, 0], time_launch]

	return modules

def updateModules(moduless, height, width, stop=False):
	global modules, HCore_Modules, active, running, HController_running, out

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
			if not HCore_Modules[name].getAvailability()[1]:
				modules[name][1] = "OFF "
				HCore_Modules.restartModule(name)

				if name == "HController" and HController_running:
					HController_running = False
					out = True
			elif  "ON" in HCore_Modules[name]["status"]:
				modules[name][1] = HCore_Modules[name]["status"] + " "

				if not stop or HCore_Modules[name]["Active"]:
					HCore_Modules[name]["time"] = str(getTime(modules["StatusBar"][4]))

				if HCore_Modules[name]["Active"]:
					active = True

				running = True

				if name == "HController":
					HController_running = True
			else:
				modules[name][1] = HCore_Modules[name]["status"]

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