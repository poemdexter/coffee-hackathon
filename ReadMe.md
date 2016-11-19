# Coffee Hackathon - Hackathon Project

### Overview
This project is the **CoffeeWatch** entry for the AT&T Hackathon at The DEC in Dallas on Nov 18th to 19th.

It is a python script running as a service on a headless Raspberry Pi 3.  There is also a java project in `coffee-status` for the Alexa skill.

**100% of the code was written here at the hackathon.**

### Purpose

The purpose of the project was to create an IoT coffee pot that would keep track of who took the last cup of coffee but didn't make another pot.  If someone uses the pot and it's empty, they can ask Alexa (Amazon Dot) who took the last cup of coffee.  Optionally, they can also ask Alexa to shame that person which causes the accused person's photo to be posted on twitter.

### Technologies Used / Flow

1. It uses an ***arduino button*** wired to the ***Raspberry Pi 3*** input pins to fire an event to a ***Python script***.  
2. That event causes a ***camera*** attached to the Raspberry Pi 3 to snap a picture and save it to disk.
3. That picture is then sent to ***Watson Visual Recognition*** via the ***python-sdk*** to identify who is in the photo.  A custom classifier was created and 2 sets of photos of each of the developers were used to teach Watson.
4. The next time someone gets coffee, the previous picture and name of person are uploaded to ***Amazon S3*** via the ***boto3*** python library.
5. If someone wants to know who used the coffee pot last they ask ***Alexa (Amazon Dot)***.  The Alexa skill was written in ***Java*** using the ***Amazon AWS SDK***, ***Alexa Skill SDK***, and ***Amazon Lambda SDK*** and deployed toAmazon Lambda.
6. If someone wants to shame the last person to use the coffee pot, Alexa will tweet using ***Twitter4J*** using the uploaded photo and name.

### Configuration

* A `config.json` file must be created populated with the Watson service credentials key and the Amazon S3 bucket name.  An example of this config can be found in `config_example.json`
* Amazon CLI must be installed and configured on the Raspberry Pi.
* `takeTimPics.sh` and `takeDanielPics.sh` can be used to create 50+ pics of someone using the Raspberry Pi 3 camera.
* After zipping those pics, `watson_training.py` can be used to teach Watson.
* Running coffee.py will start the process that waits for a button press.
