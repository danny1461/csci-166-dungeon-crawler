import argparse
from sys import argv, exit
from importlib import import_module

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
		help='Whether to train or not')
parser.add_argument(
		'--trainClass',
		nargs='?',
		type=str,
		default='',
		help='What training code to use')
parser.add_argument(
		'--trainIter',
		nargs='?',
		type=int,
		default=1000,
		help='How many iterations to train with')
parser.add_argument(
		'--episolon',
		nargs='?',
		type=float,
		default=0,
		help='How often to take a random learning action')
parser.add_argument(
		'--alpha',
		nargs='?',
		type=float,
		default=0.3,
		help='How much to consider new knowledge')
parser.add_argument(
		'--discount',
		nargs='?',
		type=float,
		default=0.5,
		help='How much to consider old knowledge')
parser.add_argument(
		'--display',
		nargs='?',
		type=str,
		default='Window',
		help='How much to consider old knowledge')
parser.add_argument(
		'--speed',
		nargs='?',
		type=float,
		default=0.1,
		help='How much to consider old knowledge')
parser.add_argument(
		'--logging',
		nargs='?',
		type=bool,
		default=False,
		help='Whether to enable logging')

commandLineArgs = parser.parse_args(commandLineArgs)

# Couple conditional requirements
if commandLineArgs.trainIter < 0:
	exit('Training iterations should be greater than 0')

if commandLineArgs.trainClass == '':
	exit('Please specify a training class')

commandLineArgs.trainClass = getattr(import_module('Training.' + commandLineArgs.trainClass), commandLineArgs.trainClass)
commandLineArgs.display = getattr(import_module('Graphics.' + commandLineArgs.display), commandLineArgs.display)