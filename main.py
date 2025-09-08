import history

new_game = True

while new_game:
    game = history.History()

    print("Welcome to Connect 4!\
          \nBy entering 'b' you can jump back to your previous move "
          "until you reach the beginning of the game.\
          \nBy entering 'f' you can jump back to your more current moves "
          "until you reach the current game field.\
          \nIf you change a previous game field all more current moves are "
          "overwritten.\
          \nBy entering 'q' you can end the current game.\
          \n")

    print("Please enter the game mode.\
          \n1: Person vs. Person\
          \n2: Person vs. KI\
          \n3: KI vs. Person\
          \n4: KI vs. KI\
          \n")

    modus = None
    while True:
            modus = input("Enter a number between 1 and 4: ")
            try:
                modus = int(modus)
            except ValueError:
                print("Please enter a (natural) number between 1 and 4: ")
            else:
                if modus >= 1 and modus <= 4:
                    break
                else:
                    print("Number must lie between 1 and 4.")

    while game.is_game_active():
        game.print_board(game.get_current_board())
        if game.get_current_player() == 1:
            print("It's yellow's turn!")
        else:
            print("It's red's turn!")
        # Game order
        if modus == 1:
            game.player_input()
        elif modus == 2 and game.get_current_player() == 1:
            game.player_input()
        elif modus == 2 and game.get_current_player() == -1:
            game.ki_input()
        elif modus == 3 and game.get_current_player() == 1:
            game.ki_input()
        elif modus == 3 and game.get_current_player() == -1:
            game.player_input()
        elif modus == 4:
            game.ki_input()
        # Check whether someone has won
        if game.get_current_state().control_win():
            print()
            game.print_board(game.get_current_board())
            print("\n\n\nPlayer " + game.get_winner() + " has won!")
            break
        # Check whether there is a draw
        if game.get_current_state().control_draw():
            print()
            game.print_board(game.get_current_board())
            print("\n\n\nIt's a draw!")
            break
        print()

    # New game or end game
    while True:
        userinput = input("Enter 'q' to end the game and 'n' to start a "
                          "new game: ")
        if userinput== "q":
            new_game = False
            break
        if userinput == "n":
            del game
            print()
            break
