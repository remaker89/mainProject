### 간단한 이미지 모자이크 도구
## 개요
from string import whitespace

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
import random
import tkinter as tk
import math
# 파일 선택 창 생성하는 모듈
from tkinter import filedialog, Label,Canvas
from PIL import Image,ImageTk


testwindow=tk.Tk() # window 생성
testwindow.title('open file') # window 이름
testwindow.geometry("900x800") # window의 크기지정
testwindow.resizable(0,0) # window의 창의 크기 조절

select_img_label=None # 선탟한 이미지의 라벨 변수
select_img=None
drawing = False  # 드래그 상태
ix, iy = -1, -1 # 시작 좌표
ex, ey = -1, -1
rect_id_list =[]
img_history=[]
scale=1,1
#rect_id = None # canvas 사각형의 id

def openFile(): # 파일 여는 함수
    global select_img,select_img_label,canvas, scale
    img_filetypes=(('png file','*.png'),('jpg files','*.jpg')) # 파일 타입 설정

    # 파일을 선택할 수 있는 메서드(파일 타입)
    root_select_img=filedialog.askopenfilename(filetypes=img_filetypes)
    Label(testwindow,text=root_select_img).pack() # 이미지 파일 경로 라벨

    #print(type(root_select_img))
    select_img=cv2.imread(root_select_img)
    #print(type(select_img))
    # opencv로 직접 처리가 가능하지만 tkinter의 label에서 표시하기 위해 객체로 변환해야함
    select_img_RGB = cv2.cvtColor(select_img, cv2.COLOR_BGR2RGB)
    select_img_PIL=Image.fromarray(select_img_RGB) #PIL변환
    #select_img_PIL.thumbnail((400,400))
    select_img1=ImageTk.PhotoImage(select_img_PIL)

    #select_img= ImageTk.PhotoImage(Image.open(root_select_img)) # 선택한 파일의 경로

    #기존의 선택된 이미지의 label을 제거
    if select_img_label is not None:
        select_img_label.destroy()

    # 어느 위치, 어떤 이미지등의 속성들을 선언
    select_img_label=Label(left_frame,image=select_img1) # 라벨에 표시, 왼쪽 프레임에 이미지를 생성
    select_img_label.image = select_img1
    # 어느위치에 배치할건지
    #select_img_label.pack()


    # 이미지와 프레임 크기를 계산
    img_width, img_height = select_img_PIL.size
    frame_width,frame_height=560,719
    scale = min(frame_width / img_width, frame_height / img_height)
    # 계산된 비율을 사용해 이미지의 크기를 다시 설정
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    # 이미지를 새 크기로 조절
    resized_img = select_img_PIL.resize((new_width, new_height), Image.Resampling.LANCZOS)
    select_img1 = ImageTk.PhotoImage(resized_img)

    for widget in left_frame.winfo_children():
        widget.destroy()

    # 새로운 Canvas 위에 이미지 배치
    canvas = Canvas(left_frame, width=new_width, height=new_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")

    # 프레임 가로의 중앙에 위치하도록 함
    canvas.create_image(0,0, anchor="nw", image=select_img1)
    canvas.image = select_img1
    # 마우스 이벤트 바인딩
    canvas.bind("<ButtonPress-1>", onmouse_down) # 마우스 누름
    canvas.bind("<B1-Motion>", onmouse_move) # 마우스 움직임
    canvas.bind("<ButtonRelease-1>", onmouse_up) # 마우스 때기


def onmouse_down(event): # 마우스를 클릭하면
    global drawing, ix,iy, rect_id, rect_id_list
    drawing=True
    ix,iy=event.x,event.y

    random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF)) # 랜덤한 컬러 적용
    # id의 위치를 확인하고 사각형의 형태로 그림
    rect_id = canvas.create_rectangle(ix, iy, event.x, event.y,fill=random_color, outline='white', width=2)
    rect_id_list.append(rect_id) # list에 rect_id를 저장
    #print(rect_id_list)


def onmouse_move(event):
    global rect_id,canvas,ex,ey

    ex = event.x
    ey = event.y
    canvas.coords(rect_id, ix, iy, event.x, event.y)


def onmouse_up(event):
    global drawing
    drawing = False


def back_shape(event=None): # 가장 마지막에 그린 도형 삭제
    global rect_id_list,rect_id
    if rect_id_list:
        rect_id=rect_id_list.pop() # list의 마지막 id 삭제
        canvas.delete(rect_id) # id를 가진 도형 삭제


def blur():
    global img_history,select_img
    intensity = 121
    coords=[ix,iy,ex,ey] # 드래그한 사각형의 좌표
    blur_select_img = select_img
    start_x, start_y, end_x, end_y = [int(c * scale) for c in coords] # 기존 이미지의 좌표, 임시로 float형태를 int형으로 변환
    print(scale)
    roi = blur_select_img[start_y:end_y, start_x:end_x]
    cv2.imshow("fuck",roi)
    I = intensity
    # 플러 처리할 data, mask 설정
    data = [1 / I for _ in range(I)]
    blur_mask = np.array(data, np.float32).reshape(int(math.sqrt(I)), int(math.sqrt(I)))
    blur_roi = pixel_blur(roi, blur_mask)

    blur_select_img[start_y:end_y, start_x:end_x] = blur_roi
    select_img = blur_select_img

    img_key_value = blur_select_img
    img_history.append(img_key_value)
    print(img_history)
    return blur_select_img

def pixel_blur(select_img, mask): # 기존 filter 적용 방식보다 더 연산이 짧은 코드
    return cv2.filter2D(select_img, -1, mask)


def save_img(): # 이미지 저장하는 함수
    img_types = []
    # 파일형식을 img_types에 추가
    img_filetypes = (('png file', '*.png'), ('jpg files', '*.jpg'))

    img_path=filedialog.asksaveasfilename(title="save image",filetypes=img_filetypes)
    print(type(select_img))

    # 경로 + 파일 형식
    img_path=img_path+".png" # if img_filetypes =="*.png" else img_path+".jpg"

    if select_img is not None and img_path:
        cv2.imwrite(img_path,select_img)

def fram(testwindow): # 프레임 생성
    global top_frame,down_frame,left_frame,right_frame

    down_frame=tk.Frame(testwindow,relief="sunken",bg='green')
    down_frame.pack(side="bottom",fill="x",expand=False,padx=20,pady=20)

    top_frame=tk.Frame(testwindow,relief="sunken",bg='black')
    top_frame.pack(side="top",fill="both",expand=True)

    left_frame=tk.Frame(top_frame,width=400,height=400,relief="solid")
    left_frame.pack(side="left",fill="both",expand=True,padx=20,pady=20)

    right_frame = tk.Frame(top_frame,width=300,height=100, relief="solid")
    right_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    return down_frame, top_frame,left_frame,right_frame

down_frame,top_frame,left_frame,right_frame=fram(testwindow)
data=[1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9]
mask=np.array(data,np.float32).reshape(3,3)

select_img_chg=tk.Button(right_frame,text='이미지 열기', command=openFile).pack()
select_img_download=tk.Button(right_frame,text='이미지 저장하기', command=save_img).pack()
back=tk.Button(right_frame,text="전으로 돌아가기", command=back_shape).pack()
blur_img=tk.Button(right_frame,text="블러 적용",command=blur).pack()


''''''
def get_frame_size(): # 왼쪽 프레임 크기 확인
    print(f"Frame 크기: {left_frame.winfo_width()} x {left_frame.winfo_height()}")

testwindow.after(100, get_frame_size)  # 100ms 후 크기 확인

testwindow.mainloop()
