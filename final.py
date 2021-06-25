#importing libraries

import cv2
import numpy as np
from tkinter import *
from PIL import ImageGrab

#For clearing canvas
def clear_widget():
    global cv
    cv.delete("all")
    
#<B1-Motion> 
def activate_event(event):
    global lastx, lasty
    cv.bind('<B1-Motion>', draw_lines)
    lastx, lasty = event.x, event.y
        
#For canvas drawing
def draw_lines(event):
    global lastx, lasty
    x, y = event.x, event.y
    cv.create_line((lastx, lasty, x, y), width = 8, fill = 'black', capstyle = ROUND, smooth = TRUE, splinesteps = 12)
    lastx, lasty = x, y
    
#Recognizing digit
def Recognize_Digit():
    global image_number
    predictions = []
    percentage = []
    filename = f'image_{image_number}.png'
    widget = cv
    
    #Getting widgit coordinates
    x = root.winfo_rootx() + widget.winfo_x()
    y = root.winfo_rooty()+widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    
    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)

    #Reading the image in color format
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    #Converting the image in grayscle
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Applying Otsu Thresholding
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    for cnt in contours:
        #Getting bounding box and extracting ROI
        x, y, w, h = cv2.boundingRect(cnt)
        #Creating rectangle
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 1)
        top = int(0.05 * th.shape[0])
        bottom = top + top
        left = int(0.05 * th.shape[1])
        right = left
        th_up = cv2.copyMakeBorder(th, top, bottom, left, right, cv2.BORDER_REPLICATE)
        #Extracting the image ROI
        roi = th[y - top:y + h + bottom, x - left:x + w + right]
        #Resizing roi image to 28x28 pixels
        img = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
        #Reshaping the image to support the model input
        img = img.reshape(1, 28, 28, 1)
        #Normalizing the image to support the model input
        img = img/255.0
        #Predicting the result
        pred = model.predict([img])[0]
        final_pred =  np.argmax(pred)
        data = str(final_pred) +'  '+ str(int(max(pred) * 100)) + '%'
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        color = (255, 0, 0)
        thickness = 1
        cv2.putText(image, data, (x, y-5), font, fontScale, color, thickness)
        
    #Showing the result on new window
    cv2.imshow('image', image)
    cv2.waitKey(0)


#Loading the model
from keras.models import load_model
model = load_model('model.h5')

#Creating main window
root = Tk()
root.resizable(0, 0)
root.title("HWDR APP")

#Initializing variables
lastx, lasty = None, None
image_number = 0


#Creating canvas for digits to draw
cv = Canvas(root, width = 640, height = 480, bg = 'white')
cv.grid(row = 0, column = 0, pady = 2, sticky = W, columnspan = 2)

cv.bind('<Button-1>', activate_event)

#Adding labels and buttons
btn_save = Button(text = "Process", command = Recognize_Digit)
btn_save.grid(row = 2, column = 0, pady = 1, padx = 1)
button_clear = Button(text = "Clear", command = clear_widget)
button_clear.grid(row = 2, column = 1, pady = 1, padx = 1)

root.mainloop()



















