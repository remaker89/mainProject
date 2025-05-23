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
testwindow.geometry("1000x900") # window의 크기지정
testwindow.resizable(True,True) # window의 창의 크기 조절

select_img_label=None # 선탟한 이미지의 라벨 변수
select_img=None # 선택한 이미지 변수
saved_img=None

def openFile(): # 파일 여는 함수
    global select_img,select_img_label
    img_filetypes=(('png file','*.png'),('jpg files','*.jpg')) # 파일 타입 설정

    # 파일을 선택할 수 있는 메서드(파일 타입)
    root_select_img=filedialog.askopenfilename(filetypes=img_filetypes)
    Label(testwindow,text=root_select_img).pack() # 이미지 파일 경로 라벨

    #print(type(root_select_img))

    select_img1=cv2.imread(root_select_img)
    print(type(select_img1))
    # opencv로 직접 처리가 가능하지만 tkinter의 label에서 표시하기 위해 객체로 변환해야함
    select_img1 = cv2.cvtColor(select_img1, cv2.COLOR_BGR2RGB)
    select_img1=Image.fromarray(select_img1)
    select_img1=ImageTk.PhotoImage(select_img1)

    #select_img= ImageTk.PhotoImage(Image.open(root_select_img)) # 선택한 파일의 경로

    #기존의 선택된 이미지의 label을 제거
    if select_img_label is not None:
        select_img_label.destroy()

    # 어느 위치, 어떤 이미지등의 속성들을 선언
    select_img_label=Label(left_frame,image=select_img1) # 라벨에 표시, 왼쪽 프레임에 이미지를 생성
    select_img_label.image = select_img1
    # 어느위치에 배치할건지
    select_img_label.pack()


def save_img(): # 이미지 저장하는 함수
    global saved_img
    img_filetypes = (('png file', '*.png'), ('jpg files', '*.jpg'))

    if saved_img is None:
        return

    img_path=filedialog.askopenfilename(filetypes=img_filetypes)

    if img_path:
        saved_img.save(img_path)


def fram(testwindow): # 프레임 생성
    global top_frame,down_frame,left_frame,right_frame

    down_frame=tk.Frame(testwindow,relief="sunken",bg='green')
    down_frame.pack(side="bottom",fill="x",expand=False,padx=20,pady=20)

    top_frame=tk.Frame(testwindow,relief="sunken",bg='black')
    top_frame.pack(side="top",fill="both",expand=True)

    left_frame=tk.Frame(top_frame,relief="solid",bg='red')
    left_frame.pack(side="left",fill="both",expand=True,padx=20,pady=20)

    right_frame = tk.Frame(top_frame, relief="solid", bg='blue')
    right_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    return down_frame, top_frame,left_frame,right_frame

down_frame,top_frame,left_frame,right_frame=fram(testwindow)

select_img_chg=tk.Button(right_frame,text='이미지 열기', command=openFile).pack()
select_img_download=tk.Button(right_frame,text='이미지 저장하기', command=openFile).pack()
testwindow.mainloop()
