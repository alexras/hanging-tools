Algorithms for solving Hanging with Friends puzzles and picking good puzzles
based on a collection of candidate letters.

`solve.py` will attempt to solve a Hanging with Friends puzzle with a minimum
number of incorrect guesses given a dictionary of words.

`make_word.py` will create the best possible word as defined by some
configurable scoring metric. Current the three methods used to score words are:

* the word's score (incl. modifiers)
* the number of distinct letters in the word
* the length of the word

with the word's score in method x used to break ties in method x - 1.

I wrote these as a little exploratory exercise. If you want to use them to
cheat at Hanging with Friends, I won't stop you, but that's not why they
exist. Cheating's bad, mmmkay.
