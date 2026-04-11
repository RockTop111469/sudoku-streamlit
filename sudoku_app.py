def input_board():
    st.write("### 数独の盤面を入力してください（空欄のままでOK）")

    board = np.zeros((9, 9), dtype=int)

    # text_input の見た目だけ整える
    st.markdown("""
        <style>
        .sudoku-input input {
            text-align: center;
            font-size: 22px;
            height: 45px;
            width: 45px;
            padding: 0;
        }
        .block-space {
            margin-right: 20px;   /* 3×3 の横スペース */
        }
        .row-space {
            margin-bottom: 20px;  /* 3×3 の縦スペース */
        }
        </style>
    """, unsafe_allow_html=True)

    for r in range(9):

        # 3×3 の縦スペース
        row_class = "row-space" if r in [3, 6] else ""

        cols = st.columns(9, gap="small")

        for c in range(9):

            # 3×3 の横スペース
            col_class = "block-space" if c in [3, 6] else ""

            key = f"cell_{r}_{c}"

            with cols[c]:
                st.markdown(f"<div class='sudoku-input {row_class} {col_class}'>",
                            unsafe_allow_html=True)

                v = st.text_input(
                    "",
                    key=key,
                    max_chars=1,
                    label_visibility="collapsed",
                    placeholder=" "
                )

                st.markdown("</div>", unsafe_allow_html=True)

            # 入力チェック
            if v.isdigit() and 1 <= int(v) <= 9:
                board[r][c] = int(v)
            else:
                board[r][c] = 0

    return board