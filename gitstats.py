#!/usr/bin/env python
import argparse
from core import Template
from plaintext import PlainTextContentBuilder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gitstat - a statistical analysis tool for git repositories')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    
    template = Template('plaintext')
    contents = PlainTextContentBuilder.build()
    
    value = template.fill(contents)
    
    print value
