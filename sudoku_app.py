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

    # 白黒反転（細い