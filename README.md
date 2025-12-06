# 🐱 AI猫検知・防犯カメラシステム (Cat Security Camera)

Webカメラ（iPhone + Iriun Webcam）の映像をリアルタイムで解析し、猫を検知すると「警告音」を鳴らして「証拠写真」を自動保存するAIシステムです。
工場の「不良品検知システム」や「侵入検知」のロジックを家庭用に応用しました。

# 🎥 デモ
![デモ](./images/demo.jpg)

# ✨ 機能
*   リアルタイム物体検知 : YOLOv8 (AI) を使用し、高速に「猫」だけを特定。
*   アラート機能 : 検知と同時に警告音を再生。連打防止のクールダウン機能付き。
*   自動撮影 : 検知した瞬間のフレームを画像として `captures/` フォルダに自動保存。
*   スマホ通知 : Discord Webhookと連携し、検知した瞬間の写真をリアルタイムでスマホに送信。外出先からでも侵入者（猫）を確認可能。
*   自動テスト: CI/CDを意識し、カメラがない環境でも静止画を使ってAIロジックを検証するテストコードを完備。

# 🛠 使用技術
*   言語 : Python 3.13
*   AIモデル : Ultralytics YOLOv8
*   画像処理 : OpenCV
*   音声処理 : Pygame
*   通知連携 : Discord Webhook (Requests)
*   環境管理 : python-dotenv
*   テスト : Pytest

# 🚀 実行方法

# 1. 準備
ライブラリのインストール
pip install -r requirements.txt
※ requirements.txt には ultralytics, opencv-python, pygame, requests, python-dotenv が含まれます。

# 2. 環境変数の設定
プロジェクト直下に .env ファイルを作成し、DiscordのWebhook URLを設定します。
（通知機能を使わない場合は不要です）
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url...

# 3. カメラ設定
PCにカメラが複数ある場合、以下のツールで番号を確認してください。
python check_cameras.py
確認した番号を cat_security.py の CAMERA_INDEX に設定します。

# 4. 起動
python cat_security.py

🧪 テストの実行
カメラがない環境でも、以下のコマンドでAIの動作チェックが可能です。
pytest
