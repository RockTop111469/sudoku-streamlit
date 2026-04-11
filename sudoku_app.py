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
# 9×9 入力 UI（罫線つき・色つき・入力チェック）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄は0）")

    board = np.zeros((9, 9), dtype=int)

    # CSS（罫線・色・中央寄せ）
    st.markdown("""
        <style>
        .sudoku-table {
            border-collapse: collapse;
            margin: auto;
        }
        .sudoku-table td {
            border: 1px solid #999;
            width: 45px;
            height: 45px;
            text-align: center;
            background-color: #f8f8f8;
        }
        .sudoku-table td:nth-child(3n) {
            border-right: 3px solid black;
        }
        .sudoku-table tr:nth-child(3n) td {
            border-bottom: 3px solid black;
        }
        .sudoku-table td:first-child {
            border-left: 3px solid black;
        }
        .sudoku-table tr:first-child td {
            border-top: 3px solid black;
        }
        </style>
    """, unsafe_allow_html=True)

    # HTML テーブル生成
    table_html = "<table class='sudoku-table'>"

    for r in range(9):
        table_html += "<tr>"
        for c in range(9):
            key = f"cell_{r}_{c}"
            table_html += f"<td>{st.text_input('', key=key, max_chars=1)}</td>"
        table_html += "</tr>"

    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

    # 入力