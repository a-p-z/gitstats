import re
from dataclasses import dataclass

from gitstats.data.model.author import Author
from gitstats.data.model.author import Committer
from gitstats.data.model.file import File

JAVA_FUNCTION_DEFINITION_PATTERN = re.compile(r".*->|.*\w\s*::\s*\w")
CONDITION_PATTERN = re.compile(r".*if")


@dataclass(frozen=True)
class Blame:
    hash: str
    author: Author
    committer: Committer
    summary: str
    file: File
    content: str

    def content_is_empty(self) -> bool:
        return not self.content.strip()

    def contains_function_definition(self) -> bool:
        return self.file.is_java() and bool(JAVA_FUNCTION_DEFINITION_PATTERN.match(self.content))

    def contains_condition(self) -> bool:
        return any(
            [
                self.file.is_groovy(),
                self.file.is_java(),
                self.file.is_javascript(),
                self.file.is_kotlin(),
                self.file.is_python(),
                self.file.is_rust(),
                self.file.is_typescript(),
                self.file.is_vue(),
            ]
        ) and bool(CONDITION_PATTERN.match(self.content))

    @staticmethod
    def is_dockerfile(blame: "Blame") -> bool:
        return blame.file.is_dockerfile()

    @staticmethod
    def is_docker_compose(blame: "Blame") -> bool:
        return blame.file.is_docker_compose()

    @staticmethod
    def is_groovy(blame: "Blame") -> bool:
        return blame.file.is_groovy()

    @staticmethod
    def is_java(blame: "Blame") -> bool:
        return blame.file.is_java()

    @staticmethod
    def is_javascript(blame: "Blame") -> bool:
        return blame.file.is_javascript()

    @staticmethod
    def is_json(blame: "Blame") -> bool:
        return blame.file.is_json()

    @staticmethod
    def is_kotlin(blame: "Blame") -> bool:
        return blame.file.is_kotlin()

    @staticmethod
    def is_pom(blame: "Blame") -> bool:
        return blame.file.is_pom()

    @staticmethod
    def is_python(blame: "Blame") -> bool:
        return blame.file.is_python()

    @staticmethod
    def is_pyproject(blame: "Blame") -> bool:
        return blame.file.is_pyproject()

    @staticmethod
    def is_readme(blame: "Blame") -> bool:
        return blame.file.is_readme()

    @staticmethod
    def is_rust(blame: "Blame") -> bool:
        return blame.file.is_rust()

    @staticmethod
    def is_sql(blame: "Blame") -> bool:
        return blame.file.is_sql()

    @staticmethod
    def is_src(blame: "Blame") -> bool:
        return not Blame.is_test(blame)

    @staticmethod
    def is_stylesheet(blame: "Blame") -> bool:
        return blame.file.is_stylesheet()

    @staticmethod
    def is_swagger(blame: "Blame") -> bool:
        return blame.file.is_swagger()

    @staticmethod
    def is_toml(blame: "Blame") -> bool:
        return blame.file.is_toml()

    @staticmethod
    def is_typescript(blame: "Blame") -> bool:
        return blame.file.is_typescript()

    @staticmethod
    def is_test(blame: "Blame") -> bool:
        return blame.file.is_test()

    @staticmethod
    def is_vue(blame: "Blame") -> bool:
        return blame.file.is_vue()

    @staticmethod
    def is_yaml(blame: "Blame") -> bool:
        return blame.file.is_yaml()
