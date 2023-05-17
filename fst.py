from tkinter import *
import time
 
window = Tk()
window.title("nemoRPG")   # 게임 이름
window.resizable(0,0)
canvas = Canvas(window, width = 640, height = 640, bg ="white")   # 창 생성
canvas.pack()
 
class Game:   # 게임 클래스
    global objects
    objects = set()   # 오브젝트 세트 생성
    def __init__(self):
        self.keys = set()   # 버튼 세트 생성
        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)
 
        obj_main = element(310, 310, 20, 20, "black")
 
        while(1):  # 메인 루프
            for key in self.keys:   # 버튼 체킹    
                if obj_main in objects:
                    if key == ord('A') and obj_main.x_accel > -10:   # A 버튼
                        obj_main.x_accel -= 1
                    if key == ord('D') and obj_main.x_accel < 10:   # D 버튼
                        obj_main.x_accel += 1
                    if key == ord('W') and obj_main.y_accel > -10:   # W 버튼
                        obj_main.y_accel -= 1
                    if key == ord('S') and obj_main.y_accel < 10:   # S 버튼
                        obj_main.y_accel += 1
 
            for obj in objects.copy():   # 오브젝트 스텝
                obj.step()
                    
            window.update()   # 업데이트
            time.sleep(0.01)   # 0.01초 만큼 sleep
                        
    def keyPressHandler(self, event):   # 버튼 세트에 버튼추가
        self.keys.add(event.keycode)
 
    def keyReleaseHandler(self, event):   # 버튼 세트에 버튼 제거
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)
 
class element:   # 오브젝트 원형
    def __init__(self, x, y, size_x, size_y, color):
        self.x, self.y = x, y   # 생성 위치
        self.size_x, self.size_y = size_x, size_y   # 크기
        self.color = color   # 색
        self.x_accel, self.y_accel = 0, 0   # 가속도
        objects.add(self)   # 오브젝트 세트에 자신 등록
        self.id = canvas.create_rectangle(x, y, x + self.size_x, y + self.size_y, fill = self.color, width =0)   # 캠버스 추가
 
    def destroy(self):   # 제거 함수
        objects.discard(self)   # 오브젝트 세트에서 자신 제거
        canvas.delete(self.id)   # 캠버스 제거
        del self
 
    def move(self):   # 움직임 계산(이동, 가속도, 중력) 함수
        x_value, y_value = self.x_accel, self.y_accel
        if x_value != 0 or y_value != 0:   # 좌표 갱신
            if canvas.coords(self.id)[0] + x_value < 0:
                x_value = -canvas.coords(self.id)[0]   # 창나감 방지
                self.x_accel = -self.x_accel   # 튕김
            if canvas.coords(self.id)[1] + y_value < 0:
                y_value = -canvas.coords(self.id)[1]
                self.y_accel = -self.y_accel
            if canvas.coords(self.id)[2] + x_value > 640:
                x_value = 640 - canvas.coords(self.id)[2]
                self.x_accel = -self.x_accel
            if canvas.coords(self.id)[3] + y_value > 640:
                y_value = 640 - canvas.coords(self.id)[3]
                self.y_accel = -self.y_accel
            canvas.move(self.id, x_value,  y_value)   # 수치만큼 이동
            self.mx, self.my = 0, 0   # 이동값 초기화
            self.x_accel -= self.x_accel/100   # 가속도 감소
            self.y_accel -= self.y_accel/100
 
    def step(self):
        self.move()
 
Game()   # 게임 실행
