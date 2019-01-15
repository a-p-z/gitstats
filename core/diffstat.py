class Diffstat:
    
    def __init__(self, diffstatstring):
        diffstatslist = diffstatstring.split("\t")
        self.filename = diffstatslist[2]
        self.insertions = int(diffstatslist[0]) if "-" != diffstatslist[0] else 0
        self.deletions = int(diffstatslist[1]) if "-" != diffstatslist[1] else 0
