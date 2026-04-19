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
# 入力UI（透明入力欄 × パイプ固定）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    st.markdown("""
        <style>
        pre {
            font-family: monospace;
            font-size: 22px;
            line-height: 1.3;
        }

        .cell-wrap {
            display: inline-block;
            position: relative;
            width: 24px;
            height: 24px;
        }

        .cell-input {
            position: absolute;
            top: 0;
            left: 0;
            width: 24px;
            height: 24px;
            font-size: 20px;
            text-align: center;
            background: transparent;
            border: none;
            outline: none;
        }

        /* スマホ縮小 */
        @media (max-width: 600px) {
            pre {
                font-size: 18px;
            }
            .cell-wrap {
                width: 20px;
                height: 20px;
            }
            .cell-input {
                width: 20px;
                height: 20px;
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
            row_html += f"<span class='cell-wrap'>___<input class='cell-input' name='{key}'></span>|"
            if c % 3 == 2:
                row_html += "|"
        row_html += "|"
        st.write(row_html, unsafe_allow_html=True)

    st.write("</pre>", unsafe_allow_html=True)

    # Streamlit 側で値を取得
    for r in range(9):
        for c in range(9):
            key = f"cell_{r}_{c}"
            v = st.session_state.get(key, "")
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)

    return board


# -------------------------
# 解答表示（透明セルなし）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    st.markdown("""
        <style>
        pre {
            font-family: monospace;
            font-size: 22px;
            line-height: 1.3;
        }
        .cell {
            display: inline-block;
            width: 24px;
            height: 24px;
            font-size: 20px;
            text-align: center;
        }
        @media (max-width: 600px) {
            pre {
                font-size: 18px;
            }
            .cell {
                width: 20px;
                height: 20px;
                font-size: 16px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.write("<pre>", unsafe_allow_html=True)

    for r in range(9):
        row_html = "||"
        for c in range(9):
            row_html += f"<span class='cell'>{board[r][c]}</span>|"
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
