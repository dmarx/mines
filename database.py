import sqlite3 as sql
import cPickle

with open('tables.sql','r') as f:
    tables_sql = f.read()

save_sql = None   
    
class Database(object):
    def __init__(self, db_name='test.db'):
        self.conn = sql.Connection(db_name)
        self.c = self.conn.cursor() # sql.Cursor(self.conn)
	try:
	    # initialize tables. Error's
	    # out if tables exist.
	    self.c.executescript(tables_sql)
	except Exception, e:
	    print e
    def __gen_new_id(self, table):
        new_id_sql = """
        SELECT max(id) + 1
        FROM """ + table +";" # Unsanitized. Not a great idea. Make it private
        new_id = self.c.execute(new_id_sql).next()[0]
        if not new_id:
	    new_id = 0
        return new_id
    def save_game(self, game, difficulty_text, game_id=None):
        # This is currently experiencing issues because of the 
        # thread "lock" object in Game.timer. Really, all we 
        # need to save is the board and the time elapsed.
        # As we're already storing elapsed separately, might as
        # well just pickle the board instead of the whole game.
        if not game_id:    
            game_id = self.__gen_new_id('saved_games')
        board = cPickle.dumps(game.board)
        remaining_bombs = game.board.remaining_bombs
        elapsed = game.timer.elapsed
        save_sql="""
        INSERT INTO saved_games
        (id, board,difficulty,remaining_bombs, elapsed)
        VALUES (?,?,?,?,?);
        """
        diff_sql = """
        SELECT difficulty FROM dim_difficulty
        WHERE difficulty_text = ?;
        """
        diff = self.c.execute(diff_sql, [difficulty_text] ).next()[0]
        self.c.execute(save_sql, [game_id, board,diff,remaining_bombs, elapsed] )
        self.conn.commit()
    def retrieve_games(self, game_id=None):        
        sql_string = """
        SELECT * FROM saved_games
        """
        if game_id:
	    sql_string += " WHERE id = ?;"
	    res = self.c.execute(sql_string,[game_id]).fetchall()
	else:
            sql_string += ";" # I believe this is unnecessary
            res = self.c.execute(sql_string).fetchall()
        games = []
        for row in res:
	    board, diff, remaining_bombs, elapsed = row
	    # This is a very dirty way of doing things. 
	    # Should really change this so we have the
	    # option to initialize the Game object with
	    # 'board' and 'elapsed' parameters. This feels
	    # very hacky.
	    g=Game(1,1,1)
	    g.board = cPickle.loads(board)
	    g.timer.elapsed = elapsed
	    games.append(g)
	return games
    def delete_saved_game(self, game_id):
        sql_string = """"
        DELETE FROM saved_games
        WHERE id = ? ;"""
        self.c.execute(sql_string, game_id)
        self.conn.commit()
    def __truncate_table(self, table):
        sql_string = "DELETE FROM "+table+";"        
        self.c.execute(sql_string)
        self.conn.commit()
    def reset_saved_games(self):
        self.__truncate_table('saved_games')
    def reset_top_games(self):
        self.__truncate_table('top_games')
    def reset_stats(self):
        #self.__truncate_table('general_stats')
        sql_string = """
        UPDATE general_stats
        SET wins = ?,
            games_played = ?
        WHERE difficulty = ?;
        """
        for diff in (0,1,2):
            self.c.execute(sql_string, (0,0, diff) )
        self.conn.commit()
    def reset_all(self):
        self.reset_saved_games()
        self.reset_top_games()
        self.reset_stats()
    def update_stats(self, difficulty, win=0):
        sql_string = """
        UPDATE general_stats
        SET games_played = games_played +1,
            wins = wins + ?
        WHERE difficulty = 
          (SELECT difficulty
           FROM dim_difficulty
           WHERE difficulty_text = ?);
        """
        # not sure if this is right way to pass values
        self.c.execute(sql_string, (win, difficulty) ) 
        self.conn.commit()
    def update_top_games(self, game):
        pass