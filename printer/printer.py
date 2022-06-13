from typing import List

from core import gitstatsLib, gitshortlog
from core.mailmap import Mailmap
from core.model.blame import Blame
from core.model.fileType import FileType
from core.model.numstat import Numstat
from core.regexes import Regexes
from core.utilities import add_impact_commit_column
from core.utilities import add_percentage_of_changes_column
from core.utilities import apply_to_column
from core.utilities import apply_to_row
from core.utilities import cumulate_rows
from core.utilities import group_rows_by_year
from core.utilities import limit
from core.utilities import replace_author_column, filter_active_authors
from core.utilities import replace_author_row
from core.utilities import sum_by_column
from core.utilities import sum_by_row
from printer.confluence import ConfluenceWikiFormatter
from printer.markdown import MarkdownFormatter


class Printer:

    def __init__(self, _format):
        self.__formatter = ConfluenceWikiFormatter() if _format == "confluencewiki" else MarkdownFormatter()

    def print(self, numstat: List[Numstat], blame: List[Blame]):
        self.__print_cumulated_commits_over_time_by_author(numstat)
        print(self.__formatter.sep())

        self.__print_impacts_over_time(numstat)
        print(self.__formatter.sep())

        self.__print_commits_over_time_by_author(numstat)
        print(self.__formatter.sep())

        self.__print_cemetery()
        print(self.__formatter.sep())

        self.__print_commits_and_impacts_by_author(numstat)
        print(self.__formatter.sep())

        self.__print_commits_by_committer(numstat)
        print(self.__formatter.sep())

        self.__print_reviews(numstat)
        print(self.__formatter.sep())

        self.__print_refs_remotes_origin()
        print(self.__formatter.sep())

        self.__print_most_frequently_committed_files(numstat)
        print(self.__formatter.sep())

        self.__print_edited_lines_of_code_by_author(numstat, blame)
        print(self.__formatter.sep())

        self.__print_most_impact_commits(numstat)
        print(self.__formatter.sep())

        self.__print_other([
            ["MavenMAN",
             "with %d edited lines in pom.xml  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.POM_XML])],

            ["SwaggerSTAR",
             "with %d edited lines in swagger.yml files  \n followed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.SWAGGER_YML])],

            ["Destroyer",
             "with a mean of %d deletions for commit (only sources)  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_deletion_ratio_by_author(numstat,
                                                        [FileType.JAVA,
                                                         FileType.GROOVY,
                                                         FileType.KOTLIN,
                                                         FileType.JAVASCRIPT,
                                                         FileType.TYPESCRIPT])],

            ["Groovyer",
             "with %d edited lines in groovy files (only sources)  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.GROOVY])],

            ["Kotlin Star",
             "with %d edited lines in kotlin files (only sources)  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.KOTLIN])],

            ["Tester",
             "with %d edited lines in tests  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame,
                                                              [FileType.JAVA_TEST,
                                                               FileType.JAVA_IT,
                                                               FileType.GROOVY_TEST,
                                                               FileType.KOTLIN_TEST,
                                                               FileType.JAVASCRIPT_TEST,
                                                               FileType.TYPESCRIPT_TEST])],

            ["Merger",
             "with %d merge committed  \n followed by %s with %d commits and %s with %d commits",
             gitshortlog.count_merges_by_author()],

            ["DjSON",
             "with %d edited lines in json files  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.JSON])],

            ["Fake Developer",
             "with %d empty lines (only sources)  \nfollowed by %s with %d empty lines and %s with %d empty lines",
             gitstatsLib.count_empty_lines_of_code_by_author(blame,
                                                             [FileType.JAVA,
                                                              FileType.GROOVY,
                                                              FileType.KOTLIN,
                                                              FileType.JAVASCRIPT,
                                                              FileType.TYPESCRIPT])],

            ["Functional Developer",
             "with %d lambda definitions (only JAVA sources)  \nfollowed by %s with %d lambdas and %s with %d lambdas",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.JAVA], r".*->|.*::")],

            ["Conditional Developer",
             "with %d if conditions created (only sources)  \nfollowed by %s with %d ifs and %s with %d ifs",
             gitstatsLib.count_edited_lines_of_code_by_author(blame,
                                                              [FileType.JAVA,
                                                               FileType.GROOVY,
                                                               FileType.KOTLIN,
                                                               FileType.JAVASCRIPT,
                                                               FileType.TYPESCRIPT],
                                                              r".*if")],
            ["DBA",
             "with %d edited lines in SQL files  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.SQL])],

            ["Css painter",
             "with %d edited lines in css files  \nfollowed by %s with %d eloc and %s with %d eloc",
             gitstatsLib.count_edited_lines_of_code_by_author(blame, [FileType.CSS])]])

        print(self.__formatter.h6("generated by %s" %
                                  self.__formatter.link("gitstats", "https://github.com/a-p-z/gitstats")))

    def __print_cumulated_commits_over_time_by_author(self, numstat):
        print(self.__formatter.section())
        print(self.__formatter.h2("Cumulated commits over time by author"))
        header, data = gitstatsLib.count_commits_over_month_by_author(numstat)
        header = replace_author_row(header)
        if len(data) > 12:
            data_a = data[:-12]
            data_b = data[-12:]
            data_a = group_rows_by_year(data_a)
            data = data_a + data_b
        cumulate_rows(data)
        print(self.__formatter.chart(header,
                                     data,
                                     confluence={"type": "area",
                                                 "width": 1024,
                                                 "height": 340,
                                                 "stacked": True,
                                                 "opacity": 80,
                                                 "dataOrientation": "vertical",
                                                 "categoryLabelPosition": "down90"},
                                     md="|%s|" % "|".join(["---:"] * len(header))))
        print(self.__formatter.section())

    def __print_impacts_over_time(self, numstat):
        print(self.__formatter.section())
        print(self.__formatter.h2("Impacts over time"))
        header = ("date", "insertions", "deletions")
        data = gitstatsLib.get_impacts_over_month(numstat)
        if len(data) > 12:
            data_a = data[:-12]
            data_b = data[-12:]
            data_a = group_rows_by_year(data_a)
            data = data_a + data_b
        print(self.__formatter.chart(header,
                                     data,
                                     confluence={"type": "area",
                                                 "width": 1024,
                                                 "height": 340,
                                                 "stacked": True,
                                                 "opacity": 80,
                                                 "dataOrientation": "vertical",
                                                 "categoryLabelPosition": "down90",
                                                 "colors": "#18FF6D,#FF7780"},
                                     md="|---:|---:|---:|"))
        print(self.__formatter.section())

    def __print_commits_over_time_by_author(self, numstat):
        print(self.__formatter.section())
        print(self.__formatter.h2("Commits over time by authors"))
        header, data = gitstatsLib.count_commits_over_month_by_author(numstat)
        header = replace_author_row(header)
        if len(data) > 12:
            data_a = data[:-12]
            data_b = data[-12:]
            data_a = group_rows_by_year(data_a)
            data = data_a + data_b
        print(self.__formatter.chart(header,
                                     data,
                                     confluence={"type": "area",
                                                 "width": 1024,
                                                 "height": 340,
                                                 "opacity": 40,
                                                 "dataOrientation": "vertical",
                                                 "categoryLabelPosition": "down90"},
                                     md="|%s|" % "|".join(["---:"] * len(header))))
        print(self.__formatter.section())

    def __print_cemetery(self):
        print(self.__formatter.section())
        print(self.__formatter.h2("Cemetery (it happens to the best of us: authors not active for over a year)"))
        dead = sorted(set(filter(lambda x: not x.is_active(), Mailmap.instance().authors_by_email.values())),
                      key=lambda d: d.end)
        header = replace_author_row(dead)
        data = list(map(lambda d: "%s - %s" % (d.start.strftime("%d/%m/%Y"), d.end.strftime("%d/%m/%Y")), dead))
        print(self.__formatter.table(header, [data], md="|%s|" % "|".join([":---:"] * len(header))))  # gravestone
        print(self.__formatter.section())

    def __print_commits_and_impacts_by_author(self, numstat):
        print(self.__formatter.section())
        print(self.__formatter.h2("Commits by Author"))
        print(self.__formatter.column())
        # TODO add star
        header = ("author", "commits", "insertions", "deletions", "% of changes", "impact/commit")
        data = gitstatsLib.count_commits_and_impacts_by_author(numstat)
        replace_author_column(data)
        data = add_percentage_of_changes_column(data, insertions_index=2, deletions_index=3)
        data = add_impact_commit_column(data, insertions_index=2, deletions_index=3, commits_index=1)
        total = sum_by_row(data, len(header))
        total[0] = "total"
        total[4] = ""
        total[5] = ""
        data.append(total)
        apply_to_row(data, -1, self.__formatter.bold)
        print(self.__formatter.table(header, data, md="|:---|---:|---:|---:|---:|---:|"))
        print(self.__formatter.column())

        print(self.__formatter.column())
        header = ("author", "commits")
        data = gitshortlog.count_commits_by_author()
        replace_author_column(data)
        data = limit(data, 8, True)
        print(self.__formatter.chart(header,
                                     data,
                                     confluence={"type": "pie",
                                                 "legend": False,
                                                 "dataOrientation": "vertical",
                                                 "width": 480,
                                                 "height": 340,
                                                 "opacity": 90},
                                     md="|:---|---:|"))
        print(self.__formatter.column())

        subject_regexes = Regexes.instance().subject_regexes
        if len(subject_regexes) > 0:
            header = ("author", "commits")
            data = gitstatsLib.count_not_compliant_subjects_by_author(numstat, subject_regexes)
            data = list(filter(lambda x: x[0].is_active(), data))
            replace_author_column(data)
            print(self.__formatter.chart(header,
                                         data,
                                         confluence={"type": "bar",
                                                     "orientation": "horizontal",
                                                     "dataOrientation": "vertical",
                                                     "legend": False,
                                                     "width": 480,
                                                     "height": 340,
                                                     "opacity": 90,
                                                     "title": "Commits without ticket reference",
                                                     "subTitle": "(only active authors)"},
                                         md="|:---|---:|"))
        print(self.__formatter.section())

    def __print_commits_by_committer(self, numstat):
        print(self.__formatter.section())
        print(self.__formatter.h2("Thieves (commits on behalf of) (only active committers/authors)"))
        header, data = gitstatsLib.count_commits_on_behalf_of(numstat)
        data = list(filter(lambda x: x[0].is_active(), data))
        filter_active_authors(header, data)
        header = replace_author_row(header)
        replace_author_column(data)
        total = sum_by_row(data, len(header))
        total[0] = "total"
        data.append(total)
        sum_by_column(data)
        header.append("total")
        if len(data) > 0 and len(data[-1]) > 0:
            data[-1][-1] = ""
        apply_to_column(data, 0, self.__formatter.bold)
        print(self.__formatter.table(header, data, md="|:---|%s|" % "|".join(["---:"] * (len(header) - 1))))
        print(self.__formatter.section())

    def __print_reviews(self, numstat):
        reviewer_regex = Regexes.instance().reviewer_regex
        if not reviewer_regex:
            return
        print(self.__formatter.section())
        print(self.__formatter.h2("Reviews (only active reviewers/authors)"))
        header, data = gitstatsLib.count_reviews(numstat, reviewer_regex)
        data = list(filter(lambda x: x[0].is_active(), data))
        filter_active_authors(header, data)
        header = replace_author_row(header)
        replace_author_column(data)
        total = sum_by_row(data, len(header))
        total[0] = "total"
        data.append(total)
        sum_by_column(data)
        header.append("total")
        if len(data) > 0 and len(data[-1]) > 0:
            data[-1][-1] = ""
        apply_to_column(data, 0, self.__formatter.bold)
        print(self.__formatter.table(header, data, md="|:---|%s|" % "|".join(["---:"] * (len(header) - 1))))
        print(self.__formatter.section())

    def __print_refs_remotes_origin(self):
        print(self.__formatter.section())
        print(self.__formatter.column())
        print(self.__formatter.h2("Forgotten remote origin refs"))
        header = ("last commit date", "author", "ref")
        data = gitstatsLib.sorted_refs_remotes_origin_by_date()
        data = limit(data, 10)
        apply_to_column(data, 0, lambda x: x.strftime("%d/%m/%Y"))
        replace_author_column(data, 1)
        apply_to_column(data, 2, lambda x: x.replace("refs/remotes/origin/", ""))
        print(self.__formatter.table(header, data, md="|:---|:---|:---|"))
        print(self.__formatter.column())

        print(self.__formatter.column())
        header = ("author", "total")
        data = gitstatsLib.count_refs_remotes_origin_by_author()
        data = limit(data, 8, True)
        replace_author_column(data)
        print(self.__formatter.chart(header,
                                     data,
                                     confluence={"type": "pie",
                                                 "legend": True,
                                                 "title": "Remote origin refs by author",
                                                 "dataOrientation": "vertical",
                                                 "width": 480,
                                                 "height": 400,
                                                 "opacity": 90},
                                     md="|:---|---:|"))
        print(self.__formatter.column())
        print(self.__formatter.section())

    def __print_most_frequently_committed_files(self, numstat):
        print(self.__formatter.section())
        print(self.__formatter.h2("Files by extension"))
        print(self.__formatter.column())
        header = ("extension", "total")
        data = gitstatsLib.count_files_by_extension()
        data = limit(data, 8, True)
        print(self.__formatter.chart(header,
                                     data,
                                     confluence={"type": "pie",
                                                 "legend": False,
                                                 "dataOrientation": "vertical",
                                                 "width": 480,
                                                 "height": 400,
                                                 "opacity": 90},
                                     md="|:---|---:|"))
        print(self.__formatter.column())

        print(self.__formatter.column())
        header = ("file", "commits")
        data = gitstatsLib.get_most_frequently_committed_files(numstat)
        data = limit(data, 10)
        print(self.__formatter.table(header, data, md="|:---|---:|"))
        print(self.__formatter.column())
        print(self.__formatter.section())

    def __print_edited_lines_of_code_by_author(self, numstat, blame):
        print(self.__formatter.section())
        print(self.__formatter.h2("Edited lines of code by author"))
        print("(only sources, empty line excluded)")
        print(self.__formatter.column())
        header = ("author", "edited line of code", "stability %")
        # TODO add star
        data = gitstatsLib.count_edited_lines_of_code_and_stability_by_author(numstat,
                                                                              blame,
                                                                              [FileType.JAVA,
                                                                               FileType.GROOVY,
                                                                               FileType.KOTLIN,
                                                                               FileType.JAVASCRIPT,
                                                                               FileType.TYPESCRIPT])
        replace_author_column(data)
        total = sum_by_row(data, len(header))
        total[0] = self.__formatter.bold("total")
        total[1] = self.__formatter.bold(total[1])
        total[2] = ""
        data.append(total)
        print(self.__formatter.table(header, data, md="|:---|---:|---:|"))
        print(self.__formatter.column())

        print(self.__formatter.column())
        header = ("author", "edited line of code")
        data = gitstatsLib.count_edited_lines_of_code_by_author(blame,
                                                                [FileType.JAVA,
                                                                 FileType.GROOVY,
                                                                 FileType.KOTLIN,
                                                                 FileType.JAVASCRIPT,
                                                                 FileType.TYPESCRIPT])
        replace_author_column(data)
        data = limit(data, 8, True)
        print(self.__formatter.chart(header,
                                     data,
                                     confluence={"type": "pie",
                                                 "legend": False,
                                                 "width": 480,
                                                 "height": 480,
                                                 "opacity": 90,
                                                 "dataOrientation": "vertical"},
                                     md="|:---|---:|"))
        print(self.__formatter.column())
        print(self.__formatter.section())

    def __print_most_impact_commits(self, numstat):
        print(self.__formatter.section())
        print(self.__formatter.h2("Most impactful commits"))
        header = ("date", "subject", "author", "num_of_file", "insertions", "deletions")
        data = gitstatsLib.sorted_commits_by_impact(numstat)[:10]
        replace_author_column(data, column=2)
        print(self.__formatter.table(header, data, md="|---:|:---|:---|---:|---:|---:|"))
        print(self.__formatter.section())

    def __print_other(self, items):
        print(self.__formatter.section())
        print(self.__formatter.h2("Other statistics"))
        items = list(filter(lambda x: len(x) > 2 and len(x[2]) > 2, items))
        for j in range(4):
            print(self.__formatter.column())
            for i in range(0, len(items), 4):
                if i + j >= len(items):
                    break
                print(self.__formatter.card(items[i + j][0], items[i + j][1], items[i + j][2]))
            print(self.__formatter.column())
        print(self.__formatter.section())
