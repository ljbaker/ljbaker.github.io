# Face-Rating Experiment

This page features all the code and stimuli necessary to run a facial categorization experiment through Amazon's Mechanical Turk. This experiment used a combination of Python and JavaScript, and has been annotated for use in future experiments. There is no citation for this study yet, but please contact me if you would like to adapt the code for personal or academic use.

## The CAFE Dataset

Thousands of studies have explored the recognition of emotion from faces alone, going all the way back to the days of Wundt, Titchener and James. However, nearly all of these investigations have been limited ot the facial expressions of adults. Lobue and Thrasher (2015) addressed this void by creating the Child Affective Facial Expression set (CAFE). The set contains photographs of 154 racially and ethnically diverse 2- to 8-year-old children posing for six emotional facial expressions (angry, disgusted, fearful, happy, sad, and surprised) as well as a resting neutral expression. Facial expressions were further labeled for "open" or "closed" mouths for angry, fearful, happy, sad and neutral faces. Disgust expressions were uniquely coded as with or without a protruding tongue. Altogether, the set contains 1192 images. 

## Applications in Machine Learning

Recognizing the emotional state of individuals, particularly children, is a necessary and labor-intensive task with many frutful applications. Psychologists often look at facial expression as an explanation for later behavior, such as studying the role of affect in the treatment of social anxiety. However, marketing and educational applications are legion. Advertising companies are often interested in the emotional response elicted by one of their campaigns, and an educational video game would benefit from identifying points where children demonstrate frustration.

The current methods of tagging emotional state are sorely lacking. Most often, teams of trained researchers move through video recordings frame by frame, manually labelling and validating the emotinal state at any given point in time. We have begin implementing machine learning methods to automate this process, using the CAFE set as training data. To expand the generalizability of this set, we are collecting hundreds to thousands of emotional faces online. The attached experiment asks online raters to categorize these new faces into seven descrete emotional states: angry, disgusted, fearful, happy, sad, surprised and neutral. These new validated stimuli will be added to our machine learning algorithm with the hope of better increasing the accuracy of the classifier.

## The Current Experiment

The entirety of the experiment is contained in the CAFE_face_rating.html page. This document uses the jsPsych package library to receive input from Mechanical Turk workers. The entirety of the jsPsych library is located in this repository for easy implimentation for future projects. Please download the library from https://github.com/jodeleeuw/jsPsych and give the team propper credit. Data is submitted as a string to mechanical turk using the mmturkey package (https://github.com/longouyang/mmturkey), which is highly recommended. The CAFE set and associated permissions of use are property of Vanessa Lobue, Associate Professor, Rutgers University. All interested parties should contact her before use. 

### Design


### Interface with Mechanical Turk
### Data Collection & Analysis
