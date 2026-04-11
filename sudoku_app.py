def input_board():
    st.write("### 数独の盤面を入力してください（空欄は0）")

    board = np.zeros((9, 9), dtype=int)

    # CSS（罫線・色・中央寄せ）
    st.markdown("""
        <style>
        .sudoku-input input {
            text-align: center;
            font-size: 22px;
            height: 45px;
            width: 45px;
            padding: 0;
        }
        .cell-box {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 45px;
            width: 45px;
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):
            key = f"cell_{r}_{c}"

            # 枠線の太さを決める
            style = ""

            # 横線
            if r % 3 == 0:
                style += "border-top: 3px solid black;"
            else:
                style += "border-top: 1px solid #999;"

            # 縦線
            if c % 3 == 0:
                style += "border-left: 3px solid black;"
            else:
                style += "border-left: 1px solid #999;"

            # 最終行・列の太線
            if r == 8:
                style += "border-bottom: 3px solid black;"
            if c == 8:
                style += "border-right: 3px solid black;"

            with cols[c]:
                st.markdown(
                    f"<div class='cell-box' style='{style}'>",
                    unsafe_allow_html=True
                )
                v = st.text_input(
                    "",
                    key=key,
                    max_chars=1,
                    label_visibility="collapsed",
                    placeholder=" ",
                    help="1〜9の数字を入力",
                    key=f"cell_{r}_{c}"
                )
                st.markdown("</div>", unsafe_allow_html=True)

            # 入力チェック
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

    return board