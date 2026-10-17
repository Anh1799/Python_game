
# Tic Tac Toe Game

board = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]

def print_board():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()

def check_winner(player):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True

    return False

def check_tie():
    return all(cell == "X" or cell == "O" for cell in board)

def play_game():
    current_player = "X"

    print("Welcome to Tic Tac Toe!")

    while True:
        print_board()

        choice = input(f"Player {current_player}, choose 1-9: ")

        if not choice.isdigit():
            print("Please enter a number!")
            continue

        position = int(choice) - 1

        if position < 0 or position > 8:
            print("Choose a number from 1 to 9!")
            continue

        if board[position] in ["X", "O"]:
            print("That spot is already taken!")
            continue

        board[position] = current_player

        if check_winner(current_player):
            print_board()
            print(f"Player {current_player} wins! 🎉")
            break

        if check_tie():
            print_board()
            print("It's a tie!")
            break

        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

play_game()
