#GUI 관련
from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import simpledialog
from tkinter.filedialog import *
from tkinter.simpledialog import *
from PIL import Image, ImageTk

#이미지 처리 관련 외부 라이브러리 불러오기
import cv2

#제작한 이미지 처리 함수 불러오기
from imgprocess import Img_pross

#GUI 관련 기능구현
class Img_edit():
    window = Tk() 

    canvas=None

    src=None
    
    height=None
    width=None
    channel=None

    drag_x=None
    drag_y=None
    drag_x1=None
    drag_y1=None

    src_before=[]
    src_orig=None


    main_col=(0,0,0)
    
    radio_var=IntVar()
    box_col="#000000"

    img=None

    def displayImage(self):
        # 기존에 canvas 에 출력한 그림이 있으면 삭제
        if self.canvas != None:
            self.canvas.destroy()

        self.canvas=Canvas(self.window,width=self.width, height=self.height)

        self.img=self.src
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.img = ImageTk.PhotoImage(image=self.img)

        self.canvas.create_image(0, 0, image=self.img, anchor=NW)
        self.canvas.pack(anchor=CENTER)

    # 파일 열기
    def func_open(self):
        readFp = askopenfilename(parent=self.window, filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*"
        ".png;*.tif;*.gif"),("모든 파일","*.*")))
        if readFp=="":
            return
        self.src = cv2.imread(readFp)
        self.height, self.width, self.channel = self.src.shape
        
        self.src_orig=self.src.copy()

        #가로 세로 900px 이상의 이미지를 열 경우 이미지를 강제로 리사이즈 하도록
        if self.height>900 or self.width>900:
            messagebox.showerror("에러","가로 900px, 세로 900px 이하로 이미지가 조정됩니다")
            if self.height==self.width:
                h=900
                w=900
            elif self.height>self.width:
                h=900
                w=900*self.width/self.height
            elif self.height<self.width:
                h=900*self.height/self.width
                w=900
                
            copy_img=Img_pross.img_resize(self.src,self.height, self.width, self.channel, int(h),int(w))
            self.src=copy_img
            self.height, self.width, self.channel = self.src.shape
            self.displayImage()

            return

        self.displayImage()

    # 파일 저장
    def func_save(self):
        photo=self.src
        # 저장할 이미지가 없으면 함수를 그냥 종료
        if photo is None:
            return  

        saveFp = asksaveasfile(parent= self.window, mode='w', defaultextension='.jpg',filetypes=(("JPG 파일", "*.jpg;*.jpeg"),("모든파일","*.*")))

        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        photo = Image.fromarray(photo)
        photo.save(saveFp.name)

    # 프로그램 종료
    def func_exit(self):
        exit()

    #이미지 리사이즈
    def img_resize(self):

        if self.canvas is None:
            return

        self.work_save()

        resize_gui=Toplevel(self.window)
        resize_gui.title("이미지 리사이즈 크기 입력")
        Label(resize_gui,text="세로").grid(row=1, column=2)
        Label(resize_gui,text="가로").grid(row=2, column=2)
        Label(resize_gui).grid(row=4, column=4)
        Label(resize_gui).grid(row=0, column=0)

        entry_h=Entry(resize_gui)
        entry_v=Entry(resize_gui)
        entry_h.grid(row=1, column=3)
        entry_v.grid(row=2, column=3)

        def close_resize_gui():
            h=int(entry_h.get())
            w=int(entry_v.get())

            if h>900 or w>900:
                messagebox.showerror("에러","가로 900px, 세로 900px 이하의 값을 입력해주세요!")
                resize_gui.withdraw()
                return

            copy_img=Img_pross.img_resize(self.src,self.height, self.width, self.channel, h,w)

            self.src=copy_img
            self.height, self.width, self.channel = self.src.shape
            self.displayImage()
            resize_gui.withdraw()

        resize_gui_ok=Button(resize_gui,text="확인", command=close_resize_gui)
        resize_gui_ok.grid(row=3, column=2, columnspan=4)
        resize_gui.mainloop()
        
    # 이미지 상하반전
    def func_mirror1(self):

        copy_img=Img_pross.img_mirror_up_to_down(self.src,self.height, self.width,self.channel)

        self.work_save()
        self.src=copy_img
        self.displayImage()

    # 이미지 좌우반전
    def func_mirror2(self):
        
        copy_img=Img_pross.img_mirror_left_to_right(self.src,self.height, self.width,self.channel)

        self.work_save()
        self.src=copy_img
        self.displayImage()
    #90도 회전
    def func_rotate90(self):
        copy_img=Img_pross.img_rotate90(self.src,self.height, self.width,self.channel)
        self.work_save()
        self.src=copy_img
        self.height, self.width,self.channel=self.src.shape
        self.displayImage()

    # 이미지 회전
    def func_rotate(self):

        ch=simpledialog.askinteger("회전 각도 입력","회전 각도를 입력해주세요")
        copy_img=Img_pross.img_rotate(self.src, self.height, self.width, self.channel, ch)

        self.work_save()
        self.src=copy_img
        self.height, self.width,self.channel=self.src.shape
        self.displayImage()

    # 이미지를 밝게
    def func_bright(self):
        copy_img = Img_pross.img_lighter(self.src, self.height, self.width, self.channel)

        self.work_save()
        self.src=copy_img
        self.displayImage()

    # 이미지를 어둡게 하는 기능
    def func_dark(self):
        copy_img = Img_pross.img_darker(self.src, self.height, self.width, self.channel)
        self.work_save()
        self.src=copy_img
        self.displayImage()

    # 이미지를 흐리게
    def func_blur(self):
        copy_img = Img_pross.img_blur(self.src, self.height, self.width, self.channel)

        self.work_save()
        self.src=copy_img
        self.displayImage()

    # 선명하게
    def func_sharpen(self):
        self.work_save()
        self.src=Img_pross.img_sharpen(self.src, self.height, self.width, self.channel)
        self.displayImage()

    # 그레이 스케일
    def func_grey(self):
        copy_img=Img_pross.img_grayscale(self.src, self.height, self.width, self.channel)
        self.work_save()
        self.src=copy_img
        self.displayImage()

    # 흑백
    def func_bw(self):
        copy_img=Img_pross.img_bw(self.src, self.height, self.width, self.channel)

        self.work_save()
        self.src=copy_img
        self.displayImage()

    # 기본 커서
    def normal_state(self):
        if self.radio_var.get()!=0:
            return
        self.window.config(cursor="arrow")

    # 브러쉬 기능
    def brush_bind(self):
        if self.radio_var.get()!=1:
            return
            #work_save()
        self.window.config(cursor="pencil")
        self.canvas.bind("<B1-Motion>",self.draw_circle)
        self.window.after(1, self.brush_bind)
        return

    def draw_circle(self,event):
        cv2.circle(self.src,(event.x,event.y),5,self.main_col,-1)
        self.displayImage()
        return

    #자르기 기능
    drag_x=None
    drag_y=None
    drag_x1=None
    drag_y1=None
    def crop_bind(self):
        if self.radio_var.get()==2:
            self.window.config(cursor="crosshair")
            self.canvas.bind("<Button-1>",self.draw_crop_start)
            self.window.after(1, self.crop_bind)

        #드래그 시작지점
    def draw_crop_start(self, event):
        self.drag_x,self.drag_y=event.x,event.y
        self.canvas.bind("<ButtonRelease-1>",self.draw_crop)

        #드래그 종료지점 및 실행여부 질문
    def draw_crop(self,event):
        self.work_save()
        self.drag_x1, self.drag_y1= event.x, event.y
        #마우스 그래그를 오른쪽상단->왼쪽하단으로 했을 경우
        if self.drag_x1<self.drag_x:
            temp=self.drag_x
            self.drag_x=self.drag_x1
            self.drag_x1=temp
        if self.drag_y1<self.drag_y:
            temp=self.drag_y
            self.drag_y=self.drag_y1
            self.drag_y1=temp
        self.canvas.create_rectangle(self.drag_x,self.drag_y,self.drag_x1,self.drag_y1,width=3)
        ask_crop=messagebox.askokcancel("자르기","이렇게 자르겠습니까?")

        #확인 후 이미지 자르기 실행
        if ask_crop==True:
            self.crop()

        self.displayImage()

        #실제 이미지 자르기 기능 구현
    def crop(self):
        photo = self.src[self.drag_y:self.drag_y1, self.drag_x: self.drag_x1]
        self.src=photo
        self.height, self.width, self.channel = self.src.shape
        return

    #작업 취소
        #브러쉬, 텍스트 기능에서는 동작하지 않음
    def work_cancel(self):
        try:
            self.src=self.src_before.pop()
            self.height, self.width, self.channel = self.src.shape
        except:
            return
        self.displayImage()

    #작업 취소 기능을 위해 이전 작업을 저장하는 기능
    def work_save(self):
        self.src_before+=[self.src]

    # 작업 초기화
    def clean_all(self):
        self.src=self.src_orig
        self.height, self.width, self.channel = self.src.shape
        self.displayImage()

    #글씨 넣기
    def bind_text(self):
        # if radio_var.get()==3:
            # canvas.bind("<ButtonRelease-1>",text_test)
        if self.radio_var.get()!=3:
            return
        self.window.config(cursor="crosshair")
        self.canvas.bind("<ButtonRelease-1>",self.text_in)
        self.window.after(1, self.bind_text)    

    count=0
    font_size=45
    def text_in(self,event):
        global frame_up
        #텍스트 입력 완료하지 않을 시 또 동작하지 않도록 카운터 설정
        if self.count==1:
            return
        self.count+=1
        
        events=event
        
        #텍스트 입력을 받는 엔트리 생성
        text_ent=Entry(self.window,width=10)
        pointx=self.window.winfo_pointerx() - self.window.winfo_rootx()
        pointy=self.window.winfo_pointery() - self.window.winfo_rooty()
        def make_ent(_text_ent):
            _text_ent.config(font=("arial", self.font_size))
            _text_ent.place(x=pointx, y=pointy)

        make_ent(text_ent)

        #동작 완료 시 이미지에 텍스트를 삽입하고 텍스트 입력용 엔트리를 삭제하는 기능
        def text_quit():
            self.work_save()
            self.count=0
            txt=text_ent.get()
            # img=cv2.putText(src,txt,(pointx,pointy),0,font_size,(0,0,0),2,cv2.LINE_AA)
            font = cv2.FONT_HERSHEY_DUPLEX
            fontsize=2
            fontcol=self.main_col
            cv2.putText(self.src, txt, (events.x,events.y+self.font_size), font, fontsize,fontcol, 2, cv2.LINE_AA)

            text_ent.place_forget()
            text_gui_ok.grid_forget()
            # text_gui_ok_discript.grid_forget()
            self.displayImage()
        
        # text_gui_ok_discript=Label(frame_up,text="텍스트 작성 완료 후 클릭 -> ")
        # text_gui_ok_discript.grid(column=0,row=1)
        text_gui_ok=Button(frame_up,text="확인", command=text_quit)
        text_gui_ok.grid(column=1,row=1)

    # 스포이드 기능
    def bind_spoid(self):
        self.window.config(cursor="crosshair")
        self.canvas.bind("<ButtonRelease-1>",self.spoid)
        # window.after(1, bind4)

    def spoid(self,event):
        global color_box
        # radio_var=0
        # if radio_var.get()!=4:
        #     return
        try:
            self.main_col = (int(self.src[event.y][event.x][0]),
            int(self.src[event.y][event.x][1]),
            int(self.src[event.y][event.x][2]))
        except:
            return
        # hex=""
        self.box_col=self.rgb_to_hex()
        color_box.config(bg=self.box_col)

    #rgb색상을 16비트 표기로 변환하는 기능
    def rgb_to_hex(self):
        hex=""
        hex+='#'
        if self.main_col[2]<10:
            hex+="0"
        hex+=format(self.main_col[2],'x')
        if self.main_col[1]<10:
            hex+="0"
        hex+=format(self.main_col[1],'x')
        if self.main_col[0]<10:
            hex+="0"
        hex+=format(self.main_col[0],'x')
        return hex

    #색상 선택 기능
    def col_sel(self):
        global color_box
        selcol=colorchooser.askcolor()
        if selcol==None:
            return
        self.main_col=(selcol[0][2],selcol[0][1],selcol[0][0])
        self.box_col=selcol[1]
        color_box.config(bg=self.box_col)

    #히스토그램 평활화
    def smooting(self):
        copy_img=Img_pross.hist_smooting(self.src, self.height, self.width, self.channel)
        
        self.work_save()
        self.src=copy_img
        self.displayImage()

    #채널조정
    def ctrl_chan(self):
        # self.work_save()
        ctrl_chan_gui=Toplevel(self.window)


        # def works(event):
        #     copy_img=Img_pross.img_ctrl_chan(self.src, self.height, self.width, self.channel, blue_bar.get(), green_bar.get(),red_bar.get() )
        #     self.src=copy_img
        #     self.displayImage()

        Label(ctrl_chan_gui,text="Red").grid(column=0, row=0)
        Label(ctrl_chan_gui,text="Green").grid(column=0, row=1)
        Label(ctrl_chan_gui,text="Blue").grid(column=0, row=2)

        red_bar=Scale(ctrl_chan_gui,showvalue=True,from_=-10, to=10,\
            resolution=1,orient="horizontal")
        green_bar=Scale(ctrl_chan_gui,showvalue=True,from_=-10, to=10,\
            resolution=1,orient="horizontal")
        blue_bar=Scale(ctrl_chan_gui,showvalue=True,from_=-10, to=10,\
            resolution=1,orient="horizontal")
        # red_bar=Scale(ctrl_chan_gui,showvalue=True, to=10,\
        #     resolution=1,command=works,orient="horizontal")
        # green_bar=Scale(ctrl_chan_gui,showvalue=True, to=10,\
        #     resolution=1,command=works,orient="horizontal")
        # blue_bar=Scale(ctrl_chan_gui,showvalue=True, to=10,\
        #     resolution=1,command=works,orient="horizontal")

        red_bar.grid(column=1, row=0)
        green_bar.grid(column=1, row=1)
        blue_bar.grid(column=1, row=2)


        def chan_ok():
            self.work_save()
            copy_img=Img_pross.img_ctrl_chan(self.src, self.height, self.width, self.channel, blue_bar.get(), green_bar.get(),red_bar.get() )
            self.src=copy_img
            ctrl_chan_gui.withdraw()
            self.displayImage()
            
        chan_ok_button=Button(ctrl_chan_gui,text="확인", command=chan_ok)
        chan_ok_button.grid(column=1, row=3, columnspan=2)

        ctrl_chan_gui.mainloop()
        self.work_cancel()

