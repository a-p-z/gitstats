# gitstats
**gitstats** is a simple statistical analysis tool for git repositories written in python.
It analyzes the history of the repository and shows general statistics per author.
It was purely developed for fun, to create a little friendly competition among team members.
Nevertheless, it calculates interesting timeline analysis and reports code changes over time for a high level overview over the repository.

## Requirements
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Poetry](https://python-poetry.org)
- [Python3.9](https://www.python.org/downloads/release/python-390/)
 
### How to install poetry [>](https://python-poetry.org/docs/)
```shell
curl -sSL https://install.python-poetry.org | python3 -
```
Set virtualenv in project
```shell
poetry config virtualenvs.in-project true
```
Create virtualenv
```commandline
poetry install
```
Run test
```shell
poetry run pytest
```
Run test with coverage
```shell
poetry run pytest --cov=src --cov-report=html tests
```

## Some features
- Cumulated commits over time by author
- Impacts over time
- Commits over time by authors
- Authors not active for over a year
- Commits by Author
- Commits without ticket reference by author
- Commits on behalf of
- Reviews
- Remote origin refs by author
- Files by extension
- Edited lines of code by author
- Most impactful commits
- Other statistics (global and of the month)

## Formats
- [markdown](https://en.wikipedia.org/wiki/Markdown)
- [confluencewiki](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html) with the possibility to automatically update a page

### Markdown
```shell
$ poetry run python src/gitstats.py --format markdown <project-directory>
```
Open the output file `gitstats.md` with a markdown viewer.

### Confluencewiki
```shell
$ poetry run python src/gitstats.py --format confluencewiki <project-directory>
```
or
```shell
$ poetry run python src/gitstats.py --format confluencewiki --base-url <base-url> --username <username> --password <password> --page-id <page-id> <project-directory>
```

![cumulated commits over time by authors](images/01-cumulatedCommitsOverTimeByAuthors.png?raw=true "Cumulated commits over time by authors")
![impact over time](images/02-impactsOverTime.png?raw=true "Impacts over time")
![commits over time by authors](images/03-commitsOverTimeByAuthors.png?raw=true "Commits over time by authors")
![commits by author](images/04-commitsByAuthor.png?raw=true "Commits by author")
![files by extension](images/05-filesByExtension.png?raw=true "Files by extension")
![edited lines of code by author](images/06-editedLinesOfCodeByAuthor.png?raw=true "Edited lines of code by author")

## Username map file
A username map file can be used to map usernames and emails. 
The # character begins a comment to the end of line, blank lines are ignored.
Each line in the file consists of a username and the email address used in the commit in <>. For example:
```
apz <antpza@gmail.com>
```

## Related projects
- [Git](https://git-scm.com/)
- [GitStats - git history statistics generator](http://gitstats.sourceforge.net/)
- [Gitinspector](https://github.com/ejwa/gitinspector)

