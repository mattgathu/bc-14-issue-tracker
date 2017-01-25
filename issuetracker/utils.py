"""
Helper Module

__author__ =
__date__  = Nov 2015

"""
# ============================================================================
# necessary imports
# ============================================================================
import string
import random
from difflib import SequenceMatcher


# ============================================================================
# helper functions
# ============================================================================
def flatten_list(lst):
    """flatten a list of lists"""
    lst = [item for sublist in lst for item in sublist]

    return lst


def random_string():
    """generate random 16 characters long str"""
    rs = (''.join(random.choice(string.ascii_uppercase)
                  for i in range(16)))

    return rs


def are_similar(str1, str2, index=0.8):
    """Check if two strings are similar using a similarity index/ratio

    are_similar(str1, str2, index=0.9) -> True/False

    """
    if (not str1 or not str2):
        return False
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    if SequenceMatcher(None, str1, str2).ratio() >= index:
        return True

    return False


# ============================================================================
# EOF
# ============================================================================
