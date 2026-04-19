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
# 入力UI（パイプ風レイアウト＋text_input）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄または0は空欄扱い）")

    board = np.zeros((9, 9), dtype=int)

    st.markdown("""
        <style>
        .s-cell input {
            text-align: center;
            font-size: 24px;
            height: 40px;
            width: 40px;
            padding: 0;
        }
        @media (max-width: 600px) {
            .s-cell input {
                font-size: 20px;
                height: 34px;
                width: 34px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns([0.4,1,0.2,1,0.2,1,0.4,1,0.2,1,0.2,1,0.4])

        col_idx = 0
        cols[col_idx].markdown("**||**"); col_idx += 1

        for c in range(9):
            with cols[col_idx]:
                v = st.text_input(
                    "",
                    key=f"cell_{r}_{c}",
                    max_chars=1,
                    label_visibility="collapsed",
                    placeholder="",
                )
            col_idx += 1

            # 区切りパイプ
            cols[col_idx].markdown("**|**")
            col_idx += 1

            # 3マスごとに太い区切り
            if c % 3 == 2:
                cols[col_idx].markdown("**|**")
                col_idx += 1

            # 値を board に反映
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

    return board


# -------------------------
# 解答表示（パイプ付きで表示）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    out = ""
    for r in range(9):
        out += "||"
        for c in range(9):
            out += f"{board[r][c]}|"
            if c % 3 == 2:
                out += "|"
        out += "|\n"

    st.text(out)


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
