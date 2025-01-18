# RUN HAPPY WHEN THE DETECTED EXPN IS HAPPY
# RUN UNHAPPY WHEN IT GETS BACK TO NORMAL, etc.
import subprocess

def happy():
    subprocess.Popen('google-chrome-stable https://www.complex.com/tag/sad', shell=True)
    pass

def angry():
    subprocess.run(['sudo', './scripts/angry/scramble.sh'])

def unangry():
    subprocess.run(['sudo', './scripts/angry/unscramble.sh'])

def sleepy():
    subprocess.run(['sh', './scripts/sleepy/sleepy.sh'])

def unsleepy():
    subprocess.run(['sh', './scripts/sleepy/unsleepy.sh'])

def sad():
    subprocess.run(['sh', './scripts/sad/sad.sh'])