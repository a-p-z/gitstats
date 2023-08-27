from gitstats.data.model.blame import Blame
from gitstats.data.model.file import File
from gitstats.infrastructure.logging import logger
from gitstats.render.model.table import Table
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_author
from gitstats.stats.edited_lines_of_code import count_edited_lines_of_code_by_author
from gitstats.stats.edited_lines_of_code import count_empty_lines_of_code_by_author


async def find_belle_vue() -> Table | None:
    return await __find("find_belle_vue", "is_vue", "vue")


async def find_conditional_developer() -> Table | None:
    logger.info("finding conditional developer")

    def contains_condition(blame: Blame) -> bool:
        return blame.contains_condition() and blame.file.is_src()

    table = Table("Conditional Developer")
    for author, eloc in (await count_edited_lines_of_code_by_author(contains_condition)).items():
        if eloc > 0:
            table.add_row(
                author.name,
                author.username,
                eloc,
                "if conditions created (only groovy, java, javascript, kotlin, python, rust, "
                "typescript and vue source files)",
            )
    table.sort(column=2, reverse=True)
    table.limit(3)
    return table if table.is_not_empty() else None


async def find_css_painter() -> Table | None:
    return await __find("find_css_painter", "is_stylesheet", "css/scss")


async def find_dba() -> Table | None:
    return await __find("find_dba", "is_sql", "SQL")


async def find_destroyer() -> Table | None:
    logger.info("finding destroyer")

    def only_interesting_source(file: File | None) -> bool:
        return (
            file is not None
            and file.is_src()
            and any(
                [
                    file.is_groovy(),
                    file.is_java(),
                    file.is_javascript(),
                    file.is_kotlin(),
                    file.is_python(),
                    file.is_rust(),
                    file.is_typescript(),
                    file.is_vue(),
                ]
            )
        )

    table = Table("Destroyer")
    for author, cai in (await count_commits_and_impact_by_author(only_interesting_source)).items():
        if cai.deletion_ratio > 0:
            table.add_row(
                author.name,
                author.username,
                __truncate(cai.deletion_ratio),
                "deletions for commit (only groovy, java, javascript, kotlin, python, rust, "
                "typescript and vue source files)",
            )
    table.sort(column=2, reverse=True)
    table.limit(3)
    return table if table.is_not_empty() else None


async def find_djson() -> Table | None:
    return await __find("find_djson", "is_json", "json")


async def find_docker_builder() -> Table | None:
    return await __find("find_docker_builder", "is_dockerfile", "Dockerfile")


async def find_docker_composer() -> Table | None:
    return await __find("find_docker_composer", "is_docker_compose", "docker-compose")


async def find_fake_developer() -> Table | None:
    def only_interesting_source(blame: Blame) -> bool:
        return (
            any(
                [
                    Blame.is_groovy(blame),
                    Blame.is_java(blame),
                    Blame.is_javascript(blame),
                    Blame.is_kotlin(blame),
                    Blame.is_python(blame),
                    Blame.is_rust(blame),
                    Blame.is_typescript(blame),
                    Blame.is_vue(blame),
                ]
            )
            and blame.file.is_src()
            and blame.content_is_empty()
        )

    logger.info("finding fake developer")
    table = Table("Fake Developer")
    for author, eloc in (await count_empty_lines_of_code_by_author(only_interesting_source)).items():
        if author is not None and eloc > 0:
            table.add_row(
                author.name,
                author.username,
                eloc,
                "empty lines (only groovy, java, javascript, kotlin, python, rust, typescript and vue  source files)",
            )
    table.sort(column=2, reverse=True)
    table.limit(3)

    return table if table.is_not_empty() else None


async def find_fearless_rustbeard() -> Table | None:
    return await __find("find_fearless_rustbeard", "is_rust", "rust")


async def find_functional_developer() -> Table | None:
    logger.info("finding functional developer")

    def contains_function_definition(blame: Blame) -> bool:
        return blame.contains_function_definition() and blame.file.is_src()

    table = Table("Fake Developer")
    for author, eloc in (await count_edited_lines_of_code_by_author(contains_function_definition)).items():
        if eloc > 0:
            table.add_row(
                author.name,
                author.username,
                eloc,
                "lambda definitions (only java source files)",
            )
    table.sort(column=2, reverse=True)
    table.limit(3)
    return table if table.is_not_empty() else None


async def find_groovyer() -> Table | None:
    return await __find("find_groovyer", "is_groovy", "groovy")


async def find_kotlin_islander() -> Table | None:
    return await __find("find_kotlin_islander", "is_kotlin", "json")


async def find_maven_man() -> Table | None:
    return await __find("find_maven_man", "is_pom", " pom.xml")


async def find_merger() -> Table | None:
    logger.info("finding merger")
    table = Table("Merger")
    for author, commits_and_impact in (await count_commits_and_impact_by_author()).items():
        if commits_and_impact.merges > 0:
            table.add_row(author.name, author.username, commits_and_impact.merges, "merge commits")
    table.sort(column=2, reverse=True)
    table.limit(3)
    return table if table.is_not_empty() else None


async def find_python_projector() -> Table | None:
    return await __find("find_python_projector", "is_pyproject", "pyproject.toml")


async def find_pythoneer_supreme() -> Table | None:
    return await __find("find_pythoneer_supreme", "is_python", "python")


async def find_swagger_star() -> Table | None:
    return await __find("find_swagger_star", "is_swagger", "swagger")


async def find_tester() -> Table | None:
    logger.info("finding tester")
    table = Table("Tester")

    def is_test(blame: Blame) -> bool:
        return Blame.is_test(blame) and not blame.content_is_empty()

    for author, eloc in (await count_edited_lines_of_code_by_author(is_test)).items():
        if eloc > 0:
            table.add_row(author.name, author.username, eloc, "edited lines in tests")
    table.sort(column=2, reverse=True)
    table.limit(3)
    return table if table.is_not_empty() else None


async def find_yaml_descriptor() -> Table | None:
    return await __find("find_yaml_descriptor", "is_yaml", "yml/yaml")


async def find_writer() -> Table | None:
    return await __find("find_writer", "is_readme", "readme.md")


async def __find(method: str, is_: str, label: str) -> Table | None:
    logger.info("finding %s", method.replace("find_", "").replace("_", " "))
    table = Table(method.replace("find_", "").replace("_", " ").capitalize())

    def filter_(blame: Blame) -> bool:
        return getattr(Blame, is_)(blame) and not blame.content_is_empty()

    for author, eloc in (await count_edited_lines_of_code_by_author(filter_)).items():
        if author is not None and eloc > 0:
            table.add_row(author.name, author.username, eloc, f"edited lines in {label} files")
    table.sort(column=2, reverse=True)
    table.limit(3)
    return table if table.is_not_empty() else None


async def get_others() -> list[Table]:
    others = [
        await find_pythoneer_supreme(),
        await find_fearless_rustbeard(),
        await find_writer(),
        await find_belle_vue(),
        await find_python_projector(),
        await find_docker_builder(),
        await find_docker_composer(),
        await find_conditional_developer(),
        await find_css_painter(),
        await find_dba(),
        await find_destroyer(),
        await find_djson(),
        await find_fake_developer(),
        await find_functional_developer(),
        await find_groovyer(),
        await find_kotlin_islander(),
        await find_maven_man(),
        await find_merger(),
        await find_swagger_star(),
        await find_tester(),
        await find_yaml_descriptor(),
    ]
    return [other for other in others if other]


def __truncate(f: float, n: int = 2) -> float:
    return float(format(f, f".{n}f"))
