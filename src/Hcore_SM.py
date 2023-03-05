'''
File: Hcore_SM.py
Created Date: Thursday, October 4th 2020, 11:26:33 pm
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
2020-11-18	Zen	Updating interaction with others module
2020-11-06	Zen	Updating UpdateModules Methods
2021-10-05	Zen	Some adjustments
2023-03-05	Zen	Adding version and updating screen display
'''

import IRONbark
import logging
import curses
import signal
import time
import os

# Global var for transition
global init_ended, running, active, out
init_ended = False
running = False
active = False
out = False

# Global for screen and tracing
global screen, debug #,original_signal
# original_signal = None
screen = None
debug = False

# Global for shared data
global HController_running, HCore_Modules, time_launch, modules
HController_running = False
HCore_Modules = None
time_launch = time.time()
modules = None
crashed = {}
version = "v0.0.0"

#----------------------------------------------------------------------#
# ------------------------------ States ------------------------------ #
#----------------------------------------------------------------------#
def a_initUI():
	# print("a_initUI")
	global running
	global init_ended
	global screen, debug
	global HCore_Modules, time_launch, modules

	if debug:
		logging.debug("Init UI")
		print("Init UI")
	else:
		initSignal()
		screen = curses.initscr()
		screen.clear()
		screen.refresh()

		initColors()

	modules = getModules(time_launch)

	HCore_Modules = IRONbark.Module(file="./data/HCore_Modules.json")
	HCore_Modules["HCore"]["Active"] = True

	running = True
	init_ended = True

def a_Main():
	# print("a_Main")
	global screen, debug
	global modules

	if debug:
		logging.debug("Main")
		print("Main")

		updateModules(modules, 0, 0)
	else:
		screen.clear()
		height, width = screen.getmaxyx()

		updateModules(modules, height, width)
		displayModules(modules, screen)

		screen.refresh()

def a_CheckState():
	# print("a_CheckState")
	global debug

	if debug:
		logging.debug("CheckState")
		print("CheckState")

	time.sleep(0.1)

def a_stopModulesAction():
	# print("a_stopModulesAction")
	global screen, debug
	global running, active
	global modules

	active = False
	running = False

	if debug:
		logging.debug("stopModulesAction")
		print("stopModulesAction")

		updateModules(modules, 0, 0, True)
	else:
		screen.clear()
		height, width = screen.getmaxyx()

		updateModules(modules, height, width, True)
		displayModules(modules, screen)

		screen.refresh()

	time.sleep(0.1)

def a_stopMain():
	# print("a_stopMain")
	global screen, debug
	global HCore_Modules

	if debug:
		logging.debug("stopMain")
		print("stopMain")
	else:

		screen.clear()
		screen.refresh()

	HCore_Modules.stopModule()

#----------------------------------------------------------------------#
# ---------------------------- Transitions --------------------------- #
#----------------------------------------------------------------------#
def t_init():
	# print("t_init")
	return True

def t_startMain():
	# print("t_startMain")
	global init_ended

	return init_ended

def t_endCS():
	# print("t_endCS")
	return True

def t_beginCS():
	# print("t_beginCS")
	global out

	return not out

def t_stopModules():
	# print("t_stopModules")
	global out

	return out

def t_waitStopAction():
	# print("t_waitStopAction")
	global running, active

	return active or running

def t_stopMain():
	# print("t_stopMain")
	global running, active

	return not active and not running

def t_exit():
	# print("t_exit")
	return True

#----------------------------------------------------------------------#
# --------------------------- Sub functions -------------------------- #
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
	global l_str, l_status, l_version
	modules = {}

	modules["HCore Manager"] 		= {"str": ["HCore Manager", [0, 0]], "Status": ["", [0, 0]], "version": ["", [0, 0]]}
	modules["Module name"] 			= {"str": ["    Module Name", [0, 0]], "Status": ["Status", [0, 0]], "version": ["Version", [0, 0]]}
	modules["HController"] 			= {"str": ["HController", [0, 0]], "Status": ["OFF", [0, 0]], "version": ["-.-.-", [0, 0]]}
	modules["HPhysicsEngine"] 		= {"str": ["HPhysicsEngine", [0, 0]], "Status": ["OFF", [0, 0]], "version": ["-.-.-", [0, 0]]}
	modules["HMovement"] 			= {"str": ["HMovement", [0, 0]], "Status": ["OFF", [0, 0]], "version": ["-.-.-", [0, 0]]}
	modules["HPathPlaner"] 			= {"str": ["HPathPlaner", [0, 0]], "Status": ["OFF", [0, 0]], "version": ["-.-.-", [0, 0]]}
	modules["HBatteryMonitoring"] 	= {"str": ["HBatteryMonitoring", [0, 0]], "Status": ["OFF", [0, 0]], "version": ["-.-.-", [0, 0]]}
	modules["StatusBar"] 			= {"str": ["TIME " + getTime(time_launch) + " | STATUS BAR | LOG: ", [0, 0]], "Status": ["NORMAL", [0, 0]], "time": time_launch}

	l_str, l_status, l_version = len("HBatteryMonitoring")+5, len("Status")+5, len("version")

	return modules

