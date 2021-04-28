# gitstats
**gitstats** is a simple statistical analysis tool for git repositories written in python.
It analyzes the history of the repository and shows general statistics per author.
It was purely developed for fun and to create a little friendly competition among team members.
Furthermore, it calculates interesting timeline analysis and reports code changes over time for a high level overview over the repository.

### Execution
gitstats can be executed running the command ``gitstats.py`` in the repository directory.
```sh
$ cd $PROJECT_DIRECTORY
$ $GITSTATS_DIRECTORY/gitstats.py --format markdown > gitstats.md
```
## Example outputs
**gitstats** is based on templates which you can customize your output
### Markdown
#### CUMULATED COMMITS OVER TIME BY AUTHOR
|date|Romolo|Numa Pompilio|Tullo Ostilio|Anco Marzio|Tarquinio Prisco|Servio Tullio|Tarquinio il Superbo|
|---|---|---|---|---|---|---|---|
|2016-02|0|0|0|0|0|0|0|
|2016-03|5|5|0|0|0|0|0|
|2016-04|56|33|0|0|0|0|0|
|2016-05|112|45|0|0|0|0|0|
|2016-06|126|70|0|0|0|2|0|
|2016-07|128|84|19|4|0|2|0|
|2016-08|133|110|21|20|0|2|0|
|2016-09|136|117|43|28|0|2|0|
|2016-10|137|135|94|43|8|2|0|
|2016-11|137|159|109|56|23|2|0|
|2016-12|137|177|128|69|49|2|0|
|2017-01|137|183|145|75|62|2|0|
|2017-02|137|199|213|86|75|2|0|
|2017-03|137|216|250|104|95|2|0|
|2017-04|137|230|295|119|120|2|0|
|2017-05|137|233|338|130|128|2|12|
|2017-06|137|233|388|148|153|2|20|
|2017-07|137|233|400|158|161|2|29|

[...]

#### COMMITS BY AUTHOR
|author|commits|insertions|deletions|% of changes|impact/commit|
|---|---|---|---|---|---|
|Tullo Ostilio|400|273229|239169|57|1280|
|Numa Pompilio|233|65995|27998|10|403|
|Tarquinio Prisco|161|73754|48478|13|759|
|Anco Marzio|158|83017|30135|12|716|
|Romolo|137|23831|14835|4|282|
|Tarquinio il Superbo|29|4609|833|0|187|
|Servio Tullio|2|28|18|0|23|
|total|1120|524463|361466|||

[...]

### Confluence wiki
Pages in [Confluence](https://www.atlassian.com/software/confluence) can be created with wiki markup. Using this mode **gitstats** prepares a content using that you can easily insert in the editor:
1. Choose **Insert** > **Markup**
2. Select **Confluence wiki**
3. Paste your text - the preview will show you how it will appear on your page
4. Choose **Insert**

![cumulated commits over time by authors](images/01-cumulatedCommitsOverTimeByAuthors.png?raw=true "Cumulated commits over time by authors")
![impacts over time](images/02-impactsOverTime.png?raw=true "Impacts over time")
![commits over time by authors](images/03-commitsOverTimeByAuthors.png?raw=true "Commits over time by authors")
![commits by author](images/04-commitsByAuthor.png?raw=true "Commits by author")
![files by extension](images/05-filesByExtension.png?raw=true "Files by extension")
![edited lines of code by author](images/06-editedLinesOfCodeByAuthor.png?raw=true "Edited lines of code by author")

See [Confluence Wiki Markup](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html)
TODO: create a client to directly create the page

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

## Requirements
- Git
- Python 3

## Related projects
- [Git](https://git-scm.com/)
- [GitStats - git history statistics generator](http://gitstats.sourceforge.net/)
- [Gitinspector](https://github.com/ejwa/gitinspector)
