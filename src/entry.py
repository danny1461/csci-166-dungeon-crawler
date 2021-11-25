import os
from sys import argv

os.chdir(os.path.dirname(argv[0]))

from Cli import commandLineArgs
from GridWorld import GridWorld
from Graphics.Console import Console

# Kick off the process
mapPath = os.path.join(os.getcwd(), '../dungeons/', commandLineArgs.map + '.txt')
world = GridWorld(fromFile = mapPath, logging = commandLineArgs.logging)
world.teamList = ['agent', 'monster', 'gaia']
renderer = Console(world)

while len(world.teams['agent']) > 0:
	if world.ticks > 100:
		break

	if world.teamNdx == 0:
		renderer.render()
	world.tick()
	
renderer.render()

if len(world.teams['agent']) > 0:
	print('quit because iterations exceeded max')