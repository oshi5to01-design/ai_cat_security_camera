import cv2
import time
import pygame
import os
import requests
from datetime import datetime
from ultralytics import YOLO
from dotenv import load_dotenv

# ==========================================
# ⚙️ 設定エリア
# ==========================================
load_dotenv()  # .envファイルを読み込む

CAMERA_INDEX = 0  # iPhoneのカメラ番号
SOUND_FILE = "alert.mp3"  # 鳴らす音ファイル
COOLDOWN_SECONDS = 10  # 連打防止の待機時間
CONFIDENCE_THRESHOLD = 0.8  # AIの自信
SAVE_DIR = "captures"  # 写真の保存先フォルダ

# DiscordのURLを取得
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


# ==========================================
# 🛠️ Discord送信関数
# ==========================================
def send_discord_alert(image_path):
    """Discordに画像とメッセージを送信する"""
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ DiscordのURLが設定されていないため、通知をスキップします")
        return

    print("🚀 Discordに通知を送信中...")

    # 送信するメッセージ
    data = {"content": "🚨 **猫を検知しました！** 🐈\nニャ〜〜"}

    try:
        # 画像ファイルを開いて送信
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(DISCORD_WEBHOOK_URL, data=data, files=files)

        if response.status_code == 204 or response.status_code == 200:
            print("✅ Discord通知成功！")
        else:
            print(f"❌ Discord送信失敗: {response.status_code}")

    except Exception as e:
        print(f"❌ 送信エラー: {e}")


# ==========================================
# 🚀 初期化
# ==========================================
print("🧠 AIモデルを読み込んでいます...")
model = YOLO("yolov8n.pt")

# 保存用フォルダ作成
os.makedirs(SAVE_DIR, exist_ok=True)

print("🎵 音声システムを起動中...")
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    if not os.path.exists(SOUND_FILE):
        print(f"❌ エラー: {SOUND_FILE} が見つかりません！")
        sound_enabled = False
    else:
        pygame.mixer.music.load(SOUND_FILE)
        sound_enabled = True
        print("✅ 音声ファイルのロード完了")
except Exception as e:
    print(f"⚠️ 音声エラー: {e}")
    sound_enabled = False

print(f"📷 カメラ({CAMERA_INDEX})を起動中...")
cap = cv2.VideoCapture(CAMERA_INDEX)

last_played_time = 0

# ==========================================
# 🔄 メインループ
# ==========================================
print("👀 監視を開始します... (終了は 'q' キー)")

if not DISCORD_WEBHOOK_URL:
    print("⚠️ 注意: .envにDISCORD_WEBHOOK_URLがないため、スマホ通知は届きません")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ カメラ映像が取得できません")
        break

    # 1. AI検知 (猫=15)
    results = model(frame, classes=[15], conf=CONFIDENCE_THRESHOLD)

    # 枠付き画像を作る
    annotated_frame = results[0].plot()

    # 2. 猫がいるかチェック
    if len(results[0].boxes) > 0:
        current_time = time.time()

        if current_time - last_played_time > COOLDOWN_SECONDS:
            print("\n🐱 猫を検知！アクション実行！")

            # A. 音を鳴らす
            if sound_enabled:
                if not pygame.mixer.music.get_busy():
                    try:
                        pygame.mixer.music.play()
                    except Exception:
                        pass

            # B. 写真を保存する
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cat_{timestamp}.jpg"
            save_path = os.path.join(SAVE_DIR, filename)

            # 枠付き画像を保存
            cv2.imwrite(save_path, annotated_frame)
            print(f"📸 証拠保存: {save_path}")

            # C. Discordに送信 (New!)
            send_discord_alert(save_path)

            last_played_time = current_time

    # 3. 画面表示
    cv2.imshow("Cat Security Camera", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
print("👋 終了しました")
