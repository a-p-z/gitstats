class Diffstat:

    def __init__(self, filename: str, insertions: int, deletions: int):
        self.file = filename
        self.insertions = insertions
        self.deletions = deletions

    @staticmethod
    def of(diffstat):
        diffstat_list = diffstat.split("\t")
        filename = diffstat_list[2]
        insertions = int(diffstat_list[0]) if "-" != diffstat_list[0] else 0
        deletions = int(diffstat_list[1]) if "-" != diffstat_list[1] else 0
        return Diffstat(filename, insertions, deletions)
