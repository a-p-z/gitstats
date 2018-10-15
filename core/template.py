import os

class Template:
    
    def __init__(self, templateName):
        basepath = os.path.dirname(os.path.abspath(__file__))
        filename = "%s/../resources/%s.txt" % (basepath, templateName)
        self.__template = self.__readFile(filename)
    
    
    def fill(self, contents):
        template = self.__template
        for key, content in contents.items():
            template = template.replace(key, content)
        
        return template
    
    
    def __readFile(self, filename):
        with open(filename, 'r') as file:
            return file.read()
