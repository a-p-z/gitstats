#!/usr/bin/env python
import argparse
from core import Template
from plaintext import PlainTextContentBuilder
from confluence import ConfluenceContentBuilder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gitstats - a statistical analysis tool for git repositories')
    parser.add_argument('--format', choices=('plaintext', 'confluence'), required=True, help="format the results in plaintext or confluence wiki markup format")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    
    if args.format == 'confluence':
        template = Template('confluence')
        contents = ConfluenceContentBuilder.build()

    elif args.format == 'plaintext':
        template = Template('plaintext')
        contents = PlainTextContentBuilder.build()
    
    value = template.fill(contents)
    
    print value
