import argparse
import asyncio
import time
from asyncio import get_event_loop
from pathlib import Path

from git import Git
from git import Repo

from gitstats.clients.confluence import ConfluenceClient
from gitstats.infrastructure.git.usernames import get_users
from gitstats.infrastructure.logging import logger
from gitstats.infrastructure.scope import application_scope
from gitstats.render.render import render


async def update_confluence_page(base_url: str, gitstats: str, page_id: int, password: str, username: str):
    client = ConfluenceClient(base_url, username, password)
    try:
        content = await client.get_content_by_id(page_id)
        title = content.get("title", "Gitstats")
        version = content.get("version", {}).get("number", 1)
        storage = await client.wiki2storage(gitstats)
        await client.update(page_id, title, storage, version + 1)
    except Exception as e:
        logger.error("Error uploading gitstats on confluence: %s", e)


async def print_to_file(format_: str, gitstats: str):
    match format_:
        case "confluencewiki":
            filename = "gitstats.confluencewiki.txt"
        case "markdown":
            filename = "markdown.md"
        case _:
            filename = format_

    path = Path(filename)
    event_loop = get_event_loop()
    await event_loop.run_in_executor(None, path.write_text, gitstats)


async def main(
    base_url: str | None,
    format_: str,
    page_id: int | None,
    password: str | None,
    project_directory: str,
    username: str | None,
    username_map: str | None,
):
    start = time.perf_counter()
    application_scope.register(Git, Repo(project_directory).git)
    application_scope.register("users", await get_users(username_map))
    gitstats = await render(format_)
    logger.info("--- %s seconds ---", time.perf_counter() - start)
    if (
        format_ == "confluencewiki"
        and base_url is not None
        and page_id is not None
        and password is not None
        and username is not None
    ):
        await update_confluence_page(base_url, gitstats, page_id, password, username)
    else:
        await print_to_file(format_, gitstats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gitstats - a statistical analysis tool for git repositories.")
    parser.add_argument(
        "--format",
        choices=("confluencewiki", "markdown"),
        required=True,
        help="print the results in markdown or in confluence wiki format.",
    )
    parser.add_argument(
        "--username-map",
        help="username map file, containing email and username for each author.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.3")
    parser.add_argument("project_directory", help="working directory")

    args, _ = parser.parse_known_args()

    if args.format == "confluencewiki":
        parser.add_argument(
            "--base-url",
            help="base url of your confluence e.g. https://your-company.org.",
        )
        args, _ = parser.parse_known_args()
        if args.base_url:
            parser.add_argument("--username", required=True, help="username.")
            parser.add_argument("--password", required=True, help="password.")
            parser.add_argument(
                "--page-id",
                required=True,
                help="id of an existing page id on your confluence.",
            )

    asyncio.run(
        main(
            getattr(args, "base_url", None),
            args.format,
            getattr(args, "page_id", None),
            getattr(args, "password", None),
            args.project_directory,
            getattr(args, "username", None),
            args.username_map,
        )
    )
