import cv2

# set up the background subtractor from OpenCV
backsub = cv2.BackgroundSubtractorMOG()
# set up the video capture (0 for your webcam or file name for a video file)
# capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture('tommy.mp4')

if capture:
    while (1): # while the camera is on
        ret, frame = capture.read()
        if ret:
            # find the background masking frame per frame
            fgmask = backsub.apply(frame, None, 0.03)
            contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
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
                if w > 10 and h > 15:
                    #includes an ID for every bounding box
                    best_id +=1

                    midx = (x+(w/2))
                    midy = (y+(h/2))
                    # draw a dot in the middle of each bounding box
                    cv2.circle(frame, (midx, midy),10,255,-1)
                    # draw the bounding box
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
                    #label each bounding box with a unique id
                    cv2.putText(frame, str(best_id), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 0), 2)

            # show the image with all the markers
            cv2.imshow("Track", frame)
            # uncomment the below to watch the black/white masking
            # cv2.imshow('fgmask', fgmask)

            # this will let you press 'Escape' to exit the video screen
            if cv2.waitKey(33)== 27:
                break

# Clean up everything before leaving
cv2.destroyAllWindows()
capture.release()




### ===================================
### OLD TEST BELOW
### ===================================



# import cv2
# import numpy as np

# # create video capture
# cap = cv2.VideoCapture(0)

# while(1):

#     # read the frames
#     _,frame = cap.read()

#     # smooth it
#     frame = cv2.blur(frame,(3,3))

#     # convert to hsv and find range of colors
#     hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#     thresh = cv2.inRange(hsv,np.array((0, 80, 80)), np.array((20, 255, 255)))
#     thresh2 = thresh.copy()

#     # find contours in the threshold image
#     contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

#     # finding contour with maximum area and store it as best_cnt
#     max_area = 0
#     best_cnt = 1
#     for cnt in contours:
#         print cnt
#         area = cv2.contourArea(cnt)
#         # print area

#         ## USE THIS FOR ONE DOT
#         # if area > max_area:
#         #     max_area = area
#         #     best_cnt = cnt

#         # USE THIS FOR MULTIPLE DOTS
#         max_area = area
#         best_cnt = cnt

#     # finding centroids of best_cnt and draw a circle there
#         M = cv2.moments(best_cnt)
#         print M
#         try: #IN CASE THERE IS 0 DIVISION
#             cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
#         except: cx, cy = 0, 0
#         # print cx, cy
#         cv2.circle(frame,(cx,cy),10,255,-1)

#     # Show it, if key pressed is 'Esc', exit the loop
#     cv2.imshow('frame',frame)
#     # cv2.imshow('thresh',thresh2)
#     if cv2.waitKey(33)== 27:
#         break

# # Clean up everything before leaving
# cv2.destroyAllWindows()
# cap.release()