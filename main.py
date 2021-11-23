from datetime import datetime
import time
import requests, json
import pvporcupine
#import speech_recognition as sr
import pyttsx3
import struct
#import pyaudio
import speech_recognition as sr
import pygame
from pygame.locals import *

pygame.init()

keepRuning = True
currentFace = "None"
global output
output = "Error"
#handle = pvporcupine.create(keywords=['picovoice'])
#r = sr.Recognizer()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Kansas City"
global API_KEY 
API_KEY = "82a239137d8704a9310012b355421da8"
global URL 
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 140)
porcupine = None
pa = None
audio_stream = None

#startup code

screen = pygame.display.set_mode((500, 500), RESIZABLE)

def uirun():
  global output
  running = True
  th = 0
  a = 255
  ti = 0
  dim = 0
  while running:
    w, h = pygame.display.get_surface().get_size()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the background with white
    screen.fill((0, 0, 25))

    # Draw img
    carImg = pygame.image.load('aiui.gif')
    ih = carImg.get_height()
    iw = carImg.get_width()
    font = pygame.font.Font('Amfallen.ttf', 32)
    text = font.render(str(output), True, (a,a,a))
    textRect = text.get_rect()
    th = th + 1
    if not output == "":
      if th > 100:  #slide up
          th = 100
          if ti <= 70:
              if int(th) >= 99:   #wait 7 sec
                  ti = ti + 1
                  time.sleep(0.1)
      if dim <= 255:     #dim away
          if ti > 69:
              print(("dim = ") + str(dim))
              print("ti = " + str(ti))
              a = a -1
              dim = dim + 1
              print("a =" + str(a))
              if a == 0:
                  print("reset")
                  output = ""
                  a = 255
                  dim = 0
                  ti = 0
                  th = 0
                      
              
      textRect.center = (w // 2, h // 2 + ih/2 - th)

      screen.blit(carImg, ((w/2)-(iw/2),(h/2)-(ih/2)))
      screen.blit(text, textRect)
      # Flip the display
      pygame.display.flip()

#Face code

def getFaceInfo():
  global output
  print("Get face name if avalible or set to none")
  printDataOut()

#Commands

def getWeather():
  global output
  global API_KEY
  global URL
  response = requests.get(URL)
  if response.status_code == 200:
    data = response.json()
    main = data['main']
    temperature = main['temp']
    temperature = int(temperature) - 273.15
    temperature = 1.8 * temperature + 32
    weather = data['weather']
    weather = weather[0]
    weather = weather['description']
    output = ("The weather is " + str(weather) + " with a temperture of " + str(int(temperature)) + " degrees.")
  elif response.status_code == 401:
    output = "Error getting the weather, check your openweathermap API code. Try again later. code = 401"
  else:
    output = "Error while getting weather! (Do you have a internet connection?) code = " + str(response.status_code)
  printDataOut()

def getTime():
  global output
  now = datetime.now()
  current_time = now.strftime("%H" + ":" +"%M")
  output = ("The current time is, " + (str(current_time)))
  printDataOut()
  

  #testing purposes only!
def printDataOut():
  print(str(output))
  print("Sending to tts!")
  sayoutput()
  
def get_next_audio_frame():
  pass
  
def sayoutput():
  global output
  engine.say(str(output))
  engine.runAndWait()
  uirun()
  

getWeather()
  #Now for the fun stuff
# while keepRuning == True:
#   try:
#    porcupine = pvporcupine.create(keywords=["picovoice", "blueberry"])
#    pa = pyaudio.PyAudio()
#    audio_stream = pa.open(
#                     rate=porcupine.sample_rate,
#                     channels=1,
#                     format=pyaudio.paInt16,
#                     input=True,
#                     frames_per_buffer=porcupine.frame_length)
#    while True:
#      pcm = audio_stream.read(porcupine.frame_length)
#      pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
#      keyword_index = porcupine.process(pcm)
#      if keyword_index >= 0:
#             print("Hotword Detected, talk now!")
#             r = sr.Recognizer()
#             with sr.Microphone() as source:
#               print("Say something!")
#               audio = r.listen(source)
#               voiceData = r.recognize_sphinx(audio)
#               print(voiceData)
#               if "weather" in str(voiceData):
#                 getWeather()
#               elif "time" in str(voiceData):
#                 getTime()
  # finally:
  #   if porcupine is not None:
  #     porcupine.delete()
  #   if audio_stream is not None:
  #     audio_stream.close()
  #   if pa is not None:
  #     pa.terminate()