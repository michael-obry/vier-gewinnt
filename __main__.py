import history

new_game = True

while new_game:
    game = history.History()

    print("Willkommen zu 4 Gewinnt!\
          \nMit der Eingabe 'b' kannst du zu deinem vorletzten Zug zurückspringen, bis du den Anfang des Spieles erreicht hast.\
          \nMit der Eingabe 'f' kannst du wieder zu deinen alten Spielzügen vorwärtsspringen, bis du den ursprüngliche Spielstand erreicht hast.\
          \nSpringst du (mehrmals) zurück und gibst einen neuen Spielzug ein, werden alle Spielstände bis zum aktuellen Spielstand überschrieben \
          \nMit der Eingabe 'q' kannst du das aktuelle Spiel beenden.\
          \n")

    print("Bitte lege den Spielmodus fest.\
          \n1: Person vs. Person\
          \n2: Person vs. KI\
          \n3: KI vs. Person\
          \n4: KI vs. KI\
          \n")

    modus = None
    while True:
            modus = input("Gib eine Zahl zwischen 1 und 4 ein: ")
            try:
                modus = int(modus)
            except ValueError:
                print("Bitte (natürliche) Zahl von 1 bis 4 eingeben")
            else:
                if modus >= 1 and modus <= 4:
                    break
                else:
                    print("Zahl muss zwischen 1 und 4 liegen")

    while game.isgameactive():
        game.print_board(game.get_current_board())
        if game.get_current_player() == 1:
            print("Gelb ist an der Reihe!")
        else:
            print("Rot ist an der Reihe!")
        #### Spielreihenfolge
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
        # Kontrolle, ob jemand gewonnen hat
        if game.get_current_state().control_win():
            print()
            game.print_board(game.get_current_board())
            print("\n\n\nSpieler " + game.get_winner() + " hat gewonnen!")
            break
        # Kontrolle, ob unentschieden
        if game.get_current_state().control_draw():
            print()
            game.print_board(game.get_current_board())
            print("\n\n\nEs steht unentschieden!")
            break
        print()

    ### Neues Spiel oder Spiel beenden
    while True:
        userinput = input("Gib 'q' ein, um das Spiel zu beenden und 'n' um ein neues Spiel zu starten : ")
        if userinput== "q":
            new_game = False
            break
        if userinput == "n":
            del game
            print()
            break

