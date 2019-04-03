#!/usr/bin/python3

import urllib.request
import argparse
import sys
import os
import re

# import errno
# import json
# import pdb
# import datetime
# import gc
# import math
# import functools
# import random

# ----------------------------------------------------- null text help formatter

class NullTextHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Text formatter for argparse help message that 
    (1) Doesn't mangle white space in the description, and
    (2) Doesn't print "helpful" optional and postional argument secionts.

    When using this text formatter, put all usage information in 
    the description field (of the argument parser), and format it
    however you want. Done."""
    def add_argument(self, action):
        pass

# ---------------------------------------------------------------- make page URL

def make_movie_review_url(movie, page_no):
    return 'https://www.rottentomatoes.com/m/{}/reviews/?page={}&type=user'.format(movie, page_no)

def get_html(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8", 'ignore')
    fp.close()
    return mystr

# -------------------------------------------------------------- extract n pages

def extract_n_of_pages(raw_html):
    # <span class="pageInfo">Page 1 of 428</span>
    e = re.compile('<span class=\"pageInfo\">Page ([0-9]+) of ([0-9]+)<\/span>')
    matches = re.findall(e, raw_html)
    if len(matches) == 0:
        raise Exception('failed to find page count!')
    return int(matches[0][1])

# -------------------------------------------------------------- extract reviews

def extract_stars(snippet):
    stars = snippet.count('glyphicon-star')
    n_halfs = snippet.count('&frac12;')
    return stars + 0.5 * n_halfs

def extract_review_stars(raw_html):
    e = re.compile('<div class="row review_table_row">.*?<\/div> <\/div> <\/div>')
    matches = re.findall(e, raw_html)
    return [extract_stars(str(match)) for match in matches]

# ------------------------------------------------------------------------- main

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        formatter_class=NullTextHelpFormatter,
        usage=argparse.SUPPRESS,
        description="""

Usage: {0} <movie>

   Instructions

Example:

   # Will look at reviews on from:
   # https://www.rottentomatoes.com/m/captain_marvel/reviews/?page=1&type=user
   > {0} captain_marvel

""".format(os.path.basename(sys.argv[0])))
    
    parser.add_argument('movie', nargs='?', type=str, default='')

    args = parser.parse_args()
    movie = args.movie
    
    raw_html = get_html(make_movie_review_url(movie, 1))
    # raw_html = ''
    # with open('zap', encoding='utf-8', errors='backslashreplace') as f:
    #     raw_html = f.read()

    def average(x):
        return sum(x) / len(x) if len(x) > 0 else 0
        
    def print_update(page_no, reviews):
        print('Page {0: 3}, {1}, average = {2}'.format(page_no, reviews, average(reviews)))
        
    # extract reviews for page 1
    reviews = extract_review_stars(raw_html)
    print_update(1, reviews)
    
    # count the number of pages
    n_pages = extract_n_of_pages(raw_html)
    page_count = 1
    for page_no in range(2, n_pages):
        raw_html = get_html(make_movie_review_url(movie, page_no))
        page_reviews = extract_review_stars(raw_html)
        print_update(page_no, page_reviews)
        reviews = reviews + page_reviews
        if len(page_reviews) == 0:
            break
        page_count += 1
    
    # Histogram of reviews
    histogram = [0] * 10
    for i in range(0, 10):
        histogram[i] = len([y for y in filter(lambda x : x == 0.5 * (i+1), reviews)])

    sans_1star = [y for y in filter(lambda x : x != 0.5, reviews)]

    av_all = average(reviews)
    av_sans = average(sans_1star)
    
    # Print results
    print("\n\n{} Summary\n".format('-' * 60))
    print("n-reviews:         {}".format(len(reviews)))
    print("n-pages:           {}".format(page_count))
    print("review average:    {0:5.3f},  i.e., {1:5.1f}, which is {2:5.1f}%, (scaled to range [0-100]%)"
          .format(av_all, av_all * 20, 100*(av_all-0.5)/4.5))
    print("non-1star average: {0:5.3f},  i.e., {1:5.1f}, which is {2:5.1f}%, (scaled to range [0-100]%)"
          .format(av_sans, av_sans*20, 100*(av_sans-0.5)/4.5))
    print("Histogram")
    for i in range(0, 10):
        print("   {:3.1f} stars: {}".format((i+1)*0.5, histogram[i]))
    print("")
