from enum import Enum
from typing import List


class FileType(Enum):
    JAVA = ".java"
    JAVA_TEST = "Test.java"
    JAVA_IT = "IT.java"
    KOTLIN = ".kt"
    KOTLIN_TEST = "Tests.tk"
    GROOVY = ".groovy"
    GROOVY_TEST = "Test.groovy"
    JAVASCRIPT = ".js"
    JAVASCRIPT_TEST = ".spec.js"
    TYPESCRIPT = ".ts"
    TYPESCRIPT_TEST = ".spec.ts"
    CSS = ".css"
    JSON = ".json"
    SQL = ".sql"
    POM_XML = "pom.xml"
    SWAGGER_YML = "swagger.yml"
    MARKDOWN = ".md"
    HTML = ".html"
    PYTHON = ".py"
    CSHARP = ".cs"

    def match(self, file: str) -> bool:
        if self == self.JAVA:
            return file.endswith(".java") and \
                   not file.endswith("Test.java") and \
                   not file.endswith("IT.java") and \
                   "/test/" not in file

        elif self == self.JAVA_TEST:
            return file.endswith("Test.java") and \
                   "/test/" in file

        elif self == self.JAVA_IT:
            return file.endswith("IT.java") and \
                   "/test/" in file

        elif self == self.KOTLIN:
            return file.endswith(".kt") and \
                   not file.endswith("Test.kt") and \
                   not file.endswith("Tests.kt") and \
                   "/test/" not in file

        elif self == self.KOTLIN_TEST:
            return (file.endswith("Test.kt") or file.endswith("Tests.kt")) and \
                   "/test/" in file

        elif self == self.GROOVY:
            return file.endswith(".groovy") and \
                   not file.endswith("Test.groovy") and \
                   "/test/" not in file

        elif self == self.GROOVY_TEST:
            return file.endswith("Test.groovy") and \
                   "/test/" in file

        elif self == self.JAVASCRIPT:
            return file.endswith(".js") and not file.endswith(".spec.js")

        elif self == self.JAVASCRIPT_TEST:
            return file.endswith(".spec.js")

        elif self == self.TYPESCRIPT:
            return file.endswith(".ts") and not file.endswith(".spec.ts")

        elif self == self.TYPESCRIPT_TEST:
            return file.endswith(".spec.ts")

        elif self == self.CSS:
            return file.endswith(".css") or file.endswith(".scss")

        elif self == self.JSON:
            return file.endswith(".json")

        elif self == self.SQL:
            return file.endswith(".sql")

        elif self == self.POM_XML:
            return file.endswith("pom.xml")

        elif self == self.SWAGGER_YML:
            return file.endswith("swagger.yml")

        elif self == self.MARKDOWN:
            return file.endswith(".md")

        elif self == self.HTML:
            return file.endswith(".html")

        elif self == self.PYTHON:
            return file.endswith(".py")

        elif self == self.CSHARP:
            return file.endswith(".cs")

    def __str__(self):
        return self.name

    @staticmethod
    def all() -> List:
        return [
            FileType.JAVA,
            FileType.JAVA_TEST,
            FileType.JAVA_IT,
            FileType.KOTLIN,
            FileType.KOTLIN_TEST,
            FileType.GROOVY,
            FileType.GROOVY_TEST,
            FileType.JAVASCRIPT,
            FileType.JAVASCRIPT_TEST,
            FileType.TYPESCRIPT,
            FileType.TYPESCRIPT_TEST,
            FileType.CSS,
            FileType.JSON,
            FileType.SQL,
            FileType.POM_XML,
            FileType.SWAGGER_YML,
            FileType.MARKDOWN,
            FileType.HTML,
            FileType.PYTHON,
            FileType.CSHARP]

    @staticmethod
    def any_match(file_types: List, file: str) -> bool:
        if len(file_types) == 0:
            return True
        return any(map(lambda file_type: file_type.match(file), file_types))
