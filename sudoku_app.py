import streamlit as st

# --- ここからソルバーのコード ---
def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None

def is_valid(board, num, pos):
    row, col = pos

    for c in range(9):
        if board[row][c] == num and c != col:
            return False

    for r in range(9):
        if board[r][col] == num and r != row:
            return False

    box_x = col // 3
    box_y = row // 3

    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if board[r][c] == num and (r, c) != pos:
                return False

    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False
# --- ここまでソルバーのコード ---

def parse_input(text):
    lines = text.strip().split("\n")
    board = []
    for line in lines:
        row = [int(ch) for ch in line.strip()]
        board.append(row)
    return board

st.title("ナンプレソルバー")

input_text = st.text_area("盤面を入力してください（0は空白）", height=200)

if st.button("Solve", key="solve_button"):
    board = parse_input(input_text)
    solve(board)
    st.write("解答：")
    st.table(board)
