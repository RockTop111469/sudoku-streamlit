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
# 入力UI（パイプ固定 × 数字だけ入力）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（0 は空欄）")

    board = np.zeros((9, 9), dtype=int)

    for r in range(9):
        row_html = "|| "
        inputs = []

        for c in range(9):
            key = f"cell_{r}_{c}"
            v = st.text_input(
                key=key,
                label="",
                max_chars=1,
                placeholder="0",
                label_visibility="collapsed"
            )
            inputs.append(v)

            row_html += f"[{key}] | "
            if c % 3 == 2:
                row_html += "| "

        # パイプ行を表示
        st.markdown(
            row_html.replace("[", "<span style='display:inline-block;width:0px;'>")
                    .replace("]", "</span>"),
            unsafe_allow_html=True
        )

        # 数値を board に反映
        for c in range(9):
            v = inputs[c]
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

    return board


# -------------------------
# 解答表示
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答:")

    out = ""
    for r in range(9):
        out += "|| "
        for c in range(9):
            out += f"{board[r][c]} | "
            if c % 3 == 2:
                out += "| "
        out += "\n"

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
