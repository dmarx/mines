from Tkinter import *
import tkMessageBox
import mines as m
import time
from database import Database

text_color = (
	  None,		# 0 
	  'blue',	# 1
	  'green3',	# 2
	  'red',	# 3
	  'dark blue',	# 4
	  'maroon',	# 5
	  'turquoise',	# 6
	  'magenta',	# 7
	  'black'	# 8
	  )

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.db = Database('mines.db')
        self.pack()
        self.beginner()
        
        self.bombs_label = Label(text="Bombs Remaining:")
        self.bombs_label.pack({"side":"left"})
        self.bombs_count = Label(text=self._game.board.remaining_bombs)
        self.bombs_count.pack({"side":"left"})
        
        self.time_label = Label(text="0")
        self.time_label.pack({"side":"right"})
        self.update_timer()
        
        self.menubar = Menu(self, relief="flat")
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Game", menu=menu)
        menu.add_command(label="Beginner", command=self.beginner)
        menu.add_command(label="Intermediate", command=self.intermediate)
        menu.add_command(label="Expert", command=self.expert)
        
        menu.add_separator()
        menu.add_command(label="Quit", command=self.master.quit)
        self.master.config(menu=self.menubar)   
        
        # Create event handler to enable game save prompt
        self.master.protocol("WM_DELETE_WINDOW", self.quit_handler)
        
    def update_timer(self):
        self.time_label.config(text = str(self._game.timer.elapsed))
        self.master.after(1000, self.update_timer)
    def build_game(self,n_rows, n_cols, n_bombs):
        try:
	    self.clear_buttons()
            self.time_label.config(text = "0")
            self.bombs_count.config(text = bombs)
        except:
	    pass
        self.buttons = []
	self._game = m.Game(n_rows,n_cols,n_bombs)
	self.map_buttons()
    def beginner(self):
	self.build_game(9,9,10)
	self.difficulty = "beginner"
    def intermediate(self):
	self.build_game(16,16,40)
	self.difficulty = "intermediate"
    def expert(self):
	self.build_game(16,30,99)
	self.difficulty = "expert"
    def map_buttons(self):
	n = 0
	for row_ix, row in enumerate(self._game.board):
	    self.buttons.append([])
	    for col_ix, tile in enumerate(row):
		n +=1
		b = Button(self, width = 1, height = 1)
		b.tile = tile
		b.row_ix = row_ix
		b.col_ix = col_ix 
		#b["command"] =  lambda a=row_ix, b=col_ix: self.on_left_click(row=a, col=b)
		b.bind('<Button-1>', lambda event, a=row_ix, b=col_ix: self.on_left_click(row=a, col=b) )
		b.bind('<Double-Button-1>', lambda event, a=row_ix, b=col_ix: self.on_double_left_click(row=a, col=b) )
		b.bind('<Button-3>', lambda event, a=row_ix, b=col_ix: self.on_right_click(row=a, col=b) )
		b.grid(row=row_ix, column=col_ix) 
		self.buttons[-1].append(b)
	#for row in self.buttons: print row
    def clear_buttons(self):
        for row in self.buttons:
	    for b in row:
	        b.destroy()
	self.buttons = []
    def on_right_click(self, row, col):
        b = self.buttons[row][col]        
        if self._game.game_over or b.tile.viewed:
	    # do nothing---maybe should be pass
	    return "break"
	self._game.flip_flag(row, col)	
	if b.tile.flag:
	    b.configure(text = str(b.tile))
	else:
	    b.configure(text = "")
	bombs = self._game.board.remaining_bombs
	print bombs
	self.bombs_count.config(text = bombs)
    def on_left_click(self, row, col):
        if self._game.game_over:
	    # do nothing...maybe should be "pass"
	    return "break"
        
	self._game.click(row, col)
	return self.show_viewed_tiles()
	#iterate through and open all just openned tiles
    def show_viewed_tiles(self):
	for row_ix, col_ix in self._game.board.viewed_tiles:
	    b = self.buttons[row_ix][col_ix]
	    b.configure(
		text = str(b.tile), 
		relief="sunken", 
		fg = text_color[b.tile.number],		
		) 
	    if b.tile.bomb:
		b.configure(bg = "red")
		self.reveal_mines()
	# this might keep the default bindings from coming into play, 
	# keeping the initial button depressed.
        return "break" 
    def on_double_left_click(self, row, col):
        print "double_click"
        self._game.open_necessarily_safe(row,col)
        if self._game.board[row][col].viewed:
	  for row_ix, col_ix in self._game.board.viewed_tiles:
	      print row_ix, col_ix, "viewed. calling show_viewed_tiles"
	      if self._game.game_over:
	      # do nothing...maybe should be "pass"
	          return "break"
	      return self.show_viewed_tiles()
	return "break"
    def reveal_mines(self):
	for row_ix, col_ix in self._game.board.bomb_locations:
	    self._game.click(row_ix, col_ix)
	    b = self.buttons[row_ix][col_ix]
	    
	    b.configure(
		text = str(b.tile), 
		relief="sunken", 
		fg = "black")
        return "break"
    def quit_handler(self):
        # askyesnocancel returns True, False or None
        if not self._game.game_over:
	  save_response = tkMessageBox.askyesnocancel("Quit?", "Would you like to save your game?")
	  if save_response is None: #cancel
	      return
	  elif save_response: #yes (save)
	      self.db.save_game(self._game, self.difficulty)
        root.destroy()        #no (don't save) or game_over
  
if __name__ == "__main__":
    root = Tk()
    root.wm_title("Mines")
    app = App(root)
    app.mainloop()