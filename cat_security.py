import cv2
import time
import pygame
import os
import requests
from datetime import datetime
from ultralytics import YOLO
from dotenv import load_dotenv

# ==========================================
# ⚙️ 定数設定 (Constants)
# ==========================================
# 定数は大文字で上に書くのがマナー
load_dotenv()
CAMERA_INDEX = 1
SOUND_FILE = "alert.mp3"
COOLDOWN_SECONDS = 10
CONFIDENCE_THRESHOLD = 0.8
SAVE_DIR = "captures"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


# ==========================================
# 🛠️ 機能関数
# ==========================================
def send_discord_alert(image_path):
    """Discordに画像とメッセージを送信する"""
    if not DISCORD_WEBHOOK_URL:
        return

    print("🚀 Discordに通知を送信中...")
    data = {"content": "🚨 **猫を検知しました！** 🐈\n証拠写真を送信します。"}

    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            requests.post(DISCORD_WEBHOOK_URL, data=data, files=files)
            print("✅ Discord通知成功！")
    except Exception as e:
        print(f"❌ 送信エラー: {e}")


def initialize_system():
    """システム初期化（モデル、音声、カメラの準備）"""
    print("🧠 AIモデルを読み込んでいます...")
    model = YOLO("yolov8n.pt")

    os.makedirs(SAVE_DIR, exist_ok=True)

    print("🎵 音声システムを起動中...")
    sound_enabled = False
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        if os.path.exists(SOUND_FILE):
            pygame.mixer.music.load(SOUND_FILE)
            sound_enabled = True
            print("✅ 音声ファイルのロード完了")
        else:
            print(f"❌ エラー: {SOUND_FILE} が見つかりません")
    except Exception as e:
        print(f"⚠️ 音声エラー: {e}")

    print(f"📷 カメラ({CAMERA_INDEX})を起動中...")
    cap = cv2.VideoCapture(CAMERA_INDEX)

    # 準備したものをまとめて返す（タプルで返す）
    return model, cap, sound_enabled


# ==========================================
# 🔄 メイン処理
# ==========================================
def main():
    """メインループ"""
    # 1. 初期化関数を呼んで、道具を受け取る
    model, cap, sound_enabled = initialize_system()

    if not cap.isOpened():
        print("❌ カメラが開けませんでした。終了します。")
        return

    last_played_time = 0
    print("👀 監視を開始します... (終了は 'q' キー)")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ 映像取得エラー")
                break

            # AI検知
            results = model(frame, classes=[15], conf=CONFIDENCE_THRESHOLD)
            annotated_frame = results[0].plot()

            # 猫チェック
            if len(results[0].boxes) > 0:
                current_time = time.time()

                if current_time - last_played_time > COOLDOWN_SECONDS:
                    print("\n🐱 猫を検知！アクション実行！")

                    # 音
                    if sound_enabled and not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()

                    # 保存
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_path = os.path.join(SAVE_DIR, f"cat_{timestamp}.jpg")
                    cv2.imwrite(save_path, annotated_frame)
                    print(f"📸 証拠保存: {save_path}")

                    # 通知
                    send_discord_alert(save_path)

                    last_played_time = current_time

            cv2.imshow("Cat Security Camera", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        # 終了処理（エラーで落ちても必ず実行される）
        print("👋 終了処理中...")
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()


# ==========================================
# 🏁 エントリーポイント
# ==========================================
if __name__ == "__main__":
    main()
