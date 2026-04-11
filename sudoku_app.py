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
    if num in board[r]: return False
    if num in board[:, c]: return False
    br, bc = (r//3)*3, (c//3)*3
    if num in board[br:br+3, bc:bc+3]: return False
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
# 入力UI（罫線なし・グレーセルのみ）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    st.markdown("""
        <style>
        .sudoku-input input {
            text-align: center;
            font-size: 22px;
            height: 45px;
            width: 45px;
            padding: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):
            key = f"cell_{r}_{c}"

            v = cols[c].text_input(
                "",
                key=key,
                max_chars=1,
                label_visibility="collapsed",
                placeholder=" "
            )

            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

    return board


# -------------------------
# 解答表示（グレーセル）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    st.markdown("""
        <style>
        .solution-cell {
            text-align: center;
            font-size: 22px;
            height: 45px;
            width: 45px;
            padding-top: 8px;
            border: 1px solid #ccc;
            background-color: #f8f8f8;
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):
            with cols[c]:
                st.markdown(
                    f"<div class='solution-cell'><b>{board[r][c]}</b></div>",
                    unsafe_allow_html=True
                )


# -------------------------
# メイン
# -------------------------
def main():
    st.title("🧩 Sudoku Solver（グレーセル版）")

    board = input_board()

    if st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            show_solution(board_copy)
        else:
            st.error("解けませんでした。")


if __name__ == "__main__":
    main()