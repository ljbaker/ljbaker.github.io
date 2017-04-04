# Face Categorization Experiment

This repository features all the code and stimuli necessary to run a change-probability experiment in Mechanical Turk. This experiment used a combination of Python and JavaScript, and has been annotated for use in future experiments. There is no citation for this study yet, but please contact me if you would like to adapt the code for personal or academic use.

## Change Detection

Despite our subjective experience of a full and complete visual world around us at all times, human visual system is surprisingly limited. At any given point in time your visual system dedicates the majority of processing to a foveated region between 4-5 degrees of visual angle, or about the size of your thumbnail at arm's distance. The majority of our visual experience is inference, gist (overall impressions of what a scene is based on global properties; i.e., "inside","a beach", etc.; [Davenport & Potter, 2004](http://journals.sagepub.com/doi/abs/10.1111/j.0956-7976.2004.00719.x)), or a handful of items held in working memory ([Luck & Vogel, 1997](http://www.nature.com/nature/journal/v390/n6657/abs/390279a0.html)).

One of the most striking demonstrations of these limitations is the phenomenon of change blindness. Observers struggle to detect differences between two alternating photographs with a filter placed in-between ([O'Reagan, Rensink & Clark, 1999](http://www.nature.com/nature/journal/v398/n6722/abs/398034a0.html)), and rarely notice differences when given no indication a change exists ([Simons & Levin, 1997](http://journals.sagepub.com/doi/abs/10.1111/j.0956-7976.2004.00719.x)). Most of the work on change blindness looks at the former situation, where participants are explicitly aware of a change. However, less is known of implicit change blindness, or the general awareness of our changing world. Given that human beings are adapted to navigate the real world with a minimum of catastrophic failures to detect relevant stimuli, the failures of awareness revealed by implicit change blindness suggest that the visual system prioritizes some information above others.

## Bayesian Perception

Previous work from our lab has demonstrated a "Bayesian-ness" of perception. Following the rules of probability, the human visual system adapts to prior information to anticipate future information. The visual system suppresses sensory activation for probable statistical properties (i.e., horizontal lines, which permeate the typical visual field), becoming more sensitive to less probable properties (i.e., oblique lines).

Decades of research have further demonstrated that statistical properties of contrast, color and motion predict the guidance of low-level attention, a phenomenon known as **salience**. Salience guides rapid attention (and the first few eye movements within a scene), as well as he detection of changes in a scene ([Wright, 2005](http://booksandjournals.brillonline.com/content/journals/10.1163/1568568054389633)), higher level information appears to guide later eye movements ([Stirk & Underwood, 2007](http://jov.arvojournals.org/article.aspx?articleid=2192967)). Furthermore, salience can predict memory for explicitly encoded material (e.g., words displayed with bold or faint lettering), but does not appear to influence passive recall of items in scene perception.

Just as likely visual properties update the sensitive of low-level vision, it is possible that implicit visual attention prioritizes those items that are most likely to change meaningfully in the future. Research has demonstrated that this may be the case. Participants are more likely to detect likely changes (e.g., a coffee cup disappearing) than unlikely ones (e.g., a window disappearing). Further research has demonstrated that this trend is adaptive, finding that viewers engaged in an explicit change-detection task with weighted probabilities to feature changes (e.g., color more likely to change than shape) detected more probable changes and fewer improbable changes over time.

## The Current Experiment

This study examines the speed and accuracy of explicit change detection in natural scenes based on salience and change probability.

In the first experiment, individuals rate a subset of objects in a scene on their likelihood of changing within the next few minutes, hours or days.

In the second experiment, individuals explicitly detect changes between two otherwise identical scenes.

We will then analyze the speed and accuracy of change detection based on salience of the item and likelihood of change. A tradeoff is hypothesized, wherein quickly-detected changes will be predicted by visual salience and slowly-detected changes will be predicted by change probability.

### Design
The change-rating experiment is contained in the change_rating.html page. This document uses the jsPsych package library to receive input from Mechanical Turk workers. The entirety of the [jsPsych library](https://github.com/jodeleeuw/jsPsych) is located in this repository for easy implementation for future projects. Please download the library and give the designer proper credit if you make modifications to this experiment. Data is submitted as a string to mechanical turk using the [mmturkey package](https://github.com/longouyang/mmturkey), which is highly recommended. The scene image stimuli were acquired from Jeremy Wolfe's [Change Blindness database](http://search.bwh.harvard.edu/new/CBDatabase.html) [Sareen, Ehinger, & Wolfe, 2015](http://search.bwh.harvard.edu/new/pubs/CBD_Sareen_2015.pdf).


The design is quite simple. Requisite plugins from the jsPsych library are imported at the top of the html page Each step of the experiment is declared as a variable with specific properties from the jsPsych plugin functionality. An initial check verifies that individuals are participating via Amazon Mechanical Turk and that they have accepted the HIT (see next section). Participants are asked to accept the consent document linked as informed_consent.html, and a pop-up window informs participants who do not consent that they cannot continue with the experiment.

The body of the experiment begins with a redundant entry of participants' AMT ID (this is for internal validation, as Amazon automatically records their AMT ID's) and their age. Participants are then given instructions before continuing to the test block.

The test block imports images aggregated from the CB database located in the WolfeCBImages folder. Five objects in each image were selected by the researchers as items for participants to rate. To-be-rated items are bounded by a 6 point line of one of five random colors. Participants view all scenes with framed items in random order. For each item in each image, participants rate the likelihood that that item will change in 5 minutes, one hour or one day.

Upon completion of the test block, we might ask participants general demographic questions, or questions about their daily experience which may be of interest to future investigation.

## Interface with Mechanical Turk

### Access and Secret Access Keys

To embed the code within a Mechanical Turk iframe window, it is first necessary to retrieve access and security keys from Amazon. Instructions can be found at http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html. For security purposes, **access and security keys should never be kept in a publicly accessible location.** Here, I placed the keys in a the python file 'config.py' which is stored locally.

### Creating a Mechanical Turk HIT

Mechanical turk assigns requests to workers using HITs (Human Intelligence Tasks). Here, we upload HIT's directly to Mechanical Turk using a simple Python script, 'create_hit.py', that specifies the requirements of the HIT, including the duration of the HIT, the requirements of workers who can see the HIT, and the pay for completion of the HIT. It is recommended that users familiarize themselves with AMT before uploading HITs in this manner. Once configured, the HIT was posted by running the script through the terminal window (on Mac: python create_hit.py).

It is highly recommended that users debug their scripts using the AMT Worker Sandbox. The sandbox permits users to upload hits with no fear of wasting money adjusting parameters. The link to the AMT sandbox has been commented out in creat_hit.py. Toggling the HOST variable switches between the sandbox and "live" HITs.

### Sending and Retrieving Data from AMT

This experiment does not use external databases to store responses. Instead, we used the mmturkey package to directly send collected data as a JSON string to Mechanical Turk. This one line of code is exceedingly useful. Data appears as a single string on the HIT approval page, along with other automatically collected data for each worker.

### Data Collection & Analysis

Analysis of the recorded data will require JSON string parsing. This stage is still in development, but updates will be recorded here at a later date.
