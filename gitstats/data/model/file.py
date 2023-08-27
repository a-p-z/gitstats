import os
from pathlib import Path as Path_
from pathlib import PosixPath as PosixPath_
from pathlib import WindowsPath as WindowsPath_


class File(Path_):
    def __new__(cls, *args, **kwargs):
        return super().__new__(WindowsPath if os.name == "nt" else PosixPath, *args, **kwargs)

    def is_dockerfile(self) -> bool:
        return self.name == "Dockerfile"

    def is_docker_compose(self) -> bool:
        return self.name.startswith("docker-compose") and self.is_yaml()

    def is_groovy(self) -> bool:
        return self.suffix.lower() == ".groovy"

    def is_java(self) -> bool:
        return self.suffix.lower() == ".java"

    def is_javascript(self) -> bool:
        return self.suffix.lower() == ".js"

    def is_json(self) -> bool:
        return self.suffix.lower() == ".json"

    def is_kotlin(self) -> bool:
        return self.suffix.lower() == ".kt"

    def is_pom(self) -> bool:
        return self.name.lower() == "pom.xml"

    def is_python(self) -> bool:
        return self.suffix.lower() == ".py"

    def is_pyproject(self) -> bool:
        return self.name.lower() == "pyproject.toml"

    def is_readme(self) -> bool:
        return self.name.lower() == "readme.md"

    def is_rust(self) -> bool:
        return self.suffix.lower() == ".rs"

    def is_sql(self):
        return self.suffix.lower() == ".sql"

    def is_src(self) -> bool:
        return not self.is_test()

    def is_stylesheet(self) -> bool:
        return self.suffix.lower() in [".css", ".scss"]

    def is_swagger(self) -> bool:
        return self.name.lower() in ["swagger.yml", "swagger.yaml"]

    def is_test(self) -> bool:
        return any(
            [
                "test" in self.parts,
                "tests" in self.parts,
                ".spec." in self.name.lower(),
                self.stem.endswith("Test"),
                self.stem.endswith("Tests"),
                self.stem.endswith("IT"),
            ]
        )

    def is_toml(self) -> bool:
        return self.suffix.lower() == ".toml"

    def is_typescript(self) -> bool:
        return self.suffix.lower() == ".ts"

    def is_vue(self):
        return self.suffix.lower() == ".vue"

    def is_yaml(self) -> bool:
        return self.suffix.lower() in [".yml", ".yaml"]


class WindowsPath(WindowsPath_, File):
    pass


class PosixPath(PosixPath_, File):
    pass
