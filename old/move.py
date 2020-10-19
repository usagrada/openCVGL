import cv2
import numpy as np
cap = cv2.VideoCapture(0)
avg = None

while True:
    # 1フレームずつ取得する。
    ret, frame = cap.read()
    if not ret:
        break

    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 比較用のフレームを取得する
    if avg is None:
        avg = gray.copy().astype("float")
        continue

    # 現在のフレームと移動平均との差を計算
    cv2.accumulateWeighted(gray, avg, 0.6)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # デルタ画像を閾値処理を行う
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    # 画像の閾値に輪郭線を入れる
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    np_thresh = np.array(thresh)
    topicSum = np.sum(np_thresh, axis=0)

    # 現在右左中央のどこにいるのかを判定するプログラム
    left = 0
    center = 0
    right = 0
    
    for i in range(len(topicSum)):
        if i*3 < len(topicSum):
            right+=topicSum[i]
        elif i*3 < len(topicSum)*2:
            center += topicSum[i]
        else:
            left+=topicSum[i]
    if left > center and left > right:
        print("left")
    elif right > center and right > left:
        print("right")
    else:
        print("center")


    # 結果を出力
    windowsize = (800, 600)
    thresh = cv2.resize(thresh, windowsize)
    cv2.imshow("Frame", frame)
    cv2.imshow("move", thresh)
    key = cv2.waitKey(30)
    if key == 27:
        break
    # break

cap.release()
cv2.destroyAllWindows()