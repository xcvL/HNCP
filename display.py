import cv2
import ctypes
import filesSL
import keras
import numpy
import pyautogui as pag
import pygame


# 초기화
pygame.init()


# 모델 경로
# path_model="D:/Coding/Python/Machine_Learning/CNN/models/model2_5.h5"
path_model="C:/1_Coding/Coding_1/PYTHON/CNN/models/model2_5.h5"


# 모델 로드
Lmodel=keras.models.load_model(path_model)


# 기본 설정
u32 = ctypes.windll.user32
(width, height) = u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)
background=pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("drawing calculator")
font = pygame.font.SysFont(None, 50)
background.fill((255, 255, 255))
clock=pygame.time.Clock()


d=5 # 선 두께
e=6 # 지우개 두께
text_size=50
oktab=0 # Tab 허용 변수
posList=[] # 한 번 선을 그릴 때 좌표들
All_posList=[] # posList의 리스트
dnum=[] # 숫자 리스트
eraseList=[] # 지우개 위치 리스트

running=True
while running:
    clock.tick(1000000)
    key=pygame.key.get_pressed()

    for event in pygame.event.get():

        # esc : 종료
        if key[pygame.K_ESCAPE]:
            running=False
            
        
        # p : 텍스트 사이즈 증가
        if key[pygame.K_p]:
                text_size+=1
                font=pygame.font.SysFont(None, text_size)

        
        # m : 텍스트 사이즈 감소
        if key[pygame.K_m]:
            text_size-=1
            font=pygame.font.SysFont(None, text_size)


        if key[pygame.K_d]:
            # d키 + mouse : 마우스로 그리기
            if event.type==pygame.MOUSEMOTION:
                xPos, yPos=pygame.mouse.get_pos()
                posList.append((xPos, yPos)) # 좌표 저장
                pygame.draw.circle(background, (0, 0, 0), (xPos, yPos), d) # 점 그리기
                if len(posList)>1:
                    pygame.draw.line(background, (0, 0, 0), posList[-2], posList[-1], 2*d+3) # 점 사이 잇기
                

            elif event.type==pygame.KEYDOWN:
                # d키 + Plus Sign(+) : 붓 굵기 증가
                if event.key==pygame.K_KP_PLUS:
                    d+=1
                # d키 + Minus Sign(-) : 붓 굵기 감소
                elif event.key==pygame.K_KP_MINUS:
                    if d>0:
                        d-=1


        # 그리기 종료시 posList를 All_posList에 저장
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                All_posList.append(posList)
                posList=[]
        
        
        # a : 전체 삭제
        if key[pygame.K_a]:
            background.fill((255, 255, 255))
            All_posList=[]
        

        # r키 : 이전 선 삭제
        if key[pygame.K_r]:
            if All_posList==[]:
                pass
            else:
                for i in All_posList[-1]:
                    pygame.draw.circle(background, (255, 255, 255), i, d) # 점 지우기
                pygame.draw.lines(background, (255, 255, 255), False, All_posList[-1], 2*d+3) # 선 지우기
                del All_posList[-1]
        

        if key[pygame.K_e]:
            # e + mouse : 마우스로 지우기
            if event.type==pygame.MOUSEMOTION:
                xPos, yPos=pygame.mouse.get_pos()
                eraseList.append((xPos, yPos)) # 좌표 저장
                pygame.draw.circle(background, (255, 255, 255), (xPos, yPos), 6) # 점 그리기
                if len(eraseList)>1:
                        pygame.draw.line(background, (255, 255, 255), eraseList[-2], eraseList[-1], 2*e+3) # 점 사이 잇기
                
            elif event.type==pygame.KEYDOWN:
                # e + Plus Sign(+) : 지우개 굵기 증가
                if event.key==pygame.K_KP_PLUS:
                    e+=1
                # e + Minus Sign(-) : 지우개 굵기 감소
                elif event.key==pygame.K_KP_MINUS:
                    if e>0:
                        e-=1
        
        
        # 지우개 종료시 eraseList 초기화
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_e:
                eraseList=[]
        
        
        # Space : 이미지 분석 시작
        if key[pygame.K_SPACE]:
            
            # 스크린샷 이미지 경로
            # path_image=f"D:/Coding/Python/Machine_Learning/CNN/screenshot.png"
            path_image="C:/1_Coding/Coding_1/PYTHON/CNN/screenshot.png"
            pag.screenshot(path_image)
            
            # 대기 문구 표시
            wait_text=font.render("Please don't touch anything and wait a moment.", True, (0, 0, 0))
            filesSL.TextShow(wait_text, background, width, height)
            pygame.display.update()

            # 이미지 가공
            src=cv2.imread(path_image,cv2.IMREAD_GRAYSCALE)
            ret, binary=cv2.threshold(src,170,255,cv2.THRESH_BINARY_INV) # 이진화
            proc_image=filesSL.ImageCutter(binary) # 사방위 불필요한 끝단 삭제 후 0으로된 열과 행 추가
            proc_image_list=filesSL.ImageSplitter(proc_image, 28, 28) # 숫자 분할

            # 분할한 이미지 예측
            pred_list=[]
            for i in proc_image_list:
                final_image=numpy.array(cv2.resize(numpy.array(i), dsize=(28, 28), interpolation=cv2.INTER_AREA)) # 28*28로 재규격화
                pred_list.append(numpy.argmax(Lmodel.predict(final_image.reshape(-1, 28, 28, 1))[0])) # 28*28*1로 재규격화 후 예측한 값을 pred_list에 추가

            # 최종 예측값
            pred=''
            for i in pred_list:
                pred+=str(i)

            # 예측값 출력
            text=font.render(pred, True, (0, 0, 0))
            filesSL.TextShow(text, background, width, height)
            
            oktab=1 # tab키 허용
                
        
        # Space키를 누르면 tab키 허용
        if oktab==1:
            # Tab키 : 예측값 저장
            if key[pygame.K_TAB]:
                dnum.append(int(pred))
                oktab=0
        
        
        # Backspace : 이전에 저장한 예측값 삭제
        if key[pygame.K_BACKSPACE]:
            if len(dnum)!=0:
                del dnum[-1]
            else:
                pass


        if len(dnum)==2:
            dnum0=str(dnum[0])
            dnum1=str(dnum[1])
            # Plus Sign(-) : 두 예측값의 덧셈값 출력
            if key[pygame.K_KP_PLUS]:
                result_text=font.render(filesSL.TextCalc(dnum, "+"), True, (0, 0, 0))
                filesSL.TextShow(result_text, background, width, height)
                dnum=[]
        

            # Minus Sign(-) : 두 예측값의 뺄셈값 출력
            if key[pygame.K_KP_MINUS]:
                result_text=font.render(filesSL.TextCalc(dnum, "-"), True, (0, 0, 0))
                filesSL.TextShow(result_text, background, width, height)
                dnum=[]
        

            # Asterisk(*) : 두 예측값의 곱셈값 출력
            if key[pygame.K_KP_MULTIPLY]:
                result_text=font.render(filesSL.TextCalc(dnum, "*"), True, (0, 0, 0))
                filesSL.TextShow(result_text, background, width, height)
                dnum=[]
        

            # Slash(/) : 두 예측값의 나눗셈값 출력
            if key[pygame.K_KP_DIVIDE]:
                result_text=font.render(filesSL.TextCalc(dnum, "/"), True, (0, 0, 0))
                filesSL.TextShow(result_text, background, width, height)
                dnum=[]

    pygame.display.update()

pygame.quit()


'''
==============
   키 매뉴얼
==============

esc
종료


p
텍스트 사이즈 증가


m
텍스트 사이즈 감소


d + mouse
마우스로 그리기

d + Plus Sign(+)
붓 굵기 증가

d + Minus Sign(-)
붓 굵기 감소


a
전체 삭제


r
이전 선 삭제


e + mouse
마우스로 지우기

e + Plus Sign(+)
지우개 굵기 증가

e + Minus Sign(-)
지우개 굵기 감소


Space
그림 분석 시작


Tab
예측값 저장


Backspace
이전에 저장한 예측값 삭제


Plus Sign(+)
두 예측값의 덧셈값 출력

Minus Sign(-)
두 예측값의 뺄셈값 출력

Asterisk(*)
두 예측값의 곱셈값 출력

Slash(/)
두 예측값의 나눗셈값 출력
'''