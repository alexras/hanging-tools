#!/usr/bin/env python

import sys
import os
import string
import argparse

def candidate_word(word, template, candidate_letters):
    # We can immediately exclude all words that aren't the right length
    if len(word) != len(template):
        return False

    for i, letter in enumerate(template):
        # If the current letter in the template is a wildcard, and the
        # corresponding letter in the candidate word is not in the set of
        # candidate letters, then it's impossible to form this word using the
        # template and the candidiate letters
        if letter == "?" and word[i] not in candidate_letters:
            return False

        # Otherwise, make sure that the current letter in the word matches the
        # current letter in the template
        if letter != "?" and word[i] != letter:
            return False

    return True

def solve(dictionary):
    # The initial set of letters we can choose consists of all the letters in
    # the alphabet
    candidate_letters = set(list(string.ascii_lowercase))

    template_valid = False

    while not template_valid:
        template_valid = True

        # Ask the user for the initial "template"
        template = raw_input("Enter template (? for unknown, a-z for letter, "
                             "ex. w?rd): ")
        template = template.strip()

        num_unknowns = template.count('?')

        template_letters = set(list(template))

        # Make sure your template's letters are valid (no extra bizarre
        # characters)
        for letter in template_letters:
            if letter != "?" and letter not in candidate_letters:
                # If the user entered an invalid template character, ask them
                # to enter the template again
                print "Invalid template character '%s'" % (letter)
                template_valid = False
                break

    # Letters that appear in the template are by definition not candidate letters
    candidate_letters = candidate_letters - template_letters

    # Filter the dictionary to the set of words that match the initial template
    with open(dictionary, "r") as fp:
        dictionary = []

        for word in fp:
            word = word.strip()

            if candidate_word(word, template, candidate_letters):
                dictionary.append(word)

    wrong_guesses = 0

    while len(dictionary) > 1 and num_unknowns > 0:
        print "%d candidate words remain" % (len(dictionary))

        # Count the number of times each letter occurs in the set of candidate
        # words
        letter_frequencies = {}

        for letter in candidate_letters:
            letter_frequencies[letter] = 0

        for word in dictionary:
            # We only want to count each letter once, so get the set of letters
            # in the word
            word_letters = set(list(word)).intersection(candidate_letters)

            for letter in word_letters:
                letter_frequencies[letter] += 1

        # Extract the letter with the highest frequency
        max_letter = None
        max_count = None

        for (letter, count) in letter_frequencies.items():
            if max_count == None or count > max_count:
                max_count = count
                max_letter = letter

        while True:
            # Ask the user if that letter is in the word
            max_letter_in_word = raw_input(
                "Is '%s' in the word? " % (max_letter)).strip()

            if max_letter_in_word in ["yes", "no"]:
                break
            else:
                print "Please answer 'yes' or 'no'"

        # The letter we picked is no longer under consideration, whether it was
        # a correct guess or not
        candidate_letters.remove(max_letter)

        if max_letter_in_word == "yes":
            # We picked the right letter. Update the template accordingly

            template = raw_input(
                "Provide the new template (? for unknown, a-z for "
                "letter, ex. w?rd): ")

            num_unknowns = template.count('?')

            # The dictionary should be filtered to match only those elements
            # that match the new template
            dictionary = filter(
                lambda x: candidate_word(x, template, candidate_letters),
                dictionary)
        else:
            # We picked the wrong letter. Filter all words from the dictionary
            # that have that letter in it

            wrong_guesses += 1

            dictionary = filter(lambda x: max_letter not in x, dictionary)

    if len(dictionary) == 0:
        print "I'm stumped."
        return 1

    print "The word is ",

    if len(dictionary) > 1:
        print "one of the following: ",

    print "%s" % (', '.join(dictionary))
    print "%d wrong guesses" % (wrong_guesses)

    return 0

def main():
    parser = argparse.ArgumentParser(description="solves a Hanging with "
                                     "Friends puzzle")
    parser.add_argument("--dictionary", default="enable1.txt",
                        help="dictionary from which to draw candidate words")

    args = parser.parse_args()

    if not os.path.exists(args.dictionary):
        sys.exit("Can't find '%s'" % (args.dictionary))

    solve(dictionary=args.dictionary)

if __name__ == "__main__":
    sys.exit(main())
