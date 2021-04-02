# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os
import sys

from textcode.analysis import numbered_text_lines
from copyrighter import detect_copyrights_from_lines

# Tracing flags
TRACE = False or os.environ.get('SCANCODE_DEBUG_COPYRIGHT', False)
# set to 1 to enable nltk deep tracing
TRACE_DEEP = 0
if os.environ.get('SCANCODE_DEBUG_COPYRIGHT_DEEP'):
    TRACE_DEEP = 1


# Tracing flags
def logger_debug(*args):
    pass


if TRACE or TRACE_DEEP:
    import logging

    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(' '.join(isinstance(a, str) and a or repr(a) for a in args))



def detect_copyrights(location, copyrights=True, holders=True, authors=True,
                      include_years=True, include_allrights=False,
                      demarkup=True,
                      deadline=sys.maxsize):
    """
    Yield tuples of (detection type, detected string, start line, end line)
    detected in file at `location`.
    Include years in copyrights if include_years is True.
    Valid detection types are: copyrights, authors, holders.
    These are included in the yielded tuples based on the values of `copyrights=True`, `holders=True`, `authors=True`,
    """
    numbered_lines = numbered_text_lines(location, demarkup=demarkup)
    numbered_lines = list(numbered_lines)
    if TRACE:
        numbered_lines = list(numbered_lines)
        for nl in numbered_lines:
            logger_debug('numbered_line:', repr(nl))

    yield from detect_copyrights_from_lines(
        numbered_lines,
        copyrights=copyrights,
        holders=holders,
        authors=authors,
        include_years=include_years,
        include_allrights=include_allrights,
        deadline=deadline)
