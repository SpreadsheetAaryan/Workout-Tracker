import cv2 as cv
import PIL
import numpy as np
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt

class Model:
    def __init__(self):
        self.model = LinearSVC()
        self.img_list = np.array([])
        self.class_list = np.array([])

    def augment_image(self, img):
        # img is a numpy array (grayscale)
        augmented = []
        # Original
        augmented.append(img)
        # Horizontal flip
        augmented.append(np.fliplr(img))
        # Vertical flip
        augmented.append(np.flipud(img))
        # Rotate 90 degrees
        augmented.append(np.rot90(img))
        # Add more augmentations as needed (e.g., brightness, noise)
        return augmented

    def train_model(self, counters):
        img_list = []
        class_list = []

        for i in range(1, counters[0]):
            img = cv.imread(f"1/frame{i}.jpg")[:, :, 0]
            img = cv.resize(img, (150, 150))
            for aug in self.augment_image(img):
                img_list.append(aug.flatten())
                class_list.append(1)

        for i in range(1, counters[1]):
            img = cv.imread(f"2/frame{i}.jpg")[:, :, 0]
            img = cv.resize(img, (150, 150))
            for aug in self.augment_image(img):
                img_list.append(aug.flatten())
                class_list.append(2)

        self.img_list = np.array(img_list)
        self.class_list = np.array(class_list)

        print('Model Training')

        self.model.fit(self.img_list, self.class_list)
        print("Model Trained")

    def predict(self, frame):
        frame = frame[1]
        cv.imwrite("frame.jpg", cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open("frame.jpg")
        img = img.resize((150, 150), PIL.Image.LANCZOS)  # <-- Use resize, not thumbnail!
        img.save("frame.jpg")
        img = cv.imread("frame.jpg")[:, :, 0]
        img = img.flatten()
        prediction = self.model.predict([img])
        return prediction[0]