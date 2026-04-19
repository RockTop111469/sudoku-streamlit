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
# 入力UI（パイプ固定・全セル入力）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    st.markdown("""
        <style>
        pre {
            font-family: monospace;
            font-size: 20px;
            line-height: 1.2;
        }
        .cell-input {
            width: 28px;
            height: 28px;
            font-size: 20px;
            text-align: center;
        }

        /* スマホ縮小 */
        @media (max-width: 600px) {
            .cell-input {
                transform: scale(0.8);
                transform-origin: top left;
            }
            pre {
                font-size: 16px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.write("<pre>", unsafe_allow_html=True)

    for r in range(9):
        row_html = "||"
        for c in range(9):
            key = f"cell_{r}_{c}"
            inp = st.text_input("", key=key, max_chars=1, label_visibility="collapsed")
            if inp.isdigit() and 1 <= int(inp) <= 9:
                board[r][c] = int(inp)
            row_html += f"<input class='cell-input' id='{key}' />|"
            if c % 3 == 2:
                row_html += "|"
        row_html += "|"
        st.write(row_html, unsafe_allow_html=True)

    st.write("</pre>", unsafe_allow_html=True)

    return board


# -------------------------
# 解答表示（パイプ固定）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    st.markdown("""
        <style>
        pre {
            font-family: monospace;
            font-size: 20px;
            line-height: 1.2;
        }
        .cell {
            display: inline-block;
            width: 28px;
            height: 28px;
            font-size: 20px;
            text-align: center;
            border: 1px solid #ccc;
            background: #f8f8f8;
        }
        @media (max-width: 600px) {
            .cell {
                transform: scale(0.8);
                transform-origin: top left;
            }
            pre {
                font-size: 16px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.write("<pre>", unsafe_allow_html=True)

    for r in range(9):
        row_html = "||"
        for c in range(9):
            row_html += f"<div class='cell'>{board[r][c]}</div>|"
            if c % 3 == 2:
                row_html += "|"
        row_html += "|"
        st.write(row_html, unsafe_allow_html=True)

    st.write("</pre>", unsafe_allow_html=True)


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
