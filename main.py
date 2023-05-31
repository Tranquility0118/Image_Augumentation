import albumentations as Image_Augumentation
from PIL import Image
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

class ImageAugmentationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Augmentation")
        self.layout = QVBoxLayout()

        # 입력 폴더 선택
        self.input_folder_label = QLabel("입력 폴더:")
        self.input_folder_lineedit = QLineEdit()
        self.input_folder_button = QPushButton("폴더 선택")
        self.input_folder_button.clicked.connect(self.select_input_folder)
        self.layout.addWidget(self.input_folder_label)
        self.layout.addWidget(self.input_folder_lineedit)
        self.layout.addWidget(self.input_folder_button)

        # 결과 폴더 선택
        self.output_folder_label = QLabel("결과 폴더:")
        self.output_folder_lineedit = QLineEdit()
        self.output_folder_button = QPushButton("폴더 선택")
        self.output_folder_button.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.output_folder_label)
        self.layout.addWidget(self.output_folder_lineedit)
        self.layout.addWidget(self.output_folder_button)

        # 폴더 이름 입력
        self.folder_name_label = QLabel("폴더 이름:")
        self.folder_name_lineedit = QLineEdit()
        self.layout.addWidget(self.folder_name_label)
        self.layout.addWidget(self.folder_name_lineedit)

        # 반복 횟수 입력
        self.iterations_label = QLabel("반복 횟수:")
        self.iterations_lineedit = QLineEdit()
        self.layout.addWidget(self.iterations_label)
        self.layout.addWidget(self.iterations_lineedit)

        # 실행 버튼
        self.run_button = QPushButton("실행")
        self.run_button.clicked.connect(self.run_image_augmentation)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)

    def select_input_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "입력 폴더 선택")
        self.input_folder_lineedit.setText(folder_path)

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "결과 폴더 선택")
        self.output_folder_lineedit.setText(folder_path)

    def run_image_augmentation(self):
        # 입력 폴더 경로
        input_folder = self.input_folder_lineedit.text()
        # 결과 폴더 경로
        output_folder = self.output_folder_lineedit.text()
        # 사용자가 입력한 폴더 이름
        user_folder_name = self.folder_name_lineedit.text()
        # 사용자가 입력한 반복 횟수
        iterations = int(self.iterations_lineedit.text())

        # 폴더 경로 생성
        run_folder = os.path.join(output_folder, user_folder_name)
        os.makedirs(run_folder, exist_ok=True)

        # 증강할 변환 정의하기
        transform = Image_Augumentation.Compose([
            Image_Augumentation.Resize(width=256, height=256),    #가로(width)와 세로(height) 크기로 조정
            Image_Augumentation.RandomCrop(width=224, height=224),#가로(width)와 세로(height) 크기로 무작위로 자름
            Image_Augumentation.HorizontalFlip(p=0.5),            #이미지를 수평으로 무작위로 뒤집습니다. 
            Image_Augumentation.Rotate(limit=30),                 #이미지를 최대 +-30도까지 무작위로 회전
            Image_Augumentation.RandomBrightnessContrast(p=0.2),  #명암 대비를 무작위로 조절
            Image_Augumentation.HueSaturationValue(p=0.2),        #색상, 채도, 명도를 무작위로 조절.
            Image_Augumentation.ShiftScaleRotate(p=0.2),          #이미지를 무작위로 이동, 확대/축소 및 회전
            Image_Augumentation.GaussianBlur(p=0.2),              #이미지에 가우시안 블러를 적용합니다
            Image_Augumentation.RandomGamma(p=0.2),               #이미지의 감마(gamma) 값을 무작위로 조절
        ])
         
        # 대상 폴더 내에 있는 이미지 파일들의 경로 가져오기
        image_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if
                       filename.lower().endswith(('.jpg', '.jpeg', '.png'))]

        # 대상 이미지 파일들 순회
        for image_path in image_paths:
            # 이미지 불러오기
            image = Image.open(image_path)

            # 반복 수 지정
            for i in range(1, iterations + 1):
                # 이미지에 변환 적용하기
                augmented_image = transform(image=np.array(image))['image']

                # 증강된 이미지 저장하기
                filename = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(run_folder, f'{filename}_augmented{i}.png')
                augmented_image = Image.fromarray(augmented_image)
                augmented_image.save(output_path)

        # 변환 완료 메시지 표시
        print("이미지 변환이 완료되었습니다.")

if __name__ == '__main__':
    app = QApplication([])
    window = ImageAugmentationGUI()
    window.show()
    app.exec_()
