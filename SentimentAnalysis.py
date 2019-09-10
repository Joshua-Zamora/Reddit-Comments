# CS2302 DATA STRUCTURES
# Author: Joshua Zamora
# OPTION A (REDDIT POSTS)
# Instructor: Diego Aguirre
# TA: Gerardo Barraza
# Last Updated 9 / 9 / 2019
# The purpose of this program is to retrieve reddit comments and sort them by connotation

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='oUyj3HxShRwhzQ',
                     client_secret='XpHumkRe7BcPXoe0ubPxQKSS7Kw',
                     user_agent='my user agent'
                     )

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


def process_comments_2(comment_list, comment):
    try:
        if comment:  # determines if a comment element in the list exists
            neg = get_text_negative_proba(comment.body)
            pos = get_text_positive_proba(comment.body)  # gives negative, positive, and neutral reading from 0-1
            neut = get_text_neutral_proba(comment.body)

            if neg > pos and neg > neut:
                negative_comments_list.append(comment.body)  # adds comment to negative list
            elif pos > neg and pos > neut:
                positive_comments_list.append(comment.body)  # adds comment to positive list
            else:
                neutral_comments_list.append(comment.body)  # adds comment to neutral list

            process_comments_2(comment_list[1:], comment_list[1])  # recursively traverses left sub-tree

            process_comments_2(comment.replies, comment.replies[0])  # recursively traverses right sub-tree

    except IndexError:  # checks if the list index is out of bounds
        return


negative_comments_list = []
neutral_comments_list = []
positive_comments_list = []


def main():
    comments = get_submission_comments(
        'https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    # process_comments_2(comments, comments[0])

    # TEST CASE 1
    url = 'https://www.reddit.com/r/worldnews/comments/d1qb2k/trump_reportedly_wanted_to_show_off_his/'
    test1 = get_submission_comments(url)

    # process_comments_2(test1, test1[0])
    # print(positive_comments_list[0])
    # print(neutral_comments_list[0])
    # print(negative_comments_list[0])
    print()

    # TEST CASE 2
    url2 = 'https://www.reddit.com/r/NintendoSwitch/comments/d1z3cl/i_asked_nintendo_support_to_draw_me_their/'
    test2 = get_submission_comments(url2)
    process_comments_2(test2, test2[0])
    print(positive_comments_list[0])
    print(neutral_comments_list[0])
    print(negative_comments_list[0])
    print()

    print('Positive list length: ', len(positive_comments_list))
    print('Neutral list length: ', len(neutral_comments_list))
    print('Negative list length: ', len(negative_comments_list))


main()
