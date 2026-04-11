import streamlit as st
import numpy as np

# -------------------------
# 数独ソルバー（バックトラッキング）
# -------------------------
def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def is_valid(board, num, pos):
    r, c = pos

    # 行チェック
    if num in board[r]:
        return False

    # 列チェック
    if num in board[:, c]:
        return False

    # 3×3 ブロックチェック
    br = (r // 3) * 3
    bc = (c // 3) * 3
    if num in board[br:br+3, bc:bc+3]:
        return False

    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True  # 解けた
    r, c = empty

    for num in range(1, 10):
        if is_valid(board, num, (r, c)):
            board[r][c] = num

            if solve_sudoku(board):
                return True

            board[r][c] = 0

    return False


# -------------------------
# 9×9 入力 UI
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄は0）")

    board = np.zeros((9, 9), dtype=int)

    cols = st.columns(9)
    for c in range(9):
        for r in range(9):
            key = f"cell_{r}_{c}"
            value = cols[c].text_input("", value="", max_chars=1, key=key)
            if value.isdigit():
                board[r][c] = int(value)

    return board


# -------------------------
# メイン処理
# -------------------------
def main():
    st.title("🧩 Sudoku Solver（手入力版）")

    board = input_board()

    if st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            st.write("### ✔ 解答:")
            st.write(board_copy)
        else:
            st.error("解けませんでした。")


if __name__ == "__main__":
    main()