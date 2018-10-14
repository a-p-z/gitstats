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


# return list of [email, deletions]
def countDeletionRatioByEmail(numstat):
    commitsAndDeletionsByEmail = defaultdict(lambda: [0, 0])
    hs = list()
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        if h not in hs:
            hs.append(h)
            commitsAndDeletionsByEmail[email][0] += 1
        commitsAndDeletionsByEmail[email][1] += deletions
    
    deletionRatioByEmail = map(lambda x: [x[0], x[1][1]/x[1][0]], commitsAndDeletionsByEmail.items())
    return sorted(deletionRatioByEmail, key = lambda x: x[1], reverse = True)


# returns [["date", "author1", "author2", ...],
#          [ date ,     n1   ,     n2   , ...],
#           ... ]
def countCommitsOverMonthByAuthor(numstat):
    commitsOverMonthByAuthor = list()
    agg = defaultdict(lambda: defaultdict(lambda: set()))
    authors = set()
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        agg[date[:7]][author].add(h)
        authors.add(author)
    
    commitsOverMonthByAuthor.append(["date"] + list(authors))
    
    for year in range(int(numstat[-1][1][:4]), int(numstat[0][1][:4]) + 1):
        for month in range(1, 13):
            if year == int(numstat[0][1][:4]) and month > int(numstat[0][1][5:7]):
                break
            date = "%d-%02d" % (year, month)
            next = "%d-%02d" % (year, month + 1) if month < 12 else "%d-%02d" % (year + 1, 1)
            commits = list()
            for author in authors:  
                commits.append(len(agg[date][author]))
            commitsOverMonthByAuthor.append([next] + commits)
    
    return commitsOverMonthByAuthor


# returns list of [date, insertions, deletions]
def getImpactsOverMonth(numstat):
    impactsOverMonth = list()
    agg = defaultdict(lambda: [0,0])
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        agg[date[:7]][0] += deletions
        agg[date[:7]][1] += insertions 
    
    for year in range(int(numstat[-1][1][:4]), int(numstat[0][1][:4]) + 1):
        for month in range(1, 13):
            if year == int(numstat[0][1][:4]) and month > int(numstat[0][1][5:7]):
                break
            date = "%d-%02d" % (year, month)
            next = "%d-%02d" % (year, month + 1) if month < 12 else "%d-%02d" % (year + 1, 1)
            impactsOverMonth.append([next] + agg[date])
    
    return impactsOverMonth


# returns list of [author, eloc]
def countEditedLinesOfCodeByAuthor(blame):
    editedLinesOfCodeByAuthor = defaultdict(int)
    
    for (file, author, email, content) in blame:
        editedLinesOfCodeByAuthor[author] += 1
    
    editedLinesOfCodeByAuthor = map(lambda x: list(x), editedLinesOfCodeByAuthor.items())
    return sorted(editedLinesOfCodeByAuthor, key = lambda x: x[1], reverse = True)

