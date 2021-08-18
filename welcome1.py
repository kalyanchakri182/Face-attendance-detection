from pydub import AudioSegment
from pydub.playback import play

def we1(): 

       sound = AudioSegment.from_mp3('attendance.mp3')
       play(sound)
