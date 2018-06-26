import re

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
        self.raw = getPart(content, 'Subject')
        self.events = getPart(content, 'Event Type')

# Class to manipulate presentation logs
class LogHandler:
    COL_SUBJECT    = 0
    COL_TRIAL      = 1
    COL_EVENT_TYPE = 2
    COL_CODE       = 3
    COL_TIME       = 4
    COL_TTIME      = 5 
    COL_DURATION   = 7 

    def __init__(self, file):
        log = LogParser(file)
        self.raw    = log.raw
        self.events = log.events

    def getFirstPulseTime(self):
        pulses = filterLines(self.raw, self.COL_EVENT_TYPE, r'Pulse')
        return int( pulses[0][1][self.COL_TIME] )

    def fixTimes(self):
        firstPulse = self.getFirstPulseTime()
        for i in range(2,len(self.raw)):
            line = self.raw[i]
            line[self.COL_TIME] = float(line[self.COL_TIME]) - firstPulse
            line[self.COL_TIME] /= 10000
            line[self.COL_TTIME] = float(line[self.COL_TTIME]) / 10000
            try:
                line[self.COL_DURATION] = float(line[self.COL_DURATION]) / 10000
            except:
                pass
            self.raw[i] = line

    # Do extraction of all data
    def extractTrials(self, cols):
        self.fixTimes()
        trials = filterLines(self.raw, cols[0][1], cols[0][2])
        
        header = ['onset', 'duration']
        header.extend([i[0] for i in cols]) # Adding extra columns
        vals = []

        nTrials = len(trials)
        for n in range(nTrials):
            trial = trials[n][1]
            onset = trial[self.COL_TIME]
            duration = trial[self.COL_DURATION]
            code = trial[self.COL_CODE]

            first = trials[n][0]
            last = len(self.raw) if n == nTrials-1 else trials[n+1][0]

            extras = []
            for col in cols[2:]:
                item = filterLines(self.raw[first:last], col[1], col[2])
                try:
                    content = item[0][1][col[3]]
                except:
                    content = 'na'
                extras.extend([content])

            vals.append([onset, duration, code] + extras)
        
        # Returning all data
        return [header] + vals


    def writeRaw(self):
        report(self.raw)

    def writeEvents(self):
        report(self.events)


## GENERAL FUNCTIONS
def filterLines(content, column, rfilter):
    return filter(lambda (i,x): re.findall(rfilter, x[column]), enumerate(content))

def report(content):
    for line in content:
        print( '\t'.join(line) )

# Extract header position
def getHeaderLine(content, firstCol):
    nLines = len(content)
    for nLine in range(nLines):
        if content[nLine][0] == firstCol and content[nLine+1][0] == '':
            return nLine
    return None

# Extract table last position
def getLastLine(content, firstLine):
    nLines = len(content)
    for nLine in range(firstLine, nLines):
        if content[nLine][0] == '':
            return nLine-1
    return nLines-1

# Extract parts of the file
def getPart(content, firstCol):
    nHeader = getHeaderLine(content, firstCol)
    nEnd = getLastLine(content, nHeader+2)
    data = [content[nHeader]]
    data.extend( content[ nHeader+2:nEnd ] )
    return data