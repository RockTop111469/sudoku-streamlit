import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract

# --- ソルバー部分 -------------------------------------------------
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

# --- テキスト入力 -------------------------------------------------
def parse_input(text):
    lines = text.strip().split("\n")
    board = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        row = [int(ch) for ch in line]
        board.append(row)
    return board

# --- OCR（数字認識）強化版 -----------------------------------------
def extract_digit(cell_img):
    gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)

    # 白黒反転（細い数字が見えやすくなる）
    gray = cv2.bitwise_not(gray)

    # コントラスト強調
    gray = cv2.equalizeHist(gray)

    # 二値化（本の数字向けに調整）
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # ノイズ除去
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # OCR設定（数字のみ）
    config = "--psm 8 -c tessedit_char_whitelist=123456789"
    text = pytesseract.image_to_string(thresh, config=config)
    text = text.strip()

    return int(text) if text.isdigit() else 0

# --- 画像 → 盤面抽出 ------------------------------------------------
def extract_board_from_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
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
        return None, None

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

    board = []
    cell_size = side // 9

    for r in range(9):
        row = []
        for c in range(9):
            y1 = r * cell_size
            y2 = (r + 1) * cell_size
            x1 = c * cell_size
            x2 = (c + 1) * cell_size

            cell = warped[y1:y2, x1:x2]
            digit = extract_digit(cell)
            row.append(digit)
        board.append(row)

    return warped, board

# --- Streamlit UI ---------------------------------------------------
st.title("ナンプレソルバー（テキスト & 画像対応・OCR強化版）")

tab1, tab2 = st.tabs(["テキスト入力", "画像から解く"])

# --- テキスト入力 ---------------------------------------------------
with tab1:
    st.write("1行9桁、9行で入力（0 は空白）")
    sample = "530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079"
    input_text = st.text_area("盤面を入力", value=sample, height=200)

    if st.button("テキストから解く"):
        try:
            board = parse_input(input_text)
            if len(board) != 9 or any(len(row) != 9 for row in board):
                st.error("9行×9列で入力してください。")
            else:
                if solve(board):
                    st.write("解答：")
                    st.table(board)
                else:
                    st.error("解けませんでした。")
        except Exception as e:
            st.error(f"入力の形式が正しくありません: {e}")

# --- 画像入力 --------------------------------------------------------
with tab2:
    uploaded_file = st.file_uploader(
        "ナンプレの画像をアップロード（本の写真など）",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img = np.array(image)

        st.image(img, caption="アップロードされた画像", use_column_width=True)

        if st.button("画像から盤面を読み取って解く"):
            warped, board = extract_board_from_image(img)

            if warped is None or board is None:
                st.error("盤面の四角形が見つかりませんでした。撮り方を変えてみてください。")
            else:
                st.image(warped, caption="抽出されたナンプレ盤面", use_column_width=True)
                st.write("読み取った盤面：")
                st.table(board)

                if solve(board):
                    st.write("解答：")
                    st.table(board)
                else:
                    st.error("解けませんでした。")
