from pydub import AudioSegment
from pydub.playback import play
#import pyttsx3
def we(): 

       sound = AudioSegment.from_mp3('intruder.mp3')
       play(sound)
        #engine = pyttsx3.init() #initializing engine
        #engine.say('kalyan')
        #engine.runAndWait()