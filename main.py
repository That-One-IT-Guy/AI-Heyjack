from datetime import datetime
from threading import Thread
import speech_recognition as sr
import struct
import pyaudio
import pvporcupine
import playsound
import os
import time
import requests, json
#import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import pygame
from pygame.locals import *
pygame.init()


keepRuning = True
currentFace = "None"
global output
global rawOut
rawOut = ""
output = "Error"
#handle = pvporcupine.create(keywords=['picovoice'])
#r = sr.Recognizer()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Kansas City"
global API_KEY 
#API_KEY = "82a239137d8704a9310012b355421da8"
API_KEY = "5dd8ff9a2f0e159dd83a44d2281a8e9d"
global URL 
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 140)


#Face code

def getFaceInfo():
  global output
  print("Get face name if avalible or set to none")
  printDataOut()

#ui

def uiRun():
  screen = pygame.display.set_mode((500, 500), RESIZABLE)
  # Run until the user asks to quit
  global output
  running = True
  font = pygame.font.Font('Amfallen.ttf', 32)
  th = 0
  a = 255
  ti = 0
  dim = 0
  carImg = pygame.image.load('aiui.gif')
  ih = carImg.get_height()
  iw = carImg.get_width()
  while running:
    w, h = pygame.display.get_surface().get_size()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the background
    screen.fill((5,1,23))
      
    if not output == "":
      text = font.render(str(output), True, (a,a,a))
      textRect = text.get_rect()
      th = th + 1
      if th >= 100:  #slide up
        th = 100
        if ti <= 50:
          if th >= 99:    #wait 5 sec
            ti = ti + 1
            time.sleep(0.1)
            if dim <= 255:
              if ti >= 49:     #dim away
                ti = 48
                a = a -5
                dim = dim + 5
                if a == 0:
                  a = 255
                  dim = 0
                  ti = 0
                  th = 0
                  output = ""  
    else:
      text = font.render(str(output), True, (a,a,a))
    textRect.center = (w // 2, h // 2 + ih/2 - th)
    screen.blit(carImg, ((w/2)-(iw/2),(h/2)-(ih/2)))
    screen.blit(text, textRect)
    # Flip the display
    pygame.display.flip()
  # Done! Time to quit.
  pygame.quit()

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
    output = "Error getting the weather, check your openweathermap API code. Try again later. code: 401"
  else:
    output = "Error while getting weather! (Do you have a internet connection?) code = " + str(response.status_code)
  printDataOut()

def getTime():
  global output
  now = datetime.now()
  current_time = now.strftime("%H" + ":" + "%M")
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
  language = 'en'
  myobj = gTTS(text=output, lang=language, slow=False)
  myobj.save("temp.mp3")
  pygame.mixer.init()
  pygame.mixer.music.load('temp.mp3')
  pygame.mixer.music.play()
  clock = pygame.time.Clock()
  while pygame.mixer.music.get_busy():
      pygame.event.poll()
      clock.tick(10)
  pygame.mixer.quit()
  os.remove("temp.mp3")
  print("sayoutput finished")

#check for wake word
def getWake():
  try:
    porcupine = pvporcupine.create(keywords=["porcupine"])

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Hotword Detected")
            getSTT()

  finally:
      if porcupine is not None:
          porcupine.delete()

      if audio_stream is not None:
          audio_stream.close()

      if pa is not None:
              pa.terminate()

#get stt data
def getSTT():
  global output
  global rawOut
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source)
    print("Time over, thanks")
    
    try:
        textdata = r.recognize_google(audio_text)
        rawOut = textdata
        getCom()
    except Exception as e:
         print(e)

  #get comand data
def getCom():
  global rawOut
  global output
  print(rawOut)
  if "time" in rawOut:
    getTime()
  elif "weather" in rawOut:
    getWeather()
  else:
    print("Command not found!")
  
#run code
if __name__ == '__main__':
  Thread(target = uiRun).start()
  Thread(target = getWake).start()
  
