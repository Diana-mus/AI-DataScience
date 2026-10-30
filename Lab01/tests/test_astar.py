# Hier ist die function um die matrix auszugeben
def print_puzzle(state):

    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                print('_', end=' ')
            else:
                print(state[i][j], end=' ')
        print()


#  Function die den leeren platz findet
def finde_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
               return i,j



#  Function die schaut welche bewegungen moeglich sind
def finde_nachbarn(state):
    row, col = finde_blank(state)
    nachbarn = []

    if row >0 :
        nachbarn.append((row-1,col))
    if row <2:
        nachbarn.append((row+1,col))
    if col >0:
        nachbarn.append((row, col - 1))
    if col < 2:
        nachbarn.append((row, col + 1))
    return nachbarn


# Funktion, die alle neuen Zustände erzeugt
def erzeuge_neue_zustaende(state):
    blank_row, blank_col = finde_blank(state)
    neue_zustaende = []

    for n_row, n_col in finde_nachbarn(state):
        kopie = [list(row) for row in state]
        kopie[blank_row][blank_col], kopie[n_row][n_col] = kopie[n_row][n_col], kopie[blank_row][blank_col]
        neue_zustaende.append(kopie)

    return neue_zustaende



# Funktion, die zaelt wie viele plaetchen falsch sind also heuristik

def hamming (state, goal):
    anzahl = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                anzahl += 1
    return anzahl

# fidnde die postion der zahl
def finde_position(state, zahl):
    for i in range(3):
        for j in range(3):
            if state[i][j] == zahl:
               return  i, j


# Manhattan-Heuristik Summe der Abstände aller Plättchen zu ihrem Zielplatz
def manhattan(state, goal):
    summe = 0
    for i in range(3):
        for j in range(3):
            zahl = state[i][j]
            if zahl != 0:
                ziel_row, ziel_col = finde_position(goal, zahl)
                abstand = abs(i - ziel_row) + abs(j - ziel_col)
                summe += abstand
    return summe

class Knoten:
     def __init__ (self,state,g,h,eltern=None):
         self.state = state #  das Puzzle
         self.g= g #  Anyahl Zug vom Start bis zum Ende
         self.h=h # Schatzung bis zum Ziel
         self.f=g+h # die formel g+h
         self.eltern=eltern #  Knoten die enstehen

def zu_tupel(state):
    ergebnis = []
    for row in state:
        ergebnis.append(tuple(row))
    return tuple(ergebnis)

def finde_weg (knoten):
    weg = []
    while knoten is not None:
        weg.append(knoten.state)
        knoten = knoten.eltern
    weg.reverse()
    return weg

def a_stern(start, goal, heuristik):
    start_knoten = Knoten(start, 0, heuristik(start, goal))
    open_list = [start_knoten]
    closed_list = set()
    erzeugte_knoten = 1

    while open_list:
        kleinste= open_list[0]
        for knoten in open_list :
          if knoten.f < kleinste.f:
              kleinste = knoten
        open_list.remove(kleinste)

        if kleinste.state == goal:
            return finde_weg(kleinste), erzeugte_knoten

        if zu_tupel(kleinste.state) in closed_list:
            continue
        closed_list.add(zu_tupel(kleinste.state))


        for neuer_state in erzeuge_neue_zustaende(kleinste.state):
          if zu_tupel(neuer_state) not in closed_list:
            g = kleinste.g + 1
            h = heuristik(neuer_state, goal)
            open_list.append(Knoten(neuer_state, g, h, kleinste))
            erzeugte_knoten += 1


    return None, erzeugte_knoten

















start_state = [[1, 2, 3],
               [0, 4, 6],
               [7, 5, 8]]

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


Beispiel = [[7, 2, 4],
           [5, 0, 6],
           [8, 3, 1]]
print_puzzle(goal_state)

print("Start:")
print_puzzle(start_state)
print()

print("Leeres Feld:", finde_blank(start_state))
print("Nachbarn:", finde_nachbarn(start_state))
print()

print("Neue Zustände:")
for neuer_zustand in erzeuge_neue_zustaende(start_state):
    print_puzzle(neuer_zustand)
    print()

print("Hamming Start:", hamming(start_state, goal_state))
print("Hamming beispiel :", hamming(Beispiel, goal_state))
print("Manhattan Start:", manhattan(start_state, goal_state))
print("Manhattan beispiel:", manhattan(Beispiel, goal_state))

for name, heuristik in [("Hamming", hamming), ("Manhattan", manhattan)]:
    weg, anzahl_knoten = a_stern(start_state, goal_state, heuristik)
    print(name)
    print("Züge:", len(weg) - 1)
    print("Erzeugte Knoten:", anzahl_knoten)
    for state in weg:
        print_puzzle(state)
        print()