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

import cv2
import numpy as np
from PIL import Image
import streamlit as st

st.title("ナンプレソルバー（画像読み取り対応）")

uploaded_file = st.file_uploader("ナンプレの画像をアップロード", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を読み込む
    image = Image.open(uploaded_file)
    img = np.array(image)

    st.image(img, caption="アップロードされた画像", use_column_width=True)

    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ぼかしてノイズ除去
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 二値化
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # 輪郭を検出
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 一番大きい四角形を探す
    biggest = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    if biggest is not None:
        # 頂点を並び替え
        pts = biggest.reshape(4, 2)
        pts = sorted(pts, key=lambda x: x[1])  # y座標でソート

        top = sorted(pts[:2], key=lambda x: x[0])
        bottom = sorted(pts[2:], key=lambda x: x[0])

        ordered = np.array([top[0], top[1], bottom[0], bottom[1]], dtype="float32")

        # 変換後のサイズ
        side = 450
        dst = np.array([[0, 0], [side, 0], [0, side], [side, side]], dtype="float32")

        # 射影変換
        matrix = cv2.getPerspectiveTransform(ordered, dst)
        warped = cv2.warpPerspective(img, matrix, (side, side))

        st.image(warped, caption="抽出されたナンプレ盤面", use_column_width=True)
    else:
        st.write("盤面の四角形が見つかりませんでした…")
