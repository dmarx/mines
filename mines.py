""" Minesweeper class """
from random import sample
import time
import threading

debugging = True

class Timer(threading.Thread):
    def __init__(self):
        self.running = False
        self.elapsed = 0
        threading.Thread.__init__(self)
    def run(self):
        n = 0
        if not self.running:
	    self.running = True
	while self.running:
	    time.sleep(0.25)
	    n+= 0.25
	    if int(n)*1.0 == n:
	        self.elapsed += 1
    def pause(self):
        self.running = False
        threading.Thread.__init__(self)
    def reset(self):
        self.__init__()

class Tile(object):
    """
    Individual tiles on the board. Container for tile attributes.
    Bombs will show as "W" in debugging mode.
    """
    def __init__(self):
        self.viewed = False        
        self.number = -1
        self.bomb = False
        self.flag = False
    def set_number(self, value):
        """Set method for number attribute."""
        self.number = value
    def set_bomb(self):
        self.bomb = True
    def set_flag(self):
        if self.viewed:
            print "Can't change flag: tile already viewed"
            return False
        elif self.flag:
            print "Can't set flag: tile already flagged."
            return False
        else:
            self.flag = True
            return True 
    def remove_flag(self): # lot of repeated code between this and set_flag.
        if self.viewed:
            print "Can't change flag: tile already viewed"
            return False
        elif not self.flag:
            print "Can't remove flag: tile not flagged."
            return False
        else:
            self.flag = False
            return True
    def view(self):
        self.viewed = True
        return self.__str__()        
    def __str__(self):
        if self.viewed:
            if self.bomb:
                outstr = "B"
            elif self.number == 0:	        
		outstr =""
            else:
                outstr = str(self.number)
        elif self.flag:
            outstr = "X"
        else:
            if self.bomb and debugging:
                outstr = "W" # Can't confuse this letter with any numbers
            elif debugging: 
                outstr = str(self.number) 
            else: 
                outstr = "?"
        return outstr
    def __repr__(self):
        """
        Sort of cheating, but it's the easiest
        way to display the board properly.
        """
        outstr = self.__str__()
        return outstr

class Board(list):
    #movements = [-1,0,1] # this doesn't work for some reason
    def __init__(self, n_rows, n_cols, n_bombs):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_bombs = n_bombs
        self.remaining_bombs = n_bombs
        self.bomb_locations = set()
        self.flag_locations = set()
        self.viewed_tiles = set() # for passing messages to GUI
        n = n_rows * n_cols
        self.__bomb_indices = sample(range(n), n_bombs)
        ix = -1
        for r in range(n_rows):
            row = []
            for c in range(n_cols):
                ix+=1
                tile = Tile()
                if ix in self.__bomb_indices:
                    tile.set_bomb()
                    self.bomb_locations.add((r,c))
                row.append(tile)
            self.append(row)
        self.__calculate_neighboring_bomb_counts()
    def __calculate_neighboring_bomb_counts(self):
        for row_ix, row in enumerate(self):
            for col_ix, tile in enumerate(row):
                if not tile.bomb:
                    count = self.__calculate_immediate_neighbors(row_ix, col_ix)
                    tile.set_number(count)
                    self[row_ix][col_ix] = tile
    def __calculate_immediate_neighbors(self, row_ix, col_ix, attr="bomb"):
        count = 0        
        movements = [-1,0,1]
        for i in movements:
            new_row_ix = row_ix + i
            if 0<=new_row_ix<self.n_rows:
                for j in movements:
                    new_col_ix = col_ix + j
                    if 0<=new_col_ix<self.n_cols \
                    and eval("self[new_row_ix][new_col_ix]."+attr):
                        count+=1
        return count
    def click_tile(self,row_ix, col_ix):
        """
        If tile is not touching any bombs, DFS through
        nieghbors. Return True iff clicked tile is newly revealed bomb.
        Untested return value.
        """
        movements = [-1,0,1]
        tile = self[row_ix][col_ix]
        if tile.viewed:
            return False
        tile.view()
        print "In board.click_tile, adding %d, %d to board.viewed_tiles" \
	  % (row_ix, col_ix)
        self.viewed_tiles.add((row_ix, col_ix))
        if tile.bomb:
            return True
        if tile.number == 0:
            for i in movements:
                new_row_ix = row_ix + i
                if 0<=new_row_ix<self.n_rows:
                    for j in movements:
                        new_col_ix = col_ix + j
                        if 0<=new_col_ix<self.n_cols \
                        and not (new_row_ix ==row_ix and new_col_ix == col_ix):
                            self.click_tile(new_row_ix, new_col_ix)
    def set_flag(self, row_ix, col_ix):
        if self.remaining_bombs ==0:
            print "Unable to flag position: all flags used." # We'll need a remove flag method
        tile = self[row_ix][col_ix]
        flag_used = tile.set_flag()
        if flag_used:
            self.remaining_bombs += -1
            self.flag_locations.add((row_ix, col_ix))
    def remove_flag(self, row_ix, col_ix):
        if self.remaining_bombs == self.n_bombs:
            print "Unable to remove flag: no flags used."
        tile = self[row_ix][col_ix]
        flag_retrieved = tile.remove_flag()
        if flag_retrieved:
            self.remaining_bombs += 1
            self.flag_locations.remove((row_ix, col_ix))
    def __str__(self):
        outstr = "\t" + str(range(self.n_cols)) + "\n\n"
        for ix, row in enumerate(self):
            outstr += str(ix) + "\t" + str(row) + "\n"
        return outstr
    def surrounding_flags_satisfied(self,row_ix, col_ix):
        """
        Counts flags surrounding a tile to enable left clicking
        viewed tiles to open surrounding tiles.
        """
        tile = self[row_ix][col_ix]
	surr_flags = self.__calculate_immediate_neighbors(row_ix, col_ix, attr="flag")
	print row_ix, col_ix, "surr_flags:", surr_flags, "tile_num:", tile.number
	if surr_flags == tile.number and tile.viewed:
	    return True
	else:
	    return False
