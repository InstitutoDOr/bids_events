# bids_events

Tool to export events from presentation log files.

## Installation

```
pip install bids_events
```

## Example of use

### Simple example
```python
from bids_events.Events import EventHandler

events_h = EventHandler('example_events.tsv')
events_h.trials = [
    ['onset', 'duration', 'condition'],
    [0,   20, 'STOP'],
    [20,  20, 'GO'],
    [40,  20, 'STOP'],
    [60,  20, 'GO'],
    [80,  20, 'STOP'],
    [100, 20, 'GO'],
    [120, 20, 'STOP'],
    [140, 20, 'GO'],
    [160, 20, 'STOP'],
    [180, 20, 'GO'],
]
events_h.export_bids()
```

### Extraction using *Presentation* LOGS
```python
from bids_events.presentation import LogHandler as Log

cols = [
    ['trial_type', Log.COL_CODE, r'cue.*'],
    ['fix_after_cue', Log.COL_CODE, r'fixAfterCue', Log.COL_TIME],
    ['reward', Log.COL_CODE, r'rew.*', Log.COL_CODE],
    ['response', Log.COL_CODE, r'press', Log.COL_TTIME],
    ['fix2', Log.COL_CODE, r'fix2', Log.COL_TTIME]
]

log = Log('S001-Run1.log')
log.extract_trials( cols )
log.export_bids('sub-S001_task-emotion_run-1')
```

Check the `./tests` folder to see more detailed examples.