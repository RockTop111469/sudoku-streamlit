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
# 入力UI（3×3 ブロック色分け）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    # CSS：text_input の背景色をブロックごとに変える
    st.markdown("""
        <style>
        .sudoku-input input {
            text-align: center;
            font-size: 22px;
            height: 45px;
            width: 45px;
            padding: 0;
        }
        .block-a input {
            background-color: #f0f0f0 !important;  /* 薄いグレー */
        }
        .block-b input {
            background-color: #ffffff !important;  /* 白 */
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):

            # 3×3 ブロックの色を決める
            block_class = "block-a" if ((r//3 + c//3) % 2 == 0) else "block-b"

            key = f"cell_{r}_{c}"

            with cols[c]:
                # text_input をラップして CSS クラスを適用
                st.markdown(f"<div class='sudoku-input {block_class}'>", unsafe_allow_html=True)

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
# 解答表示（同じ色分け）
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
        }
        .block-a {
            background-color: #f0f0f0 !important;
        }
        .block-b {
            background-color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):

            block_class = "block-a" if ((r//3 + c//3) % 2 == 0) else "block-b"

            with cols[c]:
                st.markdown(
                    f"<div class='solution-cell {block_class}'><b>{board[r][c]}</b></div>",
                    unsafe_allow_html=True
                )


# -------------------------
# メイン
# -------------------------
def main():
    st.title("🧩 Sudoku Solver（3×3 色分け版）")

    board = input_board()

    if st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            show_solution(board_copy)
        else:
            st.error("解けませんでした。")


if __name__ == "__main__":
    main()