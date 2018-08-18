import sys
sys.path.insert(0,'tests')
import setup_test

from bids_events.Events import EventHandler

# Saving data
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

print(events_h.get_filename())