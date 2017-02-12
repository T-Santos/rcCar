import serial
import pygame
from pygame.locals import *

class RemoteController(object):

	'''
		Global class data members
	'''
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
	'''
		constructor to init pygame and pyserial instances
	'''
	def __init__(self,serialPort,baudRate=9600,*args,**kwargs):

		self.__prevCommand = RemoteController.STOP
		self.__currCommand = RemoteController.STOP
		self.__serial= serial.Serial(serialPort,baudRate)

		pygame.init()
		pygame.display.set_mode((1,1))

	'''
		destructor to clean up other module instances
	'''
	def __del__(self):
		
		pygame.quit()
		self.__serial.close()

	'''
		purpose: To handle any instersting keyboard inputs
		args: pygame event object
	'''
	def processInput(self,event):

		newCommand = RemoteController.STOP

		if (event.type == pygame.QUIT):
				newCommand = RemoteController.QUIT

		elif (event.type == KEYDOWN):

				keyinput = pygame.key.get_pressed()

				#complex orders
				if keyinput[pygame.K_q]:
					newCommand = RemoteController.QUIT
				elif keyinput[pygame.K_UP] and keyinput[pygame.K_RIGHT]:
					newCommand = RemoteController.FWD+RemoteController.RIGHT
				elif keyinput[pygame.K_UP] and keyinput[pygame.K_LEFT]:
					newCommand = RemoteController.FWD+RemoteController.LEFT
				elif keyinput[pygame.K_DOWN] and keyinput[pygame.K_RIGHT]:
					newCommand = RemoteController.REV+RemoteController.RIGHT
				elif keyinput[pygame.K_DOWN] and keyinput[pygame.K_LEFT]:
					newCommand = RemoteController.REV+RemoteController.LEFT

				#simple orders
				elif keyinput[pygame.K_UP]:
					newCommand = RemoteController.FWD
				elif keyinput[pygame.K_DOWN]:
					newCommand = RemoteController.REV
				elif keyinput[pygame.K_RIGHT]:
					newCommand = RemoteController.RIGHT
				elif keyinput[pygame.K_LEFT]:
					newCommand = RemoteController.LEFT
		
		elif event.type == pygame.KEYUP:

				#up-right
				if (self.__prevCommand == RemoteController.FWD+RemoteController.RIGHT):
					if event.key == pygame.K_RIGHT:
						newCommand = RemoteController.FWD
					elif event.key == pygame.K_UP:
						newCommand = RemoteController.RIGHT

				#up-left
				elif (self.__prevCommand == RemoteController.FWD+RemoteController.LEFT):
					if event.key == pygame.K_LEFT:
						newCommand = RemoteController.FWD
					elif event.key == pygame.K_UP:
						newCommand = RemoteController.LEFT

				#back-right
				elif (self.__prevCommand == RemoteController.REV+RemoteController.RIGHT):
					if event.key == pygame.K_RIGHT:
						newCommand = RemoteController.REV
					elif event.key == pygame.K_DOWN:
						newCommand = RemoteController.RIGHT

				#back-left
				elif (self.__prevCommand == RemoteController.REV+RemoteController.LEFT):
					if event.key == pygame.K_RIGHT:
						newCommand = RemoteController.REV
					elif event.key == pygame.K_DOWN:
						newCommand = RemoteController.LEFT

		return newCommand

	'''
		all inclusive call to receive and send commands from
		keyboard to serial output
	'''
	def receiveEmitCommands(self):

		event = pygame.event.wait()

		while event.type != pygame.QUIT:

			# check for quit key combos
			if (event.type == pygame.KEYUP and event.key == pygame.K_c and 
            	event.mod & pygame.KMOD_CTRL):
				break

			# process pygame event
			self.__currCommand = self.processInput(event)
			self.sendCommand()
			self.__prevCommand = self.__currCommand

			# wait for another event
			event = pygame.event.wait()

	'''
		Send command to serial port
	'''
	def sendCommand(self):

		# get mapped command code to send
		commandCode = RemoteController.COMMANDS.get(self.__currCommand,None)

		# format to hex version
		fCommandCode = '{0:#0{1}x}'.format(commandCode,4)

		print(self.__currCommand,":",fCommandCode,":",commandCode)
		
		# send the code
		self.__serial.write(bytes(fCommandCode))
