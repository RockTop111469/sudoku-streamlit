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
    br, bc = (r//3)*3, (c//3)*3
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
# 入力UI（パイプ固定 × 全セル入力 × セル大きめ）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    # ★ あなたが渡してくれた CSS を完全統合 ★
    st.markdown("""
        <style>
        pre {
            font-family: monospace;
            font-size: 26px;   /* ← 行全体の文字サイズアップ */
            line-height: 1.35;
        }

        .cell {
            display: inline-block;
            width: 36px;      /* ← PC で大きく */
            height: 36px;
            position: relative;
        }

        .cell input {
            width: 36px;      /* ← 入力欄も大きく */
            height: 36px;
            font-size: 26px;  /* ← 数字も大きく */
            text-align: center;
            background: transparent;
            border: none;
            outline: none;
        }

        /* スマホ縮小 */
        @media (max-width: 600px) {
            pre {
                font-size: 22px;   /* ← スマホでも見やすく */
            }
            .cell {
                width: 30px;       /* ← スマホ用サイズ */
                height: 30px;
            }
            .cell input {
                width: 30px;
                height: 30px;
                font-size: 22px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.write("<pre>", unsafe_allow_html=True)

    # ★ パイプ固定レイアウトに input を直接埋め込む ★
    for r in range(9):
        row_html = "||"
        for c in range(9):
            key = f"cell_{r}_{c}"
            row_html += f"<span class='cell'><input name='{key}'></span>|"
            if c % 3 == 2:
                row_html += "|"
        row_html += "|"
        st.write(row_html, unsafe_allow_html=True)

    st.write("</pre>", unsafe_allow_html=True)

    # ★ 入力値を Python 側に反映
    for r in range(9):
        for c in range(9):
            key = f"cell_{r}_{c}"
            v = st.session_state.get(key, "")
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)

    return board


# -------------------------
# 解答表示（パイプ固定 × セル大きめ）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    st.markdown("""
        <style>
        pre {
            font-family: monospace;
            font-size: 26px;
            line-height: 1.35;
        }
        .cell {
            display: inline-block;
            width: 36px;
            height: 36px;
            font-size: 26px;
            text-align: center;
        }
        @media (max-width: 600px) {
            pre {
                font-size: 22px;
            }
            .cell {
                width: 30px;
                height: 30px;
                font-size: 22px;
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
