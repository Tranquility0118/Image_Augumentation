Image_Augumentation
===
Requirments 

python 3.11.x

pip install pyqt5

pip install albumentations

pip install pillow

Target과 Result폴더는 사용자가 임의로 지정하는 것 이므로, 변경 가능합니다. 

---
사용법
---
1. CMD or Anaconda prompt 등을 사용하여 main.py를 실행합니다.

2. 첫 번째 폴더 선택은 증강할 이미지 데이터가 있는 폴더를 선택합니다.

3. 두 번째 폴더 선택은 결과를 저장할 폴더를 선택합니다. 

4. 반복 횟수 설정(증강을 적용할 횟수로 사진1장에 반복 10을 하면 10장의 증강된 이미지를 얻을 수 있음)

5. 실행
---
증강 함수 설명
---

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
