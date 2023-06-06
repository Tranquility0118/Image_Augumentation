import albumentations as Image_Augumentation
from PIL import Image
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox, QProgressBar
from PyQt5 import QtCore

class ImageAugmentationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Augmentation")
        self.setFixedSize(400, 750)
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

        # 변환 옵션 체크박스
        self.transform_options_label = QLabel("변환 옵션:")
        self.layout.addWidget(self.transform_options_label)

        # 리사이즈 옵션
        self.resize_checkbox = QCheckBox("크기 조정")
        self.layout.addWidget(self.resize_checkbox)

        self.resize_width_label = QLabel("가로:")
        self.resize_width_lineedit = QLineEdit("256")
        self.layout.addWidget(self.resize_width_label)
        self.layout.addWidget(self.resize_width_lineedit)

        self.resize_height_label = QLabel("세로:")
        self.resize_height_lineedit = QLineEdit("256")
        self.layout.addWidget(self.resize_height_label)
        self.layout.addWidget(self.resize_height_lineedit)

        self.random_crop_checkbox = QCheckBox("랜덤 자르기")
        self.layout.addWidget(self.random_crop_checkbox)

        self.horizontal_flip_checkbox = QCheckBox("수평 뒤집기")
        self.layout.addWidget(self.horizontal_flip_checkbox)

        self.rotate_checkbox = QCheckBox("회전")
        self.layout.addWidget(self.rotate_checkbox)

        self.brightness_contrast_checkbox = QCheckBox("명암/대비 조절")
        self.layout.addWidget(self.brightness_contrast_checkbox)

        self.hue_saturation_value_checkbox = QCheckBox("색상/채도/명도 조절")
        self.layout.addWidget(self.hue_saturation_value_checkbox)

        self.shift_scale_rotate_checkbox = QCheckBox("이동/확대,축소/회전")
        self.layout.addWidget(self.shift_scale_rotate_checkbox)

        self.gaussian_blur_checkbox = QCheckBox("가우시안 블러")
        self.layout.addWidget(self.gaussian_blur_checkbox)

        self.random_gamma_checkbox = QCheckBox("감마값 조절")
        self.layout.addWidget(self.random_gamma_checkbox)

        # 실행 버튼
        self.run_button = QPushButton("실행")
        self.run_button.clicked.connect(self.run_image_augmentation)
        self.layout.addWidget(self.run_button)
        self.setLayout(self.layout)

        # 실행 상태 표시 레이블
        self.status_label = QLabel()
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)  # Set text alignment to center
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)

        # 진행 상태 표시 프로그래스바
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)
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

        # 증강할 변환 옵션 설정
        transform_options = []
        if self.resize_checkbox.isChecked():
            resize_width = int(self.resize_width_lineedit.text())
            resize_height = int(self.resize_height_lineedit.text())
            transform_options.append(Image_Augumentation.Resize(width=resize_width, height=resize_height))
        if self.random_crop_checkbox.isChecked():
            transform_options.append(Image_Augumentation.RandomCrop(width=224, height=224))
        if self.horizontal_flip_checkbox.isChecked():
            transform_options.append(Image_Augumentation.HorizontalFlip(p=0.5))
        if self.rotate_checkbox.isChecked():
            transform_options.append(Image_Augumentation.Rotate(limit=30))
        if self.brightness_contrast_checkbox.isChecked():
            transform_options.append(Image_Augumentation.RandomBrightnessContrast(p=0.2))
        if self.hue_saturation_value_checkbox.isChecked():
            transform_options.append(Image_Augumentation.HueSaturationValue(p=0.2))
        if self.shift_scale_rotate_checkbox.isChecked():
            transform_options.append(Image_Augumentation.ShiftScaleRotate(p=0.2))
        if self.gaussian_blur_checkbox.isChecked():
            transform_options.append(Image_Augumentation.GaussianBlur(p=0.2))
        if self.random_gamma_checkbox.isChecked():
            transform_options.append(Image_Augumentation.RandomGamma(p=0.2))

        # 변환 정의하기
        transform = Image_Augumentation.Compose(transform_options)

        # 대상 폴더 내에 있는 이미지 파일들의 경로 가져오기
        image_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if
                       os.path.isfile(os.path.join(input_folder, filename))]

        total_images = len(image_paths)
        processed_images = 0

        # 진행 상태 초기화
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(total_images)

        # 이미지 증강 및 저장
        for image_path in image_paths:
            try:
                # 이미지 열기
                image = Image.open(image_path)

                # Ensure image has 3 channels (RGB)
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                # Skip images with more than 3 channels
                if image.mode != 'RGB':
                    print(f"Skipping image: {image_path} - Invalid channel format")
                    continue

                # 반복 횟수에 따라 이미지 증강 및 저장
                for i in range(iterations):
                    # 이미지 변환
                    transformed_image = transform(image=np.array(image))['image']

                    # 저장할 파일 경로
                    file_name = os.path.basename(image_path)
                    output_path = os.path.join(run_folder, f"{file_name}_{i+1}.jpg")

                    # 이미지 저장
                    transformed_image = Image.fromarray(transformed_image)
                    transformed_image.save(output_path)

                    # 처리된 이미지 수 증가
                    processed_images += 1

                    # 진행 상태 업데이트
                    self.progress_bar.setValue(processed_images)

            except Exception as e:
                print(f"Error processing image: {image_path}")
                print(e)

        # 이미지 증강 완료 메시지
        self.status_label.setText("이미지 증강이 완료되었습니다.")

        self.progress_bar.setValue(total_images)
    

if __name__ == '__main__':
    app = QApplication([])
    window = ImageAugmentationGUI()
    window.show()
    app.exec_() 