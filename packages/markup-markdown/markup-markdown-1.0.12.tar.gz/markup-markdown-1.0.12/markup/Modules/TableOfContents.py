# -*- coding: utf-8 -*-
# Copyright 2015 John Reese
# Modifications copyright (C) 2022 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re
import sys

from markup.Module import Module
from markup.Transform import Transform

'''
constants
'''
# language code for headline 1: cn(zh_CN); en(en_US)
tocre = re.compile(r"^!TOC(\s+[1-6])?(\s+\w+)?(\s+\w+)?\s*$")
atxre = re.compile(r"^(#+)\s*(.+)$")
setextre = re.compile(r"^(=+|-+)\s*$")
fencedcodere = re.compile(r"^```[ \w]*$")
linkre = re.compile(r"(\[(.*?)\][\(\[].*?[\)\]])")
cn_digits = dict({
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
    "10": "十",
    "11": "十一",
    "12": "十二",
    "13": "十三",
    "14": "十四",
    "15": "十五",
    "16": "十六",
    "17": "十七",
    "18": "十八",
    "19": "十九",
    "20": "二十",
    "21": "二十一",
    "22": "二十二",
    "23": "二十三",
    "24": "二十四",
    "25": "二十五",
    "26": "二十六",
    "27": "二十七",
    "28": "二十八",
    "29": "二十九",
    "30": "三十",
    "31": "三十一",
    "32": "三十二",
    "33": "三十三",
    "34": "三十四",
    "35": "三十五",
    "36": "三十六",
    "37": "三十七",
    "38": "三十八",
    "39": "三十九",
    "40": "四十",
    "41": "四十一",
    "42": "四十二",
    "43": "四十三",
    "44": "四十四",
    "45": "四十五",
    "46": "四十六",
    "47": "四十七",
    "48": "四十八",
    "49": "四十九",
})
TOC_MODE_SECTION_ONLY = "section_only"
TOC_MODE_INDEX_N_SECTION = "top_and_section"
TOC_DEFAULT_TOP_DEPTH = 6

'''
figures
'''


def matched_figure(x): return x.strip().startswith(
    "![") and x.strip().endswith(")")


def matched_figure_caption(x): return x.strip(
)[x.strip().index("![") + 2:x.strip().index("]("):]


# tables


def matched_table(x): return x.strip().startswith(
    "<!-- markup:table-caption") and x.strip().endswith("-->")


def matched_table_caption(x): return x.strip()[26:len(x.strip()) - 3:]


