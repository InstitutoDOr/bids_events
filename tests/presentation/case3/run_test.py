# TEST ENV SET UP
import sys
sys.path.insert(0,'tests')
import setup_test

# MAIN PROGRAM
from bids_events.presentation import LogHandler as Log
import os
import re
os.chdir( os.path.dirname(os.path.realpath(__file__)) )

cols = [
    ['fix', Log.COL_CODE, r'cue'],
    ['subj', Log.COL_CODE, r'cue'],
    ['run', Log.COL_CODE, r'cue'],
    ['category', Log.COL_EVENT_TYPE, r'Video', Log.COL_CODE],
    ['clip', Log.COL_EVENT_TYPE, r'Video', Log.COL_CODE],
    ['auc', Log.COL_CODE, r'AUC=.*', Log.COL_CODE],
    ['auc/max', Log.COL_CODE, r'AUC/MAX=.*', Log.COL_CODE],
    ['peak', Log.COL_CODE, r'PICO=.*', Log.COL_CODE],
    ['video_start', Log.COL_EVENT_TYPE, r'Video', Log.COL_TIME],
    ['video_end', Log.COL_CODE, r'END_VIDEO', Log.COL_TIME]
]

files = ['PILO_Tiago-1Run.log', 'PILO_Tiago-2Run.log', 'PILO_Tiago-3Run.log', 'PILO_Tiago-4Run.log']

for f in files:
    log = Log(f)
    subj = re.search(r'^.*(?=-\dRun)', f).group(0)
    subj = re.sub('[-_]', '', subj)
    run = re.search(r'\d(?=Run)', f).group(0)
    
    log.extract_trials( cols )
    log.filter_column('category', lambda x: re.sub(r'\/.*', '', x))
    log.filter_column('clip', lambda x: re.sub(r'.*\/', '', x))
    log.filter_column('auc', lambda x: re.sub(r'.*=', '', x))
    log.filter_column('auc/max', lambda x: re.sub(r'.*=', '', x))
    log.filter_column('peak', lambda x: re.sub(r'.*=', '', x))
    log.compute_column('duration', (lambda x,y: y-x), 'onset', 'video_end' )
    log.compute_column('video_duration', (lambda x,y: y-x), 'video_start', 'video_end')
    log.compute_column('subj', lambda x: subj, 'subj' )
    log.compute_column('run', lambda x: run, 'run' )
    log.remove_column('fix')

    log.export_bids('sub-{}_task-EFFORT_run-{}'.format(subj, run))