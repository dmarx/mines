CREATE TABLE saved_games
(id                number -- might want to start autogenerating these in the game obj. Hash of date?
,board 	   string(4000)
,difficulty	   number --0,1,2,3
,remaining_bombs   number
,elapsed           number
,created_date	   date
,last_updated_date date
);

CREATE TABLE general_stats
(difficulty        number
,wins              number
,games_played      number
,created_date	   date
,last_updated_date date
);

CREATE TABLE top_games
(id                number
,difficulty        number
,elapsed           number
,win_date          date
,created_date	   date
,last_updated_date date
);

CREATE TABLE dim_difficulty
(difficulty        number
,difficulty_text   string(15)
,created_date	   date
,last_updated_date date
);

INSERT INTO dim_difficulty
(difficulty, difficulty_text)
values (0, "beginner");

INSERT INTO dim_difficulty
(difficulty, difficulty_text)
values (1, "intermediate");

INSERT INTO dim_difficulty
(difficulty, difficulty_text)
values (2, "expert");

INSERT INTO dim_difficulty
(difficulty, difficulty_text)
values (3, "custom");


INSERT INTO general_stats
(difficulty, wins, games_played)
VALUES (0,0,0);

INSERT INTO general_stats
(difficulty, wins, games_played)
VALUES (1,0,0);

INSERT INTO general_stats
(difficulty, wins, games_played)
VALUES (2,0,0);