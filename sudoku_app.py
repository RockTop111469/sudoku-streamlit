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
# 入力UI（9行×9桁テキスト）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください")
    st.write("- 9行×9桁で入力してください")
    st.write("- `0` は空欄として扱います")
    st.write("- 数字は `1〜9` のみ有効です")

    st.markdown("**＜入力例＞**")
    example = "\n".join([
        "000000046",
        "000000000",
        "001230000",
        "002007000",
        "003000500",
        "000405090",
        "000010300",
        "400006000",
        "900000000",
    ])
    st.code(example, language="text")

    default_text = "\n".join([
        "000000000",
        "000000000",
        "000000000",
        "000000000",
        "000000000",
        "000000000",
        "000000000",
        "000000000",
        "000000000",
    ])

    text = st.text_area("盤面（9行×9桁）", default_text, height=220)

    lines = [line.strip() for line in text.strip().split("\n") if line.strip() != ""]
    board = np.zeros((9, 9), dtype=int)

    if len(lines) != 9:
        st.error("行数が9行ではありません。9行で入力してください。")
        return None

    for r in range(9):
        line = lines[r]
        if len(line) != 9:
            st.error(f"{r+1}行目の桁数が9ではありません。9桁で入力してください。")
            return None
        for c in range(9):
            ch = line[c]
            if ch.isdigit() and ch != "0":
                board[r][c] = int(ch)
            else:
                board[r][c] = 0

    return board


# -------------------------
# 解答表示（9行×9桁で出力）
# -------------------------
def show_solution(board):
    st.write("### ✔ 解答（9行×9桁）")

    lines = []
    for r in range(9):
        line = "".join(str(board[r][c]) for c in range(9))
        lines.append(line)

    st.code("\n".join(lines), language="text")


# -------------------------
# メイン
# -------------------------
def main():
    st.title("🧩 ろっくとっぷ のナンプレ Solver")

    board = input_board()

    if board is not None and st.button("Solve"):
        board_copy = board.copy()
        if solve_sudoku(board_copy):
            show_solution(board_copy)
        else:
            st.error("解けませんでした。入力に矛盾がある可能性があります。")

if __name__ == "__main__":
    main()
