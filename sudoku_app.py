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
# 入力UI（HTML input → JS → Streamlit）
# -------------------------
def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    # ★ CSS（あなたの指定どおり）
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
            position: relative;
        }
        .cell input {
            width: 36px;
            height: 36px;
            font-size: 26px;
            text-align: center;
            background: transparent;
            border: none;
            outline: none;
        }
        @media (max-width: 600px) {
            pre {
                font-size: 22px;
            }
            .cell {
                width: 30px;
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

    # ★ HTML（パイプ固定）
    html = "<pre>"
    for r in range(9):
        html += "||"
        for c in range(9):
            key = f"cell_{r}_{c}"
            html += f"<span class='cell'><input id='{key}' maxlength='1'></span>|"
            if c % 3 == 2:
                html += "|"
        html += "|\n"
    html += "</pre>"

    st.markdown(html, unsafe_allow_html=True)

    # ★ JavaScript → Streamlit に値を送る
    st.markdown("""
        <script>
        const sendValues = () => {
            let data = {};
            for (let r = 0; r < 9; r++) {
                for (let c = 0; c < 9; c++) {
                    let key = `cell_${r}_${c}`;
                    let v = document.getElementById(key).value;
                    data[key] = v;
                }
            }
            window.parent.postMessage({type: "streamlit:setComponentValue", value: data}, "*");
        };

        document.addEventListener("input", sendValues);
        </script>
    """, unsafe_allow_html=True)

    # ★ Streamlit 側で JS からの値を受け取る
    values = st.experimental_get_query_params()

    # ★ board に反映
    for r in range(9):
        for c in range(9):
            key = f"cell_{r}_{c}"
            v = values.get(key, [""])[0]
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)

    return board


# -------------------------
# 解答表示
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

    html = "<pre>"
    for r in range(9):
        html += "||"
        for c in range(9):
            html += f"<span class='cell'>{board[r][c]}</span>|"
            if c % 3 == 2:
                html += "|"
        html += "|\n"
    html += "</pre>"

    st.markdown(html, unsafe_allow_html=True)


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
