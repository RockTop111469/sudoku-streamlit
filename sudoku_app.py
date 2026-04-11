def input_board():
    st.write("### 数独の盤面を入力してください（空欄は0）")

    board = np.zeros((9, 9), dtype=int)

    # CSS（セルを完全に囲む）
    st.markdown("""
        <style>
        .cell-wrapper {
            position: relative;
            width: 45px;
            height: 45px;
        }
        .cell-input input {
            position: absolute;
            top: 0;
            left: 0;
            width: 45px !important;
            height: 45px !important;
            text-align: center;
            font-size: 22px;
            padding: 0;
            border: none;
            background: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):
        cols = st.columns(9, gap="small")
        for c in range(9):

            # 枠線の太さ
            style = ""
            style += "border-top: {} solid black;".format("3px" if r % 3 == 0 else "1px")
            style += "border-left: {} solid black;".format("3px" if c % 3 == 0 else "1px")
            style += "border-bottom: {} solid black;".format("3px" if r == 8 else "1px")
            style += "border-right: {} solid black;".format("3px" if c == 8 else "1px")

            key = f"cell_{r}_{c}"

            with cols[c]:
                # 枠線つきの箱
                st.markdown(
                    f"<div class='cell-wrapper' style='{style}'>",
                    unsafe_allow_html=True
                )

                # 中に text_input を絶対配置
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