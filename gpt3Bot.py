import openai
import pyttsx3
import speech_recognition as s_r
import pyaudio
from api_key import API_KEY

# print(s_r.__version__)


openai.api_key = API_KEY

engine = pyttsx3.init()

r = s_r.Recognizer()
mic = s_r.Microphone(device_index=2)
# print(s_r.Microphone.list_microphone_names())

conversation = ""
user_name = "You"
bot_name = "Jarvis"

while True:
    with mic as source:
        print("\nOuvindo...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening.\n")

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ": " + user_input + "\n" + bot_name + ": "

    conversation += prompt  # allows for context

    # fetch response from open AI api
    response = openai.Completion.create(
        engine='text-davinci-003', prompt=conversation, max_tokens=100)
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(
        user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]

    conversation += response_str + "\n"
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()
