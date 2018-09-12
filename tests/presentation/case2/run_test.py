# TEST ENV SET UP
import sys
sys.path.insert(0,'tests')
import setup_test

# MAIN PROGRAM
from bids_events.presentation import LogHandler as Log
import os
os.chdir( os.path.dirname(os.path.realpath(__file__)) )

cols = [
    ['trial_type', Log.COL_CODE, r'REPOUSO|TAREFA'],
    ['fix_after_cue', Log.COL_EVENT_TYPE, r'Sound', Log.COL_CODE]
]

log = Log('STEST2_EXE.log')
log.extract_trials( cols, 20, onset_filter=lambda x:int(x) )
log.export_bids('sub-STEST2_task-blind_run-1')

log = Log('STEST2_IMAG_2RUN.log')
log.extract_trials( cols, 20 )
log.export_bids('sub-STEST2_task-blind_run-2')

log = Log('STEST2_IMAG_3RUN.log')
log.extract_trials( cols, 20 )
log.export_bids('sub-STEST2_task-blind_run-3')