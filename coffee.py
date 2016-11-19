import RPi.GPIO as GPIO
import os
import time
import subprocess
import json
import boto3
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3


# config setup
last_image_loc = join(dirname(__file__), 'last.jpg')
last_name_loc = join(dirname(__file__), 'last.txt')
config = {}
with open(join(dirname(__file__), 'config.json'), 'rb') as data:
  config.update(json.load(data))

# watson setup
visual_recognition = VisualRecognitionV3('2016-05-20', api_key=config['watson_key'])

# amazon S3 setup
s3 = boto3.resource('s3')

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
    
    # save accused name
    last_name = open(last_name_loc, "w")
    last_name.write(accused)
    last_name.close()
    
def upload_to_aws():
  if os.path.isfile(last_image_loc) and os.path.isfile(last_name_loc):
    # upload last image to S3
    print('Uploading pic to S3')
    last_pic = open(last_image_loc, 'rb')
    s3.Bucket(config["s3_bucket"]).put_object(Key='last.jpg', Body=last_pic)

    # upload last name to S3
    print('Uploading name to S3')
    last_name = open(last_name_loc, 'rb')
    s3.Bucket(config["s3_bucket"]).put_object(Key='last.txt', Body=last_name)
  
while True:
  input_state = GPIO.input(18)
  if input_state == False:
    print('Button Pressed')
    
    upload_to_aws()
    
    take_pic()
    
    watson_check()
    #watson_check_debug()
    
    print('Waiting 10 seconds')
    time.sleep(10)