# GUI 구현 및 실행
play=Img_edit()
# 윈도우 생성
play.window.geometry("1200x900") 
# 윈도우 크기 설정
play.window.title("Photo Editor")
#윈도우 창 이름 설정

mainMenu = Menu(play.window) 
# 메뉴 생성
play.window.config(menu= mainMenu) 
# 윈도우의 메뉴를 mainMenu 로 설정

fileMenu = Menu(mainMenu, tearoff=False)
# add_cascade() 함수로 상위메뉴와 하위메뉴를 연결해줌
# 이미지 파일 관련 메뉴
mainMenu.add_cascade(label='파일', menu = fileMenu)
fileMenu.add_command(label='파일 열기', command=play.func_open)
fileMenu.add_command(label='파일 저장', command=play.func_save)
fileMenu.add_separator()
fileMenu.add_command(label='작업 취소', command=play.work_cancel)
fileMenu.add_command(label='전체 작업 초기화', command=play.clean_all)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=play.func_exit)

# 이미지 편집 관련 메뉴
image1Menu = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label='편집', menu=image1Menu)

image1Menu.add_command(label='이미지 크기 변환', command=play.img_resize)
image1Menu.add_separator()
image1Menu.add_command(label='상하 반전', command=play.func_mirror1)
image1Menu.add_command(label='좌우 반전', command=play.func_mirror2)
image1Menu.add_command(label='시계방향으로 90도 회전', command=play.func_rotate90)
image1Menu.add_command(label='임의 회전', command=play.func_rotate)
image1Menu.add_separator()
image1Menu.add_command(label='밝게', command=play.func_bright)
image1Menu.add_command(label='어둡게', command=play.func_dark)
image1Menu.add_separator()
image1Menu.add_command(label='흐리게', command=play.func_blur)
image1Menu.add_command(label='선명하게', command=play.func_sharpen)
image1Menu.add_separator()
image1Menu.add_command(label='그레이스케일', command=play.func_grey)
image1Menu.add_command(label='흑백', command=play.func_bw)
image1Menu.add_separator()
image1Menu.add_command(label='히스토그램 평활화', command=play.smooting)
image1Menu.add_command(label='채널 조정', command=play.ctrl_chan)

