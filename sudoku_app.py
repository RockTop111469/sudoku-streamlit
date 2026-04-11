import streamlit as st
import numpy as np

def input_board():
    st.write("### 数独の盤面を入力してください（空欄は0）")

    # CSS（完全に囲まれたセル）
    st.markdown("""
        <style>
        .sudoku-grid {
            display: grid;
            grid-template-columns: repeat(9, 45px);
            grid-template-rows: repeat(9, 45px);
            justify-content: center;
            margin-top: 10px;
        }
        .sudoku-cell {
            width: 45px;
            height: 45px;
            text-align: center;
            font-size: 22px;
            border: 1px solid #999;
        }
        /* 3×3 の太線 */
        .cell-r0 { border-top: 3px solid black !important; }
        .cell-r3 { border-top: 3px solid black !important; }
        .cell-r6 { border-top: 3px solid black !important; }
        .cell-c0 { border-left: 3px solid black !important; }
        .cell-c3 { border-left: 3px solid black !important; }
        .cell-c6 { border-left: 3px solid black !important; }
        .cell-r8 { border-bottom: 3px solid black !important; }
        .cell-c8 { border-right: 3px solid black !important; }
        </style>
    """, unsafe_allow_html=True)

    # HTML 生成
    html = "<div class='sudoku-grid'>"
    for r in range(9):
        for c in range(9):
            classes = f"sudoku-cell cell-r{r} cell-c{c}"
            html += f"<input id='cell_{r}_{c}' class='{classes}' maxlength='1'>"
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    # JS で値を session_state に反映
    st.markdown("""
        <script>
        const inputs = document.querySelectorAll('.sudoku-cell');
        inputs.forEach(inp => {
            inp.addEventListener('input', () => {
                const key = inp.id;
                const value = inp.value;
                window.parent.postMessage({key: key, value: value}, '*');
            });
        });
        </script>
    """, unsafe_allow_html=True)

    # Python 側で受け取る
    board = np.zeros((9, 9), dtype=int)
    for r in range(9):
        for c in range(9):
            key = f"cell_{r}_{c}"
            v = st.session_state.get(key, "")
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)

    return board