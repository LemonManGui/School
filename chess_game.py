import chess
import chess.engine

def main():
    
    board = chess.Board()
    
    engine_path = "/Applications/Stockfish.app/Contents/MacOS/Stockfish"
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    
    print("Welcome to Python chess!")
    print(board)

    while not board.is_game_over():
        # Players turn
        move = input("Enter your move (e2e4): ")
    
        try:
            board.push_san(move)
        except ValueError:
            print("Invalid move. Try again.")
            continue
        
        print("\nAfter your move:")
        print(board)
        
        # AI's turn
        if not board.is_game_over():
            result = engine.play(board, chess.engine.Limit(time=2.0))
            board.push(result.move)
        
    engine.quit()
    
    if board.is_chechmate():
        print("Checkmate!")
    if board.is_stalmate():
        print("Stalmate!")
    if board.is_insufficiant_material():
        print("Draw due to insufficiant material.")
    else:
        print("Game over.")
        
if __name__ == "__main__":
    main()