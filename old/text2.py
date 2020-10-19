import cv2
import matplotlib.pyplot as plt


def draw_result_on_img(img, texts, w_ratio=0.35, h_ratio=0.2, alpha=0.4):
    # 文字をのせるためのマットを作成する
    overlay = img.copy()
    pt1 = (0, 0)
    pt2 = (int(img.shape[1] * w_ratio), int(img.shape[0] * h_ratio))

    mat_color = (200, 200, 200)
    fill = -1  # -1にすると塗りつぶし
    cv2.rectangle(overlay, pt1, pt2, mat_color, fill)

    mat_img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    draw_texts(mat_img, texts)

    return mat_img

def draw_texts(img, texts, font_scale=0.7, thickness=2):
    h, w, c = img.shape
    offset_x = 10  # 左下の座標
    initial_y = 0
    dy = int(img.shape[1] / 15)
    color = (0, 0, 0)  # black

    texts = [texts] if type(texts) == str else texts

    for i, text in enumerate(texts):
        offset_y = initial_y + (i+1)*dy
        cv2.putText(img, text, (offset_x, offset_y), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, color, thickness, cv2.LINE_AA)
    


img = cv2.imread("sample.png")
mat_img = draw_result_on_img(img, texts=["name: lenna", "gender: female"])

plt.figure(figsize=(8, 8))
plt.imshow(cv2.cvtColor(mat_img, cv2.COLOR_BGR2RGB))
plt.savefig("text.png")