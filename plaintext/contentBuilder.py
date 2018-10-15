from core import gitstatsLib
from utilities import splitHeaderAndData
from utilities import cumulate
from utilities import buildTable
from utilities import getTotal
from utilities import limit

class PlainTextContentBuilder:
    
    def __init__(self):
        pass
    
    @staticmethod
    def build(): 
        contents = dict()
        numstat = gitstatsLib.gitNumstat()
        blame = gitstatsLib.gitBlame()
        
        # CUMULATED_COMMITS_OVER_TIME_BY_AUTHOR
        data = gitstatsLib.countCommitsOverMonthByAuthor(numstat)
        header, data = splitHeaderAndData(data)
        data = cumulate(data)
        contents["{CUMULATED_COMMITS_OVER_TIME_BY_AUTHOR}"] = buildTable(header, data)
        
        
        # IMPACTS_OVER_TIME
        header = ("date", "deletions", "insertions")
        data = gitstatsLib.getImpactsOverMonth(numstat)
        contents["{IMPACTS_OVER_TIME}"] = buildTable(header, data)
        
        
        # COMMITS_OVER_TIME_BY_AUTHOR
        data = gitstatsLib.countCommitsOverMonthByAuthor(numstat)
        header, data = splitHeaderAndData(data)
        contents["{COMMITS_OVER_TIME_BY_AUTHOR}"] = buildTable(header, data)
        
        
        # COMMITS_AND_IMPACTS_BY_AUTHOR
        header = ("author", "commits", "insertions", "deletions", "% of changes", "impact/commit")
        data = gitstatsLib.countCommitsAndImpactsByAuthor(numstat)
        total = sum(map(lambda x: x[2] + x[3], data))
        data = map(lambda x: x + [int((x[2] + x[3]) * 100.0 / total)], data) # % of changes (insertions + deletions) / (total_insertions + total_deletions) * 100
        data = map(lambda x: x + [(x[2] + x[3]) / x[1]], data) # impact/commit (insertions + deletions) / commits
        data = data + [getTotal(data)]
        data[-1][4] = " "
        data[-1][5] = " "
        contents["{COMMITS_AND_IMPACTS_BY_AUTHOR}"] = buildTable(header, data)
        # TOTAL_COMMITS_BY_AUTHOR
        header = ("author", "commits")
        data = gitstatsLib.countCommitsByAuthor()
        data = map(lambda x: [x[0], x[2]], data)
        data = limit(data, 8)
        contents["{COMMITS_BY_AUTHOR}"] = buildTable(header, data)
        
        
        # MOST_FREQUENTLY_COMMITTED_FILES
        header = ("file", "commits")
        data = gitstatsLib.getMostFrequentlyCommittedFiles(numstat)
        data = data[:10]
        contents["{MOST_FREQUENTLY_COMMITTED_FILES}"] = buildTable(header, data)
        
        
        # FILES_BY_EXTENSION
        header = ("extension", "total")
        data = gitstatsLib.countFilesByExtension()
        data = limit(data, 8)
        contents["{FILES_BY_EXTENSION}"] = buildTable(header, data)
        
        
        # EDITED_LINES_OF_CODE_BY_AUTHOR
        header = ("author", "edited line of code", "stability")
        data = gitstatsLib.countEditedLinesOfCodeAndStabilityByAuthor(blame, numstat)
        contents["{EDITED_LINES_OF_CODE_BY_AUTHOR_CHART}"] = buildTable(header, data)
        data = data + [getTotal(data)]
        if len(data) > 1:
            data[-1][2] = ""
        data
        contents["{EDITED_LINES_OF_CODE_BY_AUTHOR_TABLE}"] = buildTable(header, data)
        
        
        # MOST_IMPACT_COMMITS
        header = ("date", "subject", "author", "num_of_file", "insertions", "deletions")
        data = gitstatsLib.orderCommitsByImpact(numstat)[:10]
        contents["{MOST_IMPACT_COMMITS}"] = buildTable(header, data)
        
        
        # MAVEN_MAN just for maven projects
        data = gitstatsLib.countEditedLinesOfCodeByAuthor(blame, "pom.xml")
        if len(data) > 0:
            data = data[0]
            contents["{MAVEN_MAN}"] = data[0]
            contents["{MAVEN_ELOC}"] = str(data[1])
        # SWAGGER_STAR just for projects with swagger.yml
        data = gitstatsLib.countEditedLinesOfCodeByAuthor(blame, "swagger.yml")
        if len(data) > 0:
            data = data[0]
            contents["{SWAGGER_STAR}"] = data[0]
            contents["{SWAGGER_ELOC}"] = str(data[1])
        # DESTROYER
        data = gitstatsLib.countDeletionRatioByAuthor(numstat)
        if len(data) > 0:
            data = data[0]
            contents["{DESTROYER}"] = data[0]
            contents["{DESTROYER_RATIO}"] = str(data[1])
        # TESTER
        data = gitstatsLib.countEditedLinesOfCodeByAuthor(blame, "test")
        if len(data) > 0:
            data = data[0]
            contents["{TESTER}"] = data[0]
            contents["{TESTS_ELOC}"] = str(data[1])
        # MERGER
        data = gitstatsLib.countMergesByAuthor()
        if len(data) > 0:
            data = data[0]
            contents["{MERGER}"] = data[0]
            contents["{NUM_OF_MERGE}"] = str(data[2])
        # FAKE_DEVELOPER
        data = gitstatsLib.countEmptyLinesOfCodeByAuthor(blame)
        if len(data) > 0:
            data = data[0]
            contents["{FAKE_DEVELOPER}"] = data[0]
            contents["{EMPTY_LINES}"] = str(data[1])
        # DJ_SON just for projects contain json files
        data = gitstatsLib.countEditedLinesOfCodeByAuthor(blame, ".json")
        if len(data) > 0:
            data = data[0]
            contents["{DJ_SON}"] = data[0]
            contents["{JSON_ELOC}"] = str(data[1])
        # GROOVYER just for projects with groovy files
        data = gitstatsLib.countEditedLinesOfCodeByAuthor(blame, ".groovy")
        if len(data) > 0:
            data = data[0]
            contents["{GROOVYER}"] = data[0]
            contents["{GROOVYER_ELOC}"] = str(data[1])
        # LAMBDA just for java projects
        data = gitstatsLib.countEditedLinesOfCodeByAuthor(blame, ".java", ".*->|.*::")
        if len(data) > 0:
            data = data[0]
            contents["{LAMBDA}"] = data[0]
            contents["{LAMBDA_ELOC}"] = str(data[1])
        # IF
        data = gitstatsLib.countEditedLinesOfCodeByAuthor(blame, "", ".*if")
        if len(data) > 0:
            data = data[0]
            contents["{IF}"] = data[0]
            contents["{IF_ELOC}"] = str(data[1])
        
        return contents
