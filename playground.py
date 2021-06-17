import deepspeech
import wave
import numpy as np
import librosa
import re
from pynput.keyboard import Key, Controller
import sounddevice as sd
from scipy.io.wavfile import write
from processor import AdminProcessor, InvalidAdminCommand
from pynput.keyboard import Key, Controller



def audio_to_int16(data):
    return (np.array(data) * 32767).astype(np.int16)


seconds = 7  # Duration of recording
model_path = '/home/rafal/Models/Speech/deepspeech-0.9.3-models.tflite'
scorer_path = '/home/rafal/Models/Speech/deepspeech-0.9.3-models.scorer'
audio_path = 'output.wav'

hot_words = []
hot_words.extend(
    'driver time penalty stop go  command clear all one two three four five six seven eight nine number punish disqualify'.split(
        ' '))

admin_commands = AdminProcessor()

keyboard = Controller()

model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)
sample_rate = model.sampleRate()

for word in hot_words:
    model.addHotWord(word, 1.0)
# lm_alpha = 0.75
# lm_beta = 1.85
# model.setScorerAlphaBeta(lm_alpha, lm_beta)

print('Recording')
my_recording = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  # Wait until recording is finished
print('Stopped recording')
write(audio_path, sample_rate, my_recording)  # Save as WAV file

y, s = librosa.load(audio_path, sr=sample_rate)
y = audio_to_int16(y)

text = model.stt(y)

print(text)

try:
    command = admin_commands.get(text)
    if command is not None:
        keyboard.type(command)
except InvalidAdminCommand:
    print('Invalid Admin Command!')


