import pytest
import os
from ultralytics import YOLO
import cv2

# テストに使う画像とモデル
TEST_IMAGE = "test_cat.png"
MODEL_FILE = "yolov8n.pt"


def test_files_exist():
    """必要なファイルが揃っているかチェック"""
    assert os.path.exists(TEST_IMAGE), "テスト用の猫画像がないよ！"
    assert os.path.exists(MODEL_FILE), "YOLOのモデルファイルがないよ！"
    assert os.path.exists("alert.mp3"), "音声ファイルがないよ！"


def test_ai_detection():
    """
    静止画（猫の写真）をAIに読ませて、
    ちゃんと「猫(class 15)」を見つけられるかテスト
    """
    # 1. モデルをロード
    model = YOLO(MODEL_FILE)

    # 2. 画像をロード
    frame = cv2.imread(TEST_IMAGE)
    assert frame is not None, "画像の読み込みに失敗したよ"

    # 3. 推論実行（猫だけを探す）
    results = model(frame, classes=[15], conf=0.5)

    # 4. 検証
    # 「検出された箱（boxes）」が1つ以上あるはず
    detected_count = len(results[0].boxes)

    print(f"検出された猫の数: {detected_count}")
    assert detected_count > 0, "猫が写ってるはずなのに検知されなかった！"
