import random
import time

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(user, computer, identity):
    if user == computer:
        return "Draw!"
    elif (user == "rock" and computer == "scissors") or \
         (user == "scissors" and computer == "paper") or \
         (user == "paper" and computer == "rock"):
        return f"{identity} wins!"
    else:
        return "computer wins!"
    
identity = input("Enter user id: ")
        
while True:
    user_choice = input("Enter 'rock', 'paper' or 'scissors' (or 'exit'): ")
    if user_choice == "exit":
        print("Thanks for playing! Goodbye.")
        break
    if user_choice not in ("rock", "paper", "scissors"):
        print("Invalid choice")
        continue
    if user_choice in ("rock", "paper", "scissors"):
        time.sleep(1)
        computer_choice = get_computer_choice()
        print(f"Computer choice: {computer_choice}")
        time.sleep(1)
        print(determine_winner(user_choice, computer_choice, identity))
        time.sleep(2)
        
