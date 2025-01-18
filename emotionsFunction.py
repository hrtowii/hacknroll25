import subprocess

def happy():
    subprocess.Popen('google-chrome-stable https://www.complex.com/tag/sad', shell=True)
    pass

def angry():
    subprocess.run(['sudo', './scripts/angry/scramble.sh'])

def unangry():
    subprocess.run(['sudo', './scripts/angry/unscramble.sh'])