def updateModules(modules, height, width, stop=False):
	global debug
	global running, active, out
	global HController_running, HCore_Modules, crashed, version #,modules,
	global l_str, l_status, l_version

	for name in modules:
		UpdateDisplay(name, width, height)

		if name != "HCore Manager" and  name != "StatusBar" and name != "Module name" and name != "HCore Manager" and name != "HPathPlaner" and name != "HBatteryMonitoring" and name != "HPhysicsEngine":
			if debug:
				logging.debug("Module: " + name)
				print("Module: ", name)

			if not HCore_Modules[name].getAvailability():
				modules[name]["Status"][0] = "OFF "
				modules[name]["version"][0] = "-.-.-"

				if name in crashed and crashed[name]:
					os.system("./start.sh " + name + " 1")
					crashed[name] = False

			else:
				modules[name]["Status"][0] = "ON "
				logging.debug(name)
				logging.debug(HCore_Modules[name])

				if HCore_Modules[name]["version"] is None:
					modules[name]["version"][0] = "-.-.-"
				else:
					modules[name]["version"][0] = HCore_Modules[name]["version"]

				running = True

				if name == "HController":
					if "PS3" in HCore_Modules[name]:
						HController_running = not HCore_Modules[name]["PS3"]["ps"]
					elif "Keyboard" in HCore_Modules[name]:
						HController_running = not HCore_Modules[name]["Keyboard"]["esc"]

					if not HController_running:
						HCore_Modules["HCore"]["Active"] = False
						out = True

					# logging.debug("HController_running " + str(HController_running))

				try:
					if int(HCore_Modules["HCore"]["time"][6:]) == int(HCore_Modules[name]["time"][6:]):
						modules[name]["Status"][0] = "ON "
					else:
						if abs(int(HCore_Modules["HCore"]["time"][6:]) - int(HCore_Modules[name]["time"][6:])) < 10:
							modules[name]["Status"][0] = "WAIT"
						elif name not in crashed:
							# 	print(HCore_Modules["HCore"]["time"], HCore_Modules["HMovement"]["time"])
							HCore_Modules[name].close()
							crashed[name] = True
						elif name in crashed:
							del crashed[name]
				except:
					print("TODO")

			# elif "ON" in HCore_Modules[name]["status"]:
			# 	# modules[name][1] = HCore_Modules[name]["status"] + " "

			# 	# if not stop or HCore_Modules[name]["Active"]:
			# 	# 	HCore_Modules[name]["time"] = str(getTime(modules["StatusBar"][4]))

			# 	# if HCore_Modules[name]["Active"]:
			# 	# 	active = True

			# 	running = True

			# 	if name == "HController":
			# 		print("HController")
			# 		HController_running = True
			# else:
			# 	modules[name][1] = HCore_Modules[name]["status"]

def UpdateDisplay(name, width, height):
	global version

	if name == "HCore Manager":
		if HCore_Modules["HCore"]["version"] != None:
			version = modules[name]["version"][0] = "v" + HCore_Modules["HCore"]["version"]
		else:
			modules[name]["version"][0] = version

		modules[name]["str"][1][0] = int((width / 2) - (len(modules[name]["str"][0]) + len(modules[name]["version"][0]) + 5) / 2)
		modules[name]["Status"][1][0] = modules[name]["str"][1][0] + len(modules[name]["str"][0])
		modules[name]["version"][1][0] = modules[name]["Status"][1][0] + len(modules[name]["Status"][0]) + 5
		modules[name]["str"][1][1] = modules[name]["Status"][1][1] = modules[name]["version"][1][1] = int((height / 2) - 4)
		return

	if name == "StatusBar":
		time = getTime(modules[name]["time"])
		modules[name]["str"][0] = "TIME " + time + " | STATUS BAR | LOG: "
		modules[name]["Status"][0] = "NORMAL"
		modules[name]["str"][1][0] = 0
		modules[name]["str"][1][1] = modules[name]["Status"][1][1] = height - 1

		modules[name]["str"][0] = " " * int((width - len(modules[name]["str"][0] + modules[name]["Status"][0]) - 1)/2) + "TIME " + getTime(modules[name]["time"]) + " | STATUS BAR | LOG: "
		modules[name]["Status"][0] = "NORMAL" + " " * int((width - len(modules[name]["str"][0] + modules[name]["Status"][0]) - 1))
		modules[name]["Status"][1][0] = len(modules[name]["str"][0])

		HCore_Modules["HCore"]["time"] = time
		return

	modules[name]["str"][1][0] = int((width/2) - (l_str + l_status + l_version) / 2)
	modules[name]["Status"][1][0] = modules[name]["str"][1][0] + l_str + int(len("Status") - len(modules[name]["Status"][0]) / 2)
	modules[name]["version"][1][0] = modules[name]["Status"][1][0] + l_status - int(len("Status") - len(modules[name]["Status"][0]) / 2) + int(len("Version") - len(modules[name]["version"][0]) / 2)
	modules[name]["str"][1][1] = modules[name]["Status"][1][1] = modules[name]["version"][1][1] = int((height / 2) - 4)


def displayModules(modules, screen):
	step = 0
	color = 1

	for name in modules:
		if "OFF" in modules[name]["Status"][0]:
			color = 1
		elif "ON" in modules[name]["Status"][0]:
			color = 2
		elif "WAIT" in modules[name]["Status"][0]:
			color = 3
		else:
			color = 0

		if name == "StatusBar":
			step = 0
			screen.attron(curses.color_pair(4))
			screen.addstr(modules[name]["str"][1][1], modules[name]["str"][1][0], modules[name]["str"][0])
			screen.addstr(modules[name]["Status"][1][1], modules[name]["Status"][1][0], modules[name]["Status"][0])
			screen.attroff(curses.color_pair(4))
			continue

		screen.addstr(modules[name]["str"][1][1] + step, modules[name]["str"][1][0], modules[name]["str"][0])

		screen.attron(curses.color_pair(color))
		screen.addstr(modules[name]["Status"][1][1] + step, modules[name]["Status"][1][0], modules[name]["Status"][0])
		screen.attroff(curses.color_pair(color))

		screen.addstr(modules[name]["version"][1][1] + step, modules[name]["version"][1][0], modules[name]["version"][0])

		if name == "HCore Manager":
			step += 2
		else:
			step += 1