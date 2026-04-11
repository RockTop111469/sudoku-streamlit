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
# 入力UI（3×3 ブロック間スペース版）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    # text_input の見た目だけ整える
    st.markdown("""
        <style>
        .sudoku-input input {
            text-align: center;
            font-size: 22px;
            height: 45px;
            width: 45px;
            padding: 0;
        }
        .space-cell {
            height: 45px;
            width: 20px;   /* ブロック間のスペース */
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):

        # 9セル + 2スペース = 11列
        cols = st.columns([1,1,1,0.3,1,1,1,0.3,1,1,1])

        col_index = 0

        for c in range(9):

            # 3×3 ブロックの後にスペースを入れる
            if c in [3, 6]:
                with cols[col_index]:
                    st.markdown("<div class='space-cell'></div>", unsafe_allow_html=True)
                col_index += 1

            key = f"cell_{r}_{c}"

            with cols[col_index]:
                v = st.text_input(
                    "",
                    key=key,
                    max_chars=1,
                    label_visibility="collapsed",
                    placeholder=" "
                )
            col_index += 1

            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

        # 3×3 ブロックの縦スペース
        if r in [2, 5]:
            st.write("")  # 空行でスペースを作る

    return board


# -------------------------
# 解答表示（3×3 ブロック間スペース版）
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
        .space-cell {
            height: 45px;
            width: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):

        cols = st.columns([1,1,1,0.3,1,1,1,0.3,1,1,1])
        col_index = 0

        for c in range(9):

            if c in [3, 6]:
                with cols[col_index]:
                    st.markdown("<div class='space-cell'></div>", unsafe_allow_html=True)
                col_index += 1

            with cols[col_index]:
                st.markdown(
                    f"<div class='solution-cell'><b>{board[r][c]}</b></div>",
                    unsafe_allow_html=True
                )
            col_index += 1

        if r in [2, 5]:
            st.write("")

# -------------------------
# メイン
# -------------------------
def main():
    st.title("🧩 Sudoku Solver（3×3 ブロック間スペース版）")

    board = input_board()

    if st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            show_solution(board_copy)
        else:
            st.error("解けませんでした。")

if __name__ == "__main__":
    main()