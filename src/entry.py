import os
from sys import argv

os.chdir(os.path.dirname(argv[0]))

from Cli import commandLineArgs
from GridWorld import GridWorld

# Kick off the process
mapPath = os.path.join(os.getcwd(), '../dungeons/', commandLineArgs.map + '.txt')
world = GridWorld(fromFile = mapPath, logging = commandLineArgs.logging)
teamSortOrder = ['agent', 'human', 'monster', 'gaia']
world.teamList.sort(key = lambda item: teamSortOrder.index(item))

while len(world.teams['agent']) > 0:
	if world.ticks > 100:
		break

	world.tick()

if len(world.teams['agent']) > 0:
	print('quit because iterations exceeded max')