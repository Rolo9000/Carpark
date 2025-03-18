# combined anpr and video
import cv2
from fastanpr import FastANPR # this line is taking a while for some reason? - shouldn't matter is continously running
import asyncio # for aync function so can use await
import numpy as np
import time

fast_anpr = FastANPR() # creates instance of FastANPR

class NumberPlateOutput:
    def __init__(self, det_box, det_conf, rec_poly, rec_text, rec_conf):
        self.det_box = det_box
        self.det_conf = det_conf
        self.rec_poly = rec_poly
        self.rec_text = rec_text
        self.rec_conf = rec_conf




# Run ANPR on the image/s
async def run_anpr(image : np.array): # image will already be type numpy array
    number_plates = await fast_anpr.run(image) # Await the coroutine

    # Print out/store results:

    for number_plate in number_plates: # sample no.plate var returned:[NumberPlate(det_box=[682, 414, 779, 455], det_conf=0.299645334482193, rec_poly=[[688, 420], [775, 420], [775, 451], [688, 451]], rec_text='BVH826', rec_conf=0.9406909346580505)]
        if len(number_plate) == 0: # if no number plates found - list will be empty
            # print("No number plates found") # commented out so program not constantly printing
            return NumberPlateOutput(0, 0, 0, "", 0)
        # note - have to do 0s like this bc numberplate still effectively in list - first item (see sample above)
        detBox = ( number_plate[0].det_box)
        detConf = ("Detection confidence:", number_plate[0].det_conf) # probs wont use - comment out
        recText = (number_plate[0].rec_text)
        recPoly = ("Recognition polygon:", number_plate[0].rec_poly) # probs wont use - comment out
        recConf = (number_plate[0].rec_conf)
        print(f"Plate Attributes:\nDetection bounding box: {detBox}\nRecognition text: {recText}\nRecognition confidence: {recConf}\n\n") # can probs get rid of thkis after testing
        output1 = NumberPlateOutput(detBox, detConf, recPoly, recText, recConf) # creates instance of NumberPlateOutput class (so all contained in one object that can access indiv. values of)
        return output1







# ---------- POINT A -------------------
# Video capture and motion detection:

threshold = 0.3 # threshold of how diff images need to be in order to capture frame and check for anpr. (may want to play around with later to test)


cap = cv2.VideoCapture(1) # cap will be the current video (probs using webcam/ip stream), 0 uses the defualt webcam**, 1 uses next cam e.g. when using droid cam

lastMean = 0 # bc for first farme there won't be a previous frame to compare to

while True:
    #print("a") # used to distinguish between frames in testing
    time.sleep(1) # waits 1 sec so not constantly checking frames, also cars likely wont be going fast enough to get past all of camera view in 1 sec
    ret, frame = cap.read()# Read a frame from the video capture.
                          # 'ret' indicates whether the frame was read successfully (True/False)
                          # 'frame' contains the captured image data (type: NumPy array - fine as anpr processing uses numpy array aswell)
    cv2.imshow('frame',frame)  # Display the captured frame in a window named 'frame'. (PROBS NOT NEEDED? - try it)
    # now check for motion:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # gets grayscale image (easier that checking for colour difference in frames)
    #cv2.imshow('frame',gray) # displays image - again, probs not needed - can comment out later
    result = np.abs(np.mean(gray) - lastMean) # calcs means of image then subratcs from mean of last image to get diff. (uses abs so +ve value)
    #print(f"mean gray: {np.mean(gray)}")
    #print(f"last mean: {lastMean}")
    
    #print(result) # prints diff of frame - probs will want to comment out after so not constantly printing while program running
    if result > threshold: # set threshold at start of program so can easily change it
      #print("Motion detected") # MAY want for testing / to display on gui
      outputA = asyncio.run(run_anpr(frame)) # calls anpr function (frame is already type numpy array)
    # CODE HERE TO DETECT REG PLATE + ADD TO DATABASE
    lastMean= np.mean(gray) # now sets current mean to last so can redo loop with next frame

    if (cv2.waitKey(1) & 0xFF == ord('q')):# Check if the 'q' key was pressed (using q as escape key)
        # cv2.waitKey(1) waits for 1 millisecond for a key press
        # & 0xFF is a bitwise AND operation to ensure we only consider the last 8 bits of the key code
        # ord('q') gets the ASCII value of the 'q' character
        break  # If 'q' was pressed, exit the loop

cap.release()# Release the VideoCapture object, freeing the webcam resources
cv2.destroyAllWindows()  # Close all OpenCV windows

# can also go on terminal and press ctrl + c to stop program if q doesn't work


# ---------- POINT B -------------------




