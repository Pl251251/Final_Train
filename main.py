import cv2
import numpy as np


vid1 = cv2.VideoCapture('3686.mp4')
img_array = []

size = (int(vid1.get(3)), int(vid1.get(4)))

print("Warning it make take a minute before the video displays since my code take a long time to run through")
print("We're sorry for the inconvenience")
while (vid1.isOpened()):
    ret, frame = vid1.read()
    if ret != True:
        break
    else:
        tangent1 = 0
        red = 0
        try:
            #perspective transform
            pts1 = np.float32([[568, 718], [932, 718],[256, 1074], [1244, 1074]])
            pts2 = np.float32([[100, 0], [500, 0], [100, 400], [500, 400]])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            #warp image
            result = cv2.warpPerspective(frame, matrix, (500, 400))
            cv2.imwrite("result.jpg",result)
            #blur,gray and edge
            blur = cv2.medianBlur(result, 7)
            gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray,50,60,apertureSize = 3)
            #roi
            roi = edges[0:400, 0:300]
            #find lines
            linesP = cv2.HoughLinesP(roi, 1, np.pi / 180, 10, None, 50, 10)
            #sort lines
            c=9000
            d=0
            for i in linesP:
                l = i[0]
                #cv2.line(result, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
                if (l[0]<c):
                    line1 =i
                    c= l[0]
                if (l[0]>d):
                    line2 =i
                    d=l[0]

            #draw left most and right most lines
            info1 = line1[0]
            info2 =line2[0]
            y1= int((info1[1] +info2[1])/2)
            y2 =int((info1[3] +info2[3])/2)
            x1 =int(((info1[0]) +int(info2[0]))/2)
            x2 = int((info1[2] +info2[2])/2)

            tangent1 = np.arctan((y2-y1)/(x2-x1))
            if tangent1 > 0:
                red = 200- (2 * tangent1)
            elif tangent1 <= 0:
                red = 200+ (2 * tangent1)


        except:
            pass

        cv2.circle(frame, (1750, 150), 50, (0,150,red), 60)
        img_array.append(frame)


out2 = cv2.VideoWriter('final1.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

for i in img_array:
    out2.write(i)
    b = cv2.resize(i,(960,540))
    cv2.imshow("Frame", b)
    cv2.waitKey(5)
out2.release()

cv2.waitKey(0)
cv2.destroyAllWindows()
