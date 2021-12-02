# csci-166-dungeon-crawler

A simple project utilizing full AI agents for enemies and heroes and seeing what strategies arise through trials.

The main story is that you are stuck in a spikepit filled labrynth with minotaurs. In each room the agent will have the decision to run away from the minotaur or try to immediatly go towards the exit. The monster will move towards the player and the player agent will move towards the monster as a reward for killing it.


Going into the src folder and typing python.exe .\entry.py --h will present this output

>options:
>usage: entry.py [-h] [--map [MAP]] [--featExt [FEATEXT]] [--train [TRAIN]] [--trainIter [TRAINITER]] [--logging [LOGGING]]
>  -h, --help            show this help message and exit
>  --map [MAP]           Which map to load
>  --featExt [FEATEXT]   Which feature extractor to use
>  --train [TRAIN]       Whether to train the model or just run it
>  --trainIter [TRAINITER]
>                        How many iterations to train with
> --logging [LOGGING]   Whether to enable logging

### Running
`python.exe .\entry.py --map gaia --trainClass FirstTry`

### Training
`python.exe .\entry.py --map gaia --trainClass FirstTry --train 1 --trainIter 100`

TODO:

- [x] Implement entry file
- [x] Offload process argument processing to helper class so Agent class can know what feature extractor was requested
- [x] Implement simple graphics library
- [x] Flesh out monster class
- [x] Flesh out agent class
- [x] Code up training wrapper for gridworld
