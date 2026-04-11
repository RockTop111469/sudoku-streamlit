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
# 入力UI（columns＋CSSで罫線）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄は0）")

    board = np.zeros((9, 9), dtype=int)

    # CSS（罫線・色）
    st.markdown("""
        <style>
        .cell {
            text-align: center;
        }
        .sudoku-col {
            padding: 0 !important;
        }
        .sudoku-input > div > input {
            text-align: center;
            font-size: 20px;
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

            # 枠線の太さを決める
            style = ""
            if r % 3 == 0:
                style += "border-top: 3px solid black;"
            else:
                style += "border-top: 1px solid #999;"

            if c % 3 == 0:
                style += "border-left: 3px solid black;"
            else:
                style += "border-left: 1px solid #999;"

            if r == 8:
                style += "border-bottom: 3px solid black;"
            if c == 8:
                style += "border-right: 3px solid black;"

            with cols[c]:
                st.markdown(
                    f"<div style='{style}' class='sudoku-col'>",
                    unsafe_allow_html=True
                )
                v = st.text_input(
                    "",
                    key=key,
                    max_chars=1,
                    label_visibility="collapsed",
                    placeholder=" ",
                    help="1〜9の数字を入力"
                )
                st.markdown("</div>", unsafe_allow_html=True)

            # 入力チェック
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

    return board


# -------------------------
# 解答表示（同じ枠線で表示）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):
            style = ""
            if r % 3 == 0:
                style += "border-top: 3px solid black;"
            else:
                style += "border-top: 1px solid #999;"

            if c % 3 == 0:
                style += "border-left: 3px solid black;"
            else:
                style += "border-left: 1px solid #999;"

            if r == 8:
                style += "border-bottom: 3px solid black;"
            if c == 8:
                style += "border-right: 3px solid black;"

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
    st.title("🧩 Sudoku Solver（UI強化版）")

    board = input_board()

    if st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            show_solution(board_copy)
        else:
            st.error("解けませんでした。")


if __name__ == "__main__":
    main()