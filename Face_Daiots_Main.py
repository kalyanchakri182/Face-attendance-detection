import face_recognition
import cv2
import os
import numpy as np
from scipy import spatial
from videocaptureasync import VideoCaptureAsync
from datetime import datetime
import csv
from gtts import gTTS
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from automail import *
from datetime import datetime
import csv
from os import path
from playsound import playsound
from welcome import *
from welcome1 import *
def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1,y1 = pt1
    x2,y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

#####################################################################################

def who_is_it(pred,employees):
    min_distance=0
    identity = "unknown"
    for (name,[idx,enc]) in employees.items():
        dist = 1 - spatial.distance.cosine(enc,pred)
        if dist > min_distance:
            min_distance=dist
            identity = name
            ids = idx
        if min_distance < 0.90:
            identity = "unknown"
            ids = 9999
    return min_distance,identity, ids

font = cv2.FONT_HERSHEY_TRIPLEX
cap =  VideoCaptureAsync(0).start()
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi', fourcc, 3.0, (640,480))

while True:
        ret,frame = cap.read()
        output = frame.copy()
        #try:
        if True:
            rgb = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb)
            face_encodings = face_recognition.face_encodings(rgb, face_locations)

            #id = 0
            ids = 0
            identity ="siri"
            now = datetime.now() # current date and time
            
            date_string = now.strftime("%y_%m_%d")
            time_string = now.strftime("%H:%M:%S")

            for (face_location,face_encoding) in zip(face_locations,face_encodings):
                top, right, bottom, left = face_location
                face = frame[top:bottom, left:right]
                employees = np.load('embeddings_face.npy',allow_pickle=True).item()
                min_distance,identity, ids = who_is_it(face_encoding,employees)
                

                if identity != "unknown":
                        #we1()
                        cv2.putText(output,"ID:" + str(ids), (left-160,bottom+80), font, 0.5, (255,255,0), 1, cv2.LINE_AA)
                        cv2.putText(output,"Name:" + str(identity),(left-160, bottom+60), font, 0.5, (255,255,0), 1, cv2.LINE_AA)
                        cv2.putText(output,"Date:" + str(date_string),(right-100,bottom+80), font,0.5, (255,255,0), 1, cv2.LINE_AA)
                        cv2.putText(output,"Time:" + str(time_string), (right-80,bottom+60), font, 0.5, (255,255,0), 1, cv2.LINE_AA)
                       
                        draw_border(output, (left, top), (right, bottom), (255,255, 255),3, 15, 10)
                        #we1()
                        mytext = identity
                        language = 'en'
                        myobj = gTTS(text=mytext+'attendancerecorded', lang=language, slow=False)
                        myobj.save("welcome.mp3")
                        os.system("mpg321 welcome.mp3")
                        
                        file_name = f'Attendance/Attendence_{date_string}.csv'
                        #if currunt moncuth folder not available, create curruntmonth folder like April_2021
                        
                        #file_name=f"{curunt_month_folder}/{file_name}"
                        if not path.exists(file_name):
                            with open(file_name, 'w') as f:
                                f.write(f'ID,Name,Date,Time\n')
                                f.close()
                        lines=[]
                        with open(file_name, 'r') as f:
                            lines=f.readlines()
                            f.close()
                            #print(lines)
                            data_to_check=f"{ids},{identity},{time_string},{date_string}"
                            #print(data_to_check)
                            existed=[line for line in lines if line.startswith(data_to_check)]
                            if(len(existed)==0):
                                lines.append(f"{ids},{identity},{date_string},{time_string}\n")
                        with open(file_name, 'w') as f:
                            f.writelines(lines)
                            f.close()
			       
                else:
                    cv2.putText(output,"Name: " + "Intruder", (left-100, bottom+50), font, 0.9, (255,255,0), 1, cv2.LINE_AA)
                    draw_border(output, (left, top), (right, bottom), (255,255, 255),3, 15, 10)
                    we()
        #except:
            #continue
        
        frame = cv2.resize(output, (640,480))
        cv2.imshow("frame",frame)
        #sout.write(frame)
        start = '18:05:20'
        end = '18:05:25'
        if time_string >start and time_string <end:
            au()
                
 
        #out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
