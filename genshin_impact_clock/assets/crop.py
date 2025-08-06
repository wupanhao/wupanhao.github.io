import cv2
import numpy as np
items = [
    [[0,607],[417,1023],"bg.png"],
    [[3,238],[367,602],"Horoscope04.png"],
    [[419,609],[832,1022],"Horoscope03.png"],
    [[616,369],[851,604],"Horoscope05.png"],
    [[387,250],[487,350],"sun.png"],
    [[382,123],[482,223],"moon.png"],
    [[514,269],[614,369],"sunrise.png"],
    [[839,679],[939,779],"sunset.png"],
    ]

def split():
    img = cv2.imread("base.png", cv2.IMREAD_UNCHANGED)
    for item in items:
        x1,y1 = item[0]
        x2,y2 = item[1]
        cv2.imwrite(item[2],img[y1:y2,x1:x2])
        
        
if __name__ == '__main__':
    split()