from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import LocaleRequirement, PercentAssignmentsApprovedRequirement, Qualifications, NumberHitsApprovedRequirement
from config import AK,SK


HOST = "mechanicalturk.sandbox.amazonaws.com"
NUM_ITERATIONS = 100
ACTIVE_HOURS = 6 #hours HIT will be active
EXP_DURATION = 15 #minutes turkers will have to complete experiment
EXPERIMENT_URL = """https://ljbaker.github.io/CAFE_face_rating.html"""

mtc = MTurkConnection(host=HOST)

quals = Qualifications();
quals.add( PercentAssignmentsApprovedRequirement('GreaterThanOrEqualTo',95) )
quals.add( NumberHitsApprovedRequirement('GreaterThanOrEqualTo',1) )
quals.add( LocaleRequirement('EqualTo', 'US') )

new_hit = mtc.create_hit(
  hit_type=None,
  question = ExternalQuestion(EXPERIMENT_URL, 600),
  lifetime = ACTIVE_HOURS*60*60, # Amount of time HIT will be available to accept unless 'max_assignments' are accepted before
  max_assignments = NUM_ITERATIONS,
  title = 'Identifying Facial Expressions',
  description = 'Participate in a simple psychological experiment on emotional recognition. You will pick a label that best defines a series of faces (e.g., "happy", "sad", etc.). The entire HIT should take approximately 5 minutes (reward is estimated according to $9/hr).',
  keywords = 'faces, emotions',
  reward = 0.75,
  duration = EXP_DURATION*60, # Maximum amount of time turkers are allowed to spend on HIT
  approval_delay = 1*60*60, # Amount of time after which HIT is automatically approved
  questions = None,
  qualifications = quals )[0]

print(new_hit.HITId)
