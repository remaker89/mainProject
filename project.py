### 간단한 이미지 모자이크 도구
## 개요

# 목적 : 사용자가 지정한 이미지의 일부 영역(예: 얼굴, 번호판 등)에 손쉽게 모자이크
# 처리를 할 수 있는 프로그램을 개발한다.

# 대상자 : Python 과 OpenCV 를 입문 수준으로 학습한 학부생
# 기본적인 이미지 입출력 및 GUI 사용법을 배우려는 자

# 기능 요구사항 (Functional Requirements) :
# FR-1 이미지 입력 / 사용자가 로컬 파일에서 이미지를 불러온다.
# FR-2 영역 지정 / 마우스 드래그로 모자이크를 적용할 영역을 선택할 수 있다.
# FR-3 모자이크 처리 / 선택한 영역에 대해 픽셀 블러 방식으로 모자이크 효과를 적용한다.
# FR-4 결과 저장 / 모자이크 처리된 이미지를 새로운 파일로 저장할 수 있다.
# FR-5 모자이크 세기조절 / 사용자로부터 모자이크 세기를 입력 받아 모자이크 강도를 조정할 수 있다.

#비기능 요구사항 (Non-functional Requirements) :
# NR-1: OpenCV 라이브러리를 사용해야 한다.
# NR-2: 이미지 입력, 영역 지정, 결과 저장, 모자이크 세기 조절은 GUI 를 이용하여 사용자로부터 필요한 정보 입력 받을 것.
# NR-3: GUI 완성을 위해 OpenCV 또는 tkinter 를 활용할 것.
# NR-4: 결과물은 PNG 또는 JPG 포맷으로 저장 가능해야 한다.

# 프로그램 흐름 (Workflow)
# [이미지 입력]  [영상 표시]  [마우스로 영역 지정]  [선택 영역에 모자이크
# 적용]  [모자이크 강도에 변화 줄 경우 모자이크 재적용]  [결과 이미지 저장]





import numpy as np,cv2
import tkinter as tk
# 파일 선택 창 생성하는 모듈
from tkinter import filedialog, Label
from PIL import Image,ImageTk

testwindow=tk.Tk() # window 생성
testwindow.title('open file') # window 이름

select_img_label=None # 선탟한 이미지의 라벨 변수
select_img=None # 선택한 이미지 변수

def openFile(): # 파일 여는 함수
    global select_img,select_img_label
    img_filetypes=(('png file','*.png'),('jpg files','*.jpg')) # 파일 타입 설정

    # 파일을 선택할 수 있는 메서드(파일 타입)
    root_select_img=filedialog.askopenfilename(filetypes=img_filetypes)
    #Label(testwindow,text=root_select_img).pack() # 이미지 파일 경로 라벨

    select_img= ImageTk.PhotoImage(Image.open(root_select_img)) # 선택한 파일의 경로

    if select_img_label is not None:
        select_img_label.destroy()

    select_img_label=Label(image=select_img).pack() # 라벨애 표시



select_img_chg=tk.Button(testwindow,text='이미지 열기', command=openFile).pack()
testwindow.mainloop()
