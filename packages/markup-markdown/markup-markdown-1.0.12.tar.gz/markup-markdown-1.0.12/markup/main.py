#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010 John Reese
# Modifications copyright (C) 2022 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys
import markup

import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# Terminal output ANSI color codes
class colors:
    BLUE = '\033[36;49;22m'
    MAGB = '\033[35;49;1m'
    GREEN = '\033[32;49;22m'
    NORMAL = '\033[0m'


# Custom event handler for watchdog observer
class MarkdownPPFileEventHandler(PatternMatchingEventHandler):
    patterns = ["*.m.md"]

    def process(self, event):
        # Look for .m.md files
        if not event.src_path.endswith(".m.md"):
            return None

        modules = markup.modules.keys()
        mmd = open(event.src_path, 'r', encoding='UTF-8')

        # Output file takes filename from input file but has .md extension
        output_filepath = (event.src_path[::-1].replace("dm.m.", "dm.", 1))[::-1]

        print(time.strftime("%c") + ":",
              colors.MAGB + output_filepath,
              colors.GREEN + "[re-]generated",
              colors.NORMAL)
        md = open(output_filepath, 'w', encoding='UTF-8')
        markup.MarkdownPP(input=mmd, output=md, modules=modules)

        # Logs time and file changed (with colors!)
        print(time.strftime("%c") + ":",
              colors.MAGB + event.src_path,
              colors.GREEN + event.event_type,
              "and processed with Markup Markdown",
              colors.NORMAL)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


def main():
    # setup command line arguments
    parser = argparse.ArgumentParser(description='Stack up for Markdown'
                                     ' files.')

    parser.add_argument('FILENAME', help='Input file name (or directory if '
                        'watching)')

    # Argument for watching directory and subdirectory to process .m.md files
    parser.add_argument('-w', '--watch', action='store_true', help='Watch '
                        'current directory and subdirectories for changing '
                        '.m.md files and process in local directory. File '
                        'output name is same as file input name.')

    parser.add_argument('-o', '--output', help='Output file name. If no '
                        'output file is specified, writes output to stdout.')
    parser.add_argument('-e', '--exclude', help='List of modules to '
                        'exclude, separated by commas. Available modules: '
                        + ', '.join(markup.modules.keys()))
    args = parser.parse_args()

    # If watch flag is on, watch dirs instead of processing individual file
    if args.watch:
        # Get full directory path to print
        p = os.path.abspath(args.FILENAME)
        print("Watching: " + p + " (and subdirectories)")

        # Custom watchdog event handler specific for .m.md files
        event_handler = MarkdownPPFileEventHandler()
        observer = Observer()
        # pass event handler, directory, and flag to recurse subdirectories
        observer.schedule(event_handler, args.FILENAME, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    else:
        mmd = open(args.FILENAME, 'r', encoding='UTF-8')
        if args.output:
            md = open(args.output, 'w', encoding='UTF-8')
        else:
            md = sys.stdout

        modules = list(markup.modules)

        if args.exclude:
            for module in args.exclude.split(','):
                if module in modules:
                    modules.remove(module)
                else:
                    print('Cannot exclude ', module, ' - no such module')

        # fix relative refs for INCLUDE issue
        filedir =  os.path.dirname(args.FILENAME)
        if filedir:
            os.chdir(filedir)

        markup.MarkdownPP(input=mmd, output=md, modules=modules)

        mmd.close()
        md.close()


if __name__ == "__main__":
    main()
