import re
import process

# return list of [h, date, subject, author, email, file, insertions, deletions]
def gitNumstat():
    numstat = list()
    lines = process.execute("git log --pretty=tformat:'%h,%aI,%s,%aN,%ae' --numstat --no-merges").split("\n")
    
    for line in lines:
        match = re.match(r"(\w+),([0-9\-T:\+]+),(.*),(.*),([a-zA-Z0-9_\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+)", line)
        if match: 
            (file, insertions, deletions) = ("", 0, 0)
            h = match.group(1)
            date = match.group(2)
            subject = match.group(3)
            author = match.group(4).title()
            email = match.group(5)
        
        elif re.match(r"\d+\t+\d+\t+.+", line):
            (insertions, deletions, file) = line.split("\t")
            numstat.append([h, date, subject, author, email, file, int(insertions), int(deletions)])
    
    return numstat
