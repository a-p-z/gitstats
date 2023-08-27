from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.data.model.blame import Blame
from gitstats.stats.edited_lines_of_code import count_edited_lines_of_code_by_author
from gitstats.stats.edited_lines_of_code import count_empty_lines_of_code_by_author
from tests import a_blame
from tests import a_filename
from tests import an_author
from tests import another_author


@mark.asyncio
@patch("gitstats.stats.edited_lines_of_code.get_blames")
async def test_count_empty_lines_of_code_by_author(mock_get_blames: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_blames.return_value = [
        a_blame(author=author1, content="   "),
        a_blame(author=author1),
        a_blame(author=author1, content="\n"),
        a_blame(author=author1),
        a_blame(author=author1, content="\t"),
        a_blame(author=author2),
        a_blame(author=author2, content=""),
        a_blame(author=author2),
    ]

    assert await count_empty_lines_of_code_by_author() == {author1: 3, author2: 1}


@mark.asyncio
@patch("gitstats.stats.edited_lines_of_code.get_blames")
async def test_count_edited_lines_of_code_by_author(mock_get_blames: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_blames.return_value = [
        a_blame(author=author1, filename=a_filename("java")),
        a_blame(author=author1, filename=a_filename("py")),
        a_blame(author=author2, filename=a_filename("py")),
        a_blame(author=author2, filename=a_filename("java")),
        a_blame(author=author2, filename=a_filename("java")),
        a_blame(author=author2, filename=a_filename("py")),
    ]

    def is_java(blame: Blame) -> bool:
        return Blame.is_java(blame)

    assert await count_edited_lines_of_code_by_author(is_java) == {author1: 1, author2: 2}
