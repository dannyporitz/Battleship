#Constants
SHIPS = [("Carrier", "A", 5),
         ("Battleship", "B", 4),
         ("Crusier", "C", 3),
         ("Submarine", "S", 3),
         ("Destroyer", "D", 2)]       

EMPTY = "O"
MISS = "X"
HIT = "!"

row_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
col_names = ["1", "2", "3", "4", "5", "6", "7", "8"]

ship_board1 = []
ship_board2 = []
target_board1 = []
target_board2 = []
boards = [ship_board1, ship_board2, target_board1, target_board2]
player1 = [ship_board1, target_board1, "Player 1"]
player2 = [ship_board2, target_board2, "Player 2"]
players = [player1, player2]

def make_board(board):
    for row in range(0, 8):
        board.append([])
        for column in range(0, 8):
            board[row].append(EMPTY)
        
def print_board(board):   
    print ("  |" , " | ".join(col_names))
    for row in range (0, 8):
        print("----------------------------------")
        print(row_names[row], "|", " | ".join(board[row]))

def place_ships(board):
    print("Place ships by entering start and end points")
    for ship in SHIPS:
        start = ""
        end = ""
        valid_placement = False
        while not valid_placement:
            start = input("\nSelect a start point for your " + ship[0] + " (" + str(ship[2]) + " spaces): ").upper()
            end = input("Select an end point: ").upper()
            if not (is_valid_coordinate(start) and is_valid_coordinate(end)):
                print("Error: Invalid coordinates")
            elif not is_line(start, end):
                print("Error: Ship must be placed in a line")
            elif not is_valid_length(start, end, ship[2]):
                print("Error: Does not match ship length")
            elif not is_empty(start, end, board):
                print("Error: Already a ship there")
            else:
                print("You placed your ship in", start, end)
                valid_placement = True
        change_line(start, end, ship[1], board)
    print("\n" * 50)
        
def is_valid_coordinate(coordinate):
    return len(coordinate) == 2 and coordinate[0] in row_names and coordinate[1] in col_names

def is_line(coordinate1, coordinate2):
    return coordinate1[0] == coordinate2[0] or coordinate1[1] == coordinate2[1]

def is_valid_length(coordinate1, coordinate2, length):
    horizontal_length = abs(int(coordinate1[1]) - int(coordinate2[1])) + 1
    vertical_length = abs(row_names.index(coordinate1[0]) - row_names.index(coordinate2[0])) + 1
    return horizontal_length == length or vertical_length == length

def is_empty(coordinate1, coordinate2, board):
    return set(get_line(coordinate1, coordinate2, board)) == {EMPTY}

#Converts a coordinate to its corresponding row and column
def convert_coordinate(coordinate):
    row = row_names.index(coordinate[0])
    col = col_names.index(coordinate[1])
    return row, col

#Converts a row and column to its corresponding coordinate
def convert_rowcol(row, col):
    return row_names[row] + col_names[col]

def get_space(coordinate, board):
    row = row_names.index(coordinate[0])
    col = col_names.index(coordinate[1])
    return board[row][col]

def get_line(coordinate1, coordinate2, board):
    spaces = []
    row1, col1 = convert_coordinate(coordinate1)
    row2, col2 = convert_coordinate(coordinate2)  
    if row1 == row2:
        for col in range(min(col1, col2), max(col1, col2) + 1):
            spaces.append(board[row1][col])
    elif col1 == col2:
        for row in range(min(row1, row2), max(row1, row2) + 1):
            spaces.append(board[row][col1])
    return spaces

def get_line_coordinates(coordinate1, coordinate2):
    coordinates = []
    row1, col1 = convert_coordinate(coordinate1)
    row2, col2 = convert_coordinate(coordinate2)
    if row1 == row2:
        for col in range(min(col1, col2), max(col1, col2) + 1):
            coordinates.append(convert_rowcol(row1, col))
    elif col1 == col2:
        for row in range(min(row1, row2), max(row1, row2) + 1):
            coordinates.append(convert_rowcol(row, col1))
    return coordinates

def change_space(coordinate, change, board):
    row, col = convert_coordinate(coordinate)
    board[row][col] = change

def change_line(coordinate1, coordinate2, change, board):
    coordinates = get_line_coordinates(coordinate1, coordinate2)
    for coordinate in coordinates:
        change_space(coordinate, change, board)

def guess(guesser, target_player):
    guess = ""
    valid_guess = False
    while not valid_guess:
        guess = input("Where will you aim? ").upper()
        if not is_valid_coordinate(guess):
            print("Error: Invalid coordinates")
        elif get_space(guess, guesser[1]) != EMPTY:
            print("You've already guessed there!")
        else:
            valid_guess = True
    result = get_space(guess, target_player[0])
    if result == EMPTY:
        print("MISS!")
        change_space(guess, MISS, guesser[1])
    else:
        print("HIT!")
        change_space(guess, HIT, guesser[1])
        change_space(guess, EMPTY, target_player[0])
        if ship_destroyed(result, target_player[0]):
            print("You have sunk your opponent's", get_ship(result) + "!")
    print()
    print_board(guesser[1])

def ship_destroyed(ship_marker, board):
    for row in range(0, 8): #row in board
        if ship_marker in board[row]:
            return False
    return True

def get_ship(ship_marker):
    for ship in SHIPS:
        if ship_marker == ship[1]:
            return ship[0]
    return None
    
def main():
    #First, set up the boards
    for brd in boards:
        make_board(brd)
    print("""
Welcome to Battleship! Each player tries to sink his opponent's ships
by guessing coordinates. The player who sinks all of the other's ships
first wins!
    """)
    #Let players place ships
    for player in players:
        print(player[2] + ", place your ships!")
        place_ships(player[0])
    #Now players alternate turns guessing
    print("\nNow let's start the game!")
    winner = None
    turn = player1
    target = player2
    while not winner:
        print(turn[2] + ", it's your turn!")
        guess(turn, target)
        #Check to see if a player has won
        if set([ship_destroyed(ship[1], target[0]) for ship in SHIPS]) == {True}:
            winner = turn
        else:
            turn, target = target, turn
        print()
    print(winner[2] + " has won!")
               

#And all that's left!
main()

