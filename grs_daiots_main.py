from busio import I2C
import adafruit_bme680
import time
import board
#import tinycircuits_wireling
# For OLED
import busio
from digitalio import DigitalInOut
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from os import path
from datetime import datetime
from time import sleep
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
from os import path
from aws_secrets import access_key,secret_access_key,schedule_interval
# connect aws console the package is boto3
import boto3
#conect with local directories
import os
import json
import schedule
import time
from time import sleep
import sys
import serial               #import serial pacakge
from time import sleep
import webbrowser
#import package for opening link in browser
import sys                  #import system package
import csv
from os import path

# Initialize and enable power to Wireling Pi Hat
#wireling = tinycircuits_wireling.Wireling()
OLED96_port = 0
BME680_port = 1
#wireling.selectPort(BME680_port)
# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, 0x77)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# A reset line may be required if there is no auto-reset circuitry
reset_pin = DigitalInOut(board.D10)

# use the 0.96" OLED Screen
#
#wireling.selectPort(OLED96_port)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=reset_pin) # 0.96" Screen

# Load a font
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)


client = boto3.client('s3',
                           aws_access_key_id = access_key,
                           aws_secret_access_key = secret_access_key)
Temprature=0
Tvoc=0
Humidity=0
Pressure=0
Altitude=0
def GPS_Info():
    global NMEA_buff
    global Latitude
    global Longitude
    
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]
    nmea_latitude = NMEA_buff[3]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[5] #extract time from GPGGA string           #convertr string into float for calculation
    if len(nmea_latitude)!=0 and len(nmea_longitude)!=0:
        print("inif")
        lat = float(nmea_latitude)                  #convert string into float for calculation
        longi =float(nmea_longitude)
        #print(lat)
        #print(longi)
        Latitude = str(convert_to_degrees(lat))
        Longitude = str(convert_to_degrees(longi))
        #print(Latitude)
        #print(Longitude)
        
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyAMA0")             #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
Latitude = 0
Longitude = 0    
def grs():
    now=datetime.now()         
    Date=now.strftime("%d-%m-%y")
    Time=now.strftime("%H:%M:%S")
    timstr=now.strftime("%H:%M:%S")
    filename=f'wheather_{timstr}.json'
    dictionary={"Date":Date,
                "Time":Time,
                "Temprature":[Temprature,"C"],
                "Tvoc":[Tvoc,"ohm"],
                "Humidity":[Humidity,"%RH"],
                "Pressure":[Pressure,"hpa"],
                "Altitude":[Altitude,"m"],
                "Latitude":Latitude,
                "Longitude":Longitude
                }
            
    json_object = json.dumps(dictionary,indent=4)
        #print(json_object)
    print(filename + "at 80")
    print(json_object)

            
            # Python program to update
    with open(filename, "w") as outfile:
  
    # Reading from json file
        outfile.write(json_object)
        
        

# that connects with working directories will send the files to s3 bucket 
    for file in os.listdir():
        print(filename + "at 91")
        if filename in file:
            upload_file_bucket = 'grs-main'
            upload_file_key = 'kalyan/' +str(file)
            client.upload_file(file, upload_file_bucket,upload_file_key)
    
schedule.every(int(schedule_interval)).minutes.do(grs)    

#interact with api to s3
try:
    while True:
        schedule.run_pending()
        #time.sleep(10)
        print("inwhile")
    
   #interact with api to s3
        tmpC = bme680.temperature
        tmpF = (tmpC * 1.8) + 32

        Temprature="%0.2f"%tmpC
        Tvoc="%d"%bme680.gas
        Humidity="%0.2f"%bme680.humidity
        Pressure="%0.2f"%bme680.pressure
        Altitude="%0.2f"%bme680.altitude
        
        display.fill(0)
        image = Image.new('1', (display.width, display.height))
        draw = ImageDraw.Draw(image)

    # Draw the text
        draw.text((0, 0),Temprature, font=font, fill=255)
        draw.text((0, 12),Tvoc, font=font, fill=255)
        draw.text((0, 24),Humidity, font=font, fill=255)
        draw.text((0, 36),Pressure, font=font, fill=255)
        draw.text((0, 48),Altitude, font=font, fill=255)
        

    # Display image
        display.image(image)
        display.show()
        time.sleep(.25)
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info() #get time, latitude, longitude
                 
except KeyboardInterrupt:
    pass           
                    

