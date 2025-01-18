import time
import emotionsFunction
from texttospeech import speak_text

print("sleepy")
emotionsFunction.sad()
emotionsFunction.sleepy()

time.sleep(10)

print("unsleepy")
emotionsFunction.unsleepy()

speak_text('''Oh, look at this guy, he's a real winner. I mean, just look at that hair, it's like he stuck his finger in a socket and it just wouldn't stop. And those glasses, oh boy, they're so big they're practically a pair of binoculars. I'm surprised he can even see his own face with those things on. And that lanyard, "SHACKERS" - is that supposed to be a joke? Because it's not funny, it's just sad. This guy is a walking disaster, a hot mess express. I'm not even sure what's more embarrassing, his hair or his fashion sense. But hey, at least he's trying, right? I mean, it's not like he's actually succeeding at anything. He's just a big ol' mess, and I'm here for it. So, keep on rocking those glasses, buddy, and that lanyard, and that hair - you're a true original.''')
