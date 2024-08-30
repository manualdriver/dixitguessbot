
-- what is the bot's overall accuracy? ~44% note: just on Ethan's storyteller clues
SELECT 
    (SUM(CASE WHEN correct = TRUE THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS accuracy_percentage
FROM 
    Guess;


-- how certain was the bot when correct? 0.245
-- how certain was the bot when incorrect? 0.237
-- note: small distinction
SELECT 
    correct, 
    AVG(certainty) AS avg_certainty 
FROM 
    Guess 
GROUP BY 
    correct;

-- how many times was each card selected by the bot?
SELECT 
    g.guessed_card, 
    COUNT(*) AS guess_count
FROM 
    Guess g
GROUP BY 
    g.guessed_card, g.correct
HAVING
	g.correct = true;
    
    

-- Selecting a certain round and it's associated cards
SELECT 
    c.card_id, 
    c.deck_index, 
    g.guess_id, 
    g.guessed_card, 
    g.correct 
FROM 
    Card c
JOIN 
    Guess g ON c.guess_id = g.guess_id
WHERE
	g.guess_id = 33;

-- Selecting a certain round for analysis

SELECT * FROM Guess g
WHERE
	g.guess_id = 22
