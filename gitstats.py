#!/usr/bin/env python3
import argparse
import logging
import time
from typing import List

from core import gitlog, gitblame, gitls
from core.model.blame import Blame
from core.model.numstat import Numstat
from printer.printer import Printer

if __name__ == "__main__":
    start_time = time.process_time()
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="gitstats - a statistical analysis tool for git repositories")
    parser.add_argument("--format", choices=("markdown", "confluencewiki"), required=True,
                        help="print the results in markdown or in confluence wiki format")
    parser.add_argument("--load", action="store_true", help="try loading previous data")
    parser.add_argument("--version", action="version", version="%(prog)s 0.2")
    args = parser.parse_args()

    if args.format == "confluencewiki":
        printer = Printer("confluencewiki")

    elif args.format == "markdown":
        printer = Printer("markdown")

    else:
        parser.exit(1, args.format + "is not supported")
        raise Exception(args.format + "is not supported")

    gitlog.git_log_numstat_merges(args.load)
    numstat: List[Numstat] = gitlog.git_log_numstat_no_merges(args.load)
    files = gitls.git_ls_files()
    blame: List[Blame] = gitblame.git_blame(files, args.load)

    printer.print(numstat, blame)
    logging.info("--- %s seconds ---" % (time.process_time() - start_time))

