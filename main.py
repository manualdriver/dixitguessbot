import os
import random
from typing import Tuple, List
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import errorcode
from model_manager import ModelManager
from players import Bot
from deck import *

def db_connect():
    print("attempting to connect to db")
    try:
        cnx = mysql.connector.connect(user=os.getenv('USER'),
                                      password=os.getenv('PASSWORD'),
                                      host='dixitdb.cdguq4e4c4jo.us-east-2.rds.amazonaws.com',
                                      database='dixitdb')
        
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def insert_guess(cnx, correct: bool, guessed_card: str, clue: str, chosencards: List[str], certainty: float):
    guessed_card_int = int(guessed_card.split('/')[-1].split('.')[0][-2:])
    
    cursor = cnx.cursor()

    insert_query = """
        INSERT INTO Guess (guessed_card, correct, clue, certainty)
        VALUES (%s, %s, %s, %s)
        """

    cursor.execute(insert_query, (guessed_card_int, correct, clue, certainty))
    
    
    cnx.commit()

    guess_id = cursor.lastrowid
    
    print(f"Inserted guess ID: {guess_id}")
    
    insert_query = """
        INSERT INTO Card (deck_index, guess_id)
        VALUES (%s, %s)
        """
        
    for card in chosencards:
        deck_index = int(card.split('/')[-1].split('.')[0][-2:])
        cursor.execute(insert_query, (deck_index, guess_id))
    
    cnx.commit()
    
    cursor.close()

def main():
    # added .env loader
    load_dotenv()
    # Configure DB
    cnx = db_connect()
    terminal_game_loop(cnx)
    
def terminal_game_loop(cnx):
    model_manager = ModelManager()
    guesser = Bot(model_manager)
    deck = setup_deck()

    while True:
        print(f"\nNew Round: select card to storytell: ")
        storyteller_card_index, clue = storyteller_turn()
        print("selected card:")
        storyteller_card = deck.pop(storyteller_card_index)
        print(storyteller_card)
        
        print("selected clue: ")
        print(clue)
        
        random.shuffle(deck)
        chosencards = []
        for i in range(5):
            chosencards.append(deck[i])
        chosencards.append(storyteller_card)
        
        print("bot choosing from: ")
        for card in chosencards:
            print(card)
        certainty, bot_guess = guesser.choose_card_based_on_clue(clue, chosencards)
        print("bot found:")
        print(bot_guess)
        correct = (storyteller_card == bot_guess)
        print("Correct? ")
        print(correct)
        
        deck = setup_deck()
        insert_guess(cnx, correct, bot_guess, clue, chosencards, certainty )

    

def storyteller_turn() -> Tuple[int, str]:
    while True:
        try:
            choice = int(input("Choose a card by entering its number: ")) - 1
            if 0 <= choice < 98:
                break
            else:
                print("Invalid choice. Please select a valid card number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    clue = input("Enter a clue for your card: ").strip()
    return choice, clue

if __name__ == "__main__":
    main()
