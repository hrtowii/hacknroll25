from openai import OpenAI
import simpleaudio
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
    wave_object = simpleaudio.WaveObject.from_wave_file('temp.mp3')
    print('playing sound using simpleaudio')

    # define an object to control the play
    play_object = wave_object.play()
    play_object.wait_done()
