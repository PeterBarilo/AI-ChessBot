import chess
from openai import OpenAI

client = OpenAI(api_key="key")

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
            print("\nYour turn")
            user_move = input("Enter your move (UCI format, e.g., for e2 to e4 enter e2e4): ")
            try:
                board.push_uci(user_move)
            except ValueError:
                print("Invalid move!")
                continue
        else:
            print("\nAI's turn...")
            failed_moves = []  
            while True:
                ai_move = get_ai_move(board, failed_moves=failed_moves)
                if ai_move and chess.Move.from_uci(ai_move) in board.legal_moves:
                    board.push_uci(ai_move)
                    print(f"AI plays: {ai_move}")
                    break
                else:
                    print("AI is considering its options...")
                    if ai_move not in failed_moves:
                        failed_moves.append(ai_move)

        print(board)

    print("\nGame Over!")
    print("Result:", board.result())

if __name__ == "__main__":
    play_chess()
