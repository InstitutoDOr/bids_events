import sys
sys.path.append('..')

from bids_events.presentation import LogHandler as Log

cols = [
    ['trial_type', Log.COL_CODE, r'cue.*'],
    ['fix_after_cue', Log.COL_CODE, r'fixAfterCue', Log.COL_TIME],
    ['reward', Log.COL_CODE, r'rew.*', Log.COL_CODE],
    ['response', Log.COL_CODE, r'press', Log.COL_TTIME],
    ['fix2', Log.COL_CODE, r'fix2', Log.COL_TTIME]
]

log = Log('STEST-Run1.log')
log.extract_trials( cols )
log.export_bids('sub-STEST_task-TDAH_run-1')

log = Log('STEST-Run2.log')
log.extract_trials( cols )
log.export_bids('sub-STEST_task-TDAH_run-2')

log = Log('STEST-Run3.log')
log.extract_trials( cols )
log.export_bids('sub-STEST_task-TDAH_run-3')