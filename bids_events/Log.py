class Log:
    def __init__(self, file):
        self.trials = [] # First line should be the header

    def export_bids(self, filename, suffix = '_events'):
        output = ''
        for line in self.trials:
            output += "\t".join([str(i) for i in line]) + "\n"

        # Generating output
        with open('{}{}.tsv'.format(filename, suffix), 'w') as f:
            f.write(output)