#!/usr/bin/env python

import argparse
import collections
import sys
import os

points_to_letters = {
    1 : ['a', 'e', 'i', 'o', 'r', 's', 't'],
    2 : ['d', 'l', 'n', 'u'],
    3 : ['g', 'h', 'y'],
    4 : ['b', 'c', 'f', 'm', 'p', 'w'],
    5 : ['k', 'v'],
    8 : ['x'],
    10 : ['j', 'q', 'z']
}

letter_values = {}

for points, letter_list in points_to_letters.items():
    for letter in letter_list:
        letter_values[letter] = points

valid_score_multipliers = [
    "triple-word", "double-word", "triple-letter", "double-letter"]

max_word_length = 8

def score_word(word, multiplier, multiplier_position):
    score = 0
    score_multiplier = 1

    for i, letter in enumerate(word):
        position = i + 1
        letter_value = letter_values[letter]
        letter_multiplier = 1

        if position == multiplier_position:
            if multiplier == "double-letter":
                letter_multiplier = 2
            elif multiplier == "triple-letter":
                letter_multiplier = 3
            elif multiplier == "double-word":
                score_multiplier = 2
            elif multiplier == "triple-word":
                score_multiplier = 3
        score += letter_multiplier * letter_value

    score *= score_multiplier

    return score

def word_hardness(word, multiplier, position):
    word_length = len(word)
    num_distinct_characters = len(set(list(word)))
    word_score = score_word(word, multiplier, position)

    return (word_score, num_distinct_characters, word_length)

def make_word(dictionary):
    # Make a multiset based on the letters we're given
    letters = collections.Counter(
        list(raw_input("Enter available letters, without spaces: ").strip()))

    score_multiplier = None

    # Ask user for a score multiplier (double- or triple-letter score, double-
    # or triple-word score)
    while score_multiplier is None:
        score_multi_string = raw_input("Enter score multiplier (one of %s): " %
                                       (', '.join(["'%s'" % (mult)
                                         for mult in valid_score_multipliers])))

        if score_multi_string not in valid_score_multipliers:
            print "Invalid score multiplier '%s'" % (score_multi_string)
        else:
            score_multiplier = score_multi_string

    # Ask user for the multiplier's position on the board
    multiplier_position = None

    while multiplier_position is None:
        try:
            current_multi_position = int(raw_input(
                    "Enter multiplier position (1 through %d): " %
                    (max_word_length)))
        except ValueError, e:
            current_multi_position = None

        if current_multi_position is None:
            # Don't accept input that isn't a number
            print "'%s' is not a number" % (str(current_multi_position))
        elif current_multi_position not in xrange(1, max_word_length + 1):
            # Don't accept input that isn't a valid position on the board
            print "%d is out-of-range" % (current_multi_position)
        else:
            multiplier_position = current_multi_position

    candidate_words = []

    with open(dictionary, "r") as fp:
        for word in fp:
            word = word.strip()

            # Can't play a word that's more than the board length long
            if len(word) > max_word_length:
                continue

            # Create a multiset for the letters in the word
            word_multiset = collections.Counter(list(word.strip()))

            # Subtract the candidate multiset from the available letters
            # multiset. If the result of the subtraction is empty, then we have
            # enough letters to create the word.
            if len(word_multiset - letters) == 0:
                candidate_words.append(word)

    # Sort the candidate words in reverse order by length
    candidate_words.sort(
        key = lambda x: word_hardness(x, score_multiplier, multiplier_position),
        reverse=True)

    # For now, just print the ten highest-scoring words

    print "Ten highest-scoring candidate words:"

    for word in candidate_words[:10]:
        print "%s (score vector: %s)" % (word, word_hardness(
                word, score_multiplier, multiplier_position))

def main():
    parser = argparse.ArgumentParser(description="creates a Hanging with "
                                     "Friends puzzle from a set of letters")
    parser.add_argument("--dictionary", default="enable1.txt",
                        help="dictionary from which to draw candidate words")

    args = parser.parse_args()

    if not os.path.exists(args.dictionary):
        sys.exit("Can't find '%s'" % (args.dictionary))

    make_word(dictionary=args.dictionary)

if __name__ == "__main__":
    sys.exit(main())




