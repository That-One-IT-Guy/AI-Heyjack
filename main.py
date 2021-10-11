import time
import pvporcupine
import speech_recognition as sr


keepRuning = True
currentFace = "None"
global output
output = "Error"
handle = pvporcupine.create(keywords=['picovoice'])
r = sr.Recognizer()

#Face code

def getFaceInfo():
  global output
  print("Get face name if avalible or set to none")
  printDataOut()

#Commands

def getWeather():
  global output
  print("Get weather for weather comand")
  printDataOut()

def getTime():
  global output
  print("getTime")
  printDataOut()
  
def printDataOut():
  print(str(output))
  
def get_next_audio_frame():
  pass
  
  #Now for the fun stuff
while keepRuning == True:
  print("Main loop goes here")
  keyword_index = handle.process(get_next_audio_frame())
  if keyword_index >=0:
    handel.delete()
    with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source)
    print("Time over, thanks")
    #inset get command stt here
    print("got hotword!")
    pass
  
