import cv2
import numpy as np
import time
# img = cv2.imread("sample.png", 1)
# cv2.imshow("画像", 1)
# cv2.waitKey(1)
# cv2.destroyAllwindows()

cap = cv2.VideoCapture(0)
hog = cv2.HOGDescriptor()
# cap = cv2.VideoCapture('768x576.avi')  

# Shi-Tomasiのコーナー検出パラメータ  
feature_params = dict( maxCorners = 100,  
                       qualityLevel = 0.3,  
                       minDistance = 7,  
                       blockSize = 7 )  

# Lucas-Kanade法のパラメータ  
lk_params = dict( winSize  = (15,15),  
                  maxLevel = 2,  
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))  

# ランダムに色を100個生成（値0～255の範囲で100行3列のランダムなndarrayを生成）  
color = np.random.randint(0, 255, (100, 3))  

# 最初のフレームの処理  
end_flag, frame = cap.read()  

# グレースケール変換  
gray_prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
# 追跡に向いた特徴  
feature_prev = cv2.goodFeaturesToTrack(gray_prev, mask = None, **feature_params)  
# 元の配列と同じ形にして0を代入  
mask = np.zeros_like(frame)  

# 全身の人を検出(SVM)  
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  
hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.1}  

while(end_flag):  
    # グレースケールに変換  
    gray_next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

    #時間取得  
    start = time.time()  
    # 人を検出した座標  
    human, r = hog.detectMultiScale(frame, **hogParams)  
    #時間取得  
    end = time.time()  
    # 検出時間を表示  
#    print("{} : {:4.1f}ms".format("detectTime", (end - start) * 1000))   

    # オプティカルフロー検出  
    # オプティカルフローとは物体やカメラの移動によって生じる隣接フレーム間の物体の動きの見え方のパターン  
    feature_next, status, err = cv2.calcOpticalFlowPyrLK(gray_prev, gray_next, feature_prev, None, **lk_params)  
    # オプティカルフローを検出した特徴点を選別（0：検出せず、1：検出した）  
    good_prev = feature_prev[status == 1]  
    good_next = feature_next[status == 1]  

    # オプティカルフローを描画  
    for i, (next_point, prev_point) in enumerate(zip(good_next, good_prev)):  
        prev_x, prev_y = prev_point.ravel()  
        next_x, next_y = next_point.ravel()  
        mask = cv2.line(mask, (next_x, next_y), (prev_x, prev_y), color[i].tolist(), 2)  
        frame = cv2.circle(frame, (next_x, next_y), 5, color[i].tolist(), -1)  

    svm_img = cv2.add(frame, mask)  

    # 人検出した数表示のため変数初期化  
    svm_human_cnt = 0    
    # 人検出した部分を長方形で囲う(SVM)  
    for (x, y, w, h) in human:  
        cv2.rectangle(svm_img, (x, y),(x+w, y+h),(0,0,255), 2)  
        svm_human_cnt += 1  

    # 人検出した数を表示  
    cv2.putText(svm_img, "Human Cnt:{}".format(int(svm_human_cnt)),(10,550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
    # cv2.moveWindow("SVM",650,100) # Window表示位置指定   
    # ウィンドウに表示  
    windowsize = (800*2, 600*2)
    svm_img = cv2.resize(svm_img, windowsize)
    cv2.imshow('SVM', svm_img)  

    # ESCキー押下で終了  
    if cv2.waitKey(30) & 0xff == 27:  
        break  

    # 次のフレーム、ポイントの準備  
    gray_prev = gray_next.copy()  
    feature_prev = good_next.reshape(-1, 1, 2)  
    end_flag, frame = cap.read()  

# 終了処理  
cv2.destroyAllWindows()  
cap.release()  