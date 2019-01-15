import re
import process
from collections import defaultdict
from commit import Commit

GIT_LOG_COMMAND = "git log --pretty=tformat:'.:*-*:.%n%h%n%aI%n%s%n%aN%n%aE%n%cN%n%cE' --numstat --no-merges --date=iso8601"

def git_log():
    return process.execute(GIT_LOG_COMMAND).split(".:*-*:.\n")[1:]

def get_commits(rawgitlogstring):
    return [Commit(rawgitlogtring) for rawgitlogtring in rawgitlogstring]

# return list of [h, date, subject, author, email, file, insertions, deletions]
def gitNumstat():
    numstat = list()
    
    for c in get_commits(git_log()):
        for d in c.diffstats:
           numstat.append([c.hash, c.date.isoformat(), c.subject, c.author.name, c.author.email, d.filename, d.insertions, d.deletions])
    
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


# return list of [author, deletions]
def countDeletionRatioByAuthor(numstat):
    commitsAndDeletionsByAuthor = defaultdict(lambda: [0, 0])
    hs = list()
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        if h not in hs:
            hs.append(h)
            commitsAndDeletionsByAuthor[author][0] += 1
        commitsAndDeletionsByAuthor[author][1] += deletions
    
    deletionRatioByAuthor = map(lambda x: [x[0], x[1][1]/x[1][0]], commitsAndDeletionsByAuthor.items())
    return sorted(deletionRatioByAuthor, key = lambda x: x[1], reverse = True)



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
def countEditedLinesOfCodeByAuthor(blame, filter='', regex='.*'):
    editedLinesOfCodeByAuthor = defaultdict(int)
    regex = re.compile(regex, flags=re.IGNORECASE)

    for (file, author, email, content) in blame:
        if filter in file.lower() and regex.match(content):
            editedLinesOfCodeByAuthor[author] += 1
    
    editedLinesOfCodeByAuthor = map(lambda x: list(x), editedLinesOfCodeByAuthor.items())
    return sorted(editedLinesOfCodeByAuthor, key = lambda x: x[1], reverse = True)


# returns list of [author, eloc, stability]
# stability is equal to 100 * eloc / insertions
def countEditedLinesOfCodeAndStabilityByAuthor(blame, numstat, filter=''):
    editedLinesOfCodeAndStabilityByAuthor = defaultdict(lambda: [0,0])
    
    for (file, author, email, content) in blame:
        if filter in file.lower():
            editedLinesOfCodeAndStabilityByAuthor[author][0] += 1
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        if filter in file.lower():
            editedLinesOfCodeAndStabilityByAuthor[author][1] += insertions
    
    editedLinesOfCodeByAuthor = map(lambda x: [x[0], x[1][0], (100 * x[1][0] / x[1][1] if x[1][1] != 0 else 100)], editedLinesOfCodeAndStabilityByAuthor.items())
    return sorted(editedLinesOfCodeByAuthor, key = lambda x: x[1], reverse = True)


# returns list of [author, eloc]
def countEmptyLinesOfCodeByAuthor(blame, filter=''):
    emptyLinesOfCodeByAuthor = defaultdict(int)
    
    for (file, author, email, content) in blame:
        if filter in file.lower() and not content.strip():
            emptyLinesOfCodeByAuthor[author] += 1
    
    emptyLinesOfCodeByAuthor = map(lambda x: list(x), emptyLinesOfCodeByAuthor.items())
    return sorted(emptyLinesOfCodeByAuthor, key = lambda x: x[1], reverse = True)


    # returns list of [email, eloc]
def countEmptyLinesOfCodeByEmail(blame, filter=''):
    emptyLinesOfCodeByEmail = defaultdict(int)
    
    for (file, author, email, content) in blame:
        if filter in file.lower() and not content.strip():
            emptyLinesOfCodeByEmail[email] += 1
    
    emptyLinesOfCodeByEmail = map(lambda x: list(x), emptyLinesOfCodeByEmail.items())
    return sorted(emptyLinesOfCodeByEmail, key = lambda x: x[1], reverse = True)


# returns list of [author, eloc]
def countEditedLinesOfCodeByEmail(blame, filter='', regex='.*'):
    editedLinesOfCodeByEmail = defaultdict(int)
    regex = re.compile(regex, flags=re.IGNORECASE)

    for (file, author, email, content) in blame:
        if filter in file.lower() and regex.match(content):
            editedLinesOfCodeByEmail[email] += 1
    
    editedLinesOfCodeByEmail = map(lambda x: list(x), editedLinesOfCodeByEmail.items())
    return sorted(editedLinesOfCodeByEmail, key = lambda x: x[1], reverse = True)


# return list of [ext, num]
def countFilesByExtension():
    filesByExtension = defaultdict(int)
    files = process.execute("git ls-files").split("\n")[0:-1]
    exts = map(lambda file: file.split(".")[-1] if "." in file else "NO EXT", files)
    
    for ext in exts:
        filesByExtension[ext] += 1
    
    filesByExtension = map(lambda x: list(x), filesByExtension.items())
    return sorted(filesByExtension, key = lambda x: x[1], reverse = True)


# return list of [file, commits]
def getMostFrequentlyCommittedFiles(numstat):
    mostFrequentlyCommittedFiles = defaultdict(int)
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        mostFrequentlyCommittedFiles[file] += 1
    
    mostFrequentlyCommittedFiles = map(lambda x: list(x), mostFrequentlyCommittedFiles.items())
    return sorted(mostFrequentlyCommittedFiles, key = lambda x: x[1], reverse = True)


# return [date, subject, author, num_of_files, insertions, deletions]
def orderCommitsByImpact(numstat):
    commits = dict()
    
    for (h, date, subject, author, email, file, insertions, deletions) in numstat:
        if h in commits.keys():
            commits[h][3] += 1
            commits[h][4] += insertions
            commits[h][5] += deletions
        else:
            commits[h] = [date[:10], subject, author, 1, insertions, deletions]
    
    return sorted(commits.values(), key = lambda x: x[4] + x[5], reverse = True)
