#TODO:
# 1 - Extract key data of each condition
# 2 - Merge key data for each trial in one line
# 3 - Define duration

import re
from Presentation import LogHandler as Log

log = Log('tests/STEST-Run1.log')
data = log.extractTrials( [
    ['trial_type', Log.COL_CODE, r'cue.*'],
    ['fix_after_cue', Log.COL_CODE, r'fixAfterCue', Log.COL_TIME],
    ['reward', Log.COL_CODE, r'rew.*', Log.COL_CODE],
    ['response', Log.COL_CODE, r'press', Log.COL_TTIME],
    ['fix2', Log.COL_CODE, r'fix2', Log.COL_TTIME]
] )

for line in data:
        print( line )