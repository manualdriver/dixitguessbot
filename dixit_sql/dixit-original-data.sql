CREATE TABLE Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    is_bot BOOLEAN,
    name VARCHAR(45)
);

CREATE TABLE Game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    winner_id INT, -- maybe not needed
    FOREIGN KEY (winner_id) REFERENCES Player(player_id) -- maybe not needed: removing this could simplify inserts
);

CREATE TABLE Round (
    round_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    round_number INT, -- in the game, which round are we in?
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);

CREATE TABLE Round_Player (
    round_id INT,
    player_id INT,
    score INT, -- just the points they scored in that round, not running total
    role ENUM('storyteller', 'guesser'),
    PRIMARY KEY (round_id, player_id),
    FOREIGN KEY (round_id) REFERENCES Round(round_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

SELECT * FROM Player;
SELECT * FROM Game;
SELECT * FROM Round;
SELECT * FROM Round_Player;