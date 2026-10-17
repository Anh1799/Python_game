import random

def guess_game():
    number = random.randint(1, 100)
    attempts = 0

    print("🎮 Welcome to Guess the Number!")
    print("Guess a number between 1 and 100.")

    while True:
        guess = int(input("Enter your guess: "))
        attempts += 1

        if guess < number:
            print("Too low! Try again.")
        elif guess > number:
            print("Too high! Try again.")
        else:
            print("🎉 Congratulations!")
            print(f"You guessed it in {attempts} attempts!")
            break

guess_game()
