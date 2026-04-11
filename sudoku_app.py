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
# 入力UI（セル完全囲み罫線）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄は0）")

    board = np.zeros((9, 9), dtype=int)

    # CSS（セルを完全に囲む）
    st.markdown("""
        <style>
        .cell-wrapper {
            position: relative;
            width: 45px;
            height: 45px;
        }
        .cell-input input {
            position: absolute;
            top: 0;
            left: 0;
            width: 45px !important;
            height: 45px !important;
            text-align: center;
            font-size: 22px;
            padding: 0;
            border: none;
            background: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):

            # 枠線の太さ
            style = ""
            style += "border-top: {} solid black;".format("3px" if r % 3 == 0 else "1px")
            style += "border-left: {} solid black;".format("3px" if c % 3 == 0 else "1px")
            style += "border-bottom: {} solid black;".format("3px" if r == 8 else "1px")
            style += "border-right: {} solid black;".format("3px" if c == 8 else "1px")

            key = f"cell_{r}_{c}"

            with cols[c]:
                # 枠線つきの箱
                st.markdown(
                    f"<div class='cell-wrapper' style='{style}'>",
                    unsafe_allow_html=True
                )

                # 中に text_input を絶対配置（key は1回だけ！）
                v = st.text_input(
                    "",
                    key=key,
                    max_chars=1,
                    label_visibility="collapsed",
                    placeholder=" "
                )

                st.markdown("</div>", unsafe_allow_html=True)

            # 入力チェック
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

    return board


# -------------------------
# 解答表示（同じ罫線で表示）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):

            style = ""
            style += "border-top: {} solid black;".format("3px" if r % 3 == 0 else "1px")
            style += "border-left: {} solid black;".format("3px" if c % 3 == 0 else "1px")
            style += "border-bottom: {} solid black;".format("3px" if r == 8 else "1px")
            style += "border-right: {} solid black;".format("3px" if c == 8 else "1px")

            with cols[c]:
                st.markdown(
                    f"<div style='{style}; text-align:center; font-size:22px; padding-top:8px;'>"
                    f"<b>{board[r][c]}</b></div>",
                    unsafe_allow_html=True
                )


# -------------------------
# メイン
# -------------------------
def main():
    st.title("🧩 Sudoku Solver（セル完全囲み罫線版）")

    board = input_board()

    if st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            show_solution(board_copy)
        else:
            st.error("解けませんでした。")


if __name__ == "__main__":
    main()