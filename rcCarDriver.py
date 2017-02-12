import serial
import pygame
from pygame.locals import *
import os
import sys
import time

FWD = "FWD"
REV = "REV"
LEFT = "LFT"
RIGHT = "RGHT"
STOP = "STP"
QUIT = "QT"

COMMANDS = {
			"STP":0,
			"RGHT":1,
			"LFT":2,
			"REV":4,
			"REVRGHT":5,
			"REVLFT":6,
			"FWD":8,
			"FWDRGHT":9,
			"FWDLFT":10,
			"QT":9999
			}

PREVIOUS_COMMAND = STOP

def processInput(event):

	newCommand = STOP

	if (event.type == pygame.QUIT):
			newCommand = QUIT

	elif (event.type == KEYDOWN):

			keyinput = pygame.key.get_pressed()

			#complex orders
			if keyinput[pygame.K_q]:
				newCommand = QUIT
			elif keyinput[pygame.K_UP] and keyinput[pygame.K_RIGHT]:
				newCommand = FWD+RIGHT
			elif keyinput[pygame.K_UP] and keyinput[pygame.K_LEFT]:
				newCommand = FWD+LEFT
			elif keyinput[pygame.K_DOWN] and keyinput[pygame.K_RIGHT]:
				newCommand = REV+RIGHT
			elif keyinput[pygame.K_DOWN] and keyinput[pygame.K_LEFT]:
				newCommand = REV+LEFT

			#simple orders
			elif keyinput[pygame.K_UP]:
				newCommand = FWD
			elif keyinput[pygame.K_DOWN]:
				newCommand = REV
			elif keyinput[pygame.K_RIGHT]:
				newCommand = RIGHT
			elif keyinput[pygame.K_LEFT]:
				newCommand = LEFT
	
	elif event.type == pygame.KEYUP:

			#up-right
			if (PREVIOUS_COMMAND == FWD+RIGHT):
				if event.key == pygame.K_RIGHT:
					newCommand = FWD
				elif event.key == pygame.K_UP:
					newCommand = RIGHT

			#up-left
			elif (PREVIOUS_COMMAND == FWD+LEFT):
				if event.key == pygame.K_LEFT:
					newCommand = FWD
				elif event.key == pygame.K_UP:
					newCommand = LEFT

			#back-right
			elif (PREVIOUS_COMMAND == REV+RIGHT):
				if event.key == pygame.K_RIGHT:
					newCommand = REV
				elif event.key == pygame.K_DOWN:
					newCommand = RIGHT

			#back-left
			elif (PREVIOUS_COMMAND == REV+LEFT):
				if event.key == pygame.K_RIGHT:
					newCommand = REV
				elif event.key == pygame.K_DOWN:
					newCommand = LEFT

	return newCommand

def getCommand():

	global PREVIOUS_COMMAND
	newCommand = STOP

	event = pygame.event.wait() 
	if event:
		newCommand = processInput(event)
		PREVIOUS_COMMAND = newCommand
		return newCommand
	else:
		return None


def getCommand2():

	global PREVIOUS_COMMAND
	newCommand = STOP

	for event in pygame.event.get():

		newCommand = processInput()

	PREVIOUS_COMMAND = newCommand
	return newCommand
			


def main():
	os.system('clear')
	print("Starting driver pgm")

	pygame.init()
	pygame.display.set_mode((1,1))
	ser = serial.Serial('/dev/ttyACM1',9600)
	# timeout=1);
	command = STOP

	while True:

		commandKey = getCommand()
		print("Iteration")
		#time.sleep(1)

		if commandKey is None:
			pass
		elif (commandKey and (commandKey != QUIT)):
			command = COMMANDS.get(commandKey,None)
			fCommand = '{0:#0{1}x}'.format(command,4)
			print(commandKey,":",fCommand,":",command)
			ser.write(bytes(fCommand))
		else:
			break
	pygame.quit()
	sys.exit()
	ser.close()



if __name__ == '__main__':
	main()