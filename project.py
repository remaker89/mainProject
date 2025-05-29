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



## 다음에 구현하고 싶은거:  외적으로 꾸밀거 더 꾸미기 등등

import numpy as np,cv2
import random
import tkinter as tk
import math
# 파일 선택 창 생성하는 모듈
from tkinter import filedialog, Label,Canvas,Scale
from PIL import Image,ImageTk
from tkinter import ttk



testwindow=tk.Tk() # window 생성
testwindow.title('open file') # window 이름
testwindow.geometry("900x800") # window의 크기지정
testwindow.resizable(0,0) # window의 창의 크기 조절

select_img_label=None # 선탟한 이미지의 라벨 변수
blur_img_label=None
select_img=None

drawing = False  # 드래그 상태
ix, iy = -1, -1 # 시작 좌표
ex, ey = -1, -1
rect_id_list ,img_history,coord=[],[],[]
scale = 1.0
canvas = None
new_width, new_height, select_img1 ,image_on_canvas= None, None,None,None
path_label = None
intensity=121
#rect_id = None # canvas 사각형의 id

def openFile(): # 파일 여는 함수
    global select_img,select_img_label,canvas, scale,new_width, new_height,select_img1,path_label, image_on_canvas
    img_filetypes=(('png file','*.png'),('jpg files','*.jpg')) # 파일 타입 설정

    # 파일을 선택할 수 있는 메서드(파일 타입)
    root_select_img=filedialog.askopenfilename(filetypes=img_filetypes)

    if path_label is not None: # 경로 label이 비어있지 않으면 삭제하고 새로운 경로를 실행 시킴
        path_label.destroy()

        # 새로운 경로 라벨을 생성하고 저장
    path_label = Label(testwindow, text=root_select_img)
    path_label.pack()


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

    #for widget in left_frame.winfo_children():
        #widget.destroy() 이거 왜 들어가있냐

    # 새로운 Canvas 위에 이미지 배치
    canvas = Canvas(left_frame, width=new_width, height=new_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")

    # 프레임 가로의 중앙에 위치하도록 함
    image_on_canvas=canvas.create_image(0,0, anchor="nw", image=select_img1)
    canvas.image = select_img1
    # 마우스 이벤트 바인딩
    canvas.bind("<ButtonPress-1>", onmouse_down) # 마우스 누름
    canvas.bind("<B1-Motion>", onmouse_move) # 마우스 움직임
    canvas.bind("<ButtonRelease-1>", onmouse_up) # 마우스 때기


def onmouse_down(event): # 마우스를 클릭하면
    global drawing, ix,iy, rect_id, rect_id_list,coord
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



def onmouse_up(event): # 마우스 방향에 따른 사각형 그리기
    global drawing
    drawing = False
    tmp = [ix, iy, event.x, event.y]
    if iy>event.y:
        tmp = [ix, event.y,event.x, iy]
    if ix>event.x:
        tmp=[event.x,iy,ix,event.y]
    if iy>event.y and ix>event.x:
        tmp=[event.x, event.y,ix, iy ]
    coord.append(tmp)

def back_shape(event=None): # 가장 마지막에 그린 도형 삭제
    global rect_id_list,rect_id
    if rect_id_list:
        rect_id=rect_id_list.pop() # list의 마지막 id 삭제
        canvas.delete(rect_id) # id를 가진 도형 삭제



def update_intensity(val): # 트랙바 값 변경시에 실행됨
    global intensity
    # 값이 홀수의 제곱이 되야하기 때문에 강제로 홀수로 만들고 제곱을 시켜줌
    val=int(float(val)) # 새로 넣은 트랙바가 정수형을 뱉어내서 실수로 바꿔줌
    if val %2==0:
        val +=1

    intensity=max(int(val),1) **2


    #blur() # 이미지가 없을때 실행이 되어서 오류가 뜸


def blur(intensity): # 블러 처리
    global img_history,select_img,coord

    if select_img is None or len(coord)==0: # 이미지가 아직 열리지 않았으면
        return
    if (ix==-1 or iy==-1 or ex==-1 or ey==-1): # 사각형이 그려지지 않으면
        return
    blur_select_img = select_img.copy()
    #coords=[ix,iy,ex,ey] # 드래그한 사각형의 좌표
    data = [1 / intensity for _ in range(intensity)] # 마스크 원소 지정
    blur_mask = np.array(data, np.float32).reshape(int(math.sqrt(intensity)), int(math.sqrt(intensity))) # mask 크기에 행과 열 사이즈에 맞게 조절

    for i in coord:
        start_x, start_y, end_x, end_y = [int(c * (1/scale)) for c in i] # 기존 이미지의 좌표, 임시로 float형태를 int형으로 변환
        #print(coord)
        #print(scale)
        roi = blur_select_img[start_y:end_y, start_x:end_x]

        if roi.size==0:
            continue
        #print(start_x, start_y, end_x, end_y)
        #print(roi)
        #cv2.imshow("fuck",roi) # 브러처리한 부분
        # 플러 처리할 data, mask 설정
        blur_roi = pixel_blur(roi, blur_mask)

        blur_select_img[start_y:end_y, start_x:end_x] = blur_roi
    select_img = blur_select_img

    img_history.append(select_img)# 블러 씌운 이미지의 키값을 리스트에 저장
    print("img_history",img_history)
    update_blur_img(blur_select_img)

def pixel_blur(roi, mask): # 기존 filter 적용 방식보다 더 연산이 짧은 코드
    return cv2.filter2D(roi, -1, mask)


def return_img(): # 도저히 다시 돌아가는 법을 못찾아 그냥 이미지를 다시 덮어씌우기로 함
    global select_img, img_history
    if img_history:
        select_img=img_history[0].copy()
        select_img=img_history.clear() # history에 있는 정보 전체 지우기
        canvas.create_image(0,0, anchor="nw", image=select_img1)


def rotate_left(): # 왼쪽으로 90도 회전!
    # 선택된 이미지가 없으면 return
    global select_img,image_on_canvas,new_width, new_height,canvas
    if select_img is None:
        return
    #select_img = rotate_img(select_img,90)
    #print(canvas.winfo_height(),canvas.winfo_width())
    select_img = cv2.rotate(select_img,cv2.ROTATE_90_CLOCKWISE)
    #print(select_img.shape)
    canvas.config(width=round(select_img.shape[1]*scale), height=round(select_img.shape[0]*scale))
    #print(canvas.winfo_height(), canvas.winfo_width())
    update_blur_img(select_img)

def rotate_right(): # 왼쪽으로 90도 회전!
    # 선택된 이미지가 없으면 return
    global select_img
    if select_img is None:
        return

    # 이미지를 돌릴때 더 간결하게 한줄로 적을 수 있는 코드가 있었음
    #select_img = rotate_img(select_img,-90)

    select_img = cv2.rotate(select_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # print(select_img.shape)
    canvas.config(width=round(select_img.shape[1] * scale), height=round(select_img.shape[0] * scale))
    # print(canvas.winfo_height(), canvas.winfo_width())
    update_blur_img(select_img)

def update_blur_img(blur_select_img): # blur에서 blur 처리한 이미지를 컨버스 위에 보이게 함
    global blur_img_label, blur_img,rect_id_list, rect_id, new_width, new_height
    blur_img=blur_select_img
    blur_img_RGB = cv2.cvtColor(blur_select_img, cv2.COLOR_BGR2RGB)
    # resize 전처리가 PIL함수이므로 이 줄에 적용시켜줘야하는거였음!!!!!!!
    blur_img_PIL = Image.fromarray(blur_img_RGB).resize((round(blur_select_img.shape[1]*scale), round(blur_select_img.shape[0]*scale)), Image.Resampling.LANCZOS)
    blur_img1 = ImageTk.PhotoImage(blur_img_PIL)


    if blur_img_label is not None:
        blur_img_label.destroy()

    if rect_id_list:
        for i in rect_id_list:
            canvas.delete(i)  # id를 가진 도형 삭제
        rect_id_list.clear()

    canvas.create_image(0, 0, anchor="nw", image=blur_img1)
    canvas.image = blur_img1


def save_img_png(): # 이미지 저장하는 함수
    # 파일형식을 img_types에 추가
    img_filetypes = (('png file', '*.png'), ('jpg files', '*.jpg'))

    img_path=filedialog.asksaveasfilename(title="save image",filetypes=img_filetypes)
    print(type(blur_img))

    # 경로 + 파일 형식
    # 만약에 끝에 파일명이 적어져있지 않으면 경로를 추가해 줌, lower는 소문자로 바꿔줌(대문자 방지)
    if not img_path.lower().endswith(".png"):
        if img_path.lower().endswith(".jpg"):
            img_path = img_path[:-4]
        img_path=img_path+".png" # if img_filetypes =="*.png" else img_path+".jpg"

    if select_img is not None and img_path:
        if img_path.lower().endswith(".png"):
            img_path = img_path[:-4]
        cv2.imwrite(img_path,blur_img)

def save_img_jpg(): # 이미지 저장하는 함수
    # 파일형식을 img_types에 추가
    img_filetypes = (('png file', '*.png'), ('jpg files', '*.jpg'))

    img_path=filedialog.asksaveasfilename(title="save image",filetypes=img_filetypes)
    print(type(blur_img))

    # 경로 + 파일 형식
    if not img_path.lower().endswith(".jpg"):
        if img_path.lower().endswith(".png"):
            img_path = img_path[:-4]
        img_path=img_path+".jpg" # if img_filetypes =="*.png" else img_path+".jpg"

    if select_img is not None and img_path:
        cv2.imwrite(img_path,blur_img)

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

select_img_chg=ttk.Button(right_frame,text='이미지 열기', command=openFile).pack(pady=10)
select_img_download_png=ttk.Button(right_frame,text='PNG로 이미지 저장하기', command=save_img_png).pack(pady=10)
select_img_download_jpg=ttk.Button(right_frame,text='JPG로 이미지 저장하기', command=save_img_jpg).pack(pady=10)
rolate_img_left=ttk.Button(right_frame,text='왼쪽으로 회전', command=rotate_left).pack(pady=10)
rolate_img_right=ttk.Button(right_frame,text='오른쪽으로 회전', command=rotate_right).pack(pady=10)
back=ttk.Button(right_frame,text="전으로 돌아가기", command=back_shape).pack(pady=10)
return_btn=ttk.Button(right_frame, text='처음 이미지로 돌아가기',command=return_img).pack(pady=10)
blur_img=ttk.Button(right_frame,text="블러 적용",command=lambda: blur(intensity)).pack(pady=10)


# 위치, 최소값, 최대밗, 수평 슬라이더, 트랙바 이름, 적용할 함수
intensity_slider = ttk.Scale(down_frame, from_=1, to=50, orient="horizontal", command=update_intensity,length=300)
intensity_slider.pack(side='left', padx=10,pady=10)  # 아래 프레임에 추가
intensity_slider.set(20)



def get_frame_size(): # 왼쪽 프레임 크기 확인
    print(f"Frame 크기: {left_frame.winfo_width()} x {left_frame.winfo_height()}")

testwindow.after(100, get_frame_size)  # 100ms 후 크기 확인

# Create a style
style = ttk.Style(testwindow)

# Import the tcl file
testwindow.tk.call("source", "theme/forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")


testwindow.mainloop()

'''
def rotate_img(image,angle): # 이미지 회전 기능
    h,w=image.shape[:2] # 이미지의 높이와 너비
    center=(w//2,h//2) # 회전할 중심 좌표
    matrix=cv2.getRotationMatrix2D(center, angle,1.0) # 원본 크기를 유지하면서 angle만큼 center를 기준으로 해서 회전함
    rotated=cv2.warpAffine(image,matrix,(w,h)) # 회전한 이미지를 생성
    return rotated # rotate_left, right에서 활용됨
    '''