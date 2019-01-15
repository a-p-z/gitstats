import re
from author import Author

class Blame:
    
    def __init__(self, rawgitblame):
        self.hash = None
        self.author = Author(None, None)
        self.committer = Author(None, None)
        self.summary = None
        self.filename = None
        self.content = None
        self.__parse(rawgitblame)

    def __parse(self, rawgitblame):
        for line in rawgitblame.split("\n"):
            if line.startswith('author '):
                self.author.name = line[7:]
                
            elif line.startswith('author-mail '):
                self.author.email = line[13:-1]
                
            elif line.startswith('committer '):
                self.committer.name = line[10:]
                
            elif line.startswith('committer-mail '):
                self.committer.email = line[16:-1]
                
            elif line.startswith('summary '):
                self.summary = line[8:]
                
            elif line.startswith('filename '):
                self.filename = line[9:]
                
            elif line.startswith('\t'):
                self.content = line[1:]
                
            elif re.match(r".{,40} \d+ \d+", line):
                self.hash = line[:40]
        
        validate(self, rawgitblame)
    
    
def validate(blame, rawgitblame):
    if not blame.hash:
        raise BlameParsingException('hash', rawgitblame)
    
    if not blame.author.name:
        raise BlameParsingException('author name', rawgitblame)
    
    if not blame.author.email:
        raise BlameParsingException('author email', rawgitblame)
    
    if not blame.committer.name:
        raise BlameParsingException('committer name', rawgitblame)
    
    if not blame.committer.email:
        raise BlameParsingException('committer email', rawgitblame)
    
    if not blame.summary:
        raise BlameParsingException('summary', rawgitblame)
    
    if not blame.filename:
        raise BlameParsingException('filename', rawgitblame)

class BlameParsingException(Exception):
    
     def __init__(self, attribute, rawgitblame):
        super(BlameParsingException, self).__init__("Error parsing blame, attribute %s not found in:\n<%s>" % (attribute, rawgitblame))




