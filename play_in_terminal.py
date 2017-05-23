### Play the game of Go in your terminal
# Author: Eric Kalosa-Kenyon
# Date: May 24, 2017
# License: BSD
###

### BEGIN: Code

## Imports

# Standard libraries
import sys
import os
import itertools as itt
from copy import copy

# 3rd party libraries
import numpy as np
import pdb

# Local libraries
import utils

## Preamble

log = utils.make_logger('go-in-terminal', verbose = True)
log.debug("Libraries successfully imported")

## Parameterize game

BOARD_SIZE = 9 # Make an X by X sized go board
DIMENSIONS = 2 # Dimensionality of the board, if not 2, YMMV
PLAYERS = 2 # Players, usually 2, if more or less YMMV
log.debug("Playing on board size {}^{} with {} players".format(
    BOARD_SIZE, DIMENSIONS, PLAYERS))

## Main loop
game_over = False
player = 1
while(game_over == False):
    break
