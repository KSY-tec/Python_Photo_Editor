import numpy as np
import cv2
import math

#이미지 처리 함수 모음
class Img_pross:
    #이미지 리사이즈
    def img_resize(_src,_height, _width,_channel,  _h,_w):
        copy_img = np.zeros(shape=(_h, _w, _channel), dtype=np.uint8)
        for y in range(0, _height):
            for x in range(0, _width):
                try:
                    for i in range(int((y-1)*_h/_height),int(y*_h/_height)+1):
                        for j in range(int((x-1)*_w/_width),int(x*_w/_width)+1):
                            copy_img[i][j][0] = _src[y][x][0] 
                            copy_img[i][j][1] = _src[y][x][1] 
                            copy_img[i][j][2] = _src[y][x][2] 
                except:
                    continue
        return copy_img

    #상하반전
    def img_mirror_up_to_down(_src,_height, _width,_channel):
        copy_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)
        for y in range(0, _height):
            for x in range(0, _width):
                copy_img[_height-y-1][x][0] = _src[y][x][0] 
                copy_img[_height-y-1][x][1] = _src[y][x][1] 
                copy_img[_height-y-1][x][2] = _src[y][x][2] 
        return copy_img

    #좌우반전
    def img_mirror_left_to_right(_src,_height, _width,_channel):
        copy_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)

        for y in range(0, _height):
            for x in range(0, _width):
                copy_img[y][_width-x-1][0] = _src[y][x][0] 
                copy_img[y][_width-x-1][1] = _src[y][x][1] 
                copy_img[y][_width-x-1][2] = _src[y][x][2] 

        return copy_img
    #90도 회전
    def img_rotate90(_src,_height, _width,_channel):
        height, width, channel=_height, _width, _channel
        ch=90
        
        width1=int(height*math.cos(math.radians(90-ch))+width*math.cos(math.radians(ch)))
        height1=int(height*math.cos(math.radians(ch))+width*math.cos(math.radians(90-ch)))

        copy_img = np.zeros(shape=(height1, width1, channel), dtype=np.uint8)

        for y in range(0, height):
            for x in range(0, width):
                try:
                    copy_img[int((x-width/2)*math.sin(math.radians(ch))+(y-height/2)*math.cos(math.radians(ch))+height1/2)][int((x-width/2)\
                        *math.cos(math.radians(ch))-(y-height/2)*math.sin(math.radians(ch))+width1/2)][0] = _src[y][x][0]
                    copy_img[int((x-width/2)*math.sin(math.radians(ch))+(y-height/2)*math.cos(math.radians(ch))+height1/2)][int((x-width/2)\
                        *math.cos(math.radians(ch))-(y-height/2)*math.sin(math.radians(ch))+width1/2)][1] = _src[y][x][1]
                    copy_img[int((x-width/2)*math.sin(math.radians(ch))+(y-height/2)*math.cos(math.radians(ch))+height1/2)][int((x-width/2)\
                        *math.cos(math.radians(ch))-(y-height/2)*math.sin(math.radians(ch))+width1/2)][2] = _src[y][x][2]
                except:
                    continue
        return copy_img
    #이미지 회전
    def img_rotate(_src,_height, _width,_channel,_ch):
        height, width, channel=_height, _width, _channel
        ch=_ch
        
        width1=int(height*math.cos(math.radians(90-ch))+width*math.cos(math.radians(ch)))
        height1=int(height*math.cos(math.radians(ch))+width*math.cos(math.radians(90-ch)))

        copy_img = np.zeros(shape=(height1, width1, channel), dtype=np.uint8)

        for y in range(0, height):
            for x in range(0, width):
                try:
                    copy_img[int((x-width/2)*math.sin(math.radians(ch))+(y-height/2)*math.cos(math.radians(ch))+height1/2)][int((x-width/2)\
                        *math.cos(math.radians(ch))-(y-height/2)*math.sin(math.radians(ch))+width1/2)][0] = _src[y][x][0]
                    copy_img[int((x-width/2)*math.sin(math.radians(ch))+(y-height/2)*math.cos(math.radians(ch))+height1/2)][int((x-width/2)\
                        *math.cos(math.radians(ch))-(y-height/2)*math.sin(math.radians(ch))+width1/2)][1] = _src[y][x][1]
                    copy_img[int((x-width/2)*math.sin(math.radians(ch))+(y-height/2)*math.cos(math.radians(ch))+height1/2)][int((x-width/2)\
                        *math.cos(math.radians(ch))-(y-height/2)*math.sin(math.radians(ch))+width1/2)][2] = _src[y][x][2]
                except:
                    continue
        for y in range(0, height1):
            for x in range(0, width1):
                if copy_img[y][x][0]==0 and copy_img[y][x][1]==0 and copy_img[y][x][2]==0:
                    try:
                        copy_img[y][x][0] = int(copy_img[y][x-1][0]*0.25+copy_img[y][x+1][0]*0.25+copy_img[y-1][x][0]*0.25+copy_img[y+1][x][0]*0.25)
                        copy_img[y][x][1] = int(copy_img[y][x-1][1]*0.25+copy_img[y][x+1][1]*0.25+copy_img[y-1][x][1]*0.25+copy_img[y+1][x][1]*0.25)
                        copy_img[y][x][2] = int(copy_img[y][x-1][2]*0.25+copy_img[y][x+1][2]*0.25+copy_img[y-1][x][2]*0.25+copy_img[y+1][x][2]*0.25)
                    except:
                        continue
        return copy_img
    #밝게
    def img_lighter(_src,_height, _width,_channel):
        copy_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)

        for y in range(0, _height):
            for x in range(0, _width):
                try:
                    copy_img[y][x][0] = int(255*math.log(_src[y][x][0],256))
                    copy_img[y][x][1] = int(255*math.log(_src[y][x][1],256))
                    copy_img[y][x][2] = int(255*math.log(_src[y][x][2],256))
                except:
                    continue
        return copy_img

    #어둡게
    def img_darker(_src,_height, _width,_channel):
        copy_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)
        for y in range(0, _height):
            for x in range(0, _width):
                copy_img[y][x][0] = int(255**(_src[y][x][0]/255))
                copy_img[y][x][1] = int(255**(_src[y][x][1]/255))
                copy_img[y][x][2] = int(255**(_src[y][x][2]/255))

        return copy_img

    #흐리게
    def img_blur(_src,_height, _width,_channel):
        img1=_src
        copy_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)
        side=1/9
        plus=1/9
        orig=1/9
        for y in range(_height):
            for x in range(_width):
                try:
                    copy_img[y][x][0] = img1[y-1][x][0]*plus+img1[y][x-1][0]*plus+img1[y][x][0]*orig+img1[y][x+1][0]\
                        *plus+img1[y+1][x][0]*plus +img1[y-1][x-1][0]*side+img1[y-1][x+1][0]*side+img1[y+1][x-1][0]*side+img1[y+1][x+1][0]*side
                    copy_img[y][x][1] = img1[y-1][x][1]*plus+img1[y][x-1][1]*plus+img1[y][x][1]*orig+img1[y][x+1][1]\
                        *plus+img1[y+1][x][1]*plus +img1[y-1][x-1][1]*side+img1[y-1][x+1][1]*side+img1[y+1][x-1][1]*side+img1[y+1][x+1][1]*side
                    copy_img[y][x][2] = img1[y-1][x][2]*plus+img1[y][x-1][2]*plus+img1[y][x][2]*orig+img1[y][x+1][2]\
                        *plus+img1[y+1][x][2]*plus +img1[y-1][x-1][2]*side+img1[y-1][x+1][2]*side+img1[y+1][x-1][2]*side+img1[y+1][x+1][2]*side

                except:
                    copy_img[y][x][0] = img1[y][x][0]
                    copy_img[y][x][1] = img1[y][x][1]
                    copy_img[y][x][2] = img1[y][x][2]
        return copy_img
    #선명하게
    def img_sharpen(_src,_height, _width,_channel):
        
        
        img1=_src
        copy_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)
        side=1/9
        plus=1/9
        orig=1/9
        for y in range(_height):
            for x in range(_width):
                try:
                    copy_img[y][x][0] = img1[y-1][x][0]*plus+img1[y][x-1][0]*plus+img1[y][x][0]*orig+img1[y][x+1][0]\
                        *plus+img1[y+1][x][0]*plus +img1[y-1][x-1][0]*side+img1[y-1][x+1][0]*side+img1[y+1][x-1][0]*side+img1[y+1][x+1][0]*side
                    copy_img[y][x][1] = img1[y-1][x][1]*plus+img1[y][x-1][1]*plus+img1[y][x][1]*orig+img1[y][x+1][1]\
                        *plus+img1[y+1][x][1]*plus +img1[y-1][x-1][1]*side+img1[y-1][x+1][1]*side+img1[y+1][x-1][1]*side+img1[y+1][x+1][1]*side
                    copy_img[y][x][2] = img1[y-1][x][2]*plus+img1[y][x-1][2]*plus+img1[y][x][2]*orig+img1[y][x+1][2]\
                        *plus+img1[y+1][x][2]*plus +img1[y-1][x-1][2]*side+img1[y-1][x+1][2]*side+img1[y+1][x-1][2]*side+img1[y+1][x+1][2]*side

                except:
                    copy_img[y][x][0] = img1[y][x][0]
                    copy_img[y][x][1] = img1[y][x][1]
                    copy_img[y][x][2] = img1[y][x][2]


        copy_img2 = np.zeros(shape=(_height, _width, _channel), dtype=int)
        for y in range(_height):
            for x in range(_width):
                copy_img2[y][x][0]=int(_src[y][x][0])-int(copy_img[y][x][0])
                copy_img2[y][x][1]=int(_src[y][x][1])-int(copy_img[y][x][1])
                copy_img2[y][x][2]=int(_src[y][x][2])-int(copy_img[y][x][2])



        copy_img3 = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)
        for y in range(_height):
            for x in range(_width):
                try:

                    if (int(_src[y][x][0])+copy_img2[y][x][0])>0 and (int(_src[y][x][0])+copy_img2[y][x][0])<255:
                        copy_img3[y][x][0]=_src[y][x][0]+copy_img2[y][x][0]
                    
                    else:
                        copy_img3[y][x][0]=_src[y][x][0]


                    if  (int(_src[y][x][1])+copy_img2[y][x][1])>0 and (int(_src[y][x][1])+copy_img2[y][x][1])<255:
                        copy_img3[y][x][1]=_src[y][x][1]+copy_img2[y][x][1]
                    else:
                        copy_img3[y][x][1]=_src[y][x][1]


                    if (int(_src[y][x][2])+copy_img2[y][x][2])>0 and (int(_src[y][x][2])+copy_img2[y][x][2])<255:
                        copy_img3[y][x][2]=_src[y][x][2]+copy_img2[y][x][2]
                    else:
                        copy_img3[y][x][2]=_src[y][x][2]
                except:
                    copy_img2[y][x][0]=_src[y][x][0]
                    copy_img2[y][x][1]=_src[y][x][1]
                    copy_img2[y][x][2]=_src[y][x][2]


        copy_img=copy_img3
        return copy_img
    #그레이스케일
    def img_grayscale(_src,_height, _width,_channel):
        copy_img = np.zeros(shape=(_height, _width,_channel), dtype=np.uint8)
        img1=_src
        for y in range(_height):
            for x in range(_width):
                copy_img[y][x][0] = int(img1[y][x][0]*0.2126+img1[y][x][1]*0.7152+img1[y][x][2]*0.0722)
                copy_img[y][x][1] = int(img1[y][x][0]*0.2126+img1[y][x][1]*0.7152+img1[y][x][2]*0.0722)
                copy_img[y][x][2] = int(img1[y][x][0]*0.2126+img1[y][x][1]*0.7152+img1[y][x][2]*0.0722)

        return copy_img
    #흑백
    def img_bw(_src,_height, _width,_channel):
        copy_img = np.zeros(shape=(_height, _width,_channel), dtype=np.uint8)
        img1=_src
        for y in range(_height):
            for x in range(_width):
                copy_img[y][x][0] = int(img1[y][x][0]*0.2126+img1[y][x][1]*0.7152+img1[y][x][2]*0.0722)
                copy_img[y][x][1] = int(img1[y][x][0]*0.2126+img1[y][x][1]*0.7152+img1[y][x][2]*0.0722)
                copy_img[y][x][2] = int(img1[y][x][0]*0.2126+img1[y][x][1]*0.7152+img1[y][x][2]*0.0722)
                if copy_img[y][x][0]>=256/2:
                    copy_img[y][x][0] = 255
                    copy_img[y][x][1] = 255
                    copy_img[y][x][2] = 255
                else:
                    copy_img[y][x][0] = 0
                    copy_img[y][x][1] = 0
                    copy_img[y][x][2] = 0
        return copy_img

    #히스토그램 평활화
    def hist_smooting(_src,_height, _width,_channel):
        hist1=[]
        hist2=[]
        hist3=[]
        for i in range(256):
            hist1+=[0]
            hist2+=[0]
            hist3+=[0]

        for y in range(_height):
            for x in range(_width):
                match1=_src[y][x][0]
                match2=_src[y][x][1]
                match3=_src[y][x][2]
                hist1[match1]+=1
                hist2[match2]+=1
                hist3[match3]+=1

        sum1=[]
        sum2=[]
        sum3=[]
        for i in range(256):
            sum1+=[0]
            sum2+=[0]
            sum3+=[0]

        sum1[0]=hist1[0]
        sum2[0]=hist2[0]
        sum3[0]=hist3[0]

        for i in range(1,256):
            sum1[i]+=sum1[i-1]+hist1[i]
            sum2[i]+=sum2[i-1]+hist2[i]
            sum3[i]+=sum3[i-1]+hist3[i]

        n1=[]
        n2=[]
        n3=[]
        for i in range(256):
            n1+=[0]
            n2+=[0]
            n3+=[0]

        for i in range(256):
            n1[i]=sum1[i]*(1/sum1[255])*255
            n2[i]=sum2[i]*(1/sum2[255])*255
            n3[i]=sum3[i]*(1/sum3[255])*255

        copy_img = np.zeros(shape=(_height, _width,_channel), dtype=np.uint8)
        for y in range(_height):
            for x in range(_width):
                copy_img[y][x][0]=int(n1[_src[y][x][0]])
                copy_img[y][x][1]=int(n2[_src[y][x][1]])
                copy_img[y][x][2]=int(n3[_src[y][x][2]])

        return copy_img

    # 이미지 채널 조정 기능
    def img_ctrl_chan(_src,_height, _width,_channel,_blue,_green,_red):
        copy_img=np.zeros(shape=(_height, _width,_channel), dtype=np.uint8)
        for y in range(0, _height):
            for x in range(0, _width):
                if _blue<0:
                    copy_img[y][x][0] = _src[y][x][0]*(_blue*0.1*-1) 
                else:
                    copy_img[y][x][0] = _src[y][x][0]*(1+_blue*0.1) 
                if _green<0:
                    copy_img[y][x][1] = _src[y][x][1]*(_green*0.1*-1)
                else:
                    copy_img[y][x][1] = _src[y][x][1]*(1+_green*0.1)
                if _red<0:
                    copy_img[y][x][2] = _src[y][x][2]*(_red*0.1*-1)
                else:
                    copy_img[y][x][2] = _src[y][x][2]*(1+_red*0.1)
        return copy_img