#왼쪽 사이드 메뉴

#왼쪽 프레임
frame_left=Frame()

bw=7
bh=3
#기본 버튼
radio0=Radiobutton(frame_left,text="Cursor",command=play.normal_state, value=0,variable=play.radio_var, indicatoron=0,width=bw,height=bh)
radio0.pack()

#브러쉬 버튼
radio1=Radiobutton(frame_left,text="Brush", command=play.brush_bind, value=1, variable=play.radio_var, indicatoron=0,width=bw,height=bh)
radio1.pack()

#자르기 버튼
radio2=Radiobutton(frame_left,text="Crop",command=play.crop_bind, value=2, variable=play.radio_var, indicatoron=0,width=bw,height=bh)
radio2.pack()

#텍스트 버튼
radio3=Radiobutton(frame_left,text="Text",command=play.bind_text, value=3, variable=play.radio_var, indicatoron=0,width=bw,height=bh)
# radio3=Button(frame_left,text="Text",command=bind3)
radio3.pack()


#스포이드 버튼
radio4=Radiobutton(frame_left, text="Spoid", command=play.bind_spoid, value=4, variable=play.radio_var, indicatoron=0,width=bw,height=bh)
radio4.pack()


#색상 표시 버튼 설명 라벨
col_lab=Label(frame_left,text="Color" ,width=bw,height=bh)
col_lab.pack()

#색상 표시 버튼
color_box=Button(frame_left,bg=play.box_col,command=play.col_sel,relief="sunken", width=bw,height=bh)
color_box.pack()

frame_left.pack(side="left")

#상단메뉴 프레임
frame_up=Frame()
frame_up.pack(side="top")

play.window.mainloop()