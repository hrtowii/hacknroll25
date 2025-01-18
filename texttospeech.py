from openai import OpenAI
import vlc
client = OpenAI(base_url="https://api.kokorotts.com/v1", api_key="not-needed")
def speak_text(text: str):
    print(f"generating audio: {text}")
    response = client.audio.speech.create(
        model="kokoro",
        voice="af_bella+af_sky",
        input=text,
        response_format="mp3"
    )
    response.stream_to_file("temp.mp3")
    p = vlc.MediaPlayer("temp.mp3")
    p.play()
    return None
