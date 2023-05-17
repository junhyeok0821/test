import time as t
from tkinter  import *
import threading
import random
import math
#윈도우 크기
w=900
h=600
#상단 버튼 선택프레임 좌표
sx=0            
sy=0
ex=130
ey=130         

#제한시간
time=60       

#점수
highscore=0
score=0    

makeCode=""
goalCode="goal"
class Game():
    def __init__(self):     #게임화면 셋팅
        self.window=Tk()
        self.window.title("Hamburger")
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.window.resizable(False, False)
        #게임화면
        self.gameCnvs=Canvas(self.window, bd=2,bg="white") 
        self.gameCnvs.pack(fill="both", expand=True)
        #게임 셋팅
        self.set()
        #첫 화면  
        self.sTi=PhotoImage(file="img\배경화면3.png")
        self.startCnvs=Canvas(self.gameCnvs,width=900,height=700,bd=0,bg="brown")  
        self.gameCnvs.create_window(w/2,h/2,window=self.startCnvs,tags="startCnvs")       
        self.startCnvs.create_image(450,350,image=self.sTi)
        #self.startCnvs.place(x=0,y=-50)
        btn1=Button(self.startCnvs, text="Game Start!",bg="red",font=("빙그레 싸만코체",20,"bold"),command=self.startMotion)
        btn1.place(x=375,y=500)

        self.window.bind('<KeyPress>',self.key)    
        self.window.mainloop()
        
    #첫 시작
    def start(self):    
        global goalCode  #게임화면 전환
        self.goalImg=random.choice(list(self.goal.keys()))                   #목표햄버거 이미지 선택
        self.hambCnvs.create_image(110,120,image=self.goalImg,tags="img")    #캔버스에 그리기
        goalCode=self.goal.get(self.goalImg)            #목표햄버거 코드값 가져오기
        self.th1 = threading.Thread(target=self.get_Goal)
        self.timerOn()
    #재시작시  
    def restart(self):
        global goalCode
        self.resultCnvs.destroy()
        self.countStart()
    
    #첫화면 올리고 카운트
    def startMotion(self):
        for x in range(10) :
            self.gameCnvs.move("startCnvs",0,5)
            t.sleep(0.01)
            self.window.update()
        for x in range(35) :
            self.gameCnvs.move("startCnvs",0,-30-x*20)
            t.sleep(0.01)
            self.window.update()
        self.startCnvs.destroy()
        self.countStart()

    #3초카운트 후 시작
    def countStart(self):
        global makeCode
        self.scoreStr="최고점수:{0}🍔"" 현재점수:{1}🍟".format(str(highscore),str(score))
        self.scoreLb.config(text=self.scoreStr)
        self.countImg=[PhotoImage(file="img\시작3.png"),PhotoImage(file="img\시작2.png"),PhotoImage(file="img\시작1.png"),PhotoImage(file="img\\start.png")]
        for i in range(3): #카운트 다운
            self.hambCnvs.delete("all")
            tagStr="count"
            self.hambCnvs.create_image(-30,110,image=self.countImg[i],tags=tagStr)
            for x in range(20):
                self.hambCnvs.move(tagStr,7,0)
                t.sleep(0.02)
                self.window.update()
            for o in range(60):
                self.window.update()
                t.sleep(0.01)
            self.hambCnvs.delete("all")
        self.hambCnvs.create_image(100,120,image=self.countImg[3],tags=tagStr) #start!! 이미지
        for o in range(100):#start!! 이후 1초 쉬고 시작
                self.window.update()
                t.sleep(0.01)
        self.hambCnvs.delete("all")
        self.buttonUnlock()
        self.start()
        
    #모든 버튼,라벨,캔버스,이미지 로딩 및 세팅
    def set(self):

        #상단 라벨 이미지
        self.topPatty = PhotoImage(file = "img\상단패티.png")
        self.topCheese = PhotoImage(file = "img\상단치즈.png")
        self.topTomato = PhotoImage(file = "img\상단토마토.png")
        self.topLettuce = PhotoImage(file = "img\상단양상추.png")
        self.topUpsideBread = PhotoImage(file = "img\상단위빵.png")
        self.topDownsideBread = PhotoImage(file = "img\상단아래빵.png")

        #메이킹 라벨 이미지
        self.UpsideBread=PhotoImage(file="img\위빵.png")
        self.patty=PhotoImage(file="img\패티.png")
        self.cheese=PhotoImage(file="img\치즈.png")
        self.lettuce=PhotoImage(file="img\양상추.png")
        self.downBread=PhotoImage(file="img\아래빵.png")
        self.tomato=PhotoImage(file="img\토마토.png")
        self.dish=PhotoImage(file="img\접시.png")

        global goalCode 
        self.bgImg = PhotoImage(file ="img\\배경화면2.png")
        self.gameCnvs.create_image(450,300,image=self.bgImg,)

        self.selectCnvs=Canvas(self.gameCnvs,bd=1,bg="pink")        #상단 라벨프레임
        self.selectCnvs.place(x=150,y=20)


        self.makeCnvs=Canvas(self.gameCnvs,bd=0,width=390,height=280,bg="orange")  #메이킹 라벨
        self.makeCnvs.place(x=150,y=290)
        self.makeY = 0  # 메이킹 라벨 재료들의 그려지는 위치 (250-makeY)
        self.make(self.dish,"")

        self.seleftF = self.selectCnvs.create_rectangle(sx,sy,ex,ey, fill="blue") #상단 버튼 셀렉프레임모양
        

        #버튼세팅
        self.upBreadBtn=Button(self.selectCnvs,bg="red",image=self.topUpsideBread,width=100,height=100,highlightcolor="black", bd=5,command=lambda:self.click("upB"))#,activebackground="blue"
        self.upBreadBtn.grid(row=0,column=0,padx=10,pady=10)

        self.pattyBtn=Button(self.selectCnvs,bg="orange",image=self.topPatty,width=100,height=100,bd=5,repeatdelay=1000,repeatinterval=100,command=lambda:self.click("patty"))
        self.pattyBtn.grid(row=0,column=1,padx=5,pady=5)

        self.cheeseBtn=Button(self.selectCnvs,bg="blue",image=self.topCheese,width=100,height=100, bd=5,command=lambda:self.click("cheese"))
        self.cheeseBtn.grid(row=0,column=2,padx=10,pady=10)

        self.lettuceBtn=Button(self.selectCnvs,bg="green",image=self.topLettuce,width=100,height=100, bd=5,command=lambda:self.click("lettuce"))
        self.lettuceBtn.grid(row=1,column=2,padx=5,pady=5)

        self.tomatoBtn=Button(self.selectCnvs,bg="red",image=self.topTomato,width=100,height=100,bd=5,command=lambda:self.click("tomato"))
        self.tomatoBtn.grid(row=1,column=1,padx=10,pady=10)

        self.downBreadBtn=Button(self.selectCnvs,bg="purple",image=self.topDownsideBread,width=100,height=100, bd=5,command=lambda:self.click("downB"))
        self.downBreadBtn.grid(row=1,column=0,padx=5,pady=5)

        #버튼 첫 포커스 및 락
        self.upBreadBtn.focus_set()
        self.buttonLock()
        
        #점수 라벨
        global score
        global highscore
        self.f= "빙그레 싸만코체"
        self.scoreStr="최고점수:{0}🍔"" 현재점수:{1}🍟".format(str(highscore),str(score))
        self.scoreLb=Label(self.gameCnvs,text=self.scoreStr,bg="white",font=(self.f,20,"bold"))
        self.scoreLb.place(x=590,y=505)

        #목표 햄버거 이미지 
        self.goalImg1=PhotoImage(file="img\두열스버거dbtlcpcltub.png")
        self.goalImg2=PhotoImage(file="img\준협스빠더버거dbpctdbpcltub.png")
        self.goalImg3=PhotoImage(file="img\치영스띠드버거dbclclclcub.png")
        self.goalImg4=PhotoImage(file="img\희진스빅맥버거dbpplctdbpplctub.png")
        self.goalImg5=PhotoImage(file="img\동현스준석버거dbcpcdbpctlpdbltub.png")
        self.goalImg6=PhotoImage(file="img\민규버거dbptcptplub.png")
        self.goalImg7=PhotoImage(file="img\가연스줄라이선샤인두잇두잇핫섬머디스이즈코스모버거dbppptllccptlub.png")
        self.goalImg8=PhotoImage(file="img\최스버거dbpcpcpcpctlub.png")
        self.goalImg9=PhotoImage(file="img\정구트리플패티버거dbpttllccppltub.png")
        self.goalImg10=PhotoImage(file="img\주희스탄불버거dbltltpplub.png")
        self.goalImg11=PhotoImage(file="img\현주스내장파괴버거dbclptlpcdbptcltub.png")
        self.goalImg12=PhotoImage(file="img\학수스버거dbctltcpub.png")
        self.goalImg13=PhotoImage(file="img\준석스비건버거dbtlctllcttlctlub.png")

        #goal dict에 목표 햄버거 이미지와 정답코드 입력
        self.goal={self.goalImg1:"dbtlcpcltub",self.goalImg2:"dbpctdbpcltub",self.goalImg3:"dbclclclcub"
        ,self.goalImg4:"dbpplctdbpplctub",self.goalImg5:"dbcpcdbpctlpdbltub",self.goalImg6:"dbptcptplub"
        ,self.goalImg7:"dbppptllccptlub",self.goalImg8:"dbpcpcpcpctlub",self.goalImg9:"dbpttllccppltub"
        ,self.goalImg10:"dbltltpplub",self.goalImg11:"dbclptlpcdbptcltub",self.goalImg12:"dbctltcpub"
        ,self.goalImg13:"dbtlctllcttlctlub"}
        
        #목표 햄버거캔버스
        self.hambCnvs=Canvas(self.gameCnvs,bg="black",width=220,height=210)
        self.hambCnvs.place(x=620,y=50)
        
        #타이머 캔버스
        self.timeCnvs=Canvas(self.gameCnvs,bg="black",width=220,height=50)
        self.timeCnvs.place(x=620,y=270)
        self.yN=[]
        self.rN=[]
        for i in range(10):
            fileY="img\\num\\YN"+str(i)+".png"
            yImg=PhotoImage(file=fileY)
            self.yN.append(yImg)
            fileR="img\\num\\RN"+str(i)+".png"
            rImg=PhotoImage(file=fileR)
            self.rN.append(rImg)
        self.yC=PhotoImage(file="img\\num\\YC.png")
        self.rC=PhotoImage(file="img\\num\\RC.png")
        self.timeCnvs.create_image(40,27.5,image=self.yN[0],tags="t1")
        self.timeCnvs.create_image(80,27.5,image=self.yN[0],tags="t2")
        self.timeCnvs.create_image(115,27.5,image=self.yC,tags="t3")
        self.timeCnvs.create_image(150,27.5,image=self.yN[0],tags="t4")
        self.timeCnvs.create_image(190,27.5,image=self.yN[0],tags="t5")
        
        #종료 캔버스
        self.lbImg=PhotoImage(file="img\\burger2.png")
        self.resultCnvs=Canvas(self.makeCnvs,bd=0,bg="orange",highlightbackground="orange",width=400,height=410)
        self.resultCnvs.create_image(200,200,image=self.lbImg)
        self.restartBtn=Button(self.resultCnvs,text="Restart",command=self.restart,font=("빙그레 싸만코체",20,"bold"),bg="orange")
        self.restartBtn.place(x=145,y=280)
        endStr="Game Over "
        self.resultCnvs.create_text(205,180,text=endStr,font=("빙그레 싸만코체",50,"bold"),fill="black")
    
    #타이머 초기화 및 타이머 시작
    def timerOn(self):
        self.startT=round(t.time(),2)
        self.runT=round(t.time(),2)
        self.timeCnvs.create_image(40,27.5,image=self.yN[6],tags="t1")
        self.timeCnvs.create_image(80,27.5,image=self.yN[0],tags="t2")
        self.timeCnvs.create_image(115,27.5,image=self.yC,tags="t3")
        self.timeCnvs.create_image(150,27.5,image=self.yN[0],tags="t4")
        self.timeCnvs.create_image(190,27.5,image=self.yN[0],tags="t5")
        #60초 동안 타이머 시작
        while self.runT-self.startT<60:
            self.runT=round(t.time(),2)
            self.timeCnvs.delete("all")
            i =(round(60-(self.runT-self.startT),2))
            self.timeSet(i)
            t.sleep(0.001)
            self.window.update()
        #타이머 종료후 게임 종료
        self.endGame()
     
     #타이머
    def timeSet(self,i):
            i10=math.trunc(i/10)                #남은시간 10의 자리수
            i1=math.trunc(i-i10*10)             #남은시간 1의 자리수
            i_1=str(round(i-int(i),2))[2:3]     #남은시간 0.1의 자리수
            i__1=str(round(i-int(i),2))[3:4]    #남은시간 0.01의 자리수
            if i>10:
                self.timeCnvs.create_image(40,27.5,image=self.yN[i10],tags="t1")  
                self.timeCnvs.create_image(80,27.5,image=self.yN[i1],tags="t2") 
                self.timeCnvs.create_image(115,27.5,image=self.yC,tags="t3")
                self.timeCnvs.create_image(150,27.5,image=self.yN[int(i_1)],tags="t4")
                if i__1=="":self.timeCnvs.create_image(190,27.5,image=self.yN[0],tags="t5")
                else:self.timeCnvs.create_image(190,27.5,image=self.yN[int(i__1)],tags="t5")
            elif i<10:
                self.timeCnvs.create_image(40,27.5,image=self.rN[i10],tags="t1")  
                self.timeCnvs.create_image(80,27.5,image=self.rN[i1],tags="t2") 
                self.timeCnvs.create_image(115,27.5,image=self.rC,tags="t3")
                if i_1==".":self.timeCnvs.create_image(150,27.5,image=self.rN[0],tags="t4") #0초버그
                else:self.timeCnvs.create_image(150,27.5,image=self.rN[int(i_1)],tags="t4")
                if i__1=="":self.timeCnvs.create_image(190,27.5,image=self.rN[0],tags="t5")
                else:self.timeCnvs.create_image(190,27.5,image=self.rN[int(i__1)],tags="t5")
            
    #게임 종료
    def endGame(self):
        global score
        global highscore
        self.buttonLock()           #버튼 잠그기
        self.hambCnvs.delete("all") #목표캔버스 초기화
        self.makeInit()             #메이킹 캔버스 초기화
        self.makeCnvs.create_window(200,-190,window=self.resultCnvs,tags="resultCnvs")
        for x in range(33):         #거대햄버거 등장
            self.makeCnvs.move("resultCnvs",0,10)
            self.window.update()
            t.sleep(0.01)
        score=0 #현재스코어 초기화
   
    #메이킹 캔버스 초기화
    def makeInit(self):
        global makeCode
        self.makeCnvs.delete("all")
        self.makeY=0
        makeCode=""
        self.make(self.dish,"")

    #목표햄버거 리셋
    def get_Goal(self):
        global goalCode
        self.hambCnvs.move("img",30,0)
        self.goalImg=random.choice(list(self.goal.keys()))
        self.hambCnvs.create_image(-92,120,image=self.goalImg,tags="img2")
        goalCode=self.goal.get(self.goalImg)
        print("goalCode:",goalCode)                   
        for x in range(20):
            self.hambCnvs.move("img",15,0)
            self.hambCnvs.move("img2",10,0)
            t.sleep(0.02)

    #버튼 커맨드 지우고 3초뒤 endM2호출 하여 클리어
    def endM(self):        
        global makeCode
        global goalCode
        if makeCode==goalCode:
             self.correct()
        else: self.wrong()
        timer = threading.Timer(2, self.endM2)
        timer.start()
        #todo 정답과 비교
        #todo 클릭 잠그기
        self.buttonLock()

    #makeCnvs 를 지우고 버튼 커맨드 다시입력
    def endM2(self):           
        if self.runT-self.startT<60: #게임 종료 전
            self.th1.start()
            self.th1 = threading.Thread(target=self.get_Goal)
            self.buttonUnlock()
            self.makeInit()

    #버튼 잠그기
    def buttonLock(self):
        self.cheeseBtn['command']=""
        self.upBreadBtn['command']=""
        self.lettuceBtn['command']=""
        self.downBreadBtn['command']=""
        self.tomatoBtn['command']=""
        self.pattyBtn['command']=""

    #버튼 커맨드 
    def buttonUnlock(self):
        self.cheeseBtn['command']=lambda:self.click("cheese")
        self.upBreadBtn['command']=lambda:self.click("upB")
        self.lettuceBtn['command']=lambda:self.click("lettuce")
        self.downBreadBtn['command']=lambda:self.click("downB")
        self.tomatoBtn['command']=lambda:self.click("tomato")
        self.pattyBtn['command']=lambda:self.click("patty")

    #정답시
    def correct(self):
        global score
        global highscore
        self.corImg = PhotoImage(file="img\정답.png")
        self.makeCnvs.create_image(190,140,image=self.corImg)
        score+=1
        if score>highscore :
            highscore = score
        self.scoreStr="최고점수:{0}🍔"" 현재점수:{1}🍟".format(str(highscore),str(score))
        self.scoreLb.config(text=self.scoreStr)

    #오답시
    def wrong(self):
        self.wrongImg = PhotoImage(file="img\오답.png")
        self.makeCnvs.create_image(185,150,image=self.wrongImg)
    
    #각 버튼 클릭시 커맨드 분배
    def click(self,str):
        if str=="upB":self.make(self.UpsideBread,"ub")
        elif str=="cheese":self.make(self.cheese,"c")
        elif str=="patty":self.make(self.patty,"p")
        elif str=="downB":self.make(self.downBread,"db")
        elif str=="lettuce":self.make(self.lettuce,"l")
        elif str=="tomato":self.make(self.tomato,"t")

    #재료 쌓기
    def make(self,img,code):
        global makeCode
        self.makeCnvs.create_image(200 ,250-self.makeY,image=img)   
        self.makeY+=15  #재료 높이 올리기
        if img ==self.lettuce:
            self.makeY-=6    
        makeCode += code
        print("makeCode:",makeCode)
        if not goalCode.startswith(makeCode):
            self.endM()
        if makeCode==goalCode:
            self.endM()
    #키셋팅
    def r(self):
        global sx
        global ex
        self.selectCnvs.delete("all")
        sx+=132
        if sx>=396:sx=0;
        ex+=132
        if ex>=526:ex=132
        self.seleftF = self.selectCnvs.create_rectangle(sx,sy,ex,ey, fill="blue")
    def u(self):
        global sy
        global ey
        self.selectCnvs.delete("all")
        sy-=132
        ey-=132
        if sy<=-132:sy=132
        if ey<=-2:ey=262
        self.seleftF = self.selectCnvs.create_rectangle(sx,sy,ex,ey, fill="blue")
    def l(self):
        global sx
        global ex
        self.selectCnvs.delete("all")
        sx-=132
        if sx<0:sx=264
        ex-=132
        if ex<130:ex=394
        self.seleftF = self.selectCnvs.create_rectangle(sx,sy,ex,ey, fill="blue")
    def d(self):
        global sy
        global ey
        self.selectCnvs.delete("all")
        sy+=132
        ey+=132
        if sy>=264:sy=0
        if ey>=394:ey=130
        self.seleftF = self.selectCnvs.create_rectangle(sx,sy,ex,ey, fill="blue")

    def key(self,event):
        if event.keycode==37:self.l()
        elif event.keycode==38:self.u()
        elif event.keycode==39:self.r()
        elif event.keycode==40:self.d()
        #버튼 셀렉프라임 의 위치에 따라 버튼 포커스 이동    
        sel = [sx,sy]
        if [0,0] == sel : self.upBreadBtn.focus_set()
        elif [132,0] == sel : self.pattyBtn.focus_set()
        elif [264,0] == sel : self.cheeseBtn.focus_set()
        if [0,132] == sel : self.downBreadBtn.focus_set()
        elif [132,132] == sel : self.tomatoBtn.focus_set()
        elif [264,132] == sel : self.lettuceBtn.focus_set()
    
   
if __name__=="__main__":
    Game()