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
