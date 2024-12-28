from openai import OpenAI
import dotenv
from gtts import gTTS
import speech_recognition as sr
import os
import json
from tools import tools, get_current_date, get_weather
import openwakeword
import pyaudio
import numpy as np
import time

# API Konfiguration laden
api_key = dotenv.get_key('.env', 'api_key')
api_endpoint = dotenv.get_key('.env', 'api_endpoint')

def init_openai_client():
    return OpenAI(base_url=api_endpoint, api_key=api_key)

def init_wake_word_detector():
    model = openwakeword.Model(wakeword_models=["ok_google"])
    return model

def wait_for_wake_word(model):
    print("Warte auf Aktivierung...")
    
    # Setup audio stream
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    try:
        while True:
            audio_data = stream.read(1024, exception_on_overflow=False)
            # Convert audio to numpy array
            audio_data = np.frombuffer(audio_data, dtype=np.float32)
            
            # Get predictions
            predictions = model.predict(audio_data)
            
            # Check if wake word detected
            if predictions[0][0] > 0.5:  # Confidence threshold
                print("Wake Word erkannt!")
                break
                
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bitte sprechen Sie jetzt...")
        return r.listen(source)

def get_ai_response(client, user_input):
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system", 
                "content": "Du bist ein hilfsbereiter Assistent. Antworte stets auf Deutsch. "
                          "Halte dich bitte immer so kurz und präzise wie möglich. Bitte nutze keine Emojis. "
                          "Nutze die verfügbaren Funktionen für Datum/Uhrzeit und Wetterabfragen."
            },
            {"role": "user", "content": user_input}
        ],
        tools=tools
    )

    message = response.choices[0].message

    # Check if the model wants to call functions
    if message.tool_calls:
        function_responses = []
        
        # Handle each tool call
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Call the appropriate function
            function_response = None
            if function_name == "get_current_date":
                function_response = get_current_date()
            elif function_name == "get_weather":
                function_response = get_weather(**function_args)

            if function_response:
                function_responses.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })

        # Get updated response with function results
        messages = [
            {
                "role": "system", 
                "content": "Du bist ein hilfsbereiter Assistent. Antworte stets auf Deutsch. "
                          "Halte dich bitte immer so kurz und präzise wie möglich. Bitte nutze keine Emojis."
            },
            {"role": "user", "content": user_input},
            message,
            *function_responses
        ]

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages
        )

    return response

def text_to_speech(text):
    tts = gTTS(text=text, lang='de')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    print("Initialisiere Wake Word Detector...")
    
    client = init_openai_client()
    wake_word_model = init_wake_word_detector()
    
    while True:
        wait_for_wake_word(wake_word_model)
        print("Ich höre zu...")
        
        try:
            audio = record_audio()
            r = sr.Recognizer()
            user_input = r.recognize_google(audio, language='de-DE')
            print("Sie sagten: " + user_input)

            response = get_ai_response(client, user_input)
            response_text = response.choices[0].message.content
            print(response_text)

            text_to_speech(response_text)

        except sr.UnknownValueError:
            print("Entschuldigung, ich konnte Sie nicht verstehen")
        
        print("Warte auf neue Aktivierung...")

if __name__ == "__main__":
    main()
