import streamlit as st
import numpy as np

# -------------------------
# 数独ソルバー
# -------------------------
def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def is_valid(board, num, pos):
    r, c = pos
    if num in board[r]:
        return False
    if num in board[:, c]:
        return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    if num in board[br:br+3, bc:bc+3]:
        return False
    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    r, c = empty
    for num in range(1, 10):
        if is_valid(board, num, (r, c)):
            board[r][c] = num
            if solve_sudoku(board):
                return True
            board[r][c] = 0
    return False


# -------------------------
# 入力UI（テキスト方式）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（0 は空欄）")

    default_text = "\n".join([
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
        "||000|000|000||000|000|000||000|000|000||",
    ])

    text = st.text_area("盤面を編集してください", default_text, height=300)

    # 9×9 の board に変換
    board = np.zeros((9, 9), dtype=int)

    lines = text.strip().split("\n")
    if len(lines) != 9:
        st.error("行数が9行ではありません")
        return board

    for r in range(9):
        line = lines[r].replace("|", "")
        if len(line) != 27:
            st.error(f"{r+1} 行目の文字数が正しくありません")
            return board

        for c in range(9):
            v = line[c*3:(c*3)+3]  # 例: "000" or "005"
            try:
                num = int(v)
                if 1 <= num <= 9:
                    board[r][c] = num
                else:
                    board[r][c] = 0
            except:
                board[r][c] = 0

    return board


# -------------------------
# 解答表示
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    out = ""
    for r in range(9):
        out += "||"
        for c in range(9):
            out += f"{board[r][c]:03d}|"
            if c % 3 == 2:
                out += "|"
        out += "|\n"

    st.text(out)


# -------------------------
# メイン
# -------------------------
def main():
    st.title("🧩 ろっくとっぷ のナンプレSolver")

    board = input_board()

    if st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            show_solution(board_copy)
        else:
            st.error("解けませんでした。")

if __name__ == "__main__":
    main()
