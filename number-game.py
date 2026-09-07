import random

playing = True

total_guesses = 0
games_played = 0

while playing:

    number = random.randint(1, 100)
    guesses = 0
    guessing = True

    while guessing:
        guess = int(input("Guess a number 1 through 100: "))

        if guess < number:
            print("Your guess is too low")
            guesses += 1

        if guess > number:
            print("Your guess is too high")
            guesses += 1

        if guess == number:
            print("You successfully guessed the number!")
            guesses += 1
            total_guesses += guesses
            games_played += 1
            guessing = False
            average_guesses = total_guesses / games_played
            print("You guessed the number in", guesses, "guesses")
            print("Your average guesses per game:", average_guesses)

    playing = input("Would you like to play again? ")

    if playing.lower() == "yes":
        playing = True
    else:
        playing = False