import RPi.GPIO as GPIO
import time
import subprocess
import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# config setup
config = {}
with open(join(dirname(__file__), 'config.json'), 'rb') as data:
  config.update(json.load(data))

# watson setup
visual_recognition = VisualRecognitionV3('2016-05-20', api_key=config['watson_key'])

# button setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def take_pic():
  print('Taking Picture')
  bash_command = "/opt/vc/bin/raspistill -w 300 -h 300 -n -t 1 -q 10 -dt -o /home/pi/Desktop/coffee/new.jpg"
  process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()

def watson_test():
  print(json.dumps(visual_recognition.list_classifiers(), indent=2))

def watson_check():
  print('Watson Image Recognition')
  with open(join(dirname(__file__), '../coffee/new.jpg'), 'rb') as image_file:
    print(json.dumps(visual_recognition.classify(images_file=image_file, threshold=0.1, classifier_ids=['employees_387877154']), indent=2))

while True:
  input_state = GPIO.input(18)
  if input_state == False:
    print('Button Pressed')
    take_pic()
    watson_check()
    time.sleep(0.2)