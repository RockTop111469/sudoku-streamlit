import streamlit as st
import cv2
import numpy as np
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import fetch_openml

# ============================================================
# 1. MNIST を使って KNN モデルを自動生成
# ============================================================
@st.cache_resource
def train_knn_model():
    st.write("MNIST をダウンロードして KNN を学習中…（初回のみ数秒）")

    mnist = fetch_openml('mnist_784', version=1, as_frame=False)
    X = mnist.data.astype(np.float32)
    y = mnist.target.astype(np.int32)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    st.write("MNIST KNN モデル準備完了！")
    return knn

# ============================================================
# 2. KNN で数字を予測（マス中央を強調）
# ============================================================
def knn_predict_digit(knn, cell_img):
    gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)

    # 軽くぼかしてノイズ除去
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # 自前の二値化（本の印刷向けに少し甘め）
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # MNIST と同じ 28×28 に変換
    resized = cv2.resize(th, (28, 28))
    sample = resized.reshape(1, -1).astype(np.float32)

    digit = knn.predict(sample)[0]
    digit = int(digit)

    return digit if digit != 0 else 0

# ============================================================
# 3. 盤面抽出（射影変換）
# ============================================================
def extract_board_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    th = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contours, _ = cv2.findContours(
        th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

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

    if biggest is None:
        return None

    pts = biggest.reshape(4, 2)
    pts = sorted(pts, key=lambda x: x[1])

    top = sorted(pts[:2], key=lambda x: x[0])
    bottom = sorted(pts[2:], key=lambda x: x[0])

    ordered = np.array(
        [top[0], top[1], bottom[0], bottom[1]],
        dtype="float32"
    )

    side = 450
    dst = np.array(
        [[0, 0], [side, 0], [0, side], [side, side]],
        dtype="float32"
    )

    matrix = cv2.getPerspectiveTransform(ordered, dst)
    warped = cv2.warpPerspective(img, matrix, (side, side))

    # 念のため正方形にリサイズ
    warped = cv2.resize(warped, (450, 450))

    return warped

# ============================================================
# 4. 盤面を 9×9 に分割して KNN で数字を読む（マス中央だけ切り出し）
# ============================================================
def extract_board_numbers(warped, knn):
    board = []
    h, w, _ = warped.shape
    cell_h = h // 9
    cell_w = w // 9

    margin_h = cell_h // 6  # 上下を少し削る
    margin_w = cell_w // 6  # 左右を少し削る

    for r in range(9):
        row = []
        for c in range(9):
            y1 = r * cell_h + margin_h
            y2 = (r + 1) * cell_h - margin_h
            x1 = c * cell_w + margin_w
            x2 = (c + 1) * cell_w - margin_w

            cell = warped[y1:y2, x1:x2]
            digit = knn_predict_digit(knn, cell)
            row.append(digit)
        board.append(row)

    return board

# ============================================================
# 5. Sudoku ソルバー
# ============================================================
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

# ============================================================
# 6. Streamlit UI
# ============================================================
st.title("ナンプレソルバー（MNIST KNN OCR版・盤面抽出改良）")

knn = train_knn_model()

uploaded_file = st.file_uploader("ナンプレ画像をアップロード", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = np.array(image)

    st.image(img, caption="アップロードされた画像", use_column_width=True)

    if st.button("画像から解く！"):
        warped = extract_board_image(img)

        if warped is None:
            st.error("盤面の四角形が見つかりませんでした。")
        else:
            st.image(warped, caption="抽出された盤面", use_column_width=True)

            board = extract_board_numbers(warped, knn)
            st.write("読み取った盤面：")
            st.table(board)

            if solve(board):
                st.write("解答：")
                st.table(board)
            else:
                st.error("解けませんでした。")