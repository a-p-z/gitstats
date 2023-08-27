from pytest import mark

from gitstats.data.model.blame import Blame
from gitstats.data.model.file import File
from tests import a_content
from tests import a_file
from tests import a_hash
from tests import a_summary
from tests import an_author


def test_content_is_empty():
    blame = Blame(a_hash(), an_author(), an_author(), a_summary(), a_file(), " \t\n  ")
    assert blame.content_is_empty()


def test_content_is_not_empty():
    blame = Blame(a_hash(), an_author(), an_author(), a_summary(), a_file(), " \ta\n  ")
    assert not blame.content_is_empty()


@mark.parametrize("content", ["(obj) -> obj.toString()", "Object :: toString"])
def test_contains_function_definition(content: str):
    blame = Blame(a_hash(), an_author(), an_author(), a_summary(), a_file("java"), content)
    assert blame.contains_function_definition()


def test_not_contains_function_definition():
    blame = Blame(a_hash(), an_author(), an_author(), a_summary(), a_file(), "")
    assert not blame.contains_function_definition()


@mark.parametrize(
    "content, ext",
    (
        ("if(a == b) {", "java"),
        ("if (a==b)", "groovy"),
        ("  if (a==b)", "kt"),
        (" if(a == b) {", "js"),
        ("if (a==b)", "ts"),
    ),
)
def test_contains_condition(content: str, ext: str):
    blame = Blame(a_hash(), an_author(), an_author(), a_summary(), a_file(ext), content)
    assert blame.contains_condition()


def test_not_contains_condition():
    blame = Blame(a_hash(), an_author(), an_author(), a_summary(), a_file(), "")
    assert not blame.contains_condition()


@mark.parametrize(
    "method, filename, expected",
    (
        ("is_docker_compose", "docker-compose.something.yml", True),
        ("is_docker_compose", "docker-compose.yml", True),
        ("is_dockerfile", "Dockerfile", True),
        ("is_groovy", "file.groovy", True),
        ("is_java", "file.JaVa", True),
        ("is_javascript", "file.Js", True),
        ("is_json", "file.JsoN", True),
        ("is_kotlin", "file.kt", True),
        ("is_pom", "folder/PoM.xMl", True),
        ("is_pyproject", "pyproject.toml", True),
        ("is_python", "file.Py", True),
        ("is_readme", "README.md", True),
        ("is_readme", "readme.md", True),
        ("is_rust", "file.rS", True),
        ("is_sql", "file.sQl", True),
        ("is_src", "blame.py", True),
        ("is_stylesheet", "file.Css", True),
        ("is_stylesheet", "file.sCss", True),
        ("is_swagger", "folder/SwaGGer.yaml", True),
        ("is_swagger", "folder/SwaGGer.yml", True),
        ("is_test", "BlameIT.java", True),
        ("is_test", "BlameTest.java", True),
        ("is_test", "BlameTests.kt", True),
        ("is_test", "test/test_blame.py", True),
        ("is_test", "test_blame.spec.js", True),
        ("is_test", "tests/test_blame.py", True),
        ("is_toml", "file.toml", True),
        ("is_typescript", "file.Ts", True),
        ("is_vue", "file.vUe", True),
        ("is_yaml", "file.yaMl", True),
        ("is_yaml", "file.ymL", True),
        #
        ("is_docker_compose", "docker-compose.no", False),
        ("is_dockerfile", "dockerfile", False),
        ("is_groovy", "file.other", False),
        ("is_java", "file.other", False),
        ("is_javascript", "file.other", False),
        ("is_json", "file.other", False),
        ("is_kotlin", "file.other", False),
        ("is_pom", "blame.py", False),
        ("is_pyproject", "pyproject.toml", True),
        ("is_python", "file.other", False),
        ("is_readme", "readme.other", False),
        ("is_rust", "file.other", False),
        ("is_sql", "file.other", False),
        ("is_src", "BlameIT.java", False),
        ("is_src", "BlameTest.java", False),
        ("is_src", "BlameTests.kt", False),
        ("is_src", "test/test_blame.py", False),
        ("is_src", "test_blame.spec.js", False),
        ("is_src", "tests/test_blame.py", False),
        ("is_stylesheet", "file.other", False),
        ("is_swagger", "blame.py", False),
        ("is_test", "blame.py", False),
        ("is_toml", "file.other", False),
        ("is_typescript", "file.other", False),
        ("is_vue", "file.other", False),
        ("is_yaml", "file.other", False),
        ("is_yaml", "file.other", False),
    ),
)
def test_is(method: str, filename: str, expected: bool):
    file = File(filename)
    blame = Blame(a_hash(), an_author(), an_author(), a_summary(), file, a_content())
    assert getattr(Blame, method)(blame) == expected