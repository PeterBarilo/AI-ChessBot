import chess
from openai import OpenAI

client = OpenAI(api_key="key")

ai_stats = {
    "total_moves": 0,   
    "illegal_moves": 0  
}

def get_ai_move(board, failed_moves=None):
    fen = board.fen()
    base_prompt = f"""
    You are an accurate and strong chess engine. The current board position is given in FEN: {fen}.
    Suggest a legal move in standard UCI format (e.g., e2e4, g8f6). Only provide the move.
    """
    if failed_moves:
        failed_moves_str = ", ".join(failed_moves)
        base_prompt += f"\nDo NOT under any circumstances suggest the following moves as they are illegal: {failed_moves_str}."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a chess engine that suggests ONLY legal moves."},
                {"role": "user", "content": base_prompt}
            ],
            temperature=0,
            max_tokens=10
        )
        move = completion.choices[0].message.content.strip()
        return move
    except Exception as e:
        print(f"Error with OpenAI: {e}")
        return None



def play_chess():
    board = chess.Board()
    print("Starting Game")
    print(board)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("\nYour turn!")
            user_move = input("Enter your move (UCI format, e.g., e2e4): ")
            try:
                board.push_uci(user_move)
            except ValueError:
                print("Invalid move! Try again.")
                continue
        else:
            print("\nAI's turn...")
            failed_moves = []  # Track all illegal moves for this turn
            while True:
                ai_stats["total_moves"] += 1
                ai_move = get_ai_move(board, failed_moves=failed_moves)
                if ai_move and chess.Move.from_uci(ai_move) in board.legal_moves:
                    board.push_uci(ai_move)
                    print(f"AI plays: {ai_move}")
                    break
                else:
                    print(f"AI suggested an illegal move: {ai_move}. Asking for another...")
                    ai_stats["illegal_moves"] += 1
                    if ai_move not in failed_moves:
                        failed_moves.append(ai_move)

        print(board)

    print("\nGame Over!")
    print(f"Result: {board.result()}")

    if ai_stats["total_moves"] > 0:
        accuracy = ((ai_stats["total_moves"] - ai_stats["illegal_moves"]) / ai_stats["total_moves"]) * 100
        print("\nAI Performance Stats:")
        print(f"- Total Moves Suggested: {ai_stats['total_moves']}")
        print(f"- Illegal Moves Suggested: {ai_stats['illegal_moves']}")
        print(f"- Accuracy: {accuracy:.2f}%")
    else:
        print("\nAI did not make any moves.")

if __name__ == "__main__":
    play_chess()
