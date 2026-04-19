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
# 入力UI（パイプ固定・数字だけ編集可能）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（0 は空欄）")

    board = np.zeros((9, 9), dtype=int)

    for r in range(9):
        cols = st.columns([0.3,1,1,1,0.3,1,1,1,0.3,1,1,1,0.3])

        col = 0
        cols[col].write("||"); col += 1

        for c in range(9):
            key = f"cell_{r}_{c}"
            v = cols[col].text_input("", key=key, max_chars=1, label_visibility="collapsed")
            col += 1

            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

            cols[col].write("|")
            col += 1

            if c % 3 == 2:
                cols[col].write("|")
                col += 1

        cols[col-1].write("|")

    return board


# -------------------------
# 解答表示
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    for r in range(9):
        cols = st.columns([0.3,1,1,1,0.3,1,1,1,0.3,1,1,1,0.3])

        col = 0
        cols[col].write("||"); col += 1

        for c in range(9):
            cols[col].write(f"**{board[r][c]}**")
            col += 1

            cols[col].write("|")
            col += 1

            if c % 3 == 2:
                cols[col].write("|")
                col += 1

        cols[col-1].write("|")


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
