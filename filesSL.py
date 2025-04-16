import cv2
import numpy
import pygame


# 이미지 가공
def ImageCutter(image):
    start1=0
    start2=0
    end1=0
    end2=0
    idx=0
    image=numpy.array(image)
    imageL=image.tolist()
    for i in imageL:
        if sum(i)!=0:
            start1=idx
            break
        idx+=1
    
    idx=len(imageL)
    for i in numpy.flip(image, axis=0).tolist():
        if sum(i)!=0:
            end1=idx
            break
        idx-=1
    image=image[start1:end1, :]
    image=numpy.insert(image, 0, 0, axis=0)
    image=numpy.insert(image, len(image)-1, 0, axis=0)
    image=image.T
    
    idx=0
    imageL=image.tolist()
    for i in imageL:
        if sum(i)!=0:
            start2=idx
            break
        idx+=1
    
    idx=len(imageL)
    for i in numpy.flip(image, axis=0).tolist():
        if sum(i)!=0:
            end2=idx
            break
        idx-=1
    image=image[start2:end2, :]
    image=numpy.insert(image, 0, 0, axis=0)
    image=numpy.insert(image, len(image)-1, 0, axis=0)
    proc_image=image.T

    return proc_image


# 이미지 분할
def ImageSplitter(image, xSize, ySize):
    image_list=[]
    jud=True
    idx=0
    image=numpy.transpose(image)
    image=image.tolist()
    for i in image:
        if jud==True:
            if sum(i)!=0:
                start=idx
                jud=False
        else:
            if sum(i)==0:
                end=idx
                jud=True
                imageT=numpy.array(image)
                imageT=imageT[start:end, :]
                imageT=numpy.insert(imageT, 0, 0, axis=0)
                imageT=numpy.insert(imageT, len(imageT)-1, 0, axis=0)
                imageT=numpy.transpose(imageT)
                imageT=numpy.array(cv2.resize(imageT.astype("float32"), dsize=(xSize, ySize), interpolation=cv2.INTER_AREA))/255
                image_list.append(imageT)
        idx+=1
    
    return image_list
# idx==True이면 sum(i)==0이라는 의미
# idx==False이면 sum(i)!=0이라는 의미


# 글자 화면에 띄우기
def TextShow(text, screen, screen_width, screen_height, do_fill=(255, 255, 255)):
    text_rect=text.get_rect()
    text_rect.centerx=round(screen_width/2)
    text_rect.centery=round(screen_height/2)
    if do_fill!=None:
        screen.fill(do_fill)
        pygame.display.update()
    screen.blit(text, text_rect)


# 계산 결과 텍스트 출력
def TextCalc(NumberList, op):
    n0=str(NumberList[0])
    n1=str(NumberList[1])
    if op=="+":
        result=n0+"+"+n1+"="+str(NumberList[0]+NumberList[1])
        return result
    elif op=="-":
        result=n0+"-"+n1+"="+str(NumberList[0]-NumberList[1])
        return result
    elif op=="*":
        result=n0+"*"+n1+"="+str(NumberList[0]*NumberList[1])
        return result
    elif op=="/":
        result=n0+"/"+n1+"="+str(NumberList[0]/NumberList[1])
        return result