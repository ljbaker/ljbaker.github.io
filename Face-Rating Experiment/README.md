# Face-Rating Experiment

This page features all the code and stimuli necessary to run a facial categorization experiment through Amazon's Mechanical Turk. This experiment used a combination of Python and JavaScript, and has been annotated for use in future experiments. There is no citation for this study yet, but please contact me if you would like to adapt the code for personal or academic use.

## The CAFE Dataset

Thousands of studies have explored the recognition of emotion from faces alone, going all the way back to the days of Wundt, Titchener and James. However, nearly all of these investigations have been limited ot the facial expressions of adults. Lobue and Thrasher (2015) addressed this void by creating the Child Affective Facial Expression set (CAFE). The set contains photographs of 154 racially and ethnically diverse 2- to 8-year-old children posing for six emotional facial expressions (angry, disgusted, fearful, happy, sad, and surprised) as well as a resting neutral expression. Facial expressions were further labeled for "open" or "closed" mouths for angry, fearful, happy, sad and neutral faces. Disgust expressions were uniquely coded as with or without a protruding tongue. Altogether, the set contains 1192 images. 

## Applications in Machine Learning

Recognizing the emotional state of individuals, particularly children, is a necessary and labor-intensive task with many frutful applications. Psychologists often look at facial expression as an explanation for later behavior, such as studying the role of affect in the treatment of social anxiety. However, marketing and educational applications are legion. Advertising companies are often interested in the emotional response elicted by one of their campaigns, and an educational video game would benefit from identifying points where children demonstrate frustration.

The current methods of tagging emotional state are sorely lacking. Most often, teams of trained researchers move through video recordings frame by frame, manually labelling and validating the emotinal state at any given point in time. We have begin implementing machine learning methods to automate this process, using the CAFE set as training data. To expand the generalizability of this set, we are collecting hundreds to thousands of emotional faces online. The attached experiment asks online raters to categorize these new faces into seven descrete emotional states: angry, disgusted, fearful, happy, sad, surprised and neutral. These new validated stimuli will be added to our machine learning algorithm with the hope of better increasing the accuracy of the classifier.

## The Current Experiment

The entirety of the experiment is contained in the CAFE_face_rating.html page. This document uses the jsPsych package library to receive input from Mechanical Turk workers. The entirety of the jsPsych library is located in this repository for easy implimentation for future projects. Please download the library from https://github.com/jodeleeuw/jsPsych and give the designer propper credit. Data is submitted as a string to mechanical turk using the mmturkey package (https://github.com/longouyang/mmturkey), which is highly recommended. The CAFE set and associated permissions of use are property of Vanessa Lobue, Associate Professor, Rutgers University. All interested parties should contact her before use. 

### Design

The design is quite simple. Requisite plugins from the jsPsych library are imported at the top of the html page Each step of the experiment is declared as a variable with specific properties from the jsPsych plugin functionality. An initial check verifies that individuals are participating via Amazon Mechanical Turk and that they have accepted the HIT (see next section). Participants are asked to accept the consent document linked as informed_consent.html, and a pop-up window informs participants who do not consent that they cannot continue with the experiment. 

The body of the experiment begins with a redundant entry of participants' AMT ID (this is for internal validation, as Amazon automatically records their AMT ID's) and their age. Participants are then given instructions befor continuing to the test block.

The test block imports images aggregated from the CAFE set and new images obtained from the internet, located in the 'all_faces' folder. At the start of the experiments, participants are randomly assigned to categorize a subset of these images (roughly 100 of the 1000 total images). For each image, participants clock a button corresponding to their best guess of the image's emotional state. Additionally, 7 charicatured emotions (or emojis) are included as an attention check. Ideally, all participatns should correctly categorize the emojis. Those that do not may be removed from analysis.

Upon completion of the test block, participants are asked some general questions about themselves and their exposure to young children as possible covariates in categorization performance. Their data is then automatically uploaded to Mechanical Turk.

### Interface with Mechanical Turk

#### Access and Secret Access Keys

To embed the code within a Mechanical Turk iframe window, it is first necessary to retrieve access and security keys from Amazon. Instructions can be found at http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html. For security purposes, **access and security keys should never be kept in a publicly accessible location.** Here, I placed the keys in a the python file 'config.py' which is stored locally. 

#### Creating a Mechanical Turk HIT

Mechanical turk assigns requests to workers using HITs (Human Inteligence Tasks). Here, we upload HIT's directly to Mechanical Turk using a simple Python script, 'create_hit.py', that specifies the requirements of the HIT, including the duration of the HIT, the requriements of workers who can see the HIT, and the pay for completion of the HIT. It is recommended that users familiarize themselves with AMT before uploading HITs in this manner. Once configured, the HIT was posted by running the script through the terminal window (on Mac: python create_hit.py)

### Data Collection & Analysis
