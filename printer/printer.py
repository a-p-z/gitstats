from typing import List

from core import gitshortlog, gitstatsLib
from core.mailmap import Mailmap
from core.model.blame import Blame
from core.model.fileType import FileType
from core.model.numstat import Numstat
from core.regexes import Regexes
from core.utilities import (
    add_impact_commit_column,
    add_percentage_of_changes_column,
    apply_to_column,
    apply_to_row,
    cumulate_rows,
    filter_active_authors,
    group_rows_by_year,
    limit,
    replace_author_column,
    replace_author_row,
    sum_by_column,
    sum_by_row,
)

from printer.confluence import ConfluenceWikiFormatter
from printer.markdown import MarkdownFormatter


class Printer:
    def __init__(self, _format):
        self.__formatter = (
            ConfluenceWikiFormatter()
            if _format == "confluencewiki"
            else MarkdownFormatter()
        )
        self.__file = (
            open("gitstats.confluencewiki.txt", "w")
            if _format == "confluencewiki"
            else open("gitstats.md", "w")
        )

    def print(self, numstat: List[Numstat], blame: List[Blame]):
        self.__print_cumulated_commits_over_time_by_author(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_impacts_over_time(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_commits_over_time_by_author(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_cemetery()
        print(self.__formatter.sep(), file=self.__file)

        self.__print_commits_and_impacts_by_author(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_commits_by_committer(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_reviews(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_refs_remotes_origin()
        print(self.__formatter.sep(), file=self.__file)

        self.__print_most_frequently_committed_files(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_edited_lines_of_code_by_author(numstat, blame)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_most_impact_commits(numstat)
        print(self.__formatter.sep(), file=self.__file)

        self.__print_other(
            [
                [
                    "Destroyer",
                    "com a média de %d remoções por commit  \nseguido por %s"
                    " com %d linhas editadas e %s com %d linhas editadas",
                    gitstatsLib.count_deletion_ratio_by_author(
                        numstat,
                        [
                            FileType.JAVA,
                            FileType.JAVASCRIPT,
                            FileType.TYPESCRIPT,
                            FileType.MARKDOWN,
                            FileType.SQL,
                            FileType.JSON,
                            FileType.CSS,
                            FileType.HTML,
                            FileType.PYTHON,
                            FileType.CSHARP,
                        ],
                    ),
                ],
                [
                    "Tester",
                    "com %d linhas editadas em testes  \nseguido por %s com %d"
                    " linhas editadas e %s com %d linhas editadas",
                    gitstatsLib.count_edited_lines_of_code_by_author(
                        blame,
                        [
                            FileType.JAVA_TEST,
                            FileType.JAVA_IT,
                            FileType.GROOVY_TEST,
                            FileType.KOTLIN_TEST,
                            FileType.JAVASCRIPT_TEST,
                            FileType.TYPESCRIPT_TEST,
                        ],
                    ),
                ],
                [
                    "Merger",
                    "com %d merges commitados  \n seguido por %s com %d"
                    " commits e %s com %d commits",
                    gitshortlog.count_merges_by_author(),
                ],
                [
                    "DjSON",
                    "com %d linhas editadas em arquivos JSON  \nseguido por %s"
                    " com %d linhas editadas e %s com %d linhas editadas",
                    gitstatsLib.count_edited_lines_of_code_by_author(
                        blame, [FileType.JSON]
                    ),
                ],
                [
                    "Fake Developer",
                    "com %d linhas vazias  \nseguido por %s com %d linhas"
                    " vazias e %s com %d linhas vazias",
                    gitstatsLib.count_empty_lines_of_code_by_author(
                        blame,
                        [
                            FileType.JAVA,
                            FileType.JAVASCRIPT,
                            FileType.TYPESCRIPT,
                            FileType.MARKDOWN,
                            FileType.SQL,
                            FileType.JSON,
                            FileType.CSS,
                            FileType.HTML,
                            FileType.PYTHON,
                            FileType.CSHARP,
                        ],
                    ),
                ],
                [
                    "Conditional Developer",
                    "com %d condicionais IF criadas  \nseguido por %s com %d"
                    " IFs e %s com %d IFs",
                    gitstatsLib.count_edited_lines_of_code_by_author(
                        blame,
                        [
                            FileType.JAVA,
                            FileType.JAVASCRIPT,
                            FileType.TYPESCRIPT,
                            FileType.MARKDOWN,
                            FileType.SQL,
                            FileType.JSON,
                            FileType.CSS,
                            FileType.HTML,
                            FileType.PYTHON,
                            FileType.CSHARP,
                        ],
                        r".*if",
                    ),
                ],
                [
                    "DBA",
                    "com %d linhas editadas em arquivos SQL  \nseguido por %s"
                    " com %d linhas editadas e %s com %d linhas editadas",
                    gitstatsLib.count_edited_lines_of_code_by_author(
                        blame, [FileType.SQL]
                    ),
                ],
                [
                    "Css painter",
                    "com %d linhas editadas em arquivos CSS  \nseguido por %s"
                    " com %d linhas editadas e %s com %d linhas editadas",
                    gitstatsLib.count_edited_lines_of_code_by_author(
                        blame, [FileType.CSS]
                    ),
                ],
            ]
        )

        print(
            self.__formatter.h6(
                "gerado por %s"
                % self.__formatter.link(
                    "gitstats", "https://github.com/a-p-z/gitstats"
                )
            ),
            file=self.__file,
        )
        self.__file.close()

    def __print_cumulated_commits_over_time_by_author(self, numstat):
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2(
                "Commits acumulados por autoria ao longo do tempo"
            ),
            file=self.__file,
        )
        header, data = gitstatsLib.count_commits_over_month_by_author(numstat)
        header = replace_author_row(header)
        if len(data) > 12:
            data_a = data[:-12]
            data_b = data[-12:]
            data_a = group_rows_by_year(data_a)
            data = data_a + data_b
        cumulate_rows(data)
        print(
            self.__formatter.chart(
                header,
                data,
                confluence={
                    "type": "area",
                    "width": 1024,
                    "height": 340,
                    "stacked": True,
                    "opacity": 80,
                    "dataOrientation": "vertical",
                    "categoryLabelPosition": "down90",
                },
                md="|%s|" % "|".join(["---:"] * len(header)),
            ),
            file=self.__file,
        )
        print(self.__formatter.section(), file=self.__file)

    def __print_impacts_over_time(self, numstat):
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2("Impactos ao longo do tempo"), file=self.__file
        )
        header = ("data", "inserções", "remoções")
        data = gitstatsLib.get_impacts_over_month(numstat)
        if len(data) > 12:
            data_a = data[:-12]
            data_b = data[-12:]
            data_a = group_rows_by_year(data_a)
            data = data_a + data_b
        print(
            self.__formatter.chart(
                header,
                data,
                confluence={
                    "type": "area",
                    "width": 1024,
                    "height": 340,
                    "stacked": True,
                    "opacity": 80,
                    "dataOrientation": "vertical",
                    "categoryLabelPosition": "down90",
                    "colors": "#18FF6D,#FF7780",
                },
                md="|---:|---:|---:|",
            ),
            file=self.__file,
        )
        print(self.__formatter.section(), file=self.__file)

    def __print_commits_over_time_by_author(self, numstat):
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2("Commits ao longo do tempo por pessoa"),
            file=self.__file,
        )
        header, data = gitstatsLib.count_commits_over_month_by_author(numstat)
        header = replace_author_row(header)
        if len(data) > 12:
            data_a = data[:-12]
            data_b = data[-12:]
            data_a = group_rows_by_year(data_a)
            data = data_a + data_b
        print(
            self.__formatter.chart(
                header,
                data,
                confluence={
                    "type": "area",
                    "width": 1024,
                    "height": 340,
                    "opacity": 40,
                    "dataOrientation": "vertical",
                    "categoryLabelPosition": "down90",
                },
                md="|%s|" % "|".join(["---:"] * len(header)),
            ),
            file=self.__file,
        )
        print(self.__formatter.section(), file=self.__file)

    def __print_cemetery(self):
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2(
                "Cemitério (pessoas inativas a mais de um ano)"
            ),
            file=self.__file,
        )
        dead = sorted(
            filter(lambda x: not x.is_active(), Mailmap.instance().get_all()),
            key=lambda d: d.end,
        )
        header = replace_author_row(dead)
        data = list(
            map(
                lambda d: "%s - %s"
                % (d.start.strftime("%d/%m/%Y"), d.end.strftime("%d/%m/%Y")),
                dead,
            )
        )
        print(
            self.__formatter.table(
                header, [data], md="|%s|" % "|".join([":---:"] * len(header))
            ),
            file=self.__file,
        )  # gravestone
        print(self.__formatter.section(), file=self.__file)

    def __print_commits_and_impacts_by_author(self, numstat):
        print(self.__formatter.section(), file=self.__file)
        print(self.__formatter.h2("Commits por pessoa"), file=self.__file)
        print(self.__formatter.column(), file=self.__file)
        # TODO add star
        header = (
            "autoria",
            "commits",
            "inserções",
            "remoções",
            "email",
            "percentual de mudanças",
            "total de mudanças / commits",
        )
        data = gitstatsLib.count_commits_and_impacts_by_author(numstat)
        print(data)
        replace_author_column(data)
        data = add_percentage_of_changes_column(
            data, insertions_index=2, deletions_index=3
        )
        data = add_impact_commit_column(
            data, insertions_index=2, deletions_index=3, commits_index=1
        )
        total = sum_by_row(data, len(header))
        total[0] = "total"
        total[4] = ""
        total[5] = ""
        data.append(total)
        apply_to_row(data, -1, self.__formatter.bold)
        print(
            self.__formatter.table(
                header, data, md="|:---|---:|---:|---:|---:|---:|---:|"
            ),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)

        print(self.__formatter.column(), file=self.__file)
        header = ("autoria", "commits")
        data = gitshortlog.count_commits_by_author()
        replace_author_column(data)
        data = limit(data, 8, True)
        print(
            self.__formatter.chart(
                header,
                data,
                confluence={
                    "type": "pie",
                    "legend": False,
                    "dataOrientation": "vertical",
                    "width": 480,
                    "height": 340,
                    "opacity": 90,
                },
                md="|:---|---:|",
            ),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)

        subject_regexes = Regexes.instance().subject_regexes
        if len(subject_regexes) > 0:
            header = ("autoria", "commits")
            data = gitstatsLib.count_not_compliant_subjects_by_author(
                numstat, subject_regexes
            )
            data = list(filter(lambda x: x[0].is_active(), data))
            replace_author_column(data)
            print(
                self.__formatter.chart(
                    header,
                    data,
                    confluence={
                        "type": "bar",
                        "orientation": "horizontal",
                        "dataOrientation": "vertical",
                        "legend": False,
                        "width": 480,
                        "height": 340,
                        "opacity": 90,
                        "title": "Commits sem tickets de referência",
                        "subTitle": "somente pessoas revisoras/autoras ativas",
                    },
                    md="|:---|---:|",
                ),
                file=self.__file,
            )
        print(self.__formatter.section(), file=self.__file)

    def __print_commits_by_committer(self, numstat):
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2(
                "Commits em nome de outra pessoa"
                " (somente pessoas revisoras/autoras ativas)"
            ),
            file=self.__file,
        )
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
        print(
            self.__formatter.table(
                header,
                data,
                md="|:---|%s|" % "|".join(["---:"] * (len(header) - 1)),
            ),
            file=self.__file,
        )
        print(self.__formatter.section(), file=self.__file)

    def __print_reviews(self, numstat):
        reviewer_regex = Regexes.instance().reviewer_regex
        if not reviewer_regex:
            return
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2(
                "Revisões (somente pessoas revisoras/autoras ativas)"
            ),
            file=self.__file,
        )
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
        print(
            self.__formatter.table(
                header,
                data,
                md="|:---|%s|" % "|".join(["---:"] * (len(header) - 1)),
            ),
            file=self.__file,
        )
        print(self.__formatter.section(), file=self.__file)

    def __print_refs_remotes_origin(self):
        print(self.__formatter.section(), file=self.__file)
        print(self.__formatter.column(), file=self.__file)
        print(
            self.__formatter.h2("Referências remotas esquecidas"),
            file=self.__file,
        )
        header = ("data do último commit", "autoria", "ref")
        data = gitstatsLib.sorted_refs_remotes_origin_by_date()
        data = limit(data, 10)
        apply_to_column(data, 0, lambda x: x.strftime("%d/%m/%Y"))
        replace_author_column(data, 1)
        apply_to_column(
            data, 2, lambda x: x.replace("refs/remotes/origin/", "")
        )
        print(
            self.__formatter.table(header, data, md="|:---|:---|:---|"),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)

        print(self.__formatter.column(), file=self.__file)
        header = ("autoria", "total")
        data = gitstatsLib.count_refs_remotes_origin_by_author()
        data = limit(data, 8, True)
        replace_author_column(data)
        print(
            self.__formatter.chart(
                header,
                data,
                confluence={
                    "type": "pie",
                    "legend": True,
                    "title": "Referências remotas na origem por pessoa",
                    "dataOrientation": "vertical",
                    "width": 480,
                    "height": 400,
                    "opacity": 90,
                },
                md="|:---|---:|",
            ),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)
        print(self.__formatter.section(), file=self.__file)

    def __print_most_frequently_committed_files(self, numstat):
        print(self.__formatter.section(), file=self.__file)
        print(self.__formatter.h2("Arquivos por extensão"), file=self.__file)
        print(self.__formatter.column(), file=self.__file)
        header = ("extensão", "total")
        data = gitstatsLib.count_files_by_extension()
        data = limit(data, 8, True)
        print(
            self.__formatter.chart(
                header,
                data,
                confluence={
                    "type": "pie",
                    "legend": False,
                    "dataOrientation": "vertical",
                    "width": 480,
                    "height": 400,
                    "opacity": 90,
                },
                md="|:---|---:|",
            ),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)

        print(self.__formatter.column(), file=self.__file)
        header = ("arquivo", "commits")
        data = gitstatsLib.get_most_frequently_committed_files(numstat)
        data = limit(data, 10)
        print(
            self.__formatter.table(header, data, md="|:---|---:|"),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)
        print(self.__formatter.section(), file=self.__file)

    def __print_edited_lines_of_code_by_author(self, numstat, blame):
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2("Linhas de código editadas por pessoa"),
            file=self.__file,
        )
        print("(only sources, empty line excluded)", file=self.__file)
        print(self.__formatter.column(), file=self.__file)
        header = (
            "autoria",
            "linhas de código editadas",
            "estabilidade percentual",
        )
        # TODO add star
        data = gitstatsLib.count_edited_lines_of_code_and_stability_by_author(
            numstat,
            blame,
            [
                FileType.JAVA,
                FileType.JAVASCRIPT,
                FileType.TYPESCRIPT,
                FileType.MARKDOWN,
                FileType.SQL,
                FileType.JSON,
                FileType.CSS,
                FileType.HTML,
                FileType.PYTHON,
                FileType.CSHARP,
            ],
        )
        replace_author_column(data)
        total = sum_by_row(data, len(header))
        total[0] = self.__formatter.bold("total")
        total[1] = self.__formatter.bold(total[1])
        total[2] = ""
        data.append(total)
        print(
            self.__formatter.table(header, data, md="|:---|---:|---:|"),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)

        print(self.__formatter.column(), file=self.__file)
        header = ("autoria", "linhas de código editadas")
        data = gitstatsLib.count_edited_lines_of_code_by_author(
            blame,
            [
                FileType.JAVA,
                FileType.JAVASCRIPT,
                FileType.TYPESCRIPT,
                FileType.MARKDOWN,
                FileType.SQL,
                FileType.JSON,
                FileType.CSS,
                FileType.HTML,
                FileType.PYTHON,
                FileType.CSHARP,
            ],
        )
        replace_author_column(data)
        data = limit(data, 8, True)
        print(
            self.__formatter.chart(
                header,
                data,
                confluence={
                    "type": "pie",
                    "legend": False,
                    "width": 480,
                    "height": 480,
                    "opacity": 90,
                    "dataOrientation": "vertical",
                },
                md="|:---|---:|",
            ),
            file=self.__file,
        )
        print(self.__formatter.column(), file=self.__file)
        print(self.__formatter.section(), file=self.__file)

    def __print_most_impact_commits(self, numstat):
        print(self.__formatter.section(), file=self.__file)
        print(
            self.__formatter.h2("Commits com maior impacto"), file=self.__file
        )
        header = (
            "data",
            "assunto",
            "autoria",
            "número do arquivo",
            "inserções",
            "remoções",
        )
        data = gitstatsLib.sorted_commits_by_impact(numstat)[:10]
        replace_author_column(data, column=2)
        print(
            self.__formatter.table(
                header, data, md="|---:|:---|:---|---:|---:|---:|"
            ),
            file=self.__file,
        )
        print(self.__formatter.section(), file=self.__file)

    def __print_other(self, items):
        print(self.__formatter.section(), file=self.__file)
        print(self.__formatter.h2("Outras estatísticas"), file=self.__file)
        items = list(filter(lambda x: len(x) > 2 and len(x[2]) > 2, items))
        for j in range(4):
            print(self.__formatter.column(), file=self.__file)
            for i in range(0, len(items), 4):
                if i + j >= len(items):
                    break
                print(
                    self.__formatter.card(
                        items[i + j][0], items[i + j][1], items[i + j][2]
                    ),
                    file=self.__file,
                )
            print(self.__formatter.column(), file=self.__file)
        print(self.__formatter.section(), file=self.__file)
