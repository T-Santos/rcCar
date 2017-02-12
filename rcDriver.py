import os
import argparse

from remoteController.RemoteController import *

def main():

	os.system('clear')
	print("Starting driver pgm")

	parser = argparse.ArgumentParser(description='Remote Controller')
	parser.add_argument('-o','--serialPort', help='Override serial port', required=False)
	args = parser.parse_args()

	if args.serialPort:
		serialPort = args.serialPort
	else:
		serialPort = '/dev/ttyACM0'

	remote = RemoteController(serialPort)

	remote.receiveEmitCommands()

if __name__ == '__main__':
	main()