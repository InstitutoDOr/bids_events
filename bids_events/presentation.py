import re
from .Events import EventHandler

# Class to manipulate presentation logs
class LogParser:
    def __init__(self, file):
        self.file = file
        self.extract_data()

    # Do extraction of all data
    def extract_data(self):
        with open(self.file) as f:
            content = f.readlines()

        # Removing \n and split with \t
        content = [x.strip().split('\t') for x in content]
        self.raw = get_part(content, 'Subject')
        self.events = get_part(content, 'Event Type')

# Class to manipulate presentation logs
class LogHandler:
    COL_SUBJECT    = 0
    COL_TRIAL      = 1
    COL_EVENT_TYPE = 2
    COL_CODE       = 3
    COL_TIME       = 4
    COL_TTIME      = 5 
    COL_DURATION   = 7
    EMPTY_CELL     = 'n/a'

    def __init__(self, file):
        log = LogParser(file)
        self.raw    = log.raw
        self.events = log.events
        self.trials = []

    def get_first_pulse_time(self):
        pulses = filter_lines(self.raw, self.COL_EVENT_TYPE, r'Pulse')
        if pulses:
            return int( pulses[0][1][self.COL_TIME] )
        else:
            return 0

    def fix_times(self):
        first_pulse = self.get_first_pulse_time()
        for i in range(2,len(self.raw)):
            line = self.raw[i]
            line[self.COL_TIME] = float(line[self.COL_TIME]) - first_pulse
            line[self.COL_TIME] /= 10000
            line[self.COL_TTIME] = float(line[self.COL_TTIME]) / 10000
            try:
                line[self.COL_DURATION] = float(line[self.COL_DURATION]) / 10000
            except:
                pass
            self.raw[i] = line

    # Do extraction of all data
    # First column is the main event - responsible to define each line
    def extract_trials(self, cols, duration = None, onset_filter = None):
        self.fix_times()
        trials = filter_lines(self.raw, cols[0][1], cols[0][2])
        
        header = ['onset', 'duration']
        header.extend([i[0] for i in cols]) # Adding extra columns
        vals = []

        n_trials = len(trials)
        for n in range(n_trials):
            trial = trials[n][1]
            onset = trial[self.COL_TIME]
            duration = trial[self.COL_DURATION] if not duration else duration
            code = trial[self.COL_CODE]
            if callable(onset_filter):
                onset = onset_filter(onset)

            # First column is mandatory (used to extract trial onset)
            first = trials[n][0]
            last = len(self.raw) if n == (n_trials-1) else trials[n+1][0]

            # Ignoring first column (trial onset)
            extras = []
            for col in cols[1:]:
                item = filter_lines(self.raw[first:last], col[1], col[2])
                try:
                    content = item[0][1][col[3]]
                except:
                    content = self.EMPTY_CELL
                extras.extend([content])

            vals.append([onset, duration, code] + extras)
        
        # Returning all data
        self.trials = [header] + vals

    # Function to manipulate values
    def remove_column(self, column):
        c_idx = self.column_pos(column)
        # Ignores header
        for idx, trial in enumerate(self.trials):
            del self.trials[idx][c_idx]
    
    # Print all lines
    def print(self, header = True):
        line_header = self.trials[0]
        lines = self.trials[1:]

        if header: print(line_header)
        for line in lines:
            print(line)

    # Function to manipulate values
    def filter_column(self, column, filter_col):
        self.compute_column( column, filter_col, column )

    # Function to create or change columns computing values using a heuristic function
    def compute_column(self, column, heuristic, *other_cols):
        # Get or create the column
        c_idx = self.column_pos(column)
        if not c_idx and c_idx != 0:
            self.trials[0].append(column)
            c_idx = len(self.trials[0]) - 1

        # Ignores header
        for idx, trial in enumerate(self.trials[1:]):
            inputs = []
            for col in other_cols:
                col = self.column_pos(col)
                inputs.append( trial[col] )
            comp_value = heuristic( *inputs )
            if c_idx == len(trial):
                self.trials[idx+1].append(comp_value)
            else:
                self.trials[idx+1][c_idx] = comp_value

    def column_pos(self, column):
        header = self.trials[0]
        if isinstance(column, str) and column in header:
            return header.index(column)
        if isinstance(column, int) and len(header) > column:
            return column
        return None

    def write_raw(self):
        report(self.raw)

    def write_events(self):
        report(self.events)

    def export_bids(self, filename, suffix = '_events'):
        events = EventHandler(filename, suffix)
        events.set_trials(self.trials)
        events.export_bids()

## GENERAL FUNCTIONS
def filter_lines(content, column, rfilter):
    return list( filter(lambda x: re.findall(rfilter, x[1][column]), enumerate(content)) )

def report(content):
    for line in content:
        print( '\t'.join(line) )

# Extract header position
def header_line(content, first_col):
    n_lines = len(content)
    for n_line in range(n_lines):
        if content[n_line][0] == first_col and content[n_line+1][0] == '':
            return n_line
    return None

# Extract table last position
def last_line(content, first_line):
    n_lines = len(content)
    for n_line in range(first_line, n_lines):
        if content[n_line][0] == '':
            return n_line-1
    return n_lines

# Extract parts of the file
def get_part(content, first_col):
    n_header = header_line(content, first_col)
    if not n_header:
        return None
    n_end = last_line(content, n_header+2)
    data = [content[n_header]]
    data.extend( content[ n_header+2:n_end ] )
    return data