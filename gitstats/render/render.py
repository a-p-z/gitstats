from jinja2 import Environment
from jinja2 import PackageLoader

from gitstats.render.cemetery import get_cemetery
from gitstats.render.commits_and_impact import get_commits_and_impacts_by_author
from gitstats.render.commits_and_impact import get_commits_by_author
from gitstats.render.commits_and_impact import get_commits_over_time_by_author
from gitstats.render.commits_and_impact import get_cumulated_commits_over_time_by_author
from gitstats.render.commits_and_impact import get_impact_over_time
from gitstats.render.commits_and_impact import get_most_frequently_committed_filenames
from gitstats.render.commits_and_impact import get_most_impactful_commits
from gitstats.render.commits_on_behalf_of import get_commits_on_behalf_of
from gitstats.render.eloc import get_edited_lines_of_code_and_stability_by_author
from gitstats.render.eloc import get_edited_lines_of_code_by_author
from gitstats.render.files import get_files_by_extension
from gitstats.render.others import get_others
from gitstats.render.references import get_forgotten_refs
from gitstats.render.references import get_total_refs_over_author


async def render(format_: str) -> str:
    file_loader = PackageLoader("gitstats", "render")
    env = Environment(loader=file_loader)
    template = env.get_template(f"templates/{format_}.jinja")
    return template.render(
        cemetery=await get_cemetery(),
        commits_and_impacts_by_author=await get_commits_and_impacts_by_author(),
        commits_by_author=await get_commits_by_author(),
        commits_on_behalf_of=await get_commits_on_behalf_of(),
        commits_over_time_by_author=await get_commits_over_time_by_author(),
        cumulated_commits_over_time_by_author=await get_cumulated_commits_over_time_by_author(),
        edited_lines_of_code_and_stability_by_author=await get_edited_lines_of_code_and_stability_by_author(),
        edited_lines_of_code_by_author=await get_edited_lines_of_code_by_author(),
        files_by_extension=await get_files_by_extension(),
        forgotten_refs=await get_forgotten_refs(),
        impact_over_time=await get_impact_over_time(),
        most_frequently_committed_filenames=await get_most_frequently_committed_filenames(),
        most_impactful_commits=await get_most_impactful_commits(),
        others=await get_others(),
        total_refs_over_author=await get_total_refs_over_author(),
    )
