import dotenv
from openai import OpenAI
import dotenv
from gtts import gTTS
import speech_recognition as sr
import os
import json
from tools import tools, get_current_date, get_weather, get_ip, location, crawl4ai, search_duckduckgo, search_wikipedia

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv('api_key')
api_endpoint = os.getenv('api_endpoint')

def init_openai_client():
    return OpenAI(base_url=api_endpoint, api_key=api_key)

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
                          "Halte dich bitte immer so kurz und präzise wie möglich. Bitte nutze keine Emojis. Gebe immer genaue Informationen, es geht um die Kariere des Nutzers."
                          "Nutze die verfügbaren Funktionen für Datum/Uhrzeit, Wetterabfragen, IP-Adressen und Standortinformationen."
            },
            {"role": "user", "content": user_input}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Check if the model wants to call functions
    if message.tool_calls:
        # Create a list to store function responses
        function_messages = []
        
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            try:
                function_args = json.loads(tool_call.function.arguments)
            except:
                function_args = {}

            # Execute the function
            if function_name == "get_current_date":
                result = get_current_date()
            elif function_name == "get_weather":
                result = get_weather(**function_args)
            elif function_name == "get_ip":
                result = get_ip()
            elif function_name == "location":
                result = location()
            elif function_name == "crawl4ai":
                result = crawl4ai()
            elif function_name == "search_duckduckgo":
                result = search_duckduckgo(**function_args)
            elif function_name == "search_wikipedia":
                result = search_wikipedia(**function_args)
            else:
                continue

            function_messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(result)
            })

        # Get the final response
        second_response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein hilfsbereiter Assistent. Antworte stets auf Deutsch. "
                              "Halte dich bitte immer so kurz und präzise wie möglich. Bitte nutze keine Emojis."
                },
                {"role": "user", "content": user_input},
                message,
                *function_messages
            ]
        )
        return second_response

    return response

def text_to_speech(text):
    tts = gTTS(text=text, lang='de')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    client = init_openai_client()

    while True:
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

        print("Bereit für die nächste Eingabe...")

if __name__ == "__main__":
    main()
