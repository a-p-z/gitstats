import re
import process
from collections import defaultdict

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


# return list of [file, author, email, content]
def gitBlame():
    blame = list()
    files = process.execute("git ls-files").split("\n")[0:-1]
    
    for file in files:
        try:
            lines = process.execute("git blame --line-porcelain %s" % file).split("\n")
            for line in lines:
                authorMatch = re.match(r"author (.+)", line)
                emailMatch = re.match(r"author-mail <(.+)>", line)
                if authorMatch:
                    author = authorMatch.group(1).title()
                    email = ""
                
                elif emailMatch:
                    email = emailMatch.group(1)
                
                elif line.startswith("\t"):
                    content = line[1:]
                    blame.append([file, author, email, content])
        
        except process.ProcessException:
            continue
    
    return blame


def countCommits():
    return int(process.execute("git rev-list --no-merges --count HEAD"))


# return list of [author, email, commits]
def countCommitsByAuthor():
    commitsByAuthor = list()
    
    for line in process.execute("git shortlog -s -e -n --no-merges").split("\n"):
        match = re.match(r"\s*(\d+)\t(.+) <(.+)>", line)
        if match:
            author = match.group(2).title()
            email = match.group(3)
            commits = match.group(1)
            commitsByAuthor.append([author, email, int(commits)])
    
    return commitsByAuthor


# return list of [author, email, merges]
def countMergesByAuthor():
    mergesByAuthor = list()
    
    for line in process.execute("git shortlog -s -e -n --merges").split("\n"):
        match = re.match(r"\s*(\d+)\t(.+) <(.+)>", line)
        if match:
            author = match.group(2).title()
            email = match.group(3)
            commits = match.group(1)
            mergesByAuthor.append([author, email, int(commits)])
    
    return mergesByAuthor


# return list of [author, commits, insertions, deletions]
def countCommitsAndImpactsByAuthor(numstat):
    commitsAndImpactsByAuthor = defaultdict(lambda: [0, 0, 0])
    hs = list()
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        if h not in hs:
            hs.append(h)
            commitsAndImpactsByAuthor[author][0] += 1
        commitsAndImpactsByAuthor[author][1] += insertions
        commitsAndImpactsByAuthor[author][2] += deletions
    
    commitsAndImpactsByAuthor = map(lambda x: [x[0]] + x[1], commitsAndImpactsByAuthor.items())
    return sorted(commitsAndImpactsByAuthor, key = lambda x: x[1], reverse = True)


