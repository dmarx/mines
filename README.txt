MINES
Author: David Marx
Date: 12/24/2012

DISCLAIMER

The motivation for this project was as a learning exercise. It is a deliberate clone
of Microsoft's Minesweeper game in design and functionality, as much as I was able,
as an exercise to learn GUI programming with Tkinter. Microsoft I'm sure has 
copyright on the Minesweeper game, but due to the existence of several widely
distributed free Minesweeper clones, and the educational impetus behind this project,
it is my understanding that any infringement on microsoft's copyright inherent in 
this project fall under fair use protection.

INSTALLATION

The only dependency is python 2.7. To run:

    $ python mines_gui.py

I will attempt to package binaries once I'm satisfied with the implemented features.
    
IMPLEMENTED FEATURES
* Game recognizes a "win" when all flags have been accurately placed.
* Left-click "opens" tiles, right-click toggles flags 
  -> no question mark functionality implemented. Not a fan, personally.
* Right clicking toggles flags.
* Clicking on an empty square iteratively opens all adjacent squares until
  squares touching bombs are found.
* Double left clicking on a tile whose number matches the number of touching flags opens
  all unopenned surrounding tiles.
* Numbers are colored to approximate original MS color scheme.
* On revealing a bomb, all other bombs revealed. "Clicked" bomb highlighted with
  red background, as in MS version.
* Upon end of game, state of all tiles becomes locked.
* Drop down menu allows selection of game difficulty: Beginner, intermediate, expert
  (as in MS version). mines.Game and mines.Board classes permit creation of arbitrary
  configurations.
* Running time (freezes at game over) and remaining bombs count displayed.
* Win or lose condition freezes timer.
--------------------------------------------------------------------------------------
BUGS TO ADDRESS
* Timer doesn't work great. Sometimes starts a second late, sometimes adds a second
  after game ends, sometimes continues counting adding arbitrary amounts. The last
  problem seems to be a non-issue, other problems could probably be eliminated by 
  increasing refresh time in mines.Timer class (currently 0.25s). Also, I believe
  the way I'm using threading causes the terminal window to sometimes stay open even after I close the app.
  
FEATURES TO ADD
* statistics tracking and reset
* "custom" difficulty
* Help menu with about button providing author/version info.
* pause functionality, esp. on game minimization, or better yet anytime
  game app is pushed to background.
* save functionality
  --> current implementation prompts to save when closing window. Should test for game.won condition
      first, since we don't need or want to save completed games. Game_id should be hash of game size
      and bomb locations: upon game completion, attempt to delete saved game maching hash! Anyway,
      we can sort of save, can't retrieve saved games yet. Also, database needs triggers.
* docstring documentation.
* Versioning tags in git.
* Publish to github