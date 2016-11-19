import RPi.GPIO as GPIO
import time
import subprocess
import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# config setup
last_image_loc = join(dirname(__file__), 'last.jpg')
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
  bash_command = "/opt/vc/bin/raspistill -w 300 -h 300 -n -t 1 -q 10 -dt -o " + last_image_loc
  process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  if error is not None:
    print(error)

def watson_check_debug():
  print('Watson Image Recognition')
  with open(last_image_loc, 'rb') as image_file:
    print(json.dumps(visual_recognition.classify(images_file=image_file, threshold=0.1, classifier_ids=['employees_387877154']), indent=2))
    
def watson_check():
  print('Watson Image Recognition')
  with open(last_image_loc, 'rb') as image_file:
    results = visual_recognition.classify(images_file=image_file, threshold=0.1, classifier_ids=['employees_387877154'])
    
    # get accused name from results
    persons = results["images"][0]["classifiers"][0]["classes"]
    persons.sort(key = lambda x: -x["score"])
    accused = str(persons[0]["class"])
    accuracy = str(persons[0]["score"])
    print('Identified ' + accused + ' (' + accuracy + ')')
    
    return accused
    
#def upload_to_aws(accused):
  # todo: upload to aws

while True:
  input_state = GPIO.input(18)
  if input_state == False:
    print('Button Pressed')
    take_pic()
    
    accused = watson_check()
    #watson_check_debug()
    
    #upload_to_aws(accused)
    time.sleep(10)