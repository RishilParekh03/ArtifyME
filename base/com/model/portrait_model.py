from base import app
import os
import cv2
import numpy as np


class PortraitModel:

    def __init__(self, file):
        print("Image is being processed...Please wait....\n")
        self.img = self.read_file(file)

    def read_file(self, file_path):
        img = cv2.imread(file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print("File Read Successfully...\n")
        return img

    def edge_mask(self, line_size, blur_val):
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        gray_blur = cv2.medianBlur(gray, blur_val)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, line_size, blur_val)
        print("Edge Mask Successfully...\n")
        return edges

    def color_palette(self, k):
        data = np.float32(self.img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.001)
        ret, label, center = cv2.kmeans(data, k, None, criteria, 4, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        res = res.reshape(self.img.shape)
        print("Color Palette Set Successfully...\n")
        return res

    def portrait(self, blur, edge_img):
        portrait_img = cv2.bitwise_and(blur, blur, mask=edge_img)
        print("Portrait Conversion Successfully...\n")
        return portrait_img

    def final_result(self, filename):
        edge_img = self.edge_mask(line_size=9, blur_val=11)
        image = self.color_palette(k=11)
        blur = cv2.GaussianBlur(image, (5, 5), 0)
        portrait_img = self.portrait(blur, edge_img)

        full_image_path = os.path.join(app.config['OUTPUT_FILES'], f"portrait_{filename}")
        image_saved = cv2.imwrite(full_image_path, cv2.cvtColor(portrait_img, cv2.COLOR_RGB2BGR))
        return image_saved, full_image_path
