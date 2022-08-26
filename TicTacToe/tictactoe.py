import random

class Game:
    def __init__(self):
        self.board = []
    
    # Create / Reset main game board
    def initite_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('*')
            self.board.append(row)
    
    # Define Function to pick starting player at random - player either 0 or 1
    def rand_first_player(self):
        return random.randint(0, 1)
    
    # Define function enabling player to choose placement on board
    def take_spot(self, player, row, col):
        # Check if spot is already occupied
        if self.board[row][col] != '*':
            row, col = list(map(int, input("Please enter row and column numbers that has not already been taken: ").split()))
            print() 
            self.take_spot(player, row - 1, col - 1)
        # Otherwise take spot
        else:
            self.board[row][col] = player
    
    # Define function checking if any game winning conditions are met
    def player_win(self, player):
        win = None

        board_size = len(self.board)

        # Check straight rows where i is row and j is col
        for i in range(board_size):
            win = True
            for j in range(board_size): 
                if self.board[i][j] != player:
                    win = False
                    break
            if win: 
                return win

        # Check straight columns where i is row and j is col
        for i in range(board_size):
            win = True
            for j in range(board_size): 
                if self.board[j][i] != player:
                    win = False
                    break
            if win: 
                return win

        # Check diagonals
        win = True
        for i in range(board_size):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win
        
        win = True
        for i in range(board_size):
            if self.board[i][board_size - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

    # Define function that checks if board is full
    def is_board_full(self):
        for row in self.board:
            for item in row:
                if item == "*":
                    return False
        return True

    # Define function to enable player turns
    def swap_player(self, player):
        return 'X' if player == "O" else "O"

    # Define function that updates board each turn
    def update_board(self):
        for row in self.board:
            for item in row: 
                print(item, end=" ")
            print()
    
    # Define game mainloop
    def start(self):
        self.initite_board()

        # Find which player starts
        player = 'X' if self.rand_first_player() == 1 else 'O'

        while True:
            print(f"Player {player} turn")

            self.update_board()

            # Take user input and secure players target spot - subtract one to comply with 0
            row, col = list(map(int, input("Please enter row and column numbers to pick spot: ").split()))
            print()

            self.take_spot(player, row - 1, col - 1)

            # Utilize logic to determine if player won
            if self.player_win(player):
                print(f"Congratulations! Player {player} has won the game.")
                break

            # Check if play ends match in draw
            if self.is_board_full():
                print("Oh no! Matcth draw.")
                break

            # If game wasn't won or draw continue by swapping players
            player = self.swap_player(player)

        # Update board again
        print()
        self.update_board()

#start game

Game().start()
