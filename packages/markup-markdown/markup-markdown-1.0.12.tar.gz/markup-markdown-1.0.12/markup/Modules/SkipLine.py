# -*- coding: utf-8 -*-
# Copyright 2022 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from markup.Module import Module
from markup.Transform import Transform


class SkipLine(Module):
    """
    Module for skip lines
    """

    marker = "<!-- markup:skip-line -->"

    def transform(self, data):
        transforms = []
        linenum = 0

        for line in data:
            striped = line.strip()
            if striped.startswith(self.marker) or striped.endswith(self.marker):
                transform = Transform(linenum, "drop")
                transforms.append(transform)
            linenum = linenum + 1

        return transforms
