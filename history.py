import numpy as np
import math
import os
import random
os.system('color')



#### Größe des Spielfeldes wird festgelegt und Funktion für neues Spielfeld definiert
m=8
n=8

sign_arrow = b'\xE2\x86\x93'.decode('utf8')

def create_board():
    board = np.empty(m*n)
    board[:]=0
    board = board.reshape(m,n)
    return board


##############################
###### Klasse Spielzug #######
##############################

class State:
    """Mit der Klasse State sollen Instanzen gebildet werden, die Daten zum
       aktuellen Spielstand verwalten und die Elemente der Klasse History bilden"""
    def __init__(self, board):
        self.__board = board

    def get_board(self):
        """Gibt eine Kopie des Spielbrettes eines Spielstandes (State) zurück"""
        return self.__board.copy()

    def control_win(self):
        """Prüft, ob es sich beim Spielstand (State), um einen finalen Spielstand - Gewinn - handelt.
           Gibt boolean zurück."""
        board = self.__board
        for i in range(0,m):
            for j in range(0,n):
                if board[i, j] != 0:
                    if ((j + 3) < n and board[i, j] == board[i, j+1] == board[i, j+2] == board[i, j+3]):  # Reihen prüfen
                        return True
                    if ((i + 3) < m and board[i, j] == board[i+1, j] == board[i+2, j] == board[i+3, j]): # Spalten prüfen
                        return True
                    if ((i + 3) < m and (j + 3) < n and board[i, j] == board[i+1, j+1] == board[i+2, j+2] == board[i+3, j+3]): # Hauptdiagonale prüfen
                        return True
                    if ((i + 3) < m  and (j - 3) >=0 and board[i, j] == board[i+1, j-1] == board[i+2, j-2] == board[i+3, j-3]): # Nebendiagonale prüfen
                        return True
        return False

    def control_draw(self):
        """Prüft, ob es sich beim Spielstand (State), um einen finalen Spielstand - Unentschieden - handelt.
           Gibt boolean zurück."""
        board = self.__board
        draw = True
        for i in range(0,m):
            for j in range(0,n):
                if (board[i, j] == 0):
                    draw = False
        if draw:
            self.__active = False
        return draw

    def get_heuristic(self):
        """Gibt für den Spielstand (State) eine Heuristik für die Reward-Methode zurück.
           Wenn Wert positiv, wird davon ausgegangen, dass Spielbeginner einen Vorteil im betreffenden Spielstand hat.
           Wenn Wert negativ, wird davon ausgegangen, dass Herausforderer einen Vorteil im betreffenden Spielstand hat."""
        board = self.__board
        result = 0
        for i in range(0,m):
            for j in range(0,n):
                patterns = list()
                ## Tendenz zur Mitte
                if j >= 2 and j < n-2 and board[i, j]!=0:
                    result += board[i, j]
                ## Reihen werden auf Muster geprüft
                if (j + 3) < n:
                    patterns.append((board[i, j], board[i, j+1], board[i, j+2], board[i, j+3]))
                ## Spalten werden auf Muster geprüft
                if (i + 3) < m:
                     patterns.append((board[i, j], board[i+1, j], board[i+2, j], board[i+3, j]))
                ## Hauptdiagonalen werden auf Muster geprüft
                if (j + 3) < n and (i + 3) < m:
                     patterns.append((board[i, j], board[i+1, j+1], board[i+2, j+2], board[i+3, j+3]))
                ## Nebendiagonalen werden auf Muster geprüft 
                if (j - 3) >= 0 and (i + 3) < m:
                     patterns.append((board[i, j], board[i+1, j-1], board[i+2, j-2], board[i+3, j-3]))
                ## Belohnung für Muster
                for pat in patterns:
                    if pat != (0,0,0,0) and (not (1 in pat) or not (-1 in pat)) and -1 < sum(pat) > 1:
                        if pat == (1,1,0,0) or pat == (-1,-1,0,0) or pat == (0,1,1,0) or pat == (0,-1,-1,0) or pat == (0,0,1,1) or pat == (0,0,-1,-1):
                            result += sum(pat)*5
                        elif pat == (1,0,0,1) or pat == (-1,0,0,-1) or pat == (1,0,1,0) or pat == (-1,0,-1,0) or pat == (0,1,0,1) or pat == (0,-1,0,-1):
                            result += sum(pat)*12
                        elif pat == (1,1,1,0) or pat == (-1,-1,-1,0) or pat == (0,1,1,1) or pat == (0,-1,-1,-1):
                            result += sum(pat)*5
                        elif pat == (1,0,1,1) or pat == (-1,0,-1,-1) or pat == (1,1,0,1) or pat == (-1,-1,0,-1):
                            result += sum(pat)*10
                del patterns
        return result

