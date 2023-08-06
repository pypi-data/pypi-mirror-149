# -----------------------------------------------------------------------------
#
# This file is the copyrighted property of Tableau Software and is protected
# by registered patents and other applicable U.S. and international laws and
# regulations.
#
# Unlicensed use of the contents of this file is prohibited. Please refer to
# the NOTICES.txt file for further details.
#
# -----------------------------------------------------------------------------


class UnclosedObjectWarning(Warning):
    """ Warning issued when a :any:`HyperProcess`, :any:`Connection`, :any:`Result` or :any:`Inserter` object has
    not been properly closed (e.g., by a ``with`` statement or explicit ``shutdown()`` or ``close()`` method.)"""
