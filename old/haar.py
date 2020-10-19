import numpy as np  
import cv2  
import time  

# 体全体のカスケードファイル
#カスケードファイルのパス設定
# cascade_file = "/usr/lib64/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml"
cascade_file = "./haarcascade_fullbody.xml"
cap = cv2.VideoCapture(0)

while True:
	#画像を読み込む
    ret, image = cap.read()
    image_gs = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cascade_file)
	#顔認識処理
    face_list = cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(150,150))

    if len(face_list) >0 :
        #検出部分に囲みを付ける
        print(face_list)
        color = (255,255,255)
        for face in face_list:
            x,y,w,h = face
            cv2.rectangle(image, (x,y), (x+w, y+h), color, thickness=8)  
        #検出結果の画像ファイルを出力する。
        cv2.imwrite("facedetect-output.png", image)
    else:
        print("No face")
    
    if cv2.waitKey(30) & 0xff == 27:  
        break  

def main():
    fullbody_detector = cv2.CascadeClassifier("/Users/local/source/opencv/face_recognition/data_xml/haarcascade_fullbody.xml")  
    # サンプル画像  
    cap = cv2.VideoCapture(0)  

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

    while(end_flag):  
        # グレースケールに変換  
        gray_next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

        start = time.time()    
        # 全身の人を検出   
        # minSize:物体が取り得る最小サイズ。これよりも小さい物体は無視される  
        # minNeighbors:物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む  
        body = fullbody_detector.detectMultiScale(gray_next,scaleFactor=1.1, minNeighbors=3, minSize=(40, 40))  
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
        img = cv2.add(frame, mask)  

        # 人検出した数表示のため変数初期化  
        human_cnt = 0  
        # 人検出した部分を長方形で囲う  
        for (x, y, w, h) in body:  
            cv2.rectangle(img, (x, y),(x+w, y+h),(0,255,0),2)  
            # 人検出した数を加算  
            human_cnt += 1  

        # 人検出した数を表示  
        cv2.putText(img, "Human Cnt:{}".format(int(human_cnt)),(10,550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)  
        # ウィンドウに表示  
        cv2.imshow('human_view', img)  

    # ESCキー  
        k = cv2.waitKey(1)  
        if k == 27:  
            break  

        # 次のフレーム、ポイントの準備  
        gray_prev = gray_next.copy()  
        feature_prev = good_next.reshape(-1, 1, 2)  
        end_flag, frame = cap.read()  

    # 終了処理  
    cv2.destroyAllWindows()  
    cap.release()  