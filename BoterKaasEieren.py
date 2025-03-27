testcase = [["X", "X", "X",],
            ["O", "O", "x",],
            ["O", "O", "X",]]

testcase1 = [["X", "X", "O",],
            ["X", "O", "x",],
            ["O", "X", "O",]]

def check_winner(board):
    
        # Check row
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
        
        # Check column
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
        
        # Check diagonaal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    
print(testcase)

