
import cv2
import urllib
import numpy as np
from time import sleep
import datetime

backsub = cv2.BackgroundSubtractorMOG()

while True:
    req = urllib.urlopen('http://tommycam.usc.edu/jpeg.cgi')
    # req = urllib.urlopen('http://vods.az511.com/adot_002.jpg')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    # print arr
    frame = cv2.imdecode(arr,-1) # 'load it as it is'
    # print frame
    print "picture taken at", datetime.datetime.now()

    fgmask = backsub.apply(frame, None, 0.01)
    contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    try: 
        hierarchy = hierarchy[0]
    except: 
        hierarchy = []

    best_id = 0

    # define the contours
    for contour, hier in zip(contours, hierarchy):
        # print contour
        # set the bounding box
        (x,y,w,h) = cv2.boundingRect(contour)

        # set the arbitrary parameters for your bounding box 
            # e.g., for a far away webcam on a crowd, you want to set this to a person's "size"
        if w > 5 and h > 5:
            #includes an ID for every bounding box

            midx = (x+(w/2))
            midy = (y+(h/2))
            # draw a dot in the middle of each bounding box

            if y > 250:
                best_id +=1

                # draw the midpoint circles
                cv2.circle(frame, (midx, midy),3,255,-1)
                print best_id, "--", "x:", midx, "y:", midy

                # draw the bounding boxes
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

                #label each bounding box with a unique id
                cv2.putText(frame, str(best_id), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # draw lines for controller buttons area
    cv2.line(frame,(100,500),(100,250),(0,0,255),1) #vertical line
    cv2.line(frame,(100,250),(650,250),(0,0,255),1) #horizontal line

    # button lines
    cv2.line(frame,(200,500),(200,250),(0,0,255),1) #v
    cv2.line(frame,(200,400),(650,400),(0,0,255),1) #h
    cv2.line(frame,(425,500),(425,250),(0,0,255),1) #v
    cv2.line(frame,(200,325),(650,325),(0,0,255),1) #h

    # buttons
    cv2.putText(frame, "START", (125, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "A", (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "B", (300, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "UP", (300, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "DOWN", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "LEFT", (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "RIGHT", (500, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


    # draw the final image with markers
    cv2.imshow('image refresh test',frame)

    # uncomment the below to watch the black/white masking
    # cv2.imshow('fgmask', fgmask)

    if cv2.waitKey(33)== 27:
        break
    sleep(3)

    # if cv2.waitKey() & 0xff == 27: quit()

# import cv2

# def get_blobs(thresh, maxblobs, maxmu03, iterations=1):
#     """
#     Return a 2-tuple list of the locations of large white blobs.
#     `thresh` is a black and white threshold image.
#     No more than `maxblobs` will be returned.
#     Moments with a mu03 larger than `maxmu03` are ignored.
#     Before sampling for blobs, the image will be eroded `iterations` times.
#     """
#     # Kernel specifies an erosion on direct pixel neighbours.
#     kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
#     # Remove noise and thin lines by eroding/dilating blobs.
#     thresh = cv2.erode(thresh, kernel, iterations=iterations)
#     thresh = cv2.dilate(thresh, kernel, iterations=iterations-1)

#     # Calculate the centers of the contours.
#     contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
#     moments = map(cv2.moments, contours)

#     # Filter out the moments that are too tall.
#     moments = filter(lambda k: abs(k['mu03']) <= maxmu03, moments)
#     # Select the largest moments.
#     moments = sorted(moments, key=lambda k: k['m00'], reverse=True)[:maxblobs]
#     # Return the centers of the moments.
#     return [(m['m10'] / m['m00'], m['m01'] / m['m00']) for m in moments if m['m00'] != 0]

# if __name__ == '__main__':
#     # Load an image and mark the 14 largest blobs.
#     image = cv2.imread('jpeg.cgi.jpg')
#     bwImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#     trackers = get_blobs(bwImage, 14, 50000, 3)
#     for tracker in trackers:
#         cv2.circle(image, tuple(int(x) for x in tracker), 3, (0, 0, 255), -1)
#     while True:
#       cv2.imshow('test', image)
#       if cv2.waitKey() & 0xff == 27: quit()