from tkinter import *
import time
import math
 
window = Tk()
window.title("nemoRPG")   # 게임 이름
window.resizable(0,0)
canvas = Canvas(window, width = 640, height = 640, bg ="white")   # 창 생성
objects, score = set(), 0   # 오브젝트 세트, 점수 선언
 
class Game:   # 게임 클래스
    global objects, score
    def __init__(self):
        self.keys = set()   # 버튼 세트 생성
        self.mx, self.my, self.mPressed = 0, 0, 0   # 마우스 좌표, 클릭 여부
        window.bind("<KeyPress>", self.keyPressHandler)   # 버튼 클릭시 함수호출
        window.bind("<KeyRelease>", self.keyReleaseHandler)   # 버튼 땔시 함수호출
        canvas.bind("<Button-1>", self.mousePress)   # 마우스 클릭시 함수호출
        canvas.bind("<B1-Motion>", self.mousePress)
        canvas.bind("<ButtonRelease-1>", self.mouseRelease)   # 마우스 땔시 함수호출
        canvas.pack()
 
        obj_main = object_main(310, 310, 20, 20, "black")   # main 오브젝트 생성
 
        score_view = canvas.create_text(540, 15, text = "SCORE: " + str(score), font = ("나눔고딕코딩", 12), fill = "red")   # 점수 드로우
        canvas.create_rectangle(5, 5, 420, 25, fill = "gray82", width =0)   # HP바 바탕 드로우
        hpbar = canvas.create_rectangle(5, 5, 420, 25, fill = "springGreen2", width =0)   # HP바 드로우
        hptext = canvas.create_text(200, 15, text ="HP: (" + str(obj_main.hp) + " / 1000)", font = ("나눔고딕코딩", 8))   # HP 숫자 드로우
 
        while(1):  # 메인 루프
            if obj_main in objects:
                for key in self.keys:   # 버튼 체킹
                    if key == ord('A') and obj_main.x_accel > -4: obj_main.x_accel -= 1   # A
                    if key == ord('D') and obj_main.x_accel < 4: obj_main.x_accel += 1   # D
                    if key == ord('W') and obj_main.y_accel > -4: obj_main.y_accel -= 1   # W
                    if key == ord('S') and obj_main.y_accel < 4: obj_main.y_accel += 10   # S
 
                if self.mPressed == 1 and obj_main.coolt == obj_main.cool:   # 마우스 클릭 시
                    obj_attack = object_attack(canvas.coords(obj_main.canvas_id)[0]+7, canvas.coords(obj_main.canvas_id)[1]+7, 6, 6, "black", 120)    # 공격 오브젝트 생성
                    obj_attack.x_accel, obj_attack.y_accel = self.movePoint(canvas.coords(obj_attack.canvas_id)[0] + 10, canvas.coords(obj_attack.canvas_id)[1] + 10, self.mx, self.my, 25)
                    obj_main.coolt, obj_main.hp = 0 , obj_main.hp - 50
 
                canvas.delete(hpbar); canvas.delete(hptext)   # hp 갱신
                hpbar = canvas.create_rectangle(5, 5, 420 * obj_main.hp / obj_main.mhp, 25, fill = "springGreen2", width =0)
                hptext = canvas.create_text(200, 15, text ="HP: (" + str(obj_main.hp) + " / 1000)", font = ("나눔고딕코딩", 8))
 
                canvas.itemconfig(score_view, text = "SCORE: " + str(score))   # 점수 갱신
 
            for obj in objects.copy(): obj.step()   # 스텝 함수 호출
 
            window.update()   # 업데이트
            time.sleep(0.01)   # 0.01초 만큼 sleep
                        
    def keyPressHandler(self, event):   # 버튼 세트에 버튼추가
        self.keys.add(event.keycode)
    def keyReleaseHandler(self, event):   # 버튼 세트에 버튼 제거
        if event.keycode in self.keys: self.keys.remove(event.keycode)
 
    def mousePress(self, event):   # 마우스 왼쪽 누를시 좌표 반환, 클릭값 1
        self.mx, self.my, self.mPressed = event.x, event.y, 1
    def mouseRelease(self, event):   # 마우스 왼쪽 땔시 좌표 반환, 클릭값 0
        self.mx, self.my, self.mPressed = event.x, event.y, 0
 
    def movePoint(self, x1, y1, x2, y2, spd):   # 해당 좌표로 이동
        return (x2 - x1) * spd / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), (y2 - y1) * spd / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
 
 
class element:   # 오브젝트 원형
    def __init__(self, x, y, size_x, size_y, color):
        self.x, self.y = x, y   # 생성 위치
        self.size_x, self.size_y = size_x, size_y   # 크기
        self.color = color   # 색
        self.x_accel, self.y_accel = 0, 0   # 가속도
        objects.add(self)   # 오브젝트 세트에 자신 등록
        self.canvas_id = canvas.create_rectangle(x, y, x + self.size_x, y + self.size_y, fill = self.color, width =0)   # 캠버스 추가
 
    def destroy(self):   # 제거 함수
        objects.discard(self)   # 오브젝트 세트에서 자신 제거
        canvas.delete(self.canvas_id)   # 캠버스 제거
        del self
 
    def move(self):   # 움직임 계산(이동, 가속도, 중력) 함수
        x_value, y_value = self.x_accel, self.y_accel
        if x_value != 0 or y_value != 0:   # 좌표 갱신
            if canvas.coords(self.canvas_id)[0] + x_value < 0: x_value, self.x_accel = -canvas.coords(self.canvas_id)[0], -self.x_accel   # 창나감 방지, 튕김효과
            if canvas.coords(self.canvas_id)[1] + y_value < 0: y_value, self.y_accel = -canvas.coords(self.canvas_id)[1], -self.y_accel
            if canvas.coords(self.canvas_id)[2] + x_value > 640: x_value, self.x_accel = 640 - canvas.coords(self.canvas_id)[2], -self.x_accel
            if canvas.coords(self.canvas_id)[3] + y_value > 640: y_value, self.y_accel = 640 - canvas.coords(self.canvas_id)[3], -self.y_accel
            canvas.move(self.canvas_id, x_value,  y_value)   # 수치만큼 이동
            self.mx, self.my = 0, 0   # 이동값 초기화
            self.x_accel, self.y_accel = self.x_accel * 0.98, self.y_accel * 0.98    # 가속도 감소
 
class object_main(element):   # main 오브젝트
    def __init__(self, x, y, size_x, size_y, color):
        super().__init__(x, y, size_x, size_y, color)   # 상속
        self.mhp, self.hp = 1000, 1000   # 체력
        self.cool, self.coolt = 25, 0   # 쿨타임
 
    def step(self):   # 스텝 함수
        global score
        score += 1
        self.move()
        if self.coolt < self.cool: self.coolt += 1  # 쿨타임 감소
        if self.hp < 0: self.destroy()   # HP 0일시 제거
        
 
class object_attack(element):   # attack 오브젝트
    def __init__(self, x, y, size_x, size_y, color, livetime):
        super().__init__(x, y, size_x, size_y, color)   # 상속
        self.livetime = livetime   # 동작 시간
        self.fortime = 0   # 지난 시간
 
    def step(self):   # 스텝 함수
        self.move()
        if self.livetime <= self.fortime: self.destroy()   # 동작 시간 오버 or 멈출시 파괴         
        self.fortime += 1    # 지난 시간 ++
 
Game()   # 게임 실행