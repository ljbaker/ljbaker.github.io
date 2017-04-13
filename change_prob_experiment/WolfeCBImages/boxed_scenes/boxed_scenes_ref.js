// LB
// 2017-4-7
// change-proability experiment
// Arrays for loading scene images into main html experiment

// random number generator if need be. Change N to desired number of orders
// var runNum = Math.floor(Math.random()*N) + 1

// prompts for likert scale
var change_prompts = [
  'how likely is it that this object will different in 5 minutes?</p>',
  'how likely is it that this object will different in 1 hour?</p>',
  'how likely is it that this object will different in 1 day?</p>'
]

// likert scale for decisions
var change_choices = ['1','2','3','4','5','6','7','8','9','10']

// every scene in dataset
var all_scenes = [
  '01_L_filler_present_mirror_BOX.png'
]

// object label box colors, in order
var object_colors = [
  'red',
  'orange',
  'yellow',
  'green',
  'blue'
  ]

// every object subset by scene
//make sure these are in object_color order: r,o,y,g,b
var all_objects = [
  [
    'mirror_CHANGE',
    'painting',
    'bedpost',
    'pillow',
    'TV',
  ]
]

// var run_faces = all_faces[runNum-1]
// var run_emotions = all_emotions[runNum-1]
