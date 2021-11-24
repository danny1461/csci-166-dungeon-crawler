import argparse
from sys import argv, exit

# If no command line args are passed, force the help page
commandLineArgs = argv[1:]
if len(commandLineArgs) == 0:
	commandLineArgs.append('-h')

# Gather arguments
parser = argparse.ArgumentParser(
		description='Simulate an operating system scheduler and job process environment')

parser.add_argument(
		'--map',
		nargs='?',
		type=str,
		default='',
		help='Which map to load')
parser.add_argument(
		'--featExt',
		nargs='?',
		type=str,
		default=50,
		help='Which feature extractor to use')
parser.add_argument(
		'--train',
		nargs='?',
		type=bool,
		default=False,
		help='Whether to train the model or just run it')
parser.add_argument(
		'--trainIter',
		nargs='?',
		type=int,
		default=1000,
		help='How many iterations to train with')
parser.add_argument(
		'--logging',
		nargs='?',
		type=bool,
		default=False,
		help='Whether to enable logging')

commandLineArgs = parser.parse_args(commandLineArgs)

# Couple conditional requirements
if (commandLineArgs.trainIter < 0):
	exit('Training iterations should be greater than 0')