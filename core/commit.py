from author import Author
from datetime import datetime
from diffstat import Diffstat

class Commit:
    
    def __init__(self, logstring):
        loglist = logstring.split("\n")
        self.hash = loglist[0]
        self.subject = loglist[2]
        self.author = Author(loglist[3], loglist[4])
        self.committer = Author(loglist[5], loglist[6])
        
        try:
            self.date = datetime.strptime(loglist[1][:-6], "%Y-%m-%dT%H:%M:%S")
        except:
            print "Error parsing date of %s" % logstring
            raise
        
        try:
            self.diffstats = [Diffstat(diffstat) for diffstat in loglist[8:-1]]
        except:
            print "Error parsing diffstat of %s" % logstring
            raise
    
    
    def sum_deletions(self):
        return sum([diffstat.deletions for diffstat in self.diffstats])
    
    
    def sum_insertions(self):
        return sum([diffstat.insertions for diffstat in self.diffstats])
    
    
    def impacted_filenames(self):
        return [diffstat.filename for diffstat in self.diffstats]
    
    
    def sum_impacts(self):
        return sum_insertions(self) + sum_deletions(self)
    