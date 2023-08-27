from asyncio import get_event_loop
from pathlib import Path

from aiocache import cached

from gitstats.infrastructure.git import USERNAME_MAP_PATTERN
from gitstats.infrastructure.logging import logger
from gitstats.infrastructure.scope import application_scope


@cached()
async def get_usernames_by_email() -> dict[str, str]:
    users = application_scope.resolve("users")
    return {user["email"]: user["username"] for user in users}


async def get_users(username_map: str | None) -> list[dict[str, str]]:
    if not username_map:
        return []
    path = Path(username_map)
    if not path.exists() or not path.is_file():
        return []
    logger.info("reading %s", username_map)
    event_loop = get_event_loop()
    output = await event_loop.run_in_executor(None, path.read_text)
    usernames = list()
    for line in output.split("\n"):
        match = USERNAME_MAP_PATTERN.match(line)
        if not match:
            logger.warning("%s in %s is not a valid", line, username_map)
            continue
        username, email = match[1], match[2]
        usernames.append({"username": username, "email": email.strip("<>").lower()})
    return usernames
