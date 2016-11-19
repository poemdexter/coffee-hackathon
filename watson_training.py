import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# config setup
config = {}
with open(join(dirname(__file__), 'config.json'), 'rb') as data:
  config.update(json.load(data))

# watson setup
visual_recognition = VisualRecognitionV3('2016-05-20', api_key=config['watson_key'])

with open(join(dirname(__file__), 'daniel.zip'), 'rb') as daniel, open(join(dirname(__file__), 'tim.zip'), 'rb') as tim:
  print(json.dumps(visual_recognition.create_classifier('employees', daniel_positive_examples=daniel, tim_positive_examples=tim), indent=2))