class TableOfContents(Module):
    """
    Module for auto-generating a table of contents based on the Markdown
    headers in the document.  The table of contents is inserted in the document
    wherever a `!TOC` marker is found at the beginning of a line.
    """

    @staticmethod
    def clean_html_string(string):
        replacements = [
            ("&", "&amp;"),
            ("<", "&lt;"),
            (">", "&gt;"),
            ("\"", "&quot;"),
            ("'", "&#39;"),
        ]
        for to_replace, with_what in replacements:
            string = string.replace(to_replace, with_what)
        return string

    @staticmethod
    def clean_title(title):
        for link in re.findall(linkre, title):
            title = title.replace(link[0], link[1])
        return title

    def fix_intent(self, section):
        """
        Fix intent
        """
        ret = ""
        count = section.count(".") - 1
        if count > 0:
            ret = "&nbsp;&nbsp;&nbsp;&nbsp;" * count

        return ret

    def fix_section_with_lang(self, section, lang):
        # print("fix_section_with_lang: section", section, ", lang", lang)
        ret = section
        if section.count(".") == 1 and lang == "cn":
            section = section.strip().replace(".", "").replace("\\", "").strip()

            if not section in cn_digits:
                print("Key not found in cn_digits: %s" % section)
                sys.exit(1)

            ret = "第" + cn_digits[section] + "章、"

        # print("fix_section_with_lang: ret", ret)
        return ret

    def resolve_figure_marker(self, lang):
        if lang == "cn":
            return "图 "
        else:
            return "Figure "

    def resolve_table_marker(self, lang):
        if lang == "cn":
            return "表 "
        else:
            return "Table "

    def resolve_chatper_index(self, linenum, transforms):
        figure_index_chapter = 0
        for x in transforms:
            if x.oper != "swap":
                continue
            # print(x.linenum, x.oper, x.data)
            if x.linenum < linenum:
                y = x.data.strip()
                if y.startswith("## "):
                    figure_index_chapter = figure_index_chapter + 1
            else:
                break
        return figure_index_chapter

    def transform(self, data):
        transforms = []

        lowestdepth = 10

        tocfound = False
        toclines = []
        tocdepth = 0
        tocdata = ""
        toch1lang = "en"
        tocmode = TOC_MODE_INDEX_N_SECTION  # 是否生成文档头部的索引目录

        headers = {}
        figures = {}

        tables = {}

        infencedcodeblock = False
        infencedcodecount = 0

        # iterate through the document looking for markers and headers
        linenum = 0
        lastline = ''
        for line in data:

            striped = line.strip()
            '''
            Bypass page breaker
            https://pandoc.org/MANUAL.html#extension-raw_attribute
            ```{=openxml}
            <w:p>
            <w:r>
                <w:br w:type="page"/>
            </w:r>
            </w:p>
            ```
            '''

            # Fenced code blocks (Github-flavored markdown)
            counted = line.count("```")
            # print("infencedcodecount", infencedcodecount, counted, striped)
            infencedcodecount = infencedcodecount + counted
            # print("infencedcodecount", infencedcodecount)
            if (infencedcodecount % 2) == 0:
                infencedcodeblock = False
            else:
                infencedcodeblock = True

            if striped.startswith("```") or striped.startswith("<w:") or striped.startswith("</w:"):
                linenum = linenum + 1
                continue

            if infencedcodeblock:
                linenum = linenum + 1
                continue

            # !TOC markers
            match = tocre.search(line)
            if match:
                tocfound = True
                depth = match.group(1)
                if depth is not None:
                    depth = int(depth)
                    tocdepth = max(depth, tocdepth)
                toclines.append(linenum)

                h1lang = match.group(2)
                if h1lang is not None:
                    h1lang = h1lang.strip().lower()
                    if h1lang in ["en", "cn"]:
                        toch1lang = h1lang
                    else:
                        print("Unexpected lang code for toc, avaiable code: en, cn")
                        sys.exit(1)

                mode = match.group(3)
                if mode is not None:
                    mode = mode.strip().lower()
                    if mode in [TOC_MODE_SECTION_ONLY, TOC_MODE_INDEX_N_SECTION]:
                        tocmode = mode
                    else:
                        print("Unexpected mode for toc, avaiable code: %s" % ([TOC_MODE_SECTION_ONLY,
                                                                           TOC_MODE_INDEX_N_SECTION]))
                        sys.exit(1)

                print("[INFO] TOC is turn on, max tocdepth %d, H1 lang %s, mode %s" % (
                    TOC_DEFAULT_TOP_DEPTH if tocdepth == 0 else tocdepth, toch1lang, tocmode))

            # hash headers
            match = atxre.search(line)
            if match:
                depth = len(match.group(1))
                title = match.group(2).strip()
                headers[linenum] = (depth, title)

                if tocfound:
                    lowestdepth = min(depth, lowestdepth)

            # underlined headers
            match = setextre.search(line)
            if match and lastline.strip():
                depth = 1 if match.group(1)[0] == "=" else 2
                title = lastline.strip()
                headers[linenum - 1] = (depth, title)

                if tocfound:
                    lowestdepth = min(depth, lowestdepth)

            # figures
            if matched_figure(line):
                figure_cap = matched_figure_caption(line)
                # print("figure_cap", figure_cap, depth, linenum)
                # set index as emtpy string, resolve later.
                figures[linenum] = ("", figure_cap)

            # tables
            if matched_table(line):
                table_cap = matched_table_caption(line)
                # set index as emtpy string, resolve later.
                tables[linenum] = ("", table_cap)

            lastline = line
            linenum += 1

        # short circuit if no !TOC directive
        if not tocfound:
            return []

        if tocdepth == 0:
            tocdepth = TOC_DEFAULT_TOP_DEPTH

        stack = []
        headernum = 0

        lastdepth = 1
        depthoffset = 1 - lowestdepth

        keys = sorted(headers.keys())

        short_titles = []

        # interate through the list of headers, generating the nested table
        # of contents data, and creating the appropriate transforms
        for linenum in keys:
            if linenum < toclines[0]:
                continue

            (depth, title) = headers[linenum]
            depth += depthoffset
            short = re.sub(r"([\s,-,\(,\)]+)", "",
                           TableOfContents.clean_title(title)).lower()

            if short in short_titles:
                i = 1
                short_i = short
                while short_i in short_titles:
                    short_i = short + "-" + str(i)
                    i += 1
                short = short_i
            short_titles.append(short)

            while depth > lastdepth:
                stack.append(headernum)
                headernum = 0
                lastdepth += 1

            while depth < lastdepth:
                headernum = stack.pop()
                lastdepth -= 1

            headernum += 1

            if depth > tocdepth:
                continue

            if depth == 1:
                section = "%d\\. " % headernum
            else:
                section = (".".join([str(x) for x in stack]) +
                           ".%d\\. " % headernum)

            short = TableOfContents.clean_html_string(short)
            title = TableOfContents.clean_html_string(title).strip()

            # top texts in doc as Toc
            tocdata += ("%s%s [%s](#%s)  \n" %
                        (self.fix_intent(section), self.fix_section_with_lang(section, toch1lang), TableOfContents.clean_title(title), short))

            # each section header in Doc
            transforms.append(Transform(linenum, "swap",
                                        data[linenum].replace(title,
                                                              self.fix_section_with_lang(section, toch1lang) + title)))

            # create shortcut link
            if tocmode != TOC_MODE_SECTION_ONLY:
                transforms.append(Transform(linenum, "prepend",
                                            "<a name=\"%s\"></a>\n\n" % short))

        # create transforms for the !TOC markers
        for linenum in toclines:
            if tocmode == TOC_MODE_SECTION_ONLY:
                transforms.append(Transform(linenum, "drop"))
            else:
                transforms.append(Transform(linenum, "swap", tocdata))

        # for x in transforms:
        #     print("transform --> %s %s %s" % (x.linenum, x.oper, x.data))

        # create caption for figures
        figure_index_num = 1
        figure_index_pre = 0
        for linenum in figures.keys():
            figure_index_curr = self.resolve_chatper_index(linenum, transforms)
            if figure_index_curr != figure_index_pre:
                figure_index_num = 1
                figure_index_pre = figure_index_curr
            else:
                figure_index_num = figure_index_num + 1

            transforms.append(Transform(linenum, "swap", data[linenum].replace("![%s](" % list(figures[linenum])[1],
                                                                               "![%s%s %s](" % (
                                                                                   self.resolve_figure_marker(
                                                                                       toch1lang),
                                                                                   "%d.%d" % (figure_index_curr,
                                                                                              figure_index_num) if figure_index_curr != 0 else "%d" % (
                                                                                           figure_index_num - 1),
                                                                                   list(figures[linenum])[1]), 1)))

        # create caption for tables
        table_index_num = 1
        table_index_pre = 0
        for linenum in tables.keys():
            # print("fff linenum", linenum)
            table_index_curr = self.resolve_chatper_index(linenum, transforms)
            # print("table_index_curr", table_index_curr, ", table_index_pre", table_index_pre)
            if table_index_curr != table_index_pre:
                table_index_num = 1
                table_index_pre = table_index_curr
            else:
                table_index_num = table_index_num + 1

            swap_content = (self.resolve_table_marker(toch1lang),
                            "%d.%d" % (table_index_curr, table_index_num) if table_index_curr != 0 else "%d" % (
                                    table_index_num - 1),
                            list(tables[linenum])[1])
            # print("SWAP TABLE", swap_content)
            transforms.append(
                Transform(linenum, "swap", "Table: %s%s %s\n" % swap_content))

        return transforms