#############################
###### Klasse History #######
#############################

class History:    
    def __init__(self):
        """Mit der Klasse State sollen Instanzen gebildet werden, die Daten zum
        aktuellen Spielstand verwalten und die Elemente der Klasse History bilden"""
        self.__hist=[State(create_board())]
        self.__id = 0
        self.__active = True ### Gibt an, ob aktuelles Spiel noch aktiv ist
        self.__current_player = 1

    def get_current_player(self):
        return self.__current_player

    def get_winner(self):
        """Gibt Farbe des Gewinners als String zurück"""
        winner = self.__current_player * (-1) ### Rückschluss auf Gewinner, nachdem Gewinner-State erkannt wurde mit control_win() aus Klasse State.
        if winner == 1:
            return "gelb"
        else:
            return "rot"

    def get_current_board(self):
        return self.__hist[self.__id].get_board()

    def get_current_state(self):
        return self.__hist[self.__id]

    def player_input(self):
        """Die Spielereingabe (einer Person) wird auf Gültigkeit geprüft.
           Möglichkeit Spiel über 'q' zu beenden.
           Vorheriger Spielstand des aktuellen Spielers in History (wenn vorhanden) durch 'b' erreichbar.
           Nächster Spielstand des aktuellen Spielers in History (wenn vorhanden) durch 'f' erreichbar.
           Wird ein alter Spielstand verändert, werden fortgeschrittenere Spielstände (> id) überschrieben.
           Ansonsten nur Integer zwischen 1 und n erlaubt, ansonsten Aufforderung Integer zwischen 1 und n zu verwenden.
           Wenn neuer Spielstand (State) gültig, wir der neue Spielstand in History gespeichert."""
        while True:
            userinput = input("Gib eine Zahl zwischen 1 und " + str(n) + " ein: ")
            # Spiel kann durch Spieler beendet werden mit Eingabe 'q'
            if userinput== "q":
                self.__active = False
                break
            # Vorheriger Spielstand in History des aktuellen Spielers
            if userinput == "b" and (self.__id - 2 >= 0):
               self.__id = self.__id - 2
               board = self.__hist[self.__id].get_board()
               print()
               self.print_board(board)
            elif userinput == "b" and (self.__id - 2 < 0):
                print("Du kannst nicht weiter zurückgehen, du hast den Anfang des Spieles erreicht")
            # Nächster Spielstand in History des aktuellen Spielers
            elif userinput == "f" and ((self.__id + 3) <= len(self.__hist)):
               self.__id = self.__id + 2
               board = self.__hist[self.__id].get_board()
               print()
               self.print_board(board)
            elif userinput == "f" and ((self.__id + 3) > len(self.__hist)):
                print("Du kannst nicht weiter vorwärts gehen, du hast den aktuellsten Spielstand erreicht")
            # Prüfung der Eingabe auf Gültigkeit und Verwaltung der Spielstände in History
            else:
                try:
                        userinput = int(userinput)
                except ValueError:
                        print("Bitte (natürliche) Zahl von 1 bis " + str(n) + " eingeben")
                else:
                    if userinput >= 1 and userinput <= n:
                        player = self.get_current_player()
                        board = self.get_current_board()
                        row = self.__islegalmove(userinput - 1, board)  ### Userspalten und Matrixindizes unterscheiden sich um den Wert 1
                        if row >= 0:   ### Prüfen, ob es ein gültiger Zug war, wenn nicht ist row == -1
                            while (self.__id + 1) < len(self.__hist):  ### fortgeschrittenere Spielstände löschen, falls älterer Spielstand in History geändert wurde
                                self.__hist.pop(self.__id + 1)
                            board[row, userinput - 1] = player
                            self.__current_player = self.__change_player(self.__current_player)
                            new_move = State(board)
                            self.__id = self.__id + 1
                            self.__hist.append(new_move)
                            return
                        else:
                            print("Spalte ist voll, bitte eine andere Spalte wählen")
                    else:
                        print("Zahl muss zwischen 1 und " + str(n) + " liegen")

    def ki_input(self):
        """Berechnet nächsten Spielzug gegeben des aktuellen Spielzuges für die KI und fügt das Ergebnis zu einer Instanz von History hinzu.
           Suchtiefe kann angepasst werden."""
        player = self.get_current_player()
        state = self.get_current_state()
        depth = 5
        result = self.alpha_beta(state, player, -math.inf, math.inf, depth)
        self.__id = self.__id + 1
        self.__current_player = self.__change_player(self.__current_player)
        self.__hist.append(result[1])
                   
    def isgameactive(self):
        """Gibt zurück (boolean), ob Spiel noch aktiv"""
        return self.__active

    #### AlphaBeta Hilfsmethoden ####
    def expand_state(self, state, player, a, b):
        """Gibt anhand des aktuellen Spielstandes, Spieler und Range des Spielinputs, Liste aller nächsten Spielzüge zurück"""
        new_states = []
        if not (state.control_win() or state.control_draw()):
            for j in range(a,b):
                new_board = state.get_board()
                row = self.__islegalmove(j, new_board)
                if row >= 0:
                    new_board[row, j] = player
                    new_state = State(new_board)
                    new_states.insert(j, new_state)
        return new_states

    def get_reward(self, state, player):
        """Hilfsmethode für Alpha-Beta-Pruning (alpha_beta). Berechnet die Punktezahl für einen Spielstand (State).
           Falls Spielstand kein finaler Spielstand ist, geht ausschließlich die Heuristik in Ausgabe (result) ein
           Falls Spielstand finaler Spielstand, gehen Heuristik und Punktzahl für Gewinn in die Ausgabe (result) ein"""
        result = 0
        win = state.control_win()
        ## reward patterns
        result += state.get_heuristic()
        if win and player == -1:  ###  Nachdem Spieler 1 den Gewinner-State erreicht hat, wäre Spieler -1 an der Reihe
            result += 1000
        elif win and player == 1: ###  Nachdem Spieler -1 den Gewinner-State erreicht hat, wäre Spieler 1 an der Reihe
            result -= 1000
        return result

    def alpha_beta(self, state, player, alpha, beta, depth):
        """Implementation des Alpha-Beta-Pruning-Algorithmus (rekursiv).
           Input: Spielstand, Spieler, alpha, beta, und variable Suchtiefe (depth)
           Output: Min-Max-Wert und bester Spielzug"""
        children = self.expand_state(state, player, 0, n)
        if (not children or depth == 0):
            return (self.get_reward(state, player), state)          
        else:
            if player == 1:
                v = -math.inf
                for c in children:
                    if alpha < beta:
                        res = self.alpha_beta(c, self.__change_player(player), alpha, beta, depth-1)
                        if res[0] > v:
                            best_state = c
                        v = max(res[0], v)
                        alpha = max(alpha, v)
                    else:
                        break
            elif player == -1:
                v = math.inf
                for c in children:
                    if alpha < beta:
                        res = self.alpha_beta(c, self.__change_player(player), alpha, beta, depth-1)
                        if res[0] < v:
                            best_state = c
                        v = min(res[0], v)
                        beta = min(beta, v)
                    else:
                        break
        return (v, best_state)
                
    #### Hilfsmethoden ####
    
    def print_board(self, board):
        """Hilfsfunktion um in Console Spielfeld 'leserlich' (human-readable) zu drucken"""
        numb = " "
        for j in range(n):
            numb += str(j+1) + " "
        print(numb)
        arrow = " "
        for j in range(n):
            arrow += sign_arrow + " "
        print(arrow)
        for i in range(m):
            elem = "|"
            for j in range(n):
                elem += self.__output_console(board[i, j]) + "|"
            print(elem)
        numb = " "
        for j in range(n):
            numb += str(j+1) + " "
        print(numb)
        
    def __output_console(self, elem):
        """Hilfsfunktion um Spielsteine als farbliche "O"s und leere Spielfelder als Leerzeichen darzustellen"""
        if elem == 1:
            return "\033[93mO\033[00m"
        elif elem ==-1:
            return "\033[91mO\033[00m"
        else:
            return " "

    def __change_player(self, player):
        """Wechselt aktuellen Spieler"""
        return player * (-1)

    def __islegalmove(self, move, board):
        """Input: Spielzug (integer) x board (matrix)
           Output: Wenn Spielzug gültig (Spalte nicht voll), dann wird die Reihe zur betreffenden Spalte ausgegeben.
                   Wenn Spielzug ungültig, dann Ausgabe -1."""
        r = m - 1
        while board[r, move]==1 or board[r, move]==-1:
            r -= 1
            if r < 0:
                break
        return r


