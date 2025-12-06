import cv2

print("📷 カメラを探しています...")

# 0番から9番まで順番にチェックする
for index in range(10):
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"✅ カメラ番号 {index}: 発見しました！")
        cap.release()
    else:
        pass  # 見つからなかったら何もしない

print("--- 終了 ---")
print("見つかった番号を cv2.VideoCapture(ココ) に入れてね！")
