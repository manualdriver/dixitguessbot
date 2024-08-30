CREATE TABLE Guess (
    guess_id INT AUTO_INCREMENT PRIMARY KEY,
    guessed_card INT,
    correct BOOLEAN,
    clue VARCHAR(45),
    certainty FLOAT
);

CREATE TABLE Card (
	card_id INT AUTO_INCREMENT PRIMARY KEY,
    deck_index INT,
    guess_id INT,
    FOREIGN KEY (guess_id) REFERENCES Guess(guess_id)
);

DROP TABLE Card;
DROP TABLE Guess;

SELECT * FROM Guess;
SELECT * FROM Card;