class Game(object):
    def __init__(self, n_rows, n_cols, n_bombs):
        self.board = Board(n_rows, n_cols, n_bombs)
        self.won = False
        self.game_over = False
        self.timer = Timer()
        #self.play()
    def activate_timer(self):
        if not self.timer.running:
	    self.timer.start()
    def pause_timer(self):
        if self.timer.running:
            self.timer.pause()
    def open_tile(self, row_ix, col_ix):
        self.activate_timer() # should be redundant
	tile = self.board[row_ix][col_ix]
        if tile.flag:
            self.board.remove_flag(row_ix, col_ix)
        bomb_triggered = self.board.click_tile(row_ix, col_ix)
        if bomb_triggered:
	    #self.game_over = True
	    self.end_game()
	    if debugging:
	        print "bomb_triggered msg recvd."
	self.check_for_win()
    def flip_flag(self, row_ix, col_ix):
        self.activate_timer()
        tile = self.board[row_ix][col_ix]
        if tile.flag:
            self.board.remove_flag(row_ix, col_ix)
        else:
            self.board.set_flag(row_ix, col_ix)
        self.check_for_win()
    def click(self, row_ix, col_ix):
        self.activate_timer()
        self.board.viewed_tiles = set() #reset variable
        self.open_tile(row_ix, col_ix)
    def open_necessarily_safe(self, row_ix, col_ix):
        self.activate_timer()
        self.board.viewed_tiles = set() #reset variable
	movements = [-1,0,1]
	if self.board.surrounding_flags_satisfied(row_ix, col_ix):
	    for i in movements:
		for j in movements:
		    new_row_ix, new_col_ix = row_ix +i, col_ix +j
		    if  0<=new_row_ix<self.board.n_rows \
		    and 0<=new_col_ix<self.board.n_cols:
		        tile = self.board[new_row_ix][new_col_ix]
		    else:
		        continue
		    if (new_row_ix, new_col_ix) != (row_ix, col_ix) \
		    and not tile.flag and not tile.viewed:
		        print "ONS condition satisfied", row_ix, col_ix
			self.open_tile(new_row_ix, new_col_ix)	
			print self.board.viewed_tiles
	print self.board.viewed_tiles
    def check_for_win(self):
	if self.board.remaining_bombs == 0 \
	and self.board.flag_locations == self.board.bomb_locations:
	      #self.game_over = True
	      self.end_game()
	      self.won = True
	      if debugging:
		  print "check_for_win condition satisfied"
    def end_game(self):
        self.pause_timer()
        self.game_over = True        
    def play(self):
        """For playing in terminal."""
        F = "F"
        f = "F"
        while True:
            print self.board
            in_vals = raw_input("Enter (row, col) to click a tile, or (row, col, F): ")
            # This should be sanitized. Oh well.
            try:
                command = eval(in_vals)
                row_ix, col_ix = command[0], command[1]
            except:
                continue
            if len(command) == 3 and command[2] == "F":
                self.flip_flag(row_ix, col_ix)
            else:
                self.click(row_ix, col_ix)            
            self.check_for_win()    
            if self.game_over:		
		if self.won:
		    print "Congratulations! You won!"
		else:
		    print "You triggered a mine :("
		if debugging:
		    print self.board.remaining_bombs
		    print self.game_over
		    print self.board
		break
if __name__ == '__main__':
    debugging = False
    games = 0
    wins =  0
    print 'Type "Q" at any time to quit'
    while True:        
        dim = raw_input("Set dimensions (rows, columns, bombs): ")
        if str(dim) == "Q":
            break
        try:
            n_rows, n_cols, n_bombs = eval(dim)
        except:
            continue
        g = Game(n_rows, n_cols, n_bombs)
        games +=1
        g.play()
        if g.won:
            wins += 1
        print "Wins: %d, Games: %d" % (wins, games)
        play_again = raw_input("Play again (y/n)?")
        play_again.lower()
        if play_again == 'n':
            break
        