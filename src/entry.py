import os
from sys import argv
os.chdir(os.path.dirname(argv[0]))

from Utils.Cli import commandLineArgs
from Apps.Abstract import Abstract as AbstractApp
from importlib import import_module

# Kick off the process
appName = 'SimulateApp'
if commandLineArgs.train:
	appName = 'TrainingApp'

appModule = import_module('Apps.' + appName)
appClass = getattr(appModule, appName)

app: AbstractApp = appClass()
